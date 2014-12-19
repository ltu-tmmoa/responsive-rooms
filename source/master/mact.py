import json
import select
import socket
import time
import SocketServer

from master import running, HOST, ACTUATORPORT

registered_actuators = []
actuator_id = 0

def AM(type = None, properties = {}, context = None):
	am = {'message': 'AM'}
	am['type'] = type
	am['properties'] = properties
	am['context'] = context
	return json.dumps(am)

def CU(facility = None, room = None, location = None):
	cu = {'message': 'CU'}
	cu['facility'] = facility
	cu['room'] = room
	if location:
		cu['location'] = {'x': location[0], 'y': location[1], 'z': location[2]}
	return json.dumps(cu)

def AU(properties = {}):
	au = {'message': 'AU'}
	au['properties'] = properties
	return json.dumps(au)

def AR(properties = {}):
	ar = {'message': 'AR'}
	ar['properties'] = properties
	return json.dumps(ar)

def ER(description = ''):
	er = {'message': 'ER'}
	er['error'] = description
	return json.dumps(er)

class Actuator:
	def __init__(self, actuator_registration = AM(), connection_object = None):
		global actuator_id
		self._actuator = {'id': str(actuator_id), 'type': actuator_registration['type'],
						'properties': actuator_registration['properties'], 'context': actuator_registration['context']}
		actuator_id += 1
		self._connection_object = connection_object
	def getType(self):
		return self._actuator['type']
	def get(self, actuator_property):
		return self._actuator['properties'][actuator_property]
	def set(self, actuator_property, value):
		self._actuator['properties'][actuator_property] = value
		send_action_update(self._connection_object, self._actuator['properties'])
	def getRoom(self):
		return self._actuator['room']

send_queue = []

def send_action_update(target, properties):
	send_queue.append({'target': target, 'properties': properties})

class ActuatorListener(SocketServer.BaseRequestHandler):
	def handle(self):
		connected = True
		last_contact = None
		while connected:
			readable, writable, _ = select.select([self.request], [self.request], [])
			for r in readable:
				if r == self.request:
					try:
						message = self.request.recv(1024).strip()
						message = json.loads(message)
						if message['message'] == 'AM':
							registered_actuators.append(Actuator(message, self))
							print "Added an actuator!"#, registered_actuators[-1]._actuator
						else:
							print "Another message than AM..."
						print
						print
						print
					except ValueError:
						pass
			for w in writable:
				if w == self.request and len(send_queue) > 0:
					for i in range(len(send_queue)-1):
						if send_queue[i]['target'] == self:
							to_send = AU(send_queue.pop(i)['properties'])
							print "Sending to actuator..."#, to_send
							self.request.sendall(to_send)
			time.sleep(0.1)

def do_listening():
	actuator_listener = SocketServer.TCPServer((HOST, ACTUATORPORT), ActuatorListener)
	actuator_listener.serve_forever()
