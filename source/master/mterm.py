# -*- coding: utf-8 -*-
from flask import Flask, request
from flask.ext.restful import Resource, Api#, reqparse
import json
import mdb
from master import TERMINALPORT

app = Flask(__name__)
api = Api(app)

database_sensors = mdb.database_sensors
database_actuators = mdb.database_actuators
database_programs = mdb.database_programs
filter_out = mdb.filter_out

class Sensors(Resource):
	def get(self):
		sensors = database_sensors
		if request.args.get('room'):
			value = request.args.get('room')
			if value == "null":
				value = None
			sensors = filter_out(database_sensors, 'room', value)
		sensor_names = ','.join([sensor['id'] for sensor in sensors])
		return app.make_response((json.dumps(sensors), 200, {'Content-Type': 'application/json', 'Collection-Items': sensor_names}))
	def put(self, sensor_id):
		for sensor in database_sensors:
			if sensor['id'] == sensor_id:
				if request.data and request.data != "null":
					sensor['room'] = request.data
				else:
					sensor['room'] = None
				return app.make_response(("", 204, {}))
		return app.make_response(("", 404, {}))

class Actuators(Resource):
	def get(self):
		actuators = database_actuators
		if request.args.get('room'):
			value = request.args.get('room')
			if value == "null":
				value = None
			actuators = filter_out(database_actuators, 'room', value)
		actuator_names = ','.join([actuator['id'] for actuator in actuators])
		return app.make_response((json.dumps(actuators), 200, {'Content-Type': 'application/json', 'Collection-Items': actuator_names}))
	def put(self, actuator_id):
		for actuator in database_actuators:
			if actuator['id'] == actuator_id:
				if request.data and request.data != "null":
					actuator['room'] = request.data
				else:
					actuator['room'] = None
				return app.make_response(("", 204, {}))
		return app.make_response(("", 404, {}))

class Programs(Resource):
	def head(self):
		program_names = ','.join([program for program in database_programs])
		return app.make_response(("", 200, {'Content-Type': 'application/lua', 'Collection-Items': program_names}))
	def post(self):
		print request.headers
		if not 'Collection-Item' in request.headers:
			return app.make_response(("No program name given in message header.", 400, {'Content-Type': 'text/plain'}))
		program_name = request.headers['Collection-Item']
		if program_name in database_programs:
			return app.make_response(("A program with that name already exists.", 403, {'Content-Type': 'text/plain'}))
		database_programs[program_name] = request.data
		return app.make_response((program_name, 201, {'Content-Type': 'text/plain',
				'Location': 'http://{}:{}/programs/{}'.format(HOST, TERMINALPORT, program_name)}))
	def get(self, program_name):
		if not program_name in database_programs:
			return app.make_response(("", 404, {}))
		return app.make_response((database_programs[program_name], 200, {'Content-Type': 'application/lua', 'Collection-Item': program_name}))
	def delete(self, program_name):
		if program_name in database_programs:
			database_programs.pop(program_name)
		return app.make_response(("", 204, {'Collection-Item': program_name}))

api.add_resource(Sensors, '/sensors', '/sensors/<string:sensor_id>/room')
api.add_resource(Actuators, '/actuators', '/actuators/<string:actuator_id>/room')
api.add_resource(Programs, '/programs', '/programs/<string:program_name>')

def start_server():
	app.run(port=TERMINALPORT)
