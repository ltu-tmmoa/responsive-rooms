# -*- coding: utf-8 -*-
import io
import json

database_sensors = []
database_actuators = []
database_programs = {}

def load_database(filename):
	global database_sensors, database_actuators, database_programs
	try:
		with io.open(filename, 'r', encoding='utf-8') as infile:
			indata = json.load(infile)
			if indata['database_sensors']:
				database_sensors = indata['database_sensors']
			if indata['database_actuators']:
				database_actuators = indata['database_actuators']
			if indata['database_programs']:
				database_programs = indata['database_programs']
	except IOError:
		pass

def dump_database(filename):
	with io.open(filename, 'w', encoding='utf-8') as outfile:
		database = json.dumps(
			{'database_sensors': database_sensors, 'database_actuators': database_actuators, 'database_programs': database_programs},
			sort_keys = True, indent = 4, ensure_ascii=False)
		outfile.write(unicode(database))

def filter_out(list_of_dicts, key, value, inner = None):
	filtered = []
	if not inner:
		for d in list_of_dicts:
			if key in d and d[key] == value:
				filtered += [d]
	else:
		for d in list_of_dicts:
			if inner in d and key in d[inner] and d[inner][key] == value:
				filtered += [d]
	return filtered

def get_program_names():
	return database_programs.keys()