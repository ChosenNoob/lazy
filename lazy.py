#!/bin/python

from socket import socket, AF_INET, SOCK_STREAM
from pypret.interpreter import Interpreter
from sys import argv
from multiprocessing import Pool, Process
from ipaddress import IPv4Address

port = 1234

def print_help():
	help_str = '''Usage: lazy [mode]
mode options:
	--client
	--server'''
	print(help_str)

def server_conn_worker(client_conn, client_addr):
	print('Handling ' + str(client_addr))
	while 1:
		data = client_conn.recv(1024)
		if not data: break

	client_conn.close()

def run_as_server():
	server_socket = socket(AF_INET, SOCK_STREAM)
	server_socket.bind(('', port))
	server_socket.listen(1)
	print("Listening...")

	while True:
		client_conn, client_addr = server_socket.accept()
		worker = Process(target=server_conn_worker, args=(client_conn, client_addr))
		worker.start()
	server_socket.close()

def client_conn_worker(ip):
	ip = IPv4Address(ip)
	print('Trying ip adress ' + str(ip))
	client_socket = socket(AF_INET, SOCK_STREAM)
	# client_socket.settimeout(5)
	client_socket.settimeout(1)
	result = None
	try:
		client_socket.connect((ip.compressed, port))
		result = ip
	except Exception:
		pass
	client_socket.close()
	return result

def run_as_client():
	minIp = 3232301313
	maxIp = 3232301567
	with Pool(maxIp - minIp + 1) as pool:
		result = pool.map(client_conn_worker, range(minIp, maxIp + 1))
		# result = pool.map(client_conn_worker, [3232235885])
		print(result)

	for i in result:
		if i != None:
			print('Success')
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

# def hello():
# 	print("Hello World!")

# interpreter = Interpreter([hello])
# interpreter.run()