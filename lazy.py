#!/bin/python

import subprocess
from socket import socket, AF_INET, SOCK_STREAM, gethostname
from pypret.interpreter import Interpreter
from sys import argv
from multiprocessing import Pool, Process
from ipaddress import IPv4Address
from os.path import isfile

PORT = 1234

def print_help():
	help_str = '''Usage: lazy [mode]
mode options:
	--client
	--server'''
	print(help_str)

# Client mode
def connect_to_host(hostname):
	# Tries to connect to given hostname, 
	# returns socket if succeeds 
	# returns None if fails
	sock = socket(AF_INET, SOCK_STREAM)
	print("Connecting {}".format(hostname))
	try:
		conn_result = sock.connect((hostname, PORT))
		return sock
	except Exception:
		sock.close()
		return None

def connect_new_host():
	# Promts user for new hostname, 
	# returns socket if succeeds to connect
	# returns None if fails
	hostname = input("Enter the hostname:")
	conn_result = connect_to_host(hostname)
	while conn_result == None:
		hostname = input("Couldn't connect. Enter the hostname:")
		conn_result = connect_to_host(hostname)

	with open("hostnames.txt", "a") as hostname_file:
		print(hostname, file=hostname_file)
	return conn_result	

def connect_existing_hosts():
	# Tries to connect existing hostnames, 
	# returns socket if succeeds to connect
	# returns None if fails
	if isfile('hostnames.txt'):
		with open("hostnames.txt") as hostname_file:
			hostnames = hostname_file.readlines()
			print(hostnames)
			for hostname in hostnames:
				return connect_to_host(hostname.strip())

def conn_handling(sock):
	print("Connected")
	while True:
		request = input("<<<")
		sock.sendall(request.encode())
		response = sock.recv(1024).decode()
		print(response)
	sock.close()

def run_as_client():
	conn_result = connect_existing_hosts()
	if conn_result != None:
		conn_handling(conn_result)
	else:
		conn_result = connect_new_host()
		if conn_result != None:
			conn_handling(conn_result)

# Server mode
def load_commands():
	# loads known commands from commands.txt to server
	commands = {}
	if isfile("commands.txt"):
		with open("commands.txt") as command_file:
			lines = command_file.readlines()
			for line in lines:
				split_line = line.split(" ", 1)
				commands[split_line[0]] = split_line[1].strip()
	print(commands)
	return commands

def server_worker(client_conn, client_addr):
	# Thread that handles each client connection
	print('Handling ' + str(client_addr))
	commands = load_commands()
	while 1:
		data = client_conn.recv(1024)
		if not data: 
			print("Connection closed by {}".format(client_addr))
			break
		request = data.decode()
		print("{} requested {}".format(client_addr, request))
		try:
			subprocess.run(commands[request])
			client_conn.sendall("success".encode())
		except KeyError as e:
			print(e)
			client_conn.sendall("not a command".encode())
		except Exception as e:
			print(e)
			client_conn.sendall("runtime error".encode())

	client_conn.close()

def run_as_server():
	# Listens and creates server_workers for each connection
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind(('', PORT))
	sock.listen(1)
	print("Hostname {}".format(gethostname()))
	print("Listening...")

	while True:
		client_conn, client_addr = sock.accept()
		worker = Process(target=server_worker, args=(client_conn, client_addr))
		worker.start()
	sock.close()

def main():
	if len(argv) == 1:
		print('Assuming client mode')
		run_as_client()
	elif len(argv) == 2:
		if argv[1] == '--client':
			run_as_client()
		elif argv[1] == '--server':
			run_as_server()
		else:
			print_help()
	else:
		print_help()

if __name__ == '__main__':
	main()