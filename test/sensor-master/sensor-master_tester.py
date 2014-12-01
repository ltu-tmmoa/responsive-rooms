import json
import select
import socket
import time

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

udp_ip = "localhost" #"255.255.255.255"
udp_port = 14000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
	print "sending MD"
	sock.sendto(MD(), (udp_ip, udp_port))
	sock.close()

	time.sleep(3.0)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('localhost', 14001))
	sock.listen(1)
	print "listening for sensor connection..."
	socket_object, other = sock.accept()
	print "got it!"

	message_queue = [CU(), ER(), json.dumps({'message':'SRr'}), '{"abc"}']

	last_message = time.time()+5.3

	while True:
		readable, writable, _ = select.select([socket_object], [socket_object], [])
		for r in readable:
			if r == socket_object:
				data = socket_object.recv(1024)
				if data:
					print "Sensor sent:", data
					print
		for w in writable:
			if w == socket_object:
				if message_queue and last_message and time.time() > last_message+7.68:
					data = message_queue[0]
					message_queue = message_queue[1:]
					socket_object.sendall(data)
					print "I sent:", data
					print
					last_message = time.time()
		time.sleep(0.1)
except KeyboardInterrupt:
	sock.close()