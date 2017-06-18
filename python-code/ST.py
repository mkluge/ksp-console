import time
import krpc

conn = krpc.connect(name='Surface speed')
vessel = conn.space_center.active_vessel
ref_frame = vessel.orbit.body.reference_frame

frame = conn.space_center.ReferenceFrame.create_hybrid(position=ref_frame, rotation=vessel.surface_reference_frame)

while True:
    velocity = vessel.velocity(vessel.orbit.body.reference_frame)
    print('Surface velocity brf = (%.1f, %.1f, %.1f)' % velocity)
    velocity = vessel.velocity(vessel.orbit.body.non_rotating_reference_frame)
    print('Surface velocity nrf = (%.1f, %.1f, %.1f)' % velocity)
    velocity = vessel.velocity(frame)
    print('Surface velocity crf = (%.1f, %.1f, %.1f)' % velocity)
    speed = vessel.flight(ref_frame).horizontal_speed
    print('Surface speed = %.1f m/s' % speed)

    time.sleep(1)
