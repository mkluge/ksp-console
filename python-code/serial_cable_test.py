#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import krpc
import serial
from time import sleep
import sys
import json
import argparse

port = "COM4"
last_scene=""
status_updates = {}

def serial_read_line():
	global ser
	serial_data = ""
	while True:
		data = ser.read(1)
		if len(data) > 0:
			data = data.decode('iso8859-1')
			if data=='\n':
				return serial_data
			serial_data += data

# auf -1 ... 1 normieren
def normiere_joystick(value):
	if value>512:
		value=512
	if value<-512:
		value=-512
	value = float(value)
	value = value/512.0
	return value

def normiere_throttle(value):
	if value<20:
		return 0;
	if value>890:
		return 1;
	return float(value)/1000.0;

def send_handshake():
	send_data = {}
	send_data["start"] = 2016
	send_serial( 3, send_data)

def send_serial( command, send_data):
	global args
	global ser
	send_data["cmd"]=command;
	data=json.dumps(send_data,separators=(',',':'))+"\n"
	if args.debugsend:
		print("sending %d bytes " % len(data))
		print("send: "+data)
		sys.stdout.flush()
	data = data.encode('iso8859-1')
	#got to send in 32 byte chunks to avoid loosing stuff
	len_data = str(len(data))+":"
	ser.write(len_data.encode('iso8859-1'))
	while( len(data)>0 ):
		send_pkt = data[:32]
		data = data[32:]
		ser.write(send_pkt)
		ser.flush()
		response = ""
		while( len(response)!=2 ):
			response += ser.read(1).decode('iso8859-1')
#		print( "response: " + response)
#		sys.stdout.flush()
		if response != "OK":
			print( "got the wrong ACK for the serial protocol: " +response )

def send_flight_data():
	global args
	global status_updates
	global conn
	if not args.noksp:
		if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
			return
		try:
			vessel = conn.space_center.active_vessel
			control = vessel.control
			orbit = vessel.orbit
			send_data = status_updates
			send_data["height"] = int(vessel.flight().surface_altitude)
			send_data["speed"] = int(vessel.flight(vessel.orbit.body.reference_frame).speed)
			send_data["sas"] = int(control.sas)
			send_data["rcs"] = int(control.rcs)
			send_data["lights"] = int(control.lights)
			send_data["gear"] = int(control.gear)
			send_data["brakes"] = int(control.brakes)
			send_serial( 2, send_data)
			status_updates={}
		except krpc.error.RPCError:
		 	pass

def time_to_string(secs):
	if secs<0:
		return "n/a"
	tap = ""
	if secs>60:
		mins = int(secs/60)
		tap = str(mins)+ " min"
		if mins<5:
			tap = tap+", "+str(secs-(mins*60))+" sec"
	else:
		tap = str(int(secs)) + " sec"
	return tap

def add_action_group_status():
    global args
    global status_updates
    global conn
    if not args.noksp:
        if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
            return
        try:
            vessel = conn.space_center.active_vessel
            control = vessel.control
            status=0
            current_value=1
            for grp in range(0,9):
                if control.get_action_group(grp):
                    status = status + current_value
                    current_value = current_value * 2
            status_updates["ag_state"] = status
        except krpc.error.RPCError:
            pass
        except ValueError:
            pass

def add_landing_info():
    global args
    global status_updates
    global conn
    if not args.noksp:
        if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
            return
        try:
            flight = conn.space_center.active_vessel.flight()
            status_updates["surf_h"] = int(flight.surface_altitude)
            speed = int( conn.space_center.active_vessel.flight( conn.space_center.active_vessel.orbit.body.reference_frame).vertical_speed)
            if( speed<0.0 ):
                status_updates["surf_t"] = time_to_string(int(flight.surface_altitude/abs(speed)))
            else:
                status_updates["surf_t"] = "n/a"
        except krpc.error.RPCError:
            pass
        except ValueError:
            pass

def add_orbit_to_status():
	global args
	global status_updates
	global conn
	if not args.noksp:
		if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
			return
		try:
			orbit = conn.space_center.active_vessel.orbit
			status_updates["ap"] = int(orbit.apoapsis_altitude)
			status_updates["ap_t"] = time_to_string(int(orbit.time_to_apoapsis))
			if orbit.periapsis_altitude>0:
				status_updates["pe"] = int(orbit.periapsis_altitude)
				status_updates["pe_t"] = time_to_string(int(orbit.time_to_periapsis))
			else:
				status_updates["pe"] = "n/a"
				status_updates["pe_t"] = "n/a"
		except krpc.error.RPCError:
		 	pass
		except ValueError:
		  	pass

def check_input( data, key, fun, *fargs):
	global args
	if key in data and not args.noksp:
		fun(*fargs)

