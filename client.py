#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

SERVER = sys.argv[1]
PORT = int(sys.argv[2])

if sys.argv[3] == "register":
    dir_sip = sys.argv[4]
    LINE = ("REGISTER sip:" + dir_sip + " SIP/2.0\r\n\r\n")
    print(LINE)
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
