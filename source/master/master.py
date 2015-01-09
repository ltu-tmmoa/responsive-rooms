# -*- coding: utf-8 -*-

HOST = '0.0.0.0'
BROADCASTADDRESS = '<broadcast>'
DISCOVERYINTERVAL = 10#30
DISCOVERYPORT = 14000
SENSORPORT = 14001
ACTUATORPORT = 14002
TERMINALPORT = 14003

running = True

from subprocess import call

import os
import sys
import threading
import time

import mdb
import mterm
import msens
import mact
import mdisc
import mprog

def CU(facility = None, room = None, location = None):
	"""Generate a context update message object.
	"""
	cu = {'message': 'CU'}
	cu['facility'] = facility
	cu['room'] = room
	if location:
		cu['location'] = {'x': location[0], 'y': location[1], 'z': location[2]}
	return cu

def get_CU(context):
	if not context:
		return CU()
	elif 'location' in context:
		return CU(context['facility'], context['room'], context['location'])
	else:
		return CU(context['facility'], context['room'])

def ER(description = ''):
	"""Generate an error report message object.
	"""
	er = {'message': 'ER'}
	er['error'] = description
	return er

def controller():
	"""Allow for controlling the master process.
	"""
	try:
		while True:
			c = raw_input('ENTER \'Q\' TO EXIT\n')
			if c.upper() == 'Q':
				mdb.dump_database(database_file)
				msens.disconnect()
				mact.disconnect()
				call(["kill", str(int(os.getpid()))])
	except KeyboardInterrupt, e:
		msens.disconnect()
		mdb.dump_database(database_file)
		call(["kill", str(int(os.getpid()))])

if __name__ == '__main__':
	if len(sys.argv) == 2 and sys.argv[1].endswith('.json'):
		database_file = sys.argv[1]
	else:
		database_file = "database.json"
	mdb.load_database(database_file)
	threading.Thread(target=mterm.start_server).start()
	#time.sleep(0.5)
	threading.Thread(target=msens.do_listening).start()
	#time.sleep(0.5)
	threading.Thread(target=mact.do_listening).start()
	#time.sleep(0.5)
	#threading.Thread(target=mprog.run_programs).start()
	time.sleep(5)
	threading.Thread(target=mdisc.do_discovery).start()
	#time.sleep(0.5)
	controller()
