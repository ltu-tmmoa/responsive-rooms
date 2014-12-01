import asyncore
import json
import select
import socket
import sys
import time

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
	er['description'] = description
	return json.dumps(er)

def handle_error(test, message, got, expected = None):
	global results
	results += 1
	test_message = 'Test {} failed; {}:\n\t'.format(C_TEST+test+C_END, message)
	if expected is not None:
		expect_message = "{} but expected {}".format(C_FAIL+got+C_END, C_OK+expected+C_END)
	else:
		expect_message = C_FAIL+got+C_END
	print test_message + expect_message + '\n'

def do_tests():
	example_md = MD()
	example_sm = SM('thermometer', {'celsius': 'number', 'fahrenheit': 'number'})
	example_cu = CU('A', '1202', (4.5, 1.9, 6.2))
	example_sr = SR({'celsius': 81.239, 'fahrenheit': 178.23})
	example_er = ER("Unrecognized message type 'SRr'.")

	discovered = registered = False
	message = source = None

	##### BIND/DISCOVERY TEST:

	test = "BIND and DISCOVER MASTER"
	connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		connection.bind((self_address, udp_port))
		connection.setblocking(0)
		ready = select.select([connection], [], [], discovery_timeout)
		if ready[0]:
			message, source = connection.recvfrom(128)
			try:
				if json.loads(message) == json.loads(example_md):
					discovered = True
				else:
					handle_error(test, "wrong discovery message", message[0:20], example_md)
			except ValueError:
				handle_error(test, "message not JSON data", message[0:20], example_md)
		else:
			handle_error(test, "no discovery message received", "no data received", example_md)
	finally:
		connection.close()
		connection = None

			##### REGISTRATION TEST:

	if discovered:
		time.sleep(4)
		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			test = "REGISTER WITH MASTER"
			connection.connect((source[0], tcp_port))
			connection.sendall(example_sm)
			registered = True
		except socket.error, e:
			handle_error(test, "could not register", e.strerror)

		##### RUNTIME/CU/SR TEST:

		if registered:
			test = "RUNTIME/CONTEXT UPDATE/SENSOR REPORT"
			start_time = time.time()
			last_report_time = None
			try:
				while time.time() < start_time + run_time:
					readable, writable, _ = select.select([connection], [connection], [])
					for r in readable:
						if r == connection:
							data = connection.recv(128)
							try:
								data = json.loads(data)
								if data['message'] == 'CU':
									sensor_info = json.loads(example_sm)
									sensor_info['context'] = data
									example_sm = json.dumps(sensor_info)
								else:
									connection.sendall(ER("Message received was not a CU message."))
							except ValueError:
								connection.sendall(ER("Data received was not valid JSON."))
							except KeyError:
								connection.sendall(ER("Data received was not a valid message."))
					for w in writable:
						if w == connection:
							if last_report_time and time.time() > last_report_time+report_interval:
								connection.sendall(example_sr)
								last_report_time = time.time()
					time.sleep(0.05)
			except socket.error, e:
				handle_error(test, "runtime aborted", e.strerror)

		##### RUNTIME/CU/SR TEST:

		if registered:
			test = "ERROR REPORT"
			try:
				connection.sendall(example_er)
			except Exception, e:
				handle_error(test, "error reporting", e.strerror)

		if connection:
			connection.close()

def main():
	# connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# connection.bind((self_address, PORT))
	# connection.listen(0)
	# connection.accept()
	# connection.close()
	do_tests()

results = 0

if __name__ == '__main__':
	main()

#print results
sys.exit(results)