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
import signal


#port = "COM4"
#port = "/dev/ttyS6"
port = "/dev/ttyS4"
ser = ""
args = ""

class PerfData:
	def __init__(self):
		self.clear()

	def startTimer( self, name):
		self.timers[name] = datetime.datetime.now()

	def stopTimer( self, name):
		stop = datetime.datetime.now()
		if not name in self.timers.keys():
			print("can't stop timer %s, has not been started yet" % (name))
			return
		delta = stop - self.timers[name]
		ms_diff = int(delta.total_seconds() * 1000)
		self.set( name, ms_diff)
		del self.timers[name]

	def set( self, key, value):
		self.values[key]=value
	
	def clear( self):
		self.values={}
		self.timers={}

	def dump( self):
		for key in self.values.keys():
			print("%s: %.2f ms" % (key, self.values[key]))

class Telemetry:
	def __init__(self, conn, args):
		self.conn = conn
		self.args = args
		self.init_vessel()

	def init_vessel(self):
		try:
			self.vessel = conn.space_center.active_vessel
			self.control = self.vessel.control
			self.orbit = self.vessel.orbit
			# Set up streams for telemetry
			self.ut = conn.add_stream(getattr, conn.space_center, 'ut')
			self.altitude = conn.add_stream(getattr, self.vessel.flight(), 'surface_altitude')
			self.apoapsis = conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
			self.speed    = conn.add_stream(getattr, self.vessel.flight(self.vessel.orbit.body.reference_frame), 'speed')
			self.sas      = conn.add_stream(getattr, self.control, 'sas')
			self.rcs      = conn.add_stream(getattr, self.control, 'rcs')
			self.lights   = conn.add_stream(getattr, self.control, 'lights')
			self.gear     = conn.add_stream(getattr, self.control, 'gear')
			self.brakes   = conn.add_stream(getattr, self.control, 'brakes')
		except krpc.error.RPCError:
			self.vessel="none"
			pass

	def add_action_group_status(self, status_updates):
		if not self.args.noksp:
			if self.conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
				return
			try:
				#vessel = self.conn.space_center.active_vessel
				control = self.vessel.control
	#			print("status of all groups is "+str(status))
	#			sys.stdout.flush()
			except krpc.error.RPCError:
				pass
			except ValueError:
				pass
		return status_updates

	def	add_orbit_to_status(self, status_updates):
		if not args.noksp:
			if self.conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
				return
			status_updates[str(INFO_PERIAPSIS)] = "n/a"
			status_updates[str(INFO_PERIAPSIS_TIME)] = "n/a"
			try:
				orbit = self.conn.space_center.active_vessel.orbit
				status_updates[str(INFO_APOAPSIS)] = int(orbit.apoapsis_altitude)
				status_updates[str(INFO_APOAPSIS_TIME)] = time_to_string(int(orbit.time_to_apoapsis))
				if orbit.periapsis_altitude>0:
					status_updates[str(INFO_PERIAPSIS)] = int(orbit.periapsis_altitude)
					status_updates[str(INFO_PERIAPSIS_TIME)] = time_to_string(int(orbit.time_to_periapsis))
			except krpc.error.RPCError:
				pass
			except ValueError:
				pass
			except OverflowError:
				pass
		return status_updates

	def	add_landing_info(self, status_updates):
		if not self.args.noksp:
			if self.conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
				return
			try:
				flight = self.conn.space_center.active_vessel.flight()
				status_updates[str(INFO_SURFACE_HEIGHT)] = int(flight.surface_altitude)
				speed = int( self.conn.space_center.active_vessel.flight( self.conn.space_center.active_vessel.orbit.body.reference_frame).vertical_speed)
				if( speed<0.0 ):
					status_updates[str(INFO_SURFACE_TIME)] = time_to_string(int(flight.surface_altitude/abs(speed)))
				else:
					status_updates[str(INFO_SURFACE_TIME)] = "n/a"
			except krpc.error.RPCError:
				pass
			except ValueError:
				pass
		return status_updates

	def add_main_data(self, status_updates):
		# if we do not have a vessel: test, if we can get one
		if self.vessel=="none":
			self.init_vessel()
			if self.vessel=="none":
				return
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

	def add_display_data(self):
		display_data = {}
		# if we do not have a vessel: test, if we can get one
		if self.vessel=="none":
			self.init_vessel()
			if self.vessel=="none":
				return
		# did the vessel change? then update streams
		if self.vessel != self.conn.space_center.active_vessel:
			self.init_vessel()

		display_data[str(INFO_HEIGHT)] = int(self.altitude())
		display_data[str(INFO_SPEED)] = int(self.speed())
		stage_resources = self.vessel.resources_in_decouple_stage(stage=self.control.current_stage, cumulative=False)
		max_lf = stage_resources.max('LiquidFuel')
		max_ox = stage_resources.max('Oxidizer')
		max_mo = stage_resources.max('MonoPropellant')
		max_el = stage_resources.max('ElectricCharge')
		if max_lf!=0:
			display_data[str(INFO_PERCENTAGE_FUEL)] = stage_resources.amount('LiquidFuel') * 100 / max_lf
		if max_ox!=0:
			display_data[str(INFO_PERCENTAGE_OXYGEN)] = stage_resources.amount('Oxidizer') * 100 / max_ox
		if max_mo!=0:
			display_data[str(INFO_PERCENTAGE_RCS)] = stage_resources.amount('MonoPropellant') * 100 / max_mo
		if max_el!=0:
			display_data[str(INFO_PERCENTAGE_BATTERY)] = stage_resources.amount('ElectricCharge') * 100 / max_el
		display_data = self.add_orbit_to_status(display_data)
		display_data = self.add_landing_info(display_data)
		return display_data

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
		# whether sas was on before the joystick values where
		# feed into ksp
		self.last_yaw=0
		self.last_pitch=0
		self.last_roll=0
		self.was_sas_on=False
		self.last_sas_type=0
		self.joystick_sas_has_been_handled=False

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
		return 0
	if value>890:
		return 1
	return float(value)/1000.0

