import time
import mdb
import mact
from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)

sensor_reports = []

class Facility:
	def __init__(self, rooms = []):
		self._roomlist = rooms
	def getRooms(self, identifier):
		filtered = []
		for room in self._roomlist:
			if actuator.getType() == identifier:
				filtered += [actuator]
		return filtered
	def getRooms(self, identifier):
		return self._roomlist

class Room:
	def __init__(self, actuatorlist = []):
		self._actuatorlist = actuatorlist
	def getActuators(self):
		return self._actuatorlist
	def getActuatorsByType(self, actuator_type):
		filtered = []
		for actuator in self._actuatorlist:
			if actuator.getType() == actuator_type:
				filtered += [actuator]
		return filtered

def register(sensorType, sensorRule):
	all_sensors_of_type = []
	print all_sensors
	for sensor in all_sensors:
		print sensor._sensorobject
		if sensor.getType() == sensorType:
			all_sensors_of_type += [Sensor(sensor)]
	sensorRule(Facility(), Room(), Sensor())

def add_report(report):
	sensor_reports.append(report)

def run_programs():
	global sensor_reports
	while True:
		for report in sensor_reports:
			print report
			value = int(report['properties']['number'])
			sensor_reports = sensor_reports[1:]
			if 'bigger_than_80.lua' in mdb.get_program_names() and value > 80 and len(mact.registered_actuators) > 0:
				print '...'
				mact.registered_actuators[0].set('text', str(value))
				mact.registered_actuators[0].set('unread', True)
			if 'smaller_than_10.lua' in mdb.get_program_names() and value < 80 and len(mact.registered_actuators) > 0:
				print '!!!'
				mact.registered_actuators[0].set('text', str(value))
				mact.registered_actuators[0].set('unread', True)
		time.sleep(0.1)