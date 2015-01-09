import time
import mdb, msens, mact, mroom
from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)

programs = {}

def like_lua(facility, room, sensor):
	random_number = sensor.get('number')
	for actuator in room.getActuatorsByType('tts'):
		actuator.set('text', random_number)

def run_programs(sensor):
	if not sensor or not sensor.getRoom():
		return
	room = sensor.getRoom()
	facility = mroom.get_facility_of_room(room)
	for program in [programs[program]['callable'] for program in programs if programs[program]['type'] == sensor.getType()]:
		program(facility, room, sensor)

def get_program_names():
	return programs.keys()

def get_program_code(program_name):
	if program_name in programs:
		return programs[program_name]['rule']
	else:
		return None

def insert_program(program_name, code):
	# {'bigger_than_80.lua':{'type':'random', 'code':'cooode', 'callable':CODE}, 'smaller_than_10.lua':{'type':'random', 'code':'morecooode', 'callable':CODE2}}
	if program_name not in programs:
		sensorType, sensorRule = parse_code(code)
		programs[program_name] = {'type': sensorType, 'rule': sensorRule, 'callable': lua.eval(sensorRule)}

def parse_code(code):
	sensorType, sensorRule = code.split("register(")[1].rsplit(")", 1)[0].split(",", 1)
	sensorType = sensorType.strip('\'"')
	sensorRule = sensorRule.strip()
	return sensorType, sensorRule

def delete_program(program_name):
	if program_name in programs:
		programs.pop(program_name)
