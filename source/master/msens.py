import json

from twisted.internet.error import ReactorAlreadyRunning
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor, task

import master, mprog, mroom

from master import HOST, SENSORPORT

registered_sensors = {}
lowest_sensor_id = 0
sensor_factory = None
unread_reports = 0

def SM(sensor_type = None, properties = {}, context = None):
	"""Generate a sensor registration message object.
	"""
	sm = {'message': 'SM'}
	sm['type'] = sensor_type
	sm['properties'] = properties
	sm['context'] = context
	return sm

def SR(properties = {}):
	"""Generate a sensor report message object.
	"""
	sr = {'message': 'SR'}
	sr['properties'] = properties
	return sr

def disconnect():
	sensor_factory.disconnect_all()

def generate_sensor_name():
	# It doesn't really matter in what form
	# or on what basis names are generated...
	global lowest_sensor_id
	name_to_return = lowest_sensor_id
	lowest_sensor_id += 1
	return str(name_to_return)

class Sensor:
	def __init__(self, sensor_registration = SM()):
		self.raw = sensor_registration
		self.raw['properties_types'] = self.raw.pop('properties')
		self.raw['properties'] = {key:None for key in self.raw['properties_types']}
		self.raw.pop('message')
		self.raw['id'] = generate_sensor_name()
		self.connection = None
		self.room = None
	def getType(self):
		return self.raw['type']
	def get(self, sensor_property):
		if 'properties' in self.raw and self.raw['properties'] and sensor_property in self.raw['properties']:
			return self.raw['properties'][sensor_property]
		else:
			return None
	def getRoom(self):
		if self.room:
			return self.room
		else:
			return None
	def _setRoom(self, new_room_id):
		self.room = mroom.get_room(new_room_id)
		location = None
		if self.raw['context'] and 'location' in self.raw['context']:
			location = self.raw['context']['location']
		new_context = master.CU(mroom.get_facility_id_of_room_id(new_room_id), self.room._id, location)
		new_context.pop('message')
		self.raw['context'] = new_context
		self.connection.sendData(json.dumps(master.get_CU(self.raw['context'])))
	def _getID(self):
		return self.raw['id']
	def _getData(self):
		# What kind of data does the user (terminal) want about a sensor? In what form?
		return {'id': self._getID(), 'type': self.getType(), 'properties': self.raw['properties_types'], 'context': self.raw['context']}

def get_sensors():
	return sensor_factory.sensors.values()

def get_sensor(sensor_id):
	if sensor_id in sensor_factory.sensors:
		return sensor_factory.sensors[sensor_id]
	else:
		return None

class SensorConnection(Protocol):
	def __init__(self):
		self.sensor_id = None
	def connectionLost(self, reason):
		self.cancel_timeout()
		self.factory.deregister_sensor(self)
	def dataReceived(self, data):
		self.cancel_timeout()
		self.add_timeout()
		self.factory.handle_message(self, data)
	def sendData(self, data):
		self.transport.writeSequence([str(data)])
	def add_timeout(self):
		self.mu = task.deferLater(reactor, 30, self.mark_unresponsive)
		self.mu.addBoth(self.do_nothing, self.do_nothing)
		self.dr = task.deferLater(reactor, 60, self.deregister)
		self.dr.addBoth(self.do_nothing, self.do_nothing)
	def do_nothing(self, a, b):
		pass
	def cancel_timeout(self):
		try:
			self.dr.cancel()
			self.mu.cancel()
		except AttributeError, e:
			pass
	def mark_unresponsive(self):
		print "Sensor {} is unresponsive...".format(self.sensor_id)
	def deregister(self):
		print "De-registering sensor {}...".format(self.sensor_id)
		self.disconnect()
	def disconnect(self):
		self.cancel_timeout()
		self.factory.deregister_sensor(self)
		self.transport.loseConnection()

class SensorFactory(Factory):
	protocol = SensorConnection
	def __init__(self):
		self.sensors = {}
		global sensor_factory
		sensor_factory = self
	def deregister_sensor(self, connection):
		if connection.sensor_id in self.sensors:
			del self.sensors[connection.sensor_id]
	def disconnect_all(self):
		for sensor in self.sensors.values():
			sensor.connection.disconnect()
	def handle_message(self, connection, line):
		try:
			message = json.loads(line)
			if connection.sensor_id in self.sensors:
				if message['message'] == 'SM':
					print "Sensor {} sent an unnecessary SM registration message..."
				elif message['message'] == 'SR':
					print "Got a report from sensor {}!".format(connection.sensor_id)
					for key in self.sensors[connection.sensor_id].raw['properties']:
						if key in message['properties']:
							self.sensors[connection.sensor_id].raw['properties'][key] = message['properties'][key]
					mprog.run_programs(self.sensors[connection.sensor_id])
				elif message['message'] == 'ER':
					print "Sensor {} reported an error: {}".format(connection.sensor_id, message['error'])
				else:
					print "Sensor {} sent an unhandled message..."
			else:
				if message['message'] == 'SM':
					sensor = Sensor(message)
					sensor.connection = connection
					connection.sensor_id = sensor._getID()
					self.sensors[connection.sensor_id] = sensor
					print "Added a sensor, {}!".format(connection.sensor_id)
				else:
					print "An unregistered sensor sent an unacceptable message..."
					connection.disconnect()
		except KeyError:
			# A message that wasn't a valid Responsive Rooms message.
			pass
		except ValueError:
			# A message that wasn't valid JSON.
			pass

def do_listening():
	print "Listening for sensors..."
	reactor.listenTCP(SENSORPORT, SensorFactory())
	try:
		reactor.run(installSignalHandlers=0)
	except ReactorAlreadyRunning, e:
		pass
