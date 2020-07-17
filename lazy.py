#!/bin/python

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
	conn_result = sock.connect_ex((hostname, PORT))
	if conn_result == 0:
		return sock
	else:
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
			for hostname in hostnames:
				return connect_to_host(hostname)
	
def conn_handling(sock):
	print("Connected")
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
def server_worker(client_conn, client_addr):
	# Thread that handles each client connection
	print('Handling ' + str(client_addr))
	while 1:
		data = client_conn.recv(1024)
		if not data: break

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