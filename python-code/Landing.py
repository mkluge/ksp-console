import math
import time
import datetime
import krpc
import sys
import signal

rows = 0
time_buffer = 15
conn = krpc.connect(name='Landing')
vessel = conn.space_center.active_vessel
ut = conn.add_stream(getattr, conn.space_center, 'ut')
ap = vessel.auto_pilot
stream_list = []
# setup a little window to watch telemetry
canvas = conn.ui.stock_canvas
# Get the size of the game window in pixels
screen_size = canvas.rect_transform.size
panel = canvas.add_panel()
# Position the panel on the left of the screen
rect = panel.rect_transform
rect.size = ( 200, 600)
ur = (screen_size[0]/2-50,screen_size[1]/2-60)
rect.upper_right = ur
rect.lower_left = (ur[0]-190,ur[1]-600)

def add_line( content ):
    global panel
    global rows
    row_height = 18
    total_width = 180
    div_at = 110
    border = 10
    height = panel.rect_transform.size[1]
    # Add a panel to contain the UI elements
    text = panel.add_text( content )
    text.rect_transform.size = ( div_at, row_height)
    row_vpos=(height/2-row_height/2) - rows*row_height
    text.rect_transform.position = ( -((total_width-2*border)-div_at)/2, row_vpos)
    text.color = (1, 1, 1)
    text.size = 12
    # and the value for this panel
    text = panel.add_text( "" )
    text.rect_transform.size = ( total_width-div_at, row_height)
    row_vpos=(height/2-row_height/2) - rows*row_height
    text.rect_transform.position = ( ((total_width-2*border)-(total_width-div_at))/2, row_vpos)
    text.color = (1, 1, 1)
    text.size = 12
    rows = rows + 1
    return text

# Add some text displaying the total engine thrust
t_thrust = add_line("Thrust")
t_yspeed = add_line("Y speed")
t_zspeed = add_line("Z speed")
t_hspeed = add_line("horz. speed")
t_vspeed = add_line("vert. speed")
t_burn = add_line("burn time")
t_land = add_line("crash time")


def signal_handler(signal, frame):
        global ap
        global conn
        global stream_list
        ap.disengage()
        conn.ui.clear()
        [conn.remove_stream(sid) for sid in stream_list]
        sys.exit(0)

#signal.signal(signal.SIGINT, signal_handler)

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

# initialize, we do steering ourselves
vessel.control.rcs = False
vessel.control.throttle = 0.0
vessel.control.sas = False
#vessel.control.speed_mode = vessel.control.speed_mode.surface
#vessel.control.sas_mode = vessel.control.sas_mode.retrograde
# main descent loop

if vessel.specific_impulse==0:
    print("no engines")
    sys.exit(1)

ap.reference_frame = vs_frame
ap.engage()

grav = vessel.orbit.body.surface_gravity
F = vessel.max_vacuum_thrust
Isp = vessel.vacuum_specific_impulse * grav
flow_rate = F / Isp
burn_time=0
while True:
    # Calculate burn time (using rocket equation)
    m0 = vessel.mass
    m1 = m0 / math.exp(math.fabs(vspeed())/Isp)
    burn_time = (m0 - m1) / flow_rate
    t_burn.content = "%.1f sec" % burn_time
    # t = (v0 + sqrt(v0*v0 + 2ah))/a
    vs=vspeed()
    if( hspeed()<1 ):
        vessel.control.throttle = 0
        break
    t_vspeed.content = "%d m/s" % vs
    time_to_landing = (vs+math.sqrt(vs*vs+2*grav*altitude()))/grav
    t_land.content = "%.1f sec" % time_to_landing
    diff = time_to_landing - burn_time
    # ups, not enough time left to kill all speed
    if diff<0:
        print("crashing, not enough time")
        break
    # lots of time, so we can cancel horizontal speed first
    if diff>time_buffer:
        hkill_time_start = ut()
        while (ut()-hkill_time_start) < time_buffer/2:
            t_hspeed.content = "%d m/s" % hspeed()
            t_vspeed.content = "%d m/s" % vspeed()
            d = velocity()
            s = speed()
            a = (d[0]/s,d[1]/s,d[2]/s)
            t_yspeed.content = "%d m/s" % d[1]
            t_zspeed.content = "%d m/s" % d[2]
            ap.target_direction = (0,-a[1],-a[2])
#            conn.drawing.clear()
#            conn.drawing.add_direction((0, math.copysign(1,d[1]), 0), vs_frame, math.fabs(d[1])).color=(0,1,0)
#            conn.drawing.add_direction((0, 0, math.copysign(1,d[2])), vs_frame, math.fabs(d[2])).color=(0,0,1)
            #ap.wait()
            r=math.sqrt(d[1]*d[1]+d[2]*d[2])
            if r>10:
                vessel.control.throttle = 1
            elif r>5:
                vessel.control.throttle = 0.3
            elif r>1:
                vessel.control.throttle = 0.1
            else:
                vessel.control.throttle = 0.0
                break
            t_thrust.content = '%d kN' % (vessel.thrust/1000)
            time.sleep(0.1)
    else:
        break

conn.drawing.clear()
print ("Landing burn sleep")
ap.reference_frame = vsv_frame
ap.target_direction = (0,-1,0)
ap.disengage()
vessel.control.sas = True
time.sleep(1)
vessel.control.sas_mode = vessel.control.sas_mode.retrograde

acc = F / vessel.mass - vessel.orbit.body.surface_gravity
vs = vspeed()
bh = (vs*vs)/(2*acc)
print("bh: %.1f" % bh)
while (altitude())>bh:
    acc = F / vessel.mass - vessel.orbit.body.surface_gravity
    vs = vspeed()
    bh = (vs*vs)/(2*acc)
    print("bh: %.1f" % bh)

#grav = float(vessel.orbit.body.mass) / float((vessel.orbit.body.equatorial_radius+flight.mean_altitude)**2)
#print(grav)
#print(flight.mean_altitude)
#twr = float(F) / float(vessel.mass*grav)
#while (altitude()*grav*0.99) < (( (altitude()*grav) + (0.5*vspeed()*vspeed()) )/twr):
#    grav = float(vessel.orbit.body.mass) / float((vessel.orbit.body.equatorial_radius+flight.mean_altitude)**2)
#    twr = float(F) / float(vessel.mass*grav)

print ("Landing burn !")
while math.fabs(vspeed())>10:
    vessel.control.throttle = 1

# now we are usually a few meters above ground
target_vspeed=-2
# keep vessel at 1.5 m/s until landed
while altitude()>5 or vspeed()>0.5 :
    vs = vspeed()
#    print(altitude())
    speed_error = target_vspeed - vs
    throttle = (vessel.mass * ((flight.g_force - vs) + speed_error)) / F
    throttle = max(min(1, throttle), 0)
    vessel.control.throttle = throttle

vessel.control.throttle = 0
time.sleep(2)
vessel.control.sas = True
conn.ui.clear()