def expand_solar_arrays( vessel, value):
	global args
	if not args.noksp:
		for solar in vessel.parts.solar_panels:
			solar.deployed = value

def check_input_and_feedback(data, key, control):
    global args
    global status_updates
    global conn
    if key in data and not args.noksp:
        if bool(data[key]):
            setattr( control, key, not getattr( control, key))
        status_updates[key] = int(getattr( control, key))

def check_analog( data, key, control, ckey):
    if key in data:
        value = data[key]
        if not args.noksp:
            setattr( control, ckey, normiere_joystick(value))

def work_on_json(input_data):
	global args
	global status_updates
	global conn

	if not args.noksp:
		if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
			return
	try:
		if args.noksp:
			return
		vessel = conn.space_center.active_vessel
		control = vessel.control
		data = json.loads(input_data)
		check_analog( data, "xtrans", control, "right")
		check_analog( data, "ytrans", control, "up")
		check_analog( data, "ztrans", control, "forward")
		check_analog( data, "yaw", control, "yaw")
		check_analog( data, "pitch", control, "pitch")
		check_analog( data, "roll", control, "roll")
		if "thrust" in data:
			value = data["thrust"]
			control.throttle = normiere_throttle(value)
		if "stage" in data and data["stage"]==1:
			control.activate_next_stage()
		check_input_and_feedback( data, "sas", control)
		check_input_and_feedback( data, "rcs", control)
		check_input_and_feedback( data, "gear", control)
		check_input_and_feedback( data, "lights", control)
		check_input_and_feedback( data, "brakes", control)
		check_input( data, "ag1", lambda: control.toggle_action_group(0))
		check_input( data, "ag2", lambda: control.toggle_action_group(1))
		check_input( data, "ag3", lambda: control.toggle_action_group(2))
		check_input( data, "ag4", lambda: control.toggle_action_group(3))
		check_input( data, "ag5", lambda: control.toggle_action_group(4))
		check_input( data, "ag6", lambda: control.toggle_action_group(5))
		check_input( data, "ag7", lambda: control.toggle_action_group(6))
		check_input( data, "ag8", lambda: control.toggle_action_group(7))
		check_input( data, "ag9", lambda: control.toggle_action_group(8))
		check_input( data, "ag10", lambda: control.toggle_action_group(9))
		check_input( data, "solar0", lambda: expand_solar_arrays( vessel, False))
		check_input( data, "solar1", lambda: expand_solar_arrays( vessel, True))
	except ValueError:
		print('Decoding JSON failed')
	except krpc.error.RPCError:
		pass

## main

last_chip_data = 0
parser = argparse.ArgumentParser()
parser.add_argument("--debugsend", help="print data sent to con", action="store_true")
parser.add_argument("--debugrecv", help="print some received from con", action="store_true")
parser.add_argument("--debugchip", help="print chip debug output", action="store_true")
parser.add_argument("--noksp", help="run without connecting to ksp", action="store_true")
args = parser.parse_args()
if args.noksp:
	print("noksp: will not connect to KSP")

# no async receives, so it is ok to set a timeout, should
# make less loops
ser = serial.Serial(port, 115200, timeout=0)
ser.reset_input_buffer()
ser.reset_output_buffer()
if not args.noksp:
	conn = krpc.connect(name='mk console')
sleep(5)
ref_time_short = datetime.datetime.now()
ref_time_long = datetime.datetime.now()
send_handshake()
now = datetime.datetime.now()
diff_short = now - ref_time_short
diff_long  = now - ref_time_long
while True:
	# this works command driven, so we send commands,
	# wait for the reply and done

	# every 2 seconds or so: send update to the arduino
	if (diff_short.seconds>1 or diff_short.microseconds>200000) and ser.out_waiting == 0:
		if not args.noksp:
			if conn.krpc.current_game_scene==conn.krpc.GameScene.flight and diff_long.seconds>1:
				add_action_group_status()
				add_orbit_to_status()
				add_landing_info()
				ref_time_long = datetime.datetime.now()
				send_flight_data()
			ref_time_short = datetime.datetime.now()

	# read the current status and button updates and so on
	get_data = {} # just a dummy
	send_serial( 1, get_data)
	serial_data=serial_read_line()
	if args.debugrecv:
		print( serial_data )
		sys.stdout.flush()
	if args.debugchip:
		try:
			data = json.loads(serial_data)
			if "chip" in data and data["chip"]!=last_chip_data:
				print("Chip: "+str(data["chip"]))
				last_chip_data = data["chip"]
				sys.stdout.flush()
		except ValueError:
			print('Decoding JSON failed for: '+lines[0])
	work_on_json(serial_data)
	now = datetime.datetime.now()
	diff_short = now - ref_time_short
	diff_long  = now - ref_time_long
