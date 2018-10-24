#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):

        for line in self.rfile:
            line_decoded = line.decode('utf-8')
            if line.strip() and line_decoded[:8] == "REGISTER":
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                self.host, self.port = self.client_address[:2]
                print("--" + line.decode('utf-8'), end="")
                print("Desde ip:puerto --> " + str(self.host) + ":" + str(self.port), "\n")


if __name__ == "__main__":

    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("-SERVER ON-\r\n")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
