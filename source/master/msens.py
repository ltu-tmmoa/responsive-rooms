import json
import select
import socket
import time
import SocketServer
import mlua

from master import running, HOST, SENSORPORT

registered_sensors = []
sensor_id = 0
sensor_reports = []

def SM(sensor_type = None, properties = {}, context = None):
	sm = {'message': 'SM'}
	sm['type'] = sensor_type
	sm['properties'] = properties
	sm['context'] = context
	return json.dumps(sm)

def CU(facility = None, room = None, location = None):
	cu = {'message': 'CU'}
	cu['facility'] = facility
	cu['room'] = room
	if location:
		cu['location'] = {'x': location[0], 'y': location[1], 'z': location[2]}
	return json.dumps(cu)

def SR(properties = {}):
	sr = {'message': 'SR'}
	sr['properties'] = properties
	return json.dumps(sr)

def ER(description = ''):
	er = {'message': 'ER'}
	er['error'] = description
	return json.dumps(er)

class Sensor:
	def __init__(self, sensor_registration = SM(), connection_object = None):
		global sensor_id
		self._sensor = {'id': str(sensor_id), 'type': sensor_registration['type'],
						'properties': sensor_registration['properties'], 'context': sensor_registration['context']}
		sensor_id += 1
		self._connection_object = connection_object
	def getType(self):
		return self._sensor['type']
	def get(self, sensor_property):
		return self._sensor['properties'][sensor_property]
	def getRoom(self):
		return self._sensor['room']

def send_context_update(request, cu = CU()):
	request.sendall(cu)

class SensorListener(SocketServer.BaseRequestHandler):
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
						if last_contact:
							print "Sensor last contacted me at", time.time()-last_contact, "seconds after initial contact"
						if message['message'] == 'SM':
							self.last_contact = time.time()
							registered_sensors.append(Sensor(message, self))
							print "Added a sensor!"#, registered_sensors[-1]._sensor
						elif message['message'] == 'SR':
							mlua.add_report(message)
						elif message['message'] == 'ER':
							print "Sensor reported an error!"#, message['error']
						print
						print
						print
					except ValueError:
						pass
			time.sleep(0.1)

def do_listening():
	sensor_listener = SocketServer.TCPServer((HOST, SENSORPORT), SensorListener)
	sensor_listener.serve_forever()
