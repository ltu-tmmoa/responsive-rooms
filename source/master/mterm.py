# -*- coding: utf-8 -*-
from flask import Flask, request
from flask.ext.restful import Resource, Api
import json
import time

import msens, mact, mprog
from master import HOST, TERMINALPORT

app = Flask(__name__)
api = Api(app)

def filter_out(list_of_dicts, key, value, inner = None):
	"""Return a subset of a list where keys (possibly keys under an inner key) are set to value.
	"""
	filtered = []
	if not inner:
		# Return all elements where list[element][key] == value
		for d in list_of_dicts:
			if key in d and d[key] == value:
				filtered += [d]
	else:
		# Return all elements where list[element][inner][key] == value
		for d in list_of_dicts:
			if inner in d and key in d[inner] and d[inner][key] == value:
				filtered += [d]
	return filtered

class HTML(Resource):
	def get(self):
		return "Please connect with a ResponsiveRooms terminal!"

class SensorsResource(Resource):
	def get(self):
		# If they request sensors of a specific room, or unassigned sensors, return those; else return all.
		if request.args.get('room'):
			value = request.args.get('room')
			if value == 'null' or value == '':
				value = None
			testthing = []
			for sensor in msens.get_sensors():
				if sensor.getRoom()._id == value:
					testthing.append(sensor)
			sensors = testthing #[sensor for sensor in msens.get_sensors() if sensor.getRoom() == value]
		else:
			sensors = msens.get_sensors()
		sensor_names = ','.join([sensor._getID() for sensor in sensors])
		sensor_data = [sensor._getData() for sensor in sensors]
		return app.make_response((json.dumps(sensor_data), 200, {'Content-Type': 'application/json', 'Collection-Items': sensor_names}))
	def put(self, sensor_id):
		sensor = msens.get_sensor(sensor_id)
		if sensor == None:
			return app.make_response(("", 404, {}))
		else:
			value = request.data
			if value == 'null' or value == '':
					value = None
			sensor._setRoom(value)
			return app.make_response(("", 204, {}))

class ActuatorsResource(Resource):
	def get(self):
		# If they request actuators of a specific room, or unassigned actuators, return those; else return all.
		if request.args.get('room'):
			value = request.args.get('room')
			if value == 'null' or value == '':
				value = None
			testthing = []
			for actuator in mact.get_actuators():
				if actuator.getRoom()._id == value:
					testthing.append(actuator)
			actuators = testthing #[actuator for actuator in mact.get_actuators() if actuator.getRoom() == value]
		else:
			actuators = mact.get_actuators()
		actuator_names = ','.join([actuator._getID() for actuator in actuators])
		actuator_data = [actuator._getData() for actuator in actuators]
		return app.make_response((json.dumps(actuator_data), 200, {'Content-Type': 'application/json', 'Collection-Items': actuator_names}))
	def put(self, actuator_id):
		actuator = mact.get_actuator(actuator_id)
		if actuator == None:
			return app.make_response(("", 404, {}))
		else:
			value = request.data
			if value == 'null' or value == '':
					value = None
			actuator._setRoom(value)
			return app.make_response(("", 204, {}))

class ProgramsResource(Resource):
	def head(self):
		# Return all program names.
		program_names = ','.join([program_name for program_name in mprog.get_program_names()])
		return app.make_response(("", 200, {'Content-Type': 'application/lua', 'Collection-Items': program_names}))
	def post(self):
		# If pre-requisites are fulfilled, insert an uploaded program.
		if not 'Collection-Item' in request.headers:
			return app.make_response(("No program name given in message header.", 400, {'Content-Type': 'text/plain'}))
		else:
			program_name = request.headers['Collection-Item']
		if program_name in mprog.get_program_names():
			return app.make_response(("A program with that name already exists.", 403, {'Content-Type': 'text/plain'}))
		else:
			mprog.insert_program(program_name, request.data)
			return app.make_response((program_name, 201, {'Content-Type': 'text/plain',
					'Location': 'http://{}:{}/programs/{}'.format(HOST, TERMINALPORT, program_name)}))
	def get(self, program_name):
		# Return source code if the program exists.
		if not program_name in mprog.get_program_names():
			return app.make_response(("", 404, {}))
		else:
			return app.make_response((mprog.get_program_code(program_name), 200, {'Content-Type': 'application/lua',
					'Collection-Item': program_name}))
	def delete(self, program_name):
		# Delete the program if it exists.
		if program_name in mprog.get_program_names():
			mprog.delete_program(program_name)
		return app.make_response(("", 204, {'Collection-Item': program_name}))

api.add_resource(HTML, '/')
api.add_resource(SensorsResource, '/sensors', '/sensors/<string:sensor_id>/room')
api.add_resource(ActuatorsResource, '/actuators', '/actuators/<string:actuator_id>/room')
api.add_resource(ProgramsResource, '/programs', '/programs/<string:program_name>')

def start_server():
	app.run(port=TERMINALPORT)
