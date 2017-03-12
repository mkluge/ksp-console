#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import krpc
import os
import serial
from time import sleep
import sys
import json
import argparse
from ksp_console import *

#port = "COM4"
port = "/dev/ttyS3"

class State:
	def __init__(self, conn):
		self.last_scene=""
		# 0 means -> slider
		# 1 means 100 from button
		# 2 means 0 from button
		self.thrust_state=0
		self.last_thrust_from_slider=0
		s = conn.space_center.SASMode
		self.sas_mode_list=[
			s.stability_assist, s.maneuver,
			s.prograde, s.retrograde, s.normal, s.anti_normal,
			s.radial, s.anti_radial, s.target, s.anti_target ]
		self.current_sas_mode=0
		self.num_sas_modes=len(self.sas_mode_list)
		s = conn.space_center.SpeedMode
		self.current_speed_mode=0
		self.speed_mode_list=[ s.orbit, s.surface, s.target ]
		self.num_speed_modes=len(self.speed_mode_list)

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
	send_serial( CMD_INIT, send_data)

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

def decode_json_array(arr):
	res={}
	for index in range( 0, len(arr), 2):
#		if int(arr[index])>7:
		res[arr[index]]=arr[index+1]
	return res

def encode_json_array(arr):
	res=[]
	for element in arr:
		res.append(int(element))
		res.append(arr[element])
	return res

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
			status_updates[str(INFO_HEIGHT)] = int(vessel.flight().surface_altitude)
			status_updates[str(INFO_SPEED)] = int(vessel.flight(vessel.orbit.body.reference_frame).speed)
			status_updates[str(BUTTON_SAS)] = int(control.sas)
			status_updates[str(BUTTON_RCS)] = int(control.rcs)
			status_updates[str(BUTTON_LIGHTS)] = int(control.lights)
			status_updates[str(BUTTON_GEAR)] = int(control.gear)
			status_updates[str(BUTTON_BREAKS)] = int(control.brakes)
			send_updates()
		except krpc.error.RPCError:
		 	pass

def send_updates():
	global args
	global status_updates
	global conn
	if not args.noksp:
		if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
			return
		try:
			send_data = encode_json_array(status_updates)
			send_serial( CMD_UPDATE_CONSOLE, {"data":send_data})
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
			for grp in [1,2,3,4,5,6,7,8,9,0]:
#				print("Status of group " +str(grp) + " is " + str(control.get_action_group(grp)))
#				sys.stdout.flush()
				if control.get_action_group(grp):
					status = status + current_value
				current_value = current_value * 2
			status_updates[str(INFO_ACTION_GROUPS)] = status
#			print("status of all groups is "+str(status))
#			sys.stdout.flush()
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
            status_updates[str(INFO_SURFACE_HEIGHT)] = int(flight.surface_altitude)
            speed = int( conn.space_center.active_vessel.flight( conn.space_center.active_vessel.orbit.body.reference_frame).vertical_speed)
            if( speed<0.0 ):
                status_updates[str(INFO_SURFACE_TIME)] = time_to_string(int(flight.surface_altitude/abs(speed)))
            else:
                status_updates[str(INFO_SURFACE_TIME)] = "n/a"
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
			status_updates[str(INFO_APOAPSIS)] = int(orbit.apoapsis_altitude)
			status_updates[str(INFO_APOAPSIS_TIME)] = time_to_string(int(orbit.time_to_apoapsis))
			if orbit.periapsis_altitude>0:
				status_updates[str(INFO_PERIAPSIS)] = int(orbit.periapsis_altitude)
				status_updates[str(INFO_PERIAPSIS_TIME)] = time_to_string(int(orbit.time_to_periapsis))
			else:
				status_updates[str(INFO_PERIAPSIS)] = "n/a"
				status_updates[str(INFO_PERIAPSIS_TIME)] = "n/a"
		except krpc.error.RPCError:
		 	pass
		except ValueError:
		  	pass

def check_input( data, key, fun, *fargs):
	global args
	if key in data and not args.noksp:
		if data[key]==1:
			fun(*fargs)

def enable_all_engines( vessel, value):
	global args
	if not args.noksp:
		for e in vessel.parts.engines:
			e.active = value

