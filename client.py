#!/bin/python

from socket import socket, AF_INET, SOCK_STREAM
from pypret.interpreter import Interpreter
from ipaddress import IPv4Address

ip = IPv4Address('192.168.1.0')
maxIp = IPv4Address('192.168.255.255')
port = 1234

sock = socket(AF_INET, SOCK_STREAM)

while ip <= maxIp:
	print("Connecting to " + ip.compressed)
	try:
		sock.connect((ip.compressed, port))
		break
	except Exception:
		ip += 1

print("Connected to " + ip.compressed)

interpreter = Interpreter([hello])
interpreter.run()