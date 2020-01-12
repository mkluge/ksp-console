import krpc
from time import sleep

conn = krpc.connect(name='Resources')
vessel = conn.space_center.active_vessel
control = vessel.control


for s in range(-1,10):
	stage_resources = vessel.resources_in_decouple_stage(s)
	print("stage:", s, stage_resources.names)
	print('Stage:', s, ' Oxidizer:', vessel.resources_in_decouple_stage(s, False).amount('Oxidizer'))

while True:
	print(control.current_stage)
#	stage_resources = vessel.resources_in_decouple_stage(stage=control.current_stage-1, cumulative=True)
	stage_resources = vessel.resources
	max_lf = stage_resources.max('LiquidFuel')
	max_ox = stage_resources.max('Oxidizer')
	print(stage_resources.amount('LiquidFuel'))
	print(stage_resources.amount('LiquidFuel'))
	sleep(1)
