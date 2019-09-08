import math
import time
import datetime
import krpc
import sys
import signal

rows = 0
time_buffer = 15
conn = krpc.connect(name='Start')
vessel = conn.space_center.active_vessel
ut = conn.add_stream(getattr, conn.space_center, 'ut')
ap = vessel.auto_pilot
stream_list = []

# Set up streams for telemetry
r_frame = vessel.orbit.body.reference_frame
vs_frame = vessel.surface_reference_frame
vsv_frame = vessel.surface_velocity_reference_frame
ref_frame = vessel.orbit.body.reference_frame
landing_frame = conn.space_center.ReferenceFrame.create_hybrid(position=r_frame, rotation=vessel.surface_reference_frame)
flight=vessel.flight(landing_frame)
velocity = conn.add_stream(getattr, flight, 'velocity')
altitude = conn.add_stream(getattr, flight, 'surface_altitude')
speed = conn.add_stream(getattr, flight, 'speed')
hspeed = conn.add_stream(getattr, flight, 'horizontal_speed')
vspeed = conn.add_stream(getattr, flight, 'vertical_speed')
stream_list = [velocity, altitude, speed, hspeed, vspeed]

vessel.control.rcs = False
vessel.control.throttle = 0.0
vessel.control.sas = True

grav = vessel.orbit.body.surface_gravity
F = vessel.max_thrust
Isp = vessel.specific_impulse * grav
flow_rate = F / Isp

target_vspeed=2
throttle_add=0.001
while altitude()<1000:
    vs = vspeed()
    print(vs)
    speed_error = target_vspeed - vs
    throttle = vessel.control.throttle
    throttle = throttle + (speed_error*throttle_add)
    throttle = (vessel.mass * ((flight.g_force - vs) + speed_error)) / F
    throttle = max(min(1, throttle), 0)
    vessel.control.throttle = throttle

vessel.control.throttle = 0
time.sleep(2)
vessel.control.sas = True
conn.ui.clear()
