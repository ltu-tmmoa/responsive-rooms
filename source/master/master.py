# -*- coding: utf-8 -*-

HOST = '127.0.0.1'
BROADCASTADDRESS = '127.0.0.1'#''#'<broadcast>'
DISCOVERYPORT = 14000
SENSORPORT = 14001
ACTUATORPORT = 14002
TERMINALPORT = 14003

running = True

from subprocess import call

import json
import os
import sys
import threading
import time
import socket

import mdb
import mterm
import msens
import mact
import mlua

def MD():
	return json.dumps({ "message": "MD" })

def do_discovery():
	while running:
		discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		discovery_socket.sendto(MD(), (BROADCASTADDRESS, DISCOVERYPORT))
		discovery_socket = None
		time.sleep(30)

def controller():
	global running
	while running:
		c = raw_input('ENTER \'Q\' TO EXIT\n')
		if c.upper() == 'Q':
			mdb.dump_database(database_file)
			running = False
			time.sleep(1)
			call(["kill", str(int(os.getpid()))])
			sys.exit()
		elif c.upper() == 'D':
			threading.Thread(target=do_discovery).start()
		elif c.upper() == 'SL':
			threading.Thread(target=msens.do_listening).start()
		elif c.upper() == 'AL':
			threading.Thread(target=mact.do_listening).start()
		elif c.upper() == 'HELLO':
			mact.registered_actuators[0].set('text', "oh hello there")
			mact.registered_actuators[0].set('unread', True)

if __name__ == '__main__':
	if len(sys.argv) == 2 and sys.argv[1].endswith('.json'):
		database_file = sys.argv[1]
	else:
		database_file = "database.json"
	mdb.load_database(database_file)
	threading.Thread(target=controller).start()
	threading.Thread(target=mterm.start_server).start()
	mlua.run_programs()