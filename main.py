#!/bin/python

from socket import socket, AF_INET, SOCK_STREAM
from pypret.interpreter import Interpreter

ip = '0.0.0.0'
port = 1234

sock = socket(AF_INET, SOCK_STREAM)
sock.bind((ip, port))
sock.listen(1)
print("Listening...")

conn, clientAddr = sock.accept()
print(clientAddr)



def hello():
	print("Hello World!")

interpreter = Interpreter([hello])
interpreter.run()