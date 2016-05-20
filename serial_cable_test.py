#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import krpc
import serial
from time import sleep
import sys
import json

port = "COM4"
ser = serial.Serial(port, 38400, timeout=0)
conn = krpc.connect(name='Hello World')
control = conn.space_center.active_vessel.control

serial_data="";

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

def send_handshake():
	send_data = {}
	send_data["start"] = 2016
	send_serial(send_data)

def send_serial(send_data):
	data=json.dumps(send_data)+"\n"
	ser.write(data.encode('iso8859-1'))

def send_flight_data():
	vessel = conn.space_center.active_vessel
	send_data = {}
	send_data["height"] = int(vessel.flight().surface_altitude)
	send_data["speed"] = int(vessel.flight(vessel.orbit.body.reference_frame).speed)
	send_serial(send_data)

def work_on_json(input_data):
	try:
		data = json.loads(input_data)
		if "yaw" in data:
			value = data["yaw"]
			control.yaw = normiere_joystick(value)
		if "pitch" in data:
			value = data["pitch"]
			control.pitch = normiere_joystick(value)
		if "roll" in data:
			value = data["roll"]
			control.roll = normiere_joystick(value)
	except ValueError:
		print('Decoding JSON failed')

## main
sleep(3)
ref_time = datetime.datetime.now()
send_handshake()
while True:
	check_serial()
	lines=serial_data.split("\n",1)
	if len(lines)==2: # means we have a full line
		serial_data = lines[1]
		work_on_json(lines[0])
	now = datetime.datetime.now()
	diff = now - ref_time
	if (diff.seconds>0 or diff.microseconds>500000) and ser.out_waiting == 0:
		send_flight_data()
		ref_time = datetime.datetime.now()