def chutes_go( vessel ):
	global args
	if not args.noksp:
		for p in vessel.parts.parachutes:
			print( "1" )
			p.deploy()
	print( "chutes" )
	sys.stdout.flush()

def full_thrust( vessel ):
	global state
	control = vessel.control
	if state.thrust_state==0:
		state.last_thrust_from_slider = control.throttle
	control.throttle=1
	state.thrust_state=1

def zero_thrust( vessel ):
	global state
	control = vessel.control
	if state.thrust_state==0:
		state.last_thrust_from_slider = control.throttle
	control.throttle=0
	state.thrust_state=2

def button_abort( vessel ):
	return

def button_fuel( vessel ):
	return

def button_reaction_wheels( vessel ):
	global args
	if not args.noksp:
		for r in vessel.parts.reaction_wheels:
			if r.active == True:
				r.active = False
			else:
				r.active = True

def camera_button():
	camera = conn.space_center.camera
	if camera.mode==conn.space_center.CameraMode.map:
		camera.mode=conn.space_center.CameraMode.automatic
	else:
		camera.mode=conn.space_center.CameraMode.map
	return

def button_test(vessel):
	return

def button_eva(vessel):
	return

def button_iva(vessel):
	return

def next_sas_mode(vessel):
	global state
	# if sas was off, just enable it
	control = vessel.control
	if control.sas == False:
		control.sas = True
		return
	next_mode = state.current_sas_mode+1
	if next_mode==state.num_sas_modes:
		next_mode=0
	control.sas_mode=state.sas_mode_list[next_mode]
	state.current_sas_mode=next_mode
	return

def next_speed_mode(vessel):
	global state
	control = vessel.control
	next_mode = state.current_speed_mode+1
	if next_mode==state.num_speed_modes:
		next_mode=0
	control.speed_mode=state.speed_mode_list[next_mode]
	state.current_speed_mode=next_mode
	return

def expand_solar_arrays( vessel, value):
	global args
	if not args.noksp:
		for solar in vessel.parts.solar_panels:
			solar.deployed = value

def check_input_and_feedback(data, key_str, key, control):
    global args
    global status_updates
    global conn
    if key in data and not args.noksp:
        if bool(data[key]):
            setattr( control, key_str, not getattr( control, key_str))
        status_updates[str(key)] = int(getattr( control, key_str))

def check_analog( data, key, control, ckey):
    if key in data:
        value = data[key]
        if not args.noksp:
            setattr( control, ckey, normiere_joystick(value))

