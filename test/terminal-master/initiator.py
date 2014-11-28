#!/usr/bin/env python

import json
import socket

HOST = '127.0.0.1'
PORT = 14000

def main():
	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.connect((HOST, PORT))
	connection.send("Initiate")
	connection.close()

if __name__ == '__main__':
	main()