def send_handshake():
	send_data = {}
	send_data["start"] = 2016
	send_serial( CMD_INIT, send_data)

def send_serial( command, send_data, chunksize=400):
	global args
	global ser
	send_data["cmd"]=command
	data=json.dumps(send_data,separators=(',',':'))+'+'
	data = data.encode('iso8859-1')
	if args.debugsend:
		print("sending %d bytes " % len(data))
		print("send: "+str(data))
		sys.stdout.flush()
	#got to send in 32 byte chunks to avoid loosing stuff
#	len_data = str(len(data))+":"
#	ser.write(len_data.encode('iso8859-1'))
	while( len(data)>0 ):
		send_pkt = data[:chunksize]
		data = data[chunksize:]
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

def send_display_update(status_updates):
	global args
	global conn
	if not args.noksp:
		if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
			return
		try:
			send_data = encode_json_array(status_updates)
			send_serial( CMD_UPDATE_DISPLAY, {"disp":send_data})
		except krpc.error.RPCError:
			pass

def send_main_update(status_updates):
	global args
	global conn
	if not args.noksp:
		if conn.krpc.current_game_scene!=conn.krpc.GameScene.flight:
			return
		try:
			send_data = encode_json_array(status_updates)
			send_serial( CMD_UPDATE_CONSOLE, {"data":send_data})
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
			try:
				solar.deployed = value
			except:
				pass

def check_input_and_feedback( data, key_str, key, control):
	global args
	global conn
	if key in data and not args.noksp:
		if bool(data[key]):
			setattr( control, key_str, not getattr( control, key_str))

def check_analog( data, key, control, ckey):
	global state
#	sas_off_limit=0.15
	if key in data:
		value = normiere_joystick(data[key])
		if not args.noksp:
