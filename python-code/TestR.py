import math
import time
import krpc
import numpy
import sys

conn = krpc.connect(name='Resources')
vessel = conn.space_center.active_vessel
control = vessel.control

stage_resources = vessel.resources_in_decouple_stage(stage=control.current_stage, cumulative=False)

print stage_resources.names
