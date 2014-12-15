import asyncore
import json
import select
import socket
import sys
import os
import time
import threading
from subprocess import call
from pygame import mixer
from pydub import AudioSegment
import requests
import wave

self_address = "127.0.0.1"
udp_port = 14000
tcp_port = 14002
discovery_timeout = 30.0
report_interval = 5.0 # Reporting once every n seconds
run_time = 60.0 # Time to report to and listen to master

C_TEST = '\033[94m'
C_OK = '\033[92m'
C_FAIL = '\033[91m'
C_END = '\033[0m'

def MD():
	return json.dumps({ "message": "MD" })

def AM(type = None, properties = {}, context = None):
	am = {'message': 'AM'}
	am['type'] = type
	am['properties'] = properties
	am['context'] = context
	return json.dumps(am)

def CU(facility = None, room = None, location = None):
	cu = {'message': 'CU'}
	cu['facility'] = facility
	cu['room'] = room
	if location:
		cu['location'] = {'x': location[0], 'y': location[1], 'z': location[2]}
	return json.dumps(cu)

def AU(properties = {}):
	au = {'message': 'AU'}
	au['properties'] = properties
	return json.dumps(au)

def AR(properties = {}):
	ar = {'message': 'AR'}
	ar['properties'] = properties
	return json.dumps(ar)

def ER(description = ''):
	er = {'message': 'ER'}
	er['error'] = description
	return json.dumps(er)

def generate_action(tts):
	mp3file = '/tmp/mastermp3.{}'
	url = "http://translate.google.com/translate_tts?ie=UTF-8&tl=en&q={}"
	text = "I was told to read this out loud: {}.".format(str(tts))
	mp3 = requests.get(url.format(text), stream=True)
	with open(mp3file.format('mp3'), 'wb') as fd:
		for chunk in mp3.iter_content(1024):
			fd.write(chunk)
	mixer.init()
	mixer.music.load(mp3file.format('mp3'))
	mixer.music.play()

locked = False
my_self = {'text': '', 'unread': False}

def do_run():
	while True:
		my_am = AM('tts', {'text': 'string', 'unread': 'boolean'})

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
		connection.sendall(my_am)
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
						if message['message'] == 'AU':
							print "Got update..."
							global locked
							#while locked:
							#	print "Update locked!"
							#	time.sleep(0.1)
							global my_self
							locked = True
							if 'text' in message['properties']:
								my_self['text'] = message['properties']['text']
							if 'unread' in message['properties']:
								my_self['unread'] = message['properties']['unread']
							print "Updated:", my_self
							locked = False
					except ValueError:
						pass
			for w in writable:
				if w == connection:
					pass
		time.sleep(5)

def action_checker():
	global locked
	global my_self
	while True:
		print "Checking action..."
		#while locked:
		#	print "Action locked!"
		#	time.sleep(0.1)
		locked = True
		if my_self['unread']:
			generate_action(my_self['text'])
			my_self['unread'] = False
		time.sleep(0.25)
		locked = False

def main():
	try:
		threading.Thread(target=action_checker).start()
		do_run()
	except socket.error, e:
		print "Socket error!", e.strerror
	except KeyboardInterrupt:
		call(["kill", str(int(os.getpid()))])

if __name__ == '__main__':
	main()