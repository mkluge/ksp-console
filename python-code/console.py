#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

    Python interface between Kerbal Space Program
    an a home grown hardware console

"""

import datetime
from time import sleep
import sys
import json
import argparse
import serial
import krpc
from ksp_console import *

# pylint: disable=no-member

PORT = "/dev/ttyACM0"
SER = object
ARGS = object
STATE = object
TELEMETRY = object
PERF_DATA = object


class PerfData:
    """ collect performance data for tuning
    """

    def __init__(self):
        self.clear()

    def start_timer(self, name):
        """ starts one timer
        """
        self.timers[name] = datetime.datetime.now()

    def stop_timer(self, name):
        """ stops one timer
        """
        stop = datetime.datetime.now()
        if not name in self.timers.keys():
            print("can't stop timer %s, has not been started yet" % (name))
            return
        delta = stop - self.timers[name]
        ms_diff = int(delta.total_seconds() * 1000)
        self.set(name, ms_diff)
        del self.timers[name]

    def set(self, key, value):
        """ sets one value
        """
        self.values[key] = value

    def clear(self):
        """ clears all result values
        """
        self.values = {}
        self.timers = {}

    def dump(self):
        """ prints all results to stdout
        """
        for key in self.values:
            print("%s: %.2f ms" % (key, self.values[key]))


class Telemetry:
    """ stup and contain all telemetry about a vessel
    """
    conn = krpc.Client
    prog_args = ""
    vessel = ""
    control = ""
    orbit = ""
    altitude = ""
    apoapsis = ""
    speed = ""
    sas = ""
    rcs = ""
    lights = ""
    gear = ""
    brakes = ""

    def __init__(self, conn, prog_args):
        self.conn = conn
        self.prog_args = prog_args
        self.init_vessel()

    def init_vessel(self):
        """ init telemetry data for a new active vessel
            always grabs the active vessel
        """
        try:
            self.vessel = self.conn.space_center.active_vessel
            self.control = self.vessel.control
            self.orbit = self.vessel.orbit
            # Set up streams for telemetry
            self.altitude = self.conn.add_stream(
                getattr, self.vessel.flight(), 'surface_altitude')
            self.apoapsis = self.conn.add_stream(
                getattr, self.vessel.orbit, 'apoapsis_altitude')
            self.speed = self.conn.add_stream(getattr, self.vessel.flight(
                self.vessel.orbit.body.reference_frame), 'speed')
            self.sas = self.conn.add_stream(getattr, self.control, 'sas')
            self.rcs = self.conn.add_stream(getattr, self.control, 'rcs')
            self.lights = self.conn.add_stream(getattr, self.control, 'lights')
            self.gear = self.conn.add_stream(getattr, self.control, 'gear')
            self.brakes = self.conn.add_stream(getattr, self.control, 'brakes')
        except krpc.error.RPCError:
            self.vessel = "none"

    def add_action_group_status(self, status_updates):
        """ add the status of the action groups to the
            status updates

            TODO: not implemented yet
        """
        if not self.prog_args.noksp:
            if self.conn.krpc.current_game_scene != self.conn.krpc.GameScene.flight:
                return status_updates
        return status_updates

    def add_orbit_to_status(self, status_updates):
        """ adds information about the current orbit parameters
            to the status
        """
        if not self.prog_args.noksp:
            if self.conn.krpc.current_game_scene != self.conn.krpc.GameScene.flight:
                return status_updates
            status_updates[str(INFO_PERIAPSIS)] = "n/a"
            status_updates[str(INFO_PERIAPSIS_TIME)] = "n/a"
            try:
                orbit = self.conn.space_center.active_vessel.orbit
                status_updates[str(INFO_APOAPSIS)] = str(
                    int(orbit.apoapsis_altitude))
                status_updates[str(INFO_APOAPSIS_TIME)] = time_to_string(
                    int(orbit.time_to_apoapsis))
                if orbit.periapsis_altitude > 0:
                    status_updates[str(INFO_PERIAPSIS)] = str(
                        int(orbit.periapsis_altitude))
                    status_updates[str(INFO_PERIAPSIS_TIME)] = time_to_string(
                        int(orbit.time_to_periapsis))
            except krpc.error.RPCError:
                pass
            except ValueError:
                pass
            except OverflowError:
                pass
        return status_updates

    def add_landing_info(self, status_updates):
        """ adds information about a possible landing
            to the status update
        """
        if not self.prog_args.noksp:
            if self.conn.krpc.current_game_scene != self.conn.krpc.GameScene.flight:
                return status_updates
            try:
                flight = self.conn.space_center.active_vessel.flight()
                status_updates[str(INFO_SURFACE_HEIGHT)] = int(
                    flight.surface_altitude)
                speed = int(self.conn.space_center.active_vessel.flight(
                    self.conn.space_center.active_vessel.orbit.body.reference_frame).vertical_speed)
                if speed < 0.0:
                    status_updates[str(INFO_SURFACE_TIME)] = time_to_string(
                        int(flight.surface_altitude/abs(speed)))
                else:
                    status_updates[str(INFO_SURFACE_TIME)] = "n/a"
            except krpc.error.RPCError:
                pass
            except ValueError:
                pass
        return status_updates

    def add_main_data(self, status_updates):
        """ adds all the standard data to the status updates
        """
        # if we do not have a vessel: test, if we can get one
        if self.vessel == "none":
            self.init_vessel()
            if self.vessel == "none":
                return status_updates
        # did the vessel change? then update streams
        if self.vessel != self.conn.space_center.active_vessel:
            self.init_vessel()

        status_updates[str(INFO_HEIGHT)] = int(self.altitude())
        status_updates[str(INFO_SPEED)] = int(self.speed())
        status_updates[str(BUTTON_SAS)] = 1 if self.sas() else 0
        status_updates[str(BUTTON_RCS)] = 1 if self.rcs() else 0
        status_updates[str(BUTTON_LIGHTS)] = 1 if self.lights() else 0
        status_updates[str(BUTTON_GEAR)] = 1 if self.gear() else 0
        status_updates[str(BUTTON_BREAKS)] = 1 if self.brakes() else 0
        status_updates = self.add_action_group_status(status_updates)
        return status_updates

    def generate_display_data(self):
        """ adds more data about the ships status to the status
            update. data is for the two pixel displays
        """
        display_data = {}
        # if we do not have a vessel: test, if we can get one
        if self.vessel == "none":
            self.init_vessel()
            if self.vessel == "none":
                return display_data
        # did the vessel change? then update streams
        if self.vessel != self.conn.space_center.active_vessel:
            self.init_vessel()

        display_data[str(INFO_HEIGHT)] = int(self.altitude())
        display_data[str(INFO_SPEED)] = int(self.speed())
        stage_resources = self.vessel.resources
        max_lf = stage_resources.max('LiquidFuel')
        max_ox = stage_resources.max('Oxidizer')
        max_mo = stage_resources.max('MonoPropellant')
        max_el = stage_resources.max('ElectricCharge')
        if max_lf != 0:
            display_data[str(INFO_PERCENTAGE_FUEL)] = int(
                stage_resources.amount('LiquidFuel') * 100 / max_lf)
        else:
            display_data[str(INFO_PERCENTAGE_FUEL)] = 0
        if max_ox != 0:
            display_data[str(INFO_PERCENTAGE_OXYGEN)] = int(
                stage_resources.amount('Oxidizer') * 100 / max_ox)
        else:
            display_data[str(INFO_PERCENTAGE_OXYGEN)] = 0
        if max_mo != 0:
            display_data[str(INFO_PERCENTAGE_RCS)] = int(
                stage_resources.amount('MonoPropellant') * 100 / max_mo)
        else:
            display_data[str(INFO_PERCENTAGE_RCS)] = 0
        if max_el != 0:
            display_data[str(INFO_PERCENTAGE_BATTERY)] = int(
                stage_resources.amount('ElectricCharge') * 100 / max_el)
        else:
            display_data[str(INFO_PERCENTAGE_BATTERY)] = 0
        display_data = self.add_orbit_to_status(display_data)
        display_data = self.add_landing_info(display_data)
        return display_data


class State:
    """ contains information about the current status
        of the game and the ship
    """

    last_scene = ""
    # 0 means -> slider
    # 1 means 100 from button
    # 2 means 0 from button
    thrust_state = 0
    last_thrust_from_slider = 0
    sas_mode_list = []
    current_sas_mode = 0
    current_speed_mode = 0
    speed_mode_list = []
    num_speed_modes = 0
    # whether sas was on before the joystick values where
    # feed into ksp
    last_yaw = 0
    last_pitch = 0
    last_roll = 0
    was_sas_on = False
    last_sas_type = 0
    joystick_sas_has_been_handled = False

    def __init__(self, conn):
        # 0 means -> slider
        # 1 means 100 from button
        # 2 means 0 from button
        self.thrust_state = 0
        self.last_thrust_from_slider = 0
        sasm = conn.space_center.SASMode
        self.sas_mode_list = [
            sasm.stability_assist, sasm.maneuver,
            sasm.prograde, sasm.retrograde, sasm.normal, sasm.anti_normal,
            sasm.radial, sasm.anti_radial, sasm.target, sasm.anti_target]
        self.current_sas_mode = 0
        self.num_sas_modes = len(self.sas_mode_list)
        spem = conn.space_center.SpeedMode
        self.current_speed_mode = 0
        self.speed_mode_list = [spem.orbit, spem.surface, spem.target]
        self.num_speed_modes = len(self.speed_mode_list)
        # whether sas was on before the joystick values where
        # feed into ksp
        self.last_yaw = 0
        self.last_pitch = 0
        self.last_roll = 0
        self.was_sas_on = False
        self.last_sas_type = 0
        self.joystick_sas_has_been_handled = False


def serial_read_line(port):
    """ reads data from the serial line until we get
        an "\n" as a terminator
    """
    serial_data = ""
    while True:
        data = port.read(1)
        if len(data) > 0:
            data = data.decode('iso8859-1')
            if data == '\n':
                return serial_data
            serial_data += data


def normiere_joystick(value):
    """ normalizes the console input to what krpc
        wants for the game ( 1 ... -1 )
    """
    if value > 512:
        value = 512
    if value < -512:
        value = -512
    value = float(value)
    value = value/512.0
    return value


def normiere_throttle(value):
    """ normalizes throttle values from console
        to game/krpc input
    """
    if value < 20:
        return 0
    if value > 890:
        return 1
    return float(value)/1000.0


def send_handshake():
    """ sends the initial handshake to the console
        so that it starts
    """
    send_data = {}
    send_data["start"] = 2016
    send_serial(CMD_INIT, send_data)


def send_serial(command, send_data, chunksize=32):
    """ sends data and take care of chunking and
        some delay between chunks
    """
    global ARGS
    global SER
    send_data["cmd"] = command
    data = json.dumps(send_data, separators=(',', ':'))+'+'
    data = data.encode('iso8859-1')
    if ARGS.debugsend:
        print("sending %d bytes " % len(data))
        print("send: "+str(data))
        sys.stdout.flush()
    # got to send in chunks to avoid loosing stuff
    # (if needed)
    while len(data) > 0:
        send_pkt = data[:chunksize]
        data = data[chunksize:]
        SER.write(send_pkt)
        # wait between packets ...
        sleep(0.05)
        if ARGS.debugsend:
            print("packet out:" + str(send_pkt))
    # check the response
    response = ""
    while len(response) != 2:
        response += SER.read(1).decode('iso8859-1')
    if response != "OK":
        print("got the wrong ACK for the serial protocol: " + response)


def decode_json_array(arr):
    """ decodes an array from the console to an
        dictionary as used here
    """
    res = {}
#	print(len(arr))
    for index in range(0, len(arr), 2):
        #		if int(arr[index])>7:
        res[arr[index]] = arr[index+1]
    return res


def encode_json_array(arr):
    """ encodes an dictionary as used here
        to an array as used by the console
    """
    res = []
    for element in arr:
        res.append(int(element))
        res.append(arr[element])
    return res


def send_display_update(conn, status_updates):
    """ generates and sends data necessary for udpating
        the displays to the console
    """
    global ARGS
    if not ARGS.noksp:
        if conn.krpc.current_game_scene != conn.krpc.GameScene.flight:
            return
        try:
            send_data = encode_json_array(status_updates)
            send_serial(CMD_UPDATE_DISPLAY, {"disp": send_data})
        except krpc.error.RPCError:
            pass


def send_main_update(connection, status_updates):
    """ sends update from the game to the console
    """
    global ARGS
    if not ARGS.noksp:
        if connection.krpc.current_game_scene != connection.krpc.GameScene.flight:
            return
        try:
            send_data = encode_json_array(status_updates)
            send_serial(CMD_UPDATE_CONSOLE, {"data": send_data})
        except krpc.error.RPCError:
            pass


def time_to_string(secs):
    """ convert time data to a nice string
    """
    if secs < 0:
        return "n/a"
    tap = ""
    if secs > 60:
        mins = int(secs/60)
        tap = str(mins) + " min"
        if mins < 5:
            tap = tap+", "+str(secs-(mins*60))+" sec"
    else:
        tap = str(int(secs)) + " sec"

    return tap


def check_input(data, key, fun, *fargs):
    """ calls a function, if a certain data point is set
        in the data delivered from the console
    """
    global ARGS
    if key in data and not ARGS.noksp:
        if data[key] == 1:
            fun(*fargs)


def enable_all_engines(vessel, value):
    """ enables all engines on the vessel
    """
    global ARGS
    if not ARGS.noksp:
        for engine in vessel.parts.engines:
            engine.active = value


def chutes_go(vessel):
    """ deploys all available chutes at the vessel
    """
    global ARGS
    if not ARGS.noksp:
        for chute in vessel.parts.parachutes:
            chute.deploy()


def full_thrust(vessel):
    """ full power to all engines
    """
    global STATE
    control = vessel.control
    if STATE.thrust_state == 0:
        STATE.last_thrust_from_slider = control.throttle
    control.throttle = 1
    STATE.thrust_state = 1


def zero_thrust(vessel):
    """ all engines to zero power
    """
    global STATE
    control = vessel.control
    if STATE.thrust_state == 0:
        STATE.last_thrust_from_slider = control.throttle
    control.throttle = 0
    STATE.thrust_state = 2


def button_abort(vessel):
    """ abort button pressed
        TODO: implement or delete
    """
    return


def button_fuel(vessel):
    """ fuel button pressed
        TODO: implement or delete
    """
    return


def button_reaction_wheels(vessel):
    """ switch the state of all reaction wheels in
        the vessel
    """
    global ARGS
    if not ARGS.noksp:
        for wheel in vessel.parts.reaction_wheels:
            if wheel.active:
                wheel.active = False
            else:
                wheel.active = True


def camera_button(conn):
    """ switch the camera mode
    """
    camera = conn.space_center.camera
    if camera.mode == conn.space_center.CameraMode.map:
        camera.mode = conn.space_center.CameraMode.automatic
    else:
        camera.mode = conn.space_center.CameraMode.map


def button_test(vessel):
    """ TEST button pressed
        TODO: implement or delete
    """
    return


def button_eva(vessel):
    """ EVA button pressed
        TODO: implement or delete
    """
    return


def button_iva(vessel):
    """ IVA button pressed
        TODO: implement or delete
    """
    return


def next_sas_mode(vessel):
    """ switch to the next SAS mode
    """
    global STATE
    # if sas was off, just enable it
    control = vessel.control
    if not control.sas:
        control.sas = True
        return
    next_mode = STATE.current_sas_mode+1
    if next_mode == STATE.num_sas_modes:
        next_mode = 0
    control.sas_mode = STATE.sas_mode_list[next_mode]
    STATE.current_sas_mode = next_mode


def next_speed_mode(vessel):
    """ switch to the next speed mode
    """
    global STATE
    control = vessel.control
    next_mode = STATE.current_speed_mode+1
    if next_mode == STATE.num_speed_modes:
        next_mode = 0
    control.speed_mode = STATE.speed_mode_list[next_mode]
    STATE.current_speed_mode = next_mode


def expand_solar_arrays(vessel, value):
    """ deploy or retract all solar arrays
    """
    global ARGS
    if not ARGS.noksp:
        for solar in vessel.parts.solar_panels:
            try:
                solar.deployed = value
            except:
                pass


def check_input_and_feedback(data, key_str, key, control):
    """ sends values from the console to the game
    """
    global ARGS
    if key in data and not ARGS.noksp:
        if bool(data[key]):
            setattr(control, key_str, not getattr(control, key_str))


def check_analog(data, key, control, ckey):
    """ checks analog data from the joysticks ans
        send them to the game
    """
    global STATE
    if key in data:
        value = normiere_joystick(data[key])
        if not ARGS.noksp:
            setattr(control, ckey, value)


def work_on_json(conn, input_data):
    """ takes the json data from the console, analyzes it, and
        sends it to the game
    """
    global ARGS
    global STATE

    if not ARGS.noksp:
        if conn.krpc.current_game_scene != conn.krpc.GameScene.flight:
            return
    try:
        json_data = json.loads(input_data)
        data = decode_json_array(json_data["data"])
        if ARGS.debugrecv:
            if len(data) > 0:
                print(data)
                sys.stdout.flush()
        if ARGS.noksp:
            return
        vessel = conn.space_center.active_vessel
        control = vessel.control
        check_analog(data, KSP_INPUT_XTRANS, control, "right")
        check_analog(data, KSP_INPUT_YTRANS, control, "up")
        check_analog(data, KSP_INPUT_ZTRANS, control, "forward")
        check_analog(data, KSP_INPUT_YAW, control, "yaw")
        check_analog(data, KSP_INPUT_PITCH, control, "pitch")
        check_analog(data, KSP_INPUT_ROLL, control, "roll")
        if ARGS.debugrecv:
            print(data)
            sys.stdout.flush()
        if KSP_INPUT_THRUST in data:
            value = normiere_throttle(data[KSP_INPUT_THRUST])
            if STATE.thrust_state == 0:
                control.throttle = value
            else:
                # only set if slider has been moved
                if abs(STATE.last_thrust_from_slider-value) > 0.05:
                    STATE.thrust_state = 0
                    control.throttle = value
        if BUTTON_STAGE in data and data[BUTTON_STAGE] == 1:
            control.activate_next_stage()
        check_input_and_feedback(data, "sas", BUTTON_SAS, control)
        check_input_and_feedback(data, "rcs", BUTTON_RCS, control)
        check_input_and_feedback(data, "gear", BUTTON_GEAR, control)
        check_input_and_feedback(data, "lights", BUTTON_LIGHTS, control)
        check_input_and_feedback(data, "brakes", BUTTON_BREAKS, control)
        # the action buttons seem to be mixed up, in krpc there are called 0-9
        # ksp calls them 1-10; the mapping is 1-9->1-9 and 10->0
        check_input(data, BUTTON_ACTION_1,
                    lambda: control.toggle_action_group(1))
        check_input(data, BUTTON_ACTION_2,
                    lambda: control.toggle_action_group(2))
        check_input(data, BUTTON_ACTION_3,
                    lambda: control.toggle_action_group(3))
        check_input(data, BUTTON_ACTION_4,
                    lambda: control.toggle_action_group(4))
        check_input(data, BUTTON_ACTION_5,
                    lambda: control.toggle_action_group(5))
        check_input(data, BUTTON_ACTION_6,
                    lambda: control.toggle_action_group(6))
        check_input(data, BUTTON_ACTION_7,
                    lambda: control.toggle_action_group(7))
        check_input(data, BUTTON_ACTION_8,
                    lambda: control.toggle_action_group(8))
        check_input(data, BUTTON_ACTION_9,
                    lambda: control.toggle_action_group(9))
        check_input(data, BUTTON_ACTION_10,
                    lambda: control.toggle_action_group(0))
        check_input(data, BUTTON_SOLAR_OFF,
                    lambda: expand_solar_arrays(vessel, False))
        check_input(data, BUTTON_SOLAR_ON,
                    lambda: expand_solar_arrays(vessel, True))
        check_input(data, BUTTON_ENGINES_ON,
                    lambda: enable_all_engines(vessel, True))
        check_input(data, BUTTON_ENGINES_OFF,
                    lambda: enable_all_engines(vessel, False))
        check_input(data, BUTTON_ABORT, lambda: button_abort(vessel))
        check_input(data, BUTTON_FUEL, lambda: button_fuel(vessel))
        check_input(data, BUTTON_REACTION_WHEELS,
                    lambda: button_reaction_wheels(vessel))
        check_input(data, BUTTON_STORE, lambda: conn.space_center.quicksave())
        check_input(data, BUTTON_LOAD, lambda: conn.space_center.quickload())
        check_input(data, BUTTON_CAMERA, lambda: camera_button(conn))
        check_input(data, BUTTON_TEST, lambda: button_test(vessel))
        check_input(data, BUTTON_EVA, lambda: button_eva(vessel))
        check_input(data, BUTTON_IVA, lambda: button_iva(vessel))
        check_input(data, BUTTON_SAS_MODE, lambda: next_sas_mode(vessel))
        check_input(data, BUTTON_SPEED_MODE, lambda: next_speed_mode(vessel))
        check_input(data, BUTTON_THRUST_FULL, lambda: full_thrust(vessel))
        check_input(data, BUTTON_THRUST_ZERO, lambda: zero_thrust(vessel))
        check_input(data, BUTTON_CHUTES, lambda: chutes_go(vessel))
    except ValueError:
        print('Decoding JSON failed')
#	except krpc.error.RPCError:
#		pass


def main_function():
    """ the "way to large" main function
        TODO: fix this, make classes an so on
    """
    global SER
    global ARGS
    global STATE
    global TELEMETRY
    global PERF_DATA

    PERF_DATA = PerfData()
    last_chip_data = 0
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debugsend", help="print data sent to con", action="store_true")
    parser.add_argument(
        "--debugrecv", help="print some received from con", action="store_true")
    parser.add_argument(
        "--debugchip", help="print chip debug output", action="store_true")
    parser.add_argument(
        "--noksp", help="run without connecting to ksp", action="store_true")
    ARGS = parser.parse_args()

    serial_connected = False
    krpc_connected = False
    # run forever (until ctrl-c)
    while True:
        try:
            # first: try to connect everything
            if not krpc_connected and not ARGS.noksp:
                conn = krpc.connect(name='mk console')
                STATE = State(conn)
                TELEMETRY = Telemetry(conn, ARGS)
                krpc_connected = True
                ref_time = datetime.datetime.now()
        except (krpc.error.RPCError, ConnectionRefusedError):
            krpc_connected = False

        try:
            if not serial_connected:
                print("trying serial")
                ser = serial.Serial(PORT, 115200, timeout=2)
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                sleep(5)
                print("sending handshake")
                send_handshake()
                print("serial OK")
                serial_connected = True
        except (serial.SerialException, ConnectionRefusedError):
            print("serial failed")
            serial_connected = False

        try:
            should_send = False
            if serial_connected and krpc_connected:
                while True:

                    # we have two types of commands
                    # 1) just requests data, there is a response
                    # 2) just send data to the arduino, there is no response
                    # so, after we have send one of type 1 we know we have
                    # to wait for a reply before we can send again
                    # after we send one of type 2) we don't know how long
                    # the processing in the arduino is going to take, so
                    # we always send after a command of type 2 one type 1
                    # command

                    now = datetime.datetime.now()
                    time_diff = now - ref_time
                    # this works command driven, so we send commands,
                    # wait for the reply and done

                    # every 1-2 seconds: send update to the arduino
                    if time_diff.seconds > 1:
                        if conn.krpc.current_game_scene == conn.krpc.GameScene.flight:
                            # send main controller data
                            main_updates = {}
                            PERF_DATA.start_timer("collectMainData")
                            main_updates = TELEMETRY.add_main_data(
                                main_updates)
                            PERF_DATA.stop_timer("collectMainData")
                            PERF_DATA.start_timer("sendMainUpdates")
                            send_main_update(conn, main_updates)
                            PERF_DATA.stop_timer("sendMainUpdates")
                            # every second time: also send display update
                            if should_send:
                                PERF_DATA.start_timer("collectDisplayData")
                                display_updates = TELEMETRY.generate_display_data()
                                PERF_DATA.stop_timer("collectDisplayData")
                                PERF_DATA.start_timer("sendDisplayUpdates")
                                send_display_update(conn, display_updates)
                                PERF_DATA.stop_timer("sendDisplayUpdates")
                                should_send = False
# disabled to omit sending display data
                            else:
                                should_send = True
                        ref_time = now

                    # read the current status and button updates and so on
                    PERF_DATA.start_timer("update process")
                    PERF_DATA.start_timer("send GET_UPDATES")
                    send_serial(CMD_GET_UPDATES, {})
                    PERF_DATA.stop_timer("send GET_UPDATES")
                    PERF_DATA.start_timer("readline")
                    serial_data = serial_read_line(SER)
                    PERF_DATA.stop_timer("readline")
                    if ARGS.debugrecv:
                        print(serial_data)
                        sys.stdout.flush()
                    if ARGS.debugchip:
                        try:
                            data = json.loads(serial_data)
                            if "chip" in data and data["chip"] != last_chip_data:
                                print("Chip: "+str(data["chip"]))
                                last_chip_data = data["chip"]
                                sys.stdout.flush()
                        except ValueError:
                            print('Decoding JSON failed for: '+data)
                    PERF_DATA.start_timer("workJson")
                    work_on_json(conn, serial_data)
                    PERF_DATA.stop_timer("workJson")
                    PERF_DATA.stop_timer("update process")
                    PERF_DATA.dump()
                    PERF_DATA.clear()
            else:
                # not everything connected, sleep and try again
                print("Connection missing: KRPC:%s Serial:%s\n" %
                      ("online" if krpc_connected else "offline",
                       "connected" if serial_connected else "disconnected"))
                sleep(1)
        except (krpc.error.RPCError, ConnectionRefusedError):
            krpc_connected = False
        except serial.SerialException:
            serial_connected = False


if __name__ == '__main__':
    main_function()
