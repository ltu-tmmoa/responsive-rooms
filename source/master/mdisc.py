# -*- coding: utf-8 -*-

import json
import time
import socket

from master import running, BROADCASTADDRESS, DISCOVERYPORT, DISCOVERYINTERVAL

def MD():
	"""Generate a master's discovery message.
	"""
	return { "message": "MD" }

def do_discovery():
	"""Initiate a master's discovery process.
	"""
	while running:
		try:
			print "Sending out a discovery message..."
			discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			discovery_socket.sendto(json.dumps(MD()), (BROADCASTADDRESS, DISCOVERYPORT))
		except socket.error, e:
			print "Socket error in discovery process:", e.strerror
		time.sleep(DISCOVERYINTERVAL)
