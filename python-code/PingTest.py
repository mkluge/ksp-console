#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import serial
from time import sleep
import sys
import argparse
import signal

# main
def main_function():
	global args

	parser = argparse.ArgumentParser()
	parser.add_argument("--port", help="which port to use", nargs=1, type=str, default="/dev/ttyS6")
	args = parser.parse_args()
	port = args.port[0]

	ser = serial.Serial( port, 115200, timeout=2)
	ser.reset_input_buffer()
	ser.reset_output_buffer()
	start = datetime.datetime.now()
	ser.write(b"r")
	ser.flush()
	ser.read(1)
	stop = datetime.datetime.now()
	delta = stop - start
	ms_diff = int(delta.total_seconds() * 1000)
	print( "ping: %d milliseconds" % ms_diff )


if __name__ == '__main__':
    main_function()
