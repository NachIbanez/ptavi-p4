#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    METHOD = sys.argv[3]
    DIR_SIP = sys.argv[4]
    EXPIRES = sys.argv[5]
except IndexError:
    sys.exit("Usage: client.py port register sip_address expires_value")


if METHOD == "register":

    LINE = ("REGISTER sip:" + DIR_SIP + " SIP/2.0\r\n" + "Expires: " + str(EXPIRES) + "\r\n")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((SERVER, PORT))
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'), end="")

else:
    LINE = " ".join(sys.argv[3:])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((SERVER, PORT))
        print("Enviando:", LINE)
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'), end="")
