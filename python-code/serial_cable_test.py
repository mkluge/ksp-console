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
	if args.debug:
		print("send: "+data)
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
			send_data["ap"] = int(orbit.apoapsis_altitude)
			send_data["ap_t"] = int(orbit.time_to_apoapsis)
			send_data["pe"] = int(orbit.periapsis_altitude)
			send_data["pe_t"] = int(orbit.time_to_periapsis)
			send_serial(send_data)
			status_updates={}
		except krpc.error.RPCError:
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
	except ValueError:
		print('Decoding JSON failed')
	except krpc.error.RPCError:
	 	pass

## main

last_chip_data = 0
parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="print some debug output", action="store_true")
parser.add_argument("--debugchip", help="print chip debug output", action="store_true")
parser.add_argument("--noksp", help="run without connecting to ksp", action="store_true")
args = parser.parse_args()
if args.debug:
	print("debug: will print a lot of debug output")
if args.noksp:
	print("noksp: will not connect to KSP")

ser = serial.Serial(port, 38400, timeout=0)
if not args.noksp:
	conn = krpc.connect(name='mk console')
sleep(3)
ref_time = datetime.datetime.now()
send_handshake()
while True:
	check_serial()
	lines=serial_data.split("\n",1)
	if len(lines)==2: # means we have a full line
		if args.debug:
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
	diff = now - ref_time
	if (diff.seconds>0 or diff.microseconds>200000) and ser.out_waiting == 0:
		send_flight_data()
		ref_time = datetime.datetime.now()