def work_on_json(input_data):
	global args
	global status_updates
	global conn
	global state

	if not args.noksp:
		if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
			return
	try:
		json_data = json.loads(input_data)
		data = decode_json_array(json_data["data"])
		if args.debugrecv:
			if len(data)>0:
				print( data )
				sys.stdout.flush()
		if args.noksp:
			return
		vessel = conn.space_center.active_vessel
		control = vessel.control
		check_analog( data, KSP_INPUT_XTRANS, control, "right")
		check_analog( data, KSP_INPUT_YTRANS, control, "up")
		check_analog( data, KSP_INPUT_ZTRANS, control, "forward")
		check_analog( data, KSP_INPUT_YAW, control, "yaw")
		check_analog( data, KSP_INPUT_PITCH, control, "pitch")
		check_analog( data, KSP_INPUT_ROLL, control, "roll")
		if args.debugrecv:
			print( data )
			sys.stdout.flush()
		if KSP_INPUT_THRUST in data:
			value = normiere_throttle(data[KSP_INPUT_THRUST])
			if state.thrust_state==0:
				control.throttle = value
			else:
				# only set if slider has been moved
				if abs(state.last_thrust_from_slider-value)>0.05:
					state.thrust_state=0
					control.throttle=value
		if BUTTON_STAGE in data and data[BUTTON_STAGE]==1:
			control.activate_next_stage()
		check_input_and_feedback( data, "sas", BUTTON_SAS, control)
		check_input_and_feedback( data, "rcs", BUTTON_RCS, control)
		check_input_and_feedback( data, "gear", BUTTON_GEAR, control)
		check_input_and_feedback( data, "lights", BUTTON_LIGHTS, control)
		check_input_and_feedback( data, "brakes", BUTTON_BREAKS, control)
		# the action buttons seem to be mixed up, in krpc there are called 0-9
		# ksp calls them 1-10; the mapping is 1-9->1-9 and 10->0
		check_input( data, BUTTON_ACTION_1, lambda: control.toggle_action_group(1))
		check_input( data, BUTTON_ACTION_2, lambda: control.toggle_action_group(2))
		check_input( data, BUTTON_ACTION_3, lambda: control.toggle_action_group(3))
		check_input( data, BUTTON_ACTION_4, lambda: control.toggle_action_group(4))
		check_input( data, BUTTON_ACTION_5, lambda: control.toggle_action_group(5))
		check_input( data, BUTTON_ACTION_6, lambda: control.toggle_action_group(6))
		check_input( data, BUTTON_ACTION_7, lambda: control.toggle_action_group(7))
		check_input( data, BUTTON_ACTION_8, lambda: control.toggle_action_group(8))
		check_input( data, BUTTON_ACTION_9, lambda: control.toggle_action_group(9))
		check_input( data, BUTTON_ACTION_10, lambda: control.toggle_action_group(0))
		check_input( data, BUTTON_SOLAR_OFF, lambda: expand_solar_arrays( vessel, False))
		check_input( data, BUTTON_SOLAR_ON, lambda: expand_solar_arrays( vessel, True))
		check_input( data, BUTTON_ENGINES_ON, lambda: enable_all_engines( vessel, True))
		check_input( data, BUTTON_ENGINES_OFF, lambda: enable_all_engines( vessel, False))
		check_input( data, BUTTON_ABORT, lambda: button_abort( vessel ))
		check_input( data, BUTTON_FUEL, lambda: button_fuel( vessel, True))
		check_input( data, BUTTON_REACTION_WHEELS, lambda: button_reaction_wheels( vessel, True))
		check_input( data, BUTTON_STORE, lambda: conn.space_center.quicksave() )
		check_input( data, BUTTON_LOAD, lambda: conn.space_center.quickload() )
		check_input( data, BUTTON_CAMERA, lambda: camera_button() )
		check_input( data, BUTTON_TEST, lambda: button_test(vessel) )
		check_input( data, BUTTON_EVA, lambda: button_eva(vessel) )
		check_input( data, BUTTON_IVA, lambda: button_iva(vessel) )
		check_input( data, BUTTON_SAS_MODE, lambda: next_sas_mode(vessel) )
		check_input( data, BUTTON_SPEED_MODE, lambda: next_speed_mode(vessel) )
		check_input( data, BUTTON_THRUST_FULL, lambda: full_thrust(vessel) )
		check_input( data, BUTTON_THRUST_ZERO, lambda: zero_thrust(vessel) )
		check_input( data, BUTTON_CHUTES, lambda: chutes_go(vessel) )
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
else:
	conn = krpc.connect(name='mk console')
	state = State(conn)

# no async receives, so it is ok to set a timeout, should
# make less loops
ser = serial.Serial(port, 115200, timeout=0)
ser.reset_input_buffer()
ser.reset_output_buffer()

sleep(3)
send_handshake()
ref_time = datetime.datetime.now()
while True:
	now = datetime.datetime.now()
	time_diff = now - ref_time
	# this works command driven, so we send commands,
	# wait for the reply and done

	# every 2 seconds or so: send update to the arduino
#	if (diff_short.seconds>1 or diff_short.microseconds>200000) and ser.out_waiting == 0:
	if (time_diff.seconds>2):
		if not args.noksp:
			if conn.krpc.current_game_scene==conn.krpc.GameScene.flight:
				add_action_group_status()
				add_orbit_to_status()
				add_landing_info()
				ref_time_long = datetime.datetime.now()
				send_flight_data()
		ref_time = now

	# read the current status and button updates and so on
	send_serial( CMD_GET_UPDATES, {})
	serial_data=serial_read_line()
#	if args.debugrecv:
#		print( decode_json_array(serial_data["data"]) )
#		sys.stdout.flush()
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
	# if this generated updates -> send them right away
	if len(status_updates)>0:
		send_updates()
