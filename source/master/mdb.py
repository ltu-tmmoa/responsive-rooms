# -*- coding: utf-8 -*-
import io
import json

database_sensors = []
database_actuators = []
database_programs = {}

def load_database(filename):
	"""Load a stored database into memory.
	"""
	global database_sensors, database_actuators, database_programs
	try:
		with io.open(filename, 'r', encoding='utf-8') as infile:
			indata = json.load(infile)
			## It makes no sense to import sensors and actuators;
			## if the master restarts, they have to re-register.
			#if indata['database_sensors']:
			#	database_sensors = indata['database_sensors']
			#if indata['database_actuators']:
			#	database_actuators = indata['database_actuators']
			if indata['database_programs']:
				database_programs = indata['database_programs']
	except IOError:
		pass

def dump_database(filename):
	"""Store the sensors, actuators and programs in memory, on disk.
	"""
	with io.open(filename, 'w', encoding='utf-8') as outfile:
		database = json.dumps({
			## It makes no sense to export sensors and actuators;
			## if the master restarts, they have to re-register.
			#'database_sensors': database_sensors,
			#'database_actuators': database_actuators,
			'database_programs': database_programs},
			sort_keys = True, indent = 4, ensure_ascii=False)
		outfile.write(unicode(database))