#			# if SAS is on and we have rotation, disable yaw
#			# and steer
#			if key==KSP_INPUT_YAW:
#				state.last_yaw=value
#			if key==KSP_INPUT_ROLL:
#				state.last_roll=value
#			if key==KSP_INPUT_PITCH:
#				state.last_pitch=value
#			if abs(state.last_yaw)>sas_off_limit or abs(state.last_roll)>sas_off_limit or abs(state.last_pitch)>sas_off_limit:
#				if state.joystick_sas_has_been_handled==False:
#				   	if control.sas==True:
#						state.last_sas_type = control.sas_mode
#						state.was_sas_on = True
#						control.sas = False
#					else:
#						state.was_sas_on = False
#					state.joystick_sas_has_been_handled=True
#			else:
#				if state.was_sas_on == True:
#					control.sas = True
#					control.sas_mode = state.last_sas_type
#					state.sas_was_on = False
#				state.joystick_sas_has_been_handled = False
			setattr( control, ckey, value)

def work_on_json(input_data):
	global args
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
		check_input( data, BUTTON_FUEL, lambda: button_fuel( vessel))
		check_input( data, BUTTON_REACTION_WHEELS, lambda: button_reaction_wheels( vessel))
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
#	except krpc.error.RPCError:
#		pass

# main
def main_function():
	global ser
	global args
	global conn
	global state
	global telemetry
	global perf_data

	perf_data = PerfData()
	last_chip_data = 0
	parser = argparse.ArgumentParser()
	parser.add_argument("--debugsend", help="print data sent to con", action="store_true")
	parser.add_argument("--debugrecv", help="print some received from con", action="store_true")
	parser.add_argument("--debugchip", help="print chip debug output", action="store_true")
	parser.add_argument("--noksp", help="run without connecting to ksp", action="store_true")
	args = parser.parse_args()

	serial_connected = False
	krpc_connected = False
	# run forever (until ctrl-c)
	while True:
		try:
			# first: try to connect everything
			if krpc_connected == False and not args.noksp:
				conn = krpc.connect(name='mk console')
				state = State(conn)
				telemetry = Telemetry(conn, args)
				krpc_connected = True
				ref_time = datetime.datetime.now()
		except (krpc.error.RPCError, ConnectionRefusedError):
			krpc_connected = False
			pass

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
					#if (time_diff.seconds>1 or time_diff.microseconds>300000) and ser.out_waiting == 0:
					if (time_diff.seconds>1 ):
						if conn.krpc.current_game_scene==conn.krpc.GameScene.flight:
							# send main controller data
							main_updates = {}
							perf_data.startTimer("collectMainData")
							main_updates = telemetry.add_main_data(main_updates)
							perf_data.stopTimer("collectMianData")
							perf_data.startTimer("sendMainUpdates")
							send_main_update(main_updates)
							perf_data.stopTimer("sendMainUpdates")
							# every second time: also send display update
							if should_send==True:
								perf_data.startTimer("collectDisplayData")
								display_updates = telemetry.add_display_data()
								perf_data.stopTimer("collectDisplayData")
								perf_data.startTimer("sendDisplayUpdates")
								send_display_update(display_updates)
								perf_data.stopTimer("sendDisplayUpdates")
								should_send = False
							else:
								should_send = True
						ref_time = now

					# read the current status and button updates and so on
					perf_data.startTimer("update process")
					perf_data.startTimer("send GET_UPDATES")
					send_serial( CMD_GET_UPDATES, {})
					perf_data.stopTimer("send GET_UPDATES")
					perf_data.startTimer("readline")
					serial_data=serial_read_line()
					perf_data.stopTimer("readline")
					if args.debugrecv:
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
					perf_data.startTimer("workJson")
					work_on_json(serial_data)
					perf_data.stopTimer("workJson")
					perf_data.stopTimer("update process")
					perf_data.dump()
					perf_data.clear()
			else:
				# not everything connected, sleep and try again
				print( "Connection missing: KRPC:%s Serial:%s\n" %
					   ("online" if krpc_connected else "offline",
						"connected" if serial_connected else "disconnected"))
				sleep(1)
		except (krpc.error.RPCError, ConnectionRefusedError):
			krpc_connected = False
			pass
		except serial.SerialException:
			serial_connected = False
			pass

if __name__ == '__main__':
    main_function()
