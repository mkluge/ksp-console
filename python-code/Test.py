import math
import time
import krpc
import numpy
import sys


conn = krpc.connect(name='Navball directions')
vessel = conn.space_center.active_vessel
r_frame = vessel.orbit.body.reference_frame
vs_frame = vessel.surface_reference_frame


vessel.control.sas = True
time.sleep(1)
vessel.control.sas_mode = vessel.control.sas_mode.retrograde

sys.exit(0)


#frame = vessel.surface_reference_frame
ap = vessel.auto_pilot
#ap.reference_frame = vessel.surface_velocity_reference_frame
#ap.reference_frame = vessel.surface_velocity_reference_frame
#ap.target_direction = (0,-1,0)
#ap.engage()

# Point the vessel west (heading of 270 degrees), with a pitch of 0 degrees
#d = vessel.flight(frame).velocity
#s = vessel.flight(frame).speed
#d = (d[0]/s,d[1]/s,-d[2]/s)
#ap.wait()
#time.sleep(20)

#while True:
#    print(vessel.flight(r_frame).horizontal_speed)
#    time.sleep(0.5)

#conn.drawing.add_direction((1, 0, 0), vessel.surface_reference_frame, d[0])
#conn.drawing.add_direction((0, 1, 0), vessel.surface_velocity_reference_frame, d[1])
#conn.drawing.add_direction((1, 0, 0), vessel.surface_velocity_reference_frame, d[0])
while True:
    d = vessel.velocity(r_frame)
    print(d)
#    s = vessel.flight(r_frame).speed
#    hs = vessel.flight(r_frame).horizontal_speed
#    vs = vessel.flight(r_frame).vertical_speed
#    a = (d[0]/s,d[1]/s,d[2]/s)
    conn.drawing.clear()
    conn.drawing.add_direction((math.copysign(1,d[0]), 0, 0), vs_frame, math.fabs(d[0])).color=(1,0,0)
    conn.drawing.add_direction((0, math.copysign(1,d[1]), 0), vs_frame, math.fabs(d[1])).color=(0,1,0)
    conn.drawing.add_direction((0, 0, math.copysign(1,d[2])), vs_frame, math.fabs(d[2])).color=(0,0,1)
#    angle = numpy.arcsin( hs/s )
#    print( "%.2f %.2f %.2f" % a )
#    print( "%3.2f %3.2f %d %d" % ( angle, math.degrees(angle), hs, s) )

#    ap.target_direction = (0,-d[1],-d[2])
#    ap.target_direction = (0,-a[1],-a[2])


while True:
    d = vessel.flight(frame).velocity
    s = vessel.flight(frame).speed/10
    d = (d[0]/s,d[1]/s,d[2]/s)
#    print("%3.1f %3.1f %3.1f" % d)
#    d = vessel.flight(vessel.surface_velocity_reference_frame).direction
#    d = vessel.flight(frame).direction
#    print("%3.1f %3.1f %3.1f" % d)
#    print("%3.1f %3.1f %3.1f" % (math.degrees(numpy.arcsin(d[0])),math.degrees(numpy.arcsin(d[1])),math.degrees(numpy.arcsin(d[2]))))
#    print("%3.1f %3.1f %3.1f" % (math.degrees(numpy.arccos(d[0])),math.degrees(numpy.arccos(d[1])),math.degrees(numpy.arccos(d[2]))))
#    print("--")
#    time.sleep(5)



ap.engage()


# Point the vessel west (heading of 270 degrees), with a pitch of 0 degrees
ap.target_direction = (0, 0, 0)
ap.wait()
time.sleep(20)

ap.disengage()






conn = krpc.connect(name='Visual Debugging')
vessel = conn.space_center.active_vessel

ref_frame = vessel.surface_velocity_reference_frame
#ref_frame = vessel.orbit.body.reference_frame
conn.drawing.add_direction((0, -1, 0), ref_frame)
while True:
    pass


time_buffer = 15

conn = krpc.connect(name='Landing')
vessel = conn.space_center.active_vessel
ap = vessel.auto_pilot
#frame = vessel.orbit.body.reference_frame
frame = vessel.orbital_reference_frame
ap.reference_frame = frame
#ap.engage()

# Set up streams for telemetry
ut = conn.add_stream(getattr, conn.space_center, 'ut')
#speed = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.orbital_reference_frame), 'speed')
speed = conn.add_stream(getattr, vessel.flight(frame), 'speed')
#ap.target_direction = (0.75,0.5,0)

while True:
    print(vessel.flight(frame).velocity)
    print(vessel.flight(frame).direction)
    print("--")
    time.sleep(5)


# initialize, we do steering ourselves
vessel.control.rcs = False
vessel.control.sas = False
vessel.control.throttle = 0.0
vessel.auto_pilot.reference_frame = vessel.orbit.body.orbital_reference_frame
#vessel.auto_pilot.engage()

print("Orientation")
while True:
    print(vessel.flight(vessel.orbit.body.orbital_reference_frame).direction)
    d=vessel.flight(vessel.orbit.body.orbital_reference_frame).retrograde
    print(d)
    print("--")
#    vessel.auto_pilot.target_pitch_and_heading(0,270)
    time.sleep(1)

vessel.auto_pilot.wait()
time.sleep(1)
vessel.auto_pilot.target_direction = (0,-1,0)
vessel.auto_pilot.wait()
time.sleep(1)
vessel.auto_pilot.target_direction = (1,0,0)
vessel.auto_pilot.wait()
time.sleep(1)
vessel.auto_pilot.target_direction = (-1,0,0)
vessel.auto_pilot.wait()
time.sleep(1)


#while hspeed()>0.1:
#    vessel.control.throttle = 1.0
#vessel.control.throttle = 0.0
