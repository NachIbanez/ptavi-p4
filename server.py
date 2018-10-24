#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):


    def handle(self):

        for line in self.rfile:
            line_decoded = line.decode('utf-8')
            if line_decoded[:line_decoded.find(" ")] == "REGISTER":
                direccion_sip = line_decoded[line_decoded.find(" "):line_decoded.rfind(" ")]
                diccionario_registro[direccion_sip] = \
                    self.client_address[0]
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                self.host, self.port = self.client_address[:2]
                print("--" + line.decode('utf-8'), end="")
                print("Desde ip:puerto --> " + str(self.host) + ":" + str(self.port), "\n")
            elif line_decoded[:line_decoded.find(" ")] == "Expires:":
                expires = line_decoded[line_decoded.find(" "):][1:].replace(" ", "")
                if int(expires) == 0:
                    del diccionario_registro[direccion_sip]
        print(diccionario_registro)


if __name__ == "__main__":

    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    diccionario_registro = {}
    print("-SERVER ON-\r\n")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
