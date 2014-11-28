#!/usr/bin/env python

import json
import socket
import sys
import requests # http://docs.python-requests.org/en/latest/

HOST = '127.0.0.1'
PORT = 14000

C_TEST = '\033[94m'
C_OK = '\033[92m'
C_FAIL = '\033[91m'
C_END = '\033[0m'

def handle_error(test, message, got, expected = None):
	global results
	results += 1
	test_message = 'Test {} failed; {}:\n\t'.format(C_TEST+test+C_END, message)
	if expected is not None:
		expect_message = "{} but expected {}".format(C_FAIL+got+C_END, C_OK+expected+C_END)
	else:
		expect_message = C_FAIL+got+C_END
	print test_message + expect_message + '\n'

def header_check(response, header, expected_value = None):
	try:
		if expected_value:
			if response.headers[header] == expected_value:
				return (True, expected_value)
			else:
				return (False, response.headers[header])
		else:
			response.headers[header]
			return (True, "was set")
	except KeyError:
		return (False, "was not set")

def do_tests(other):
	session = requests.Session()

	##### SENSOR TESTS:

	url = "http://{}:14003/{}".format(other, "sensors")
	test_string = "GET " + url
	headers = {'Accept':'application/json'}
	response = session.get(url, headers = headers)
	if response.status_code != 200:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "200")
	(check, result) = header_check(response, 'Content-Type', 'application/json')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'application/json')
	(check, result) = header_check(response, 'Collection-Items')
	if not check:
		handle_error(test_string, "returned wrong Collection-Items", result)
	try:
		json.loads(response.content)
	except ValueError:
		handle_error(test_string, "did not return valid JSON data", response.content[0:20] + '...')
	session.close()

	url = "http://{}:14003/{}".format(other, "sensors?room=A1")
	test_string = "GET " + url
	headers = {'Accept':'application/json'}
	response = session.get(url, headers = headers)
	if response.status_code != 200:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "200")
	(check, result) = header_check(response, 'Content-Type', 'application/json')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'application/json')
	(check, result) = header_check(response, 'Collection-Items')
	if not check:
		handle_error(test_string, "returned wrong Collection-Items", result)
	try:
		json.loads(response.content)
	except ValueError:
		handle_error(test_string, "did not return valid JSON data", response.content[0:20] + '...')
	session.close()

	url = "http://{}:14003/{}".format(other, "sensors?room=null")
	test_string = "GET " + url
	headers = {'Accept':'application/json'}
	response = session.get(url, headers = headers)
	if response.status_code != 200:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "200")
	(check, result) = header_check(response, 'Content-Type', 'application/json')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'application/json')
	(check, result) = header_check(response, 'Collection-Items')
	if not check:
		handle_error(test_string, "returned wrong Collection-Items", result)
	try:
		json.loads(response.content)
	except ValueError:
		handle_error(test_string, "did not return valid JSON data", response.content[0:20] + '...')
	session.close()

	url = "http://{}:14003/{}".format(other, "sensors/1/room")
	testdata = "testroom"
	test_string = "PUT " + url# + " (data = " + testdata[0:20] + ")"
	headers = {'Content-Type':'text/plain'}
	response = session.put(url, headers = headers, data = testdata)
	if response.status_code != 204:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "204")
	session.close()

	##### ACTUATOR TESTS:

	url = "http://{}:14003/{}".format(other, "actuators")
	test_string = "GET " + url
	headers = {'Accept':'application/json'}
	response = session.get(url, headers = headers)
	if response.status_code != 200:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "200")
	(check, result) = header_check(response, 'Content-Type', 'application/json')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'application/json')
	(check, result) = header_check(response, 'Collection-Items')
	if not check:
		handle_error(test_string, "returned wrong Collection-Items", result)
	try:
		json.loads(response.content)
	except ValueError:
		handle_error(test_string, "did not return valid JSON data", response.content[0:20] + '...')
	session.close()

	url = "http://{}:14003/{}".format(other, "actuators?room=A1")
	test_string = "GET " + url
	headers = {'Accept':'application/json'}
	response = session.get(url, headers = headers)
	if response.status_code != 200:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "200")
	(check, result) = header_check(response, 'Content-Type', 'application/json')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'application/json')
	(check, result) = header_check(response, 'Collection-Items')
	if not check:
		handle_error(test_string, "returned wrong Collection-Items", result)
	try:
		json.loads(response.content)
	except ValueError:
		handle_error(test_string, "did not return valid JSON data", response.content[0:20] + '...')
	session.close()

	url = "http://{}:14003/{}".format(other, "actuators?room=null")
	test_string = "GET " + url
	headers = {'Accept':'application/json'}
	response = session.get(url, headers = headers)
	if response.status_code != 200:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "200")
	(check, result) = header_check(response, 'Content-Type', 'application/json')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'application/json')
	(check, result) = header_check(response, 'Collection-Items')
	if not check:
		handle_error(test_string, "returned wrong Collection-Items", result)
	try:
		json.loads(response.content)
	except ValueError:
		handle_error(test_string, "did not return valid JSON data", response.content[0:20] + '...')
	session.close()

	url = "http://{}:14003/{}".format(other, "actuators/A/room")
	testdata = "testroom"
	test_string = "PUT " + url# + " (data = " + testdata[0:20] + ")"
	headers = {'Content-Type':'text/plain'}
	response = session.put(url, headers = headers, data = testdata)
	if response.status_code != 204:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "204")
	session.close()

	##### PROGRAM TESTS:

	url = "http://{}:14003/{}".format(other, "programs")
	test_string = "HEAD " + url
	headers = {'Accept':'application/lua'}
	response = session.head(url, headers = headers)
	if response.status_code != 200:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "200")
	(check, result) = header_check(response, 'Content-Type', 'application/lua')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'application/lua')
	(check, result) = header_check(response, 'Collection-Items')
	if not check:
		handle_error(test_string, "returned wrong Collection-Items", result)
	session.close()

	url = "http://{}:14003/{}".format(other, "programs")
	testdata = "print 'Test program in Lua'"
	program_name = 'myTestProgram.lua'
	test_string = "POST " + url + " (data = \"" + testdata[0:20] + "...\") (program name missing or empty)"
	headers = {	'Accept': 'text/plain',
				'Content-Type': 'application/lua',
				'Collection-Item': ''}
	response = session.post(url, headers = headers, data = bytes(testdata))
	if response.status_code != 400:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "400")
	(check, result) = header_check(response, 'Content-Type', 'text/plain')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'text/plain')
	if not (response.content and response.content == 'No program name given in message header.'):
		handle_error(test_string, "returned unexpected error explanation", response.content[0:20], 'No program name given in message header.')
	session.close()

	url = "http://{}:14003/{}".format(other, "programs")
	testdata = "print 'Test program in Lua'"
	program_name = 'myTestProgram.lua'
	test_string = "POST " + url + " (data = \"" + testdata[0:20] + "...\")"
	headers = {	'Accept': 'text/plain',
				'Content-Type': 'application/lua',
				'Collection-Item': program_name}
	response = session.post(url, headers = headers, data = bytes(testdata))
	if response.status_code != 201:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "201")
	(check, result) = header_check(response, 'Content-Type', 'text/plain')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'text/plain')
	(check, result) = header_check(response, 'Location')
	if not (check and len(response.headers['Location']) is not 0):
		handle_error(test_string, "returned no valid location", result)
	if not (response.content and response.content == program_name):
		handle_error(test_string, "returned wrong program name", response.content[0:20], program_name)
	session.close()

	url = "http://{}:14003/{}".format(other, "programs")
	testdata = "print 'Test program in Lua'"
	program_name = 'myTestProgram.lua'
	test_string = "POST " + url + " (data = \"" + testdata[0:20] + "...\") (program name already exists)"
	headers = {	'Accept': 'text/plain',
				'Content-Type': 'application/lua',
				'Collection-Item': program_name}
	response = session.post(url, headers = headers, data = bytes(testdata))
	if response.status_code != 403:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "403")
	(check, result) = header_check(response, 'Content-Type', 'text/plain')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'text/plain')
	if not (response.content and response.content == 'A program with that name already exists.'):
		handle_error(test_string, "returned unexpected error explanation", response.content[0:20], 'A program with that name already exists.')
	session.close()

	program_name = 'myTestProgram.lua'
	url = "http://{}:14003/{}".format(other, "programs/" + program_name)
	test_string = "GET " + url
	headers = {'Accept':'application/lua'}
	response = session.get(url, headers = headers)
	if response.status_code != 200:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "200")
	(check, result) = header_check(response, 'Content-Type', 'application/lua')
	if not check:
		handle_error(test_string, "returned wrong Content-Type", result, 'application/lua')
	(check, result) = header_check(response, 'Collection-Item', program_name)
	if not check:
		handle_error(test_string, "returned wrong Collection-Item", result, program_name)
	if not len(response.text) > 0:
		handle_error(test_string, "did not return content", 'content was not set')
	session.close()

	program_name = 'nonExistingProgram'
	url = "http://{}:14003/{}".format(other, "programs/" + program_name)
	test_string = "GET " + url
	headers = {'Accept':'application/lua'}
	response = session.get(url, headers = headers)
	if response.status_code != 404:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "404")
	session.close()

	program_name = 'myTestProgram.lua'
	url = "http://{}:14003/{}".format(other, "programs/" + program_name)
	test_string = "DELETE " + url
	response = session.delete(url)
	if response.status_code != 204:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "204")
	(check, result) = header_check(response, 'Collection-Item', program_name)
	if not check:
		handle_error(test_string, "returned wrong Collection-Item", result, program_name)
	session.close()

	program_name = 'nonExistingProgram.lua'
	url = "http://{}:14003/{}".format(other, "programs/" + program_name)
	test_string = "DELETE " + url
	response = session.delete(url)
	if response.status_code != 204:
		handle_error(test_string, "returned wrong status code", str(response.status_code) + " " + response.reason, "204")
	(check, result) = header_check(response, 'Collection-Item', program_name)
	if not check:
		handle_error(test_string, "returned wrong Collection-Item", result, program_name)
	session.close()

def main():
	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.bind((HOST, PORT))
	connection.listen(0)
	_, other = connection.accept()
	connection.close()
	do_tests(other[0])

results = 0

if __name__ == '__main__':
	main()

#print results
sys.exit(results)
