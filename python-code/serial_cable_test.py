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
serial_data="";

status_updates = {}

def check_serial():
	global serial_data
	data = ser.read(9999)
	if len(data) > 0:
    		serial_data += data.decode('iso8859-1')

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
	send_serial(send_data)

def send_serial(send_data):
	global args
	data=json.dumps(send_data)+"\n"
	if args.debugsend:
		print("send: "+json.dumps(send_data))
		sys.stdout.flush()
	ser.write(data.encode('iso8859-1'))

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
			send_data["breaks"] = int(control.breaks)
			send_serial(send_data)
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

def add_landing_info():
	global args
	global status_updates
	global conn
	if not args.noksp:
		if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
			return
		try:
			fligth = conn.space_center.active_vessel.flight()
			status_updates["surf_h"] = int(flight.surface_altitude)
			status_updates["surf_t"] = time_to_string(int(flight.surface_altitude/flight.vertical_speed))
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

def work_on_json(input_data):
	global args
	global status_updates
	global conn

	if not args.noksp:
		if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
			return
	try:
		if not args.noksp:
			control = conn.space_center.active_vessel.control
		data = json.loads(input_data)
		if "xtrans" in data:
			value = data["xtrans"]
			if not args.noksp:
				control.right = normiere_joystick(value)
		if "ytrans" in data:
			value = data["ytrans"]
			if not args.noksp:
				control.up = normiere_joystick(value)
		if "ztrans" in data:
			value = data["ztrans"]
			if not args.noksp:
				control.forward = normiere_joystick(value)
		if "yaw" in data:
			value = data["yaw"]
			if not args.noksp:
				control.yaw = normiere_joystick(value)
		if "pitch" in data:
			value = data["pitch"]
			if not args.noksp:
				control.pitch = normiere_joystick(value)
		if "roll" in data:
			value = data["roll"]
			if not args.noksp:
				control.roll = normiere_joystick(value)
		if "thrust" in data:
			value = data["thrust"]
			if not args.noksp:
				control.throttle = normiere_throttle(value)
		if "stage" in data and data["stage"]==1:
			if not args.noksp:
				control.activate_next_stage()
		if "sas" in data:
			if not args.noksp:
				if bool(data["sas"]):
					control.sas = not control.sas
				status_updates["sas"] = int(control.sas)
		if "rcs" in data:
			if not args.noksp:
				if bool(data["rcs"]):
					control.rcs = not control.rcs
				status_updates["rcs"] = int(control.rcs)
		if "gear" in data:
			if not args.noksp:
				if bool(data["gear"]):
					control.gear = not control.gear
				status_updates["gear"] = int(control.gear)
		if "lights" in data:
			if not args.noksp:
				if bool(data["lights"]):
					control.lights = not control.lights
				status_updates["lights"] = int(control.lights)
		if "breaks" in data:
			if not args.noksp:
				if bool(data["breaks"]):
					control.breaks = not control.breaks
				status_updates["breaks"] = int(control.breaks)
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

ser = serial.Serial(port, 38400, timeout=0)
if not args.noksp:
	conn = krpc.connect(name='mk console')
sleep(3)
ref_time_short = datetime.datetime.now()
ref_time_long = datetime.datetime.now()
send_handshake()
while True:
	check_serial()
	lines=serial_data.split("\n",1)
	if len(lines)==2: # means we have a full line
		if args.debugrecv:
			print( lines[0] )
			sys.stdout.flush()
		serial_data = lines[1]
		if args.debugchip:
			try:
				data = json.loads(lines[0])
				if "chip" in data:
					if data["chip"]!=last_chip_data:
						print("Chip: "+str(data["chip"]))
						last_chip_data = data["chip"]
				sys.stdout.flush()
			except ValueError:
				print('Decoding JSON failed for: '+lines[0])
		work_on_json(lines[0])
	now = datetime.datetime.now()
	diff_short = now - ref_time_short
	diff_long  = now - ref_time_long
	if (diff_short.seconds>0 or diff_short.microseconds>200000) and ser.out_waiting == 0:
		if diff_long.seconds>1:
			add_orbit_to_status()
			add_landing_info()
			ref_time_long = datetime.datetime.now()
		send_flight_data()
		ref_time_short = datetime.datetime.now()
