#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import serial
from time import sleep
from time import time
import sys
import json
import argparse
from ksp_console import *
import signal


#port = "COM4"
port = "/dev/ttyS6"
ser = ""
args = ""

class Telemetry:
	def __init__(self, conn, args):
		self.conn = conn
		self.args = args
		self.init_vessel()

	def init_vessel(self):
		self.altitude = 0
		self.apoapsis = 999
		self.speed    = 0
		self.sas      = False
		self.rcs      = False
		self.lights   = False
		self.gear     = False
		self.brakes   = False

	def	add_orbit_to_status(self, status_updates):
		status_updates[str(INFO_PERIAPSIS)] = "999"
		status_updates[str(INFO_PERIAPSIS_TIME)] = "8s"
		return status_updates

	def	add_landing_info(self, status_updates):
		status_updates[str(INFO_SURFACE_HEIGHT)] = "124"
		status_updates[str(INFO_SURFACE_TIME)] = "2s"
		return status_updates

	def add_data(self, status_updates):
		self.altitude = self.altitude+1
		self.speed    = 22
		if (int(time())%10) < 5:
			self.button = 1
		else:
			self.button = 0
		status_updates[str(INFO_HEIGHT)] = self.altitude
		status_updates[str(INFO_SPEED)] = self.speed
		status_updates[str(BUTTON_SAS)] = self.button
		status_updates[str(BUTTON_RCS)] = self.button
		status_updates[str(BUTTON_LIGHTS)] = self.button
		status_updates[str(BUTTON_GEAR)] = self.button
		status_updates[str(BUTTON_BREAKS)] = self.button
		status_updates = self.add_orbit_to_status(status_updates)
		status_updates = self.add_landing_info(status_updates)
		return status_updates

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
	print(len(arr))
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

def send_updates(status_updates):
	send_data = encode_json_array(status_updates)
	send_serial( CMD_UPDATE_CONSOLE, {"data":send_data})
	status_updates={}

def work_on_json(input_data):
	global args
	global state

	json_data = json.loads(input_data)
	data = decode_json_array(json_data["data"])
	if args.debugrecv:
		if len(data)>0:
			print( data )
			sys.stdout.flush()

# main
def main_function():
	global ser
	global args
	global state
	global telemetry

	last_chip_data = 0
	parser = argparse.ArgumentParser()
	parser.add_argument("--debugsend", help="print data sent to con", action="store_true")
	parser.add_argument("--debugrecv", help="print some received from con", action="store_true")
	parser.add_argument("--debugchip", help="print chip debug output", action="store_true")
	args = parser.parse_args()
	telemetry = Telemetry( "nix", args)
	ref_time = datetime.datetime.now()

	serial_connected = False
	# run forever (until ctrl-c)
	while True:
		try:
			if serial_connected == False:
				print("trying serial")
				ser = serial.Serial( port, 115200, timeout=2)
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
			pass

		try:
			if serial_connected:
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
					#if (time_diff.seconds>1 or time_diff.microseconds>300000) and ser.out_waiting == 0:
					if (time_diff.seconds>1 or time_diff.microseconds>100000):
						status_updates = {}
						status_updates = telemetry.add_data(status_updates)
						send_updates(status_updates)
						ref_time = now

					# read the current status and button updates and so on
					send_serial( CMD_GET_UPDATES, {})
					serial_data=serial_read_line()
					if args.debugrecv:
						print("Got %d bytes of data\n" % (len(serial_data)))
						print(serial_data)
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
			else:
				# not everything connected, sleep and try again
				print( "Connection missing: Serial:%s\n" %
						("connected" if serial_connected else "disconnected"))
				sleep(1)
		except serial.SerialException:
			serial_connected = False
			pass

if __name__ == '__main__':
    main_function()
