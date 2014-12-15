import asyncore
import json
import select
import socket
import sys
import time
import random
import os
from subprocess import call

self_address = "127.0.0.1"
udp_port = 14000
tcp_port = 14001
discovery_timeout = 30.0
report_interval = 5.0 # Reporting once every n seconds
run_time = 60.0 # Time to report to and listen to master

C_TEST = '\033[94m'
C_OK = '\033[92m'
C_FAIL = '\033[91m'
C_END = '\033[0m'

def MD():
	return json.dumps({ "message": "MD" })

def SM(type = None, properties = {}, context = None):
	sm = {'message': 'SM'}
	sm['type'] = type
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

def generate_report():
	return SR({'number': random.randrange(0, 100)})

def do_run():
	while True:
		my_sm = SM('random', {'number': 'number'})
		example_sr = SR({'celsius': 81.239, 'fahrenheit': 178.23})
		example_er = ER("Unrecognized message type 'SRr'.")

		discovered = registered = False
		message = source = None

		print "Doing discovery..."
		connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		while not discovered:
			connection.bind((self_address, udp_port))
			connection.setblocking(0)
			ready = select.select([connection], [], [], discovery_timeout)
			if ready[0]:
				message, source = connection.recvfrom(128)
				try:
					if json.loads(message) == json.loads(MD()):
						discovered = True
				except ValueError:
					pass
			if not discovered:
				time.sleep(0.1)
		connection.close()
		print "Discovered!"
		print "In communication..."
		time.sleep(2.5)
		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connection.connect((source[0], tcp_port))
		connection.sendall(my_sm)
		connected = True
		start_time = time.time()
		last_report_time = None
		while connected:
			readable, writable, _ = select.select([connection], [connection], [])
			for r in readable:
				if r == connection:
					message = connection.recv(1024)
					try:
						message = json.loads(message)
						# Handle CU here.
					except ValueError:
						pass
			for w in writable:
				if w == connection:
					if last_report_time and time.time() > last_report_time+report_interval:
						connection.sendall(generate_report())
						last_report_time = time.time()
					elif not last_report_time:
						connection.sendall(generate_report())
						last_report_time = time.time()
		time.sleep(5)

def main():
	try:
		do_run()
	except socket.error, e:
		print "Socket error!", e.strerror
	except KeyboardInterrupt:
		call(["kill", str(int(os.getpid()))])

if __name__ == '__main__':
	main()