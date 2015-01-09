import json

from twisted.internet.error import ReactorAlreadyRunning
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor, task

import master, mroom

from master import HOST, ACTUATORPORT

registered_actuators = {}
lowest_actuator_id = 0
actuator_factory = None

def AM(actuator_type = None, properties = {}, context = None):
	"""Generate an actutator registration message object.
	"""
	am = {'message': 'AM'}
	am['type'] = actuator_type
	am['properties'] = properties
	am['context'] = context
	return am

def AU(properties = {}):
	"""Generate an actutator update message object.
	"""
	au = {'message': 'AU'}
	au['properties'] = properties
	return au

def AR(properties = {}):
	"""Generate an actutator report message object.
	"""
	ar = {'message': 'AR'}
	ar['properties'] = properties
	return ar

def disconnect():
	actuator_factory.disconnect_all()

def generate_actuator_name():
	# It doesn't really matter in what form
	# or on what basis names are generated...
	global lowest_actuator_id
	name_to_return = lowest_actuator_id
	lowest_actuator_id += 1
	return str(name_to_return)

class Actuator:
	def __init__(self, actuator_registration = AM()):
		self.raw = actuator_registration
		self.raw['properties_types'] = self.raw.pop('properties')
		self.raw['properties'] = {key:None for key in self.raw['properties_types']}
		self.raw.pop('message')
		self.raw['id'] = generate_actuator_name()
		self.connection = None
		self.room = None
	def getType(self):
		return self.raw['type']
	def get(self, actuator_property):
		if 'properties' in self.raw and self.raw['properties'] and actuator_property in self.raw['properties']:
			return self.raw['properties'][actuator_property]
		else:
			return None
	def set(self, actuator_property, new_value):
		if 'properties' in self.raw and actuator_property in self.raw['properties']:
			self.raw['properties'][actuator_property] = new_value
			self.connection.sendData(json.dumps(AU({actuator_property: new_value})))
	def getRoom(self):
		if self.room:
			return self.room
		else:
			return None
	def _setRoom(self, new_room_id):
		self.room = mroom.get_room(new_room_id)
		mroom.put_actuator_in_room(self, new_room_id)
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
		# What kind of data does the user (terminal) want about an actuator? In what form?
		return {'id': self._getID(), 'type': self.getType(), 'properties': self.raw['properties_types'], 'context': self.raw['context']}

def get_actuators():
	return actuator_factory.actuators.values()

def get_actuator(actuator_id):
	if actuator_id in actuator_factory.actuators:
		return actuator_factory.actuators[actuator_id]
	else:
		return None

class ActuatorConnection(Protocol):
	def __init__(self):
		self.actuator_id = None
	def connectionLost(self, reason):
		self.cancel_timeout()
		self.factory.deregister_actuator(self)
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
		print "Actuator {} is unresponsive...".format(self.actuator_id)
	def deregister(self):
		print "De-registering actuator {}...".format(self.actuator_id)
		self.disconnect()
	def disconnect(self):
		self.cancel_timeout()
		self.factory.deregister_actuator(self)
		self.transport.loseConnection()

class ActuatorFactory(Factory):
	protocol = ActuatorConnection
	def __init__(self):
		self.actuators = {}
		global actuator_factory
		actuator_factory = self
	def deregister_actuator(self, connection):
		if connection.actuator_id in self.actuators:
			del self.actuators[connection.actuator_id]
	def disconnect_all(self):
		for actuator in self.actuators.values():
			actuator.connection.disconnect()
	def handle_message(self, connection, line):
		try:
			message = json.loads(line)
			if connection.actuator_id in self.actuators:
				if message['message'] == 'AM':
					print "Actuator {} sent an unnecessary AM registration message..."
				elif message['message'] == 'AR':
					print "Got a report from actuator {}!".format(connection.actuator_id)
					for key in self.actuators[connection.actuator_id].raw['properties']:
						if key in message['properties']:
							self.actuators[connection.actuator_id].raw['properties'][key] = message['properties'][key]
				elif message['message'] == 'ER':
					print "Actuator {} reported an error: {}".format(connection.actuator_id, message['error'])
				else:
					print "Actuator {} sent an unhandled message..."
			else:
				if message['message'] == 'AM':
					actuator = Actuator(message)
					actuator.connection = connection
					connection.actuator_id = actuator._getID()
					self.actuators[connection.actuator_id] = actuator
					print "Added an actuator, {}!".format(connection.actuator_id)
				else:
					print "An unregistered actuator sent an unacceptable message..."
					connection.disconnect()
		except KeyError:
			# A message that wasn't a valid Responsive Rooms message.
			pass
		except ValueError:
			# A message that wasn't valid JSON.
			pass

def do_listening():
	print "Listening for actuators..."
	reactor.listenTCP(ACTUATORPORT, ActuatorFactory())
	try:
		reactor.run(installSignalHandlers=0)
	except ReactorAlreadyRunning, e:
		pass
