#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    diccionario_registro = {}

    def register2json(self):
        usuarios = list(self.diccionario_registro)
        for usuario in usuarios:
            gmt_expires = self.diccionario_registro[usuario][1]
            gmt_actual = (time.strftime(' GMT %Y-%m-%d %H:%M:%S',
                          time.gmtime(time.time())))
            if gmt_expires < gmt_actual:
                del self.diccionario_registro[usuario]
        with open("registered.json", "w") as json_file:
            json.dump(self.diccionario_registro, json_file, indent=4)

    def json2registered(self):
        try:
            with open("registered.json", "r") as json_file:
                self.diccionario_registro = json.load(json_file)
        except FileNotFoundError:
            pass

    def handle(self):
        self.json2registered()
        for line in self.rfile:
            line_decoded = line.decode('utf-8')
            if line_decoded[:line_decoded.find(" ")] == "REGISTER":
                direccion_sip = line_decoded[line_decoded.find(" "):
                                             line_decoded.rfind(" ")]
                self.diccionario_registro[direccion_sip] = \
                    [self.client_address[0]]
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                self.host, self.port = self.client_address[:2]
                print("--" + line.decode('utf-8'), end="")
                print("Desde ip:puerto --> " + str(self.host) +
                      ":" + str(self.port), "\n")
            elif line_decoded[:line_decoded.find(" ")] == "Expires:":
                expires = line_decoded[line_decoded.find(" "
                                                         ):][1:].replace(" ",
                                                                         "")
                gmt_expires = time.strftime(" GMT %Y-%m-%d %H:%M:%S",
                                            time.gmtime(time.time()
                                                        + int(expires)))
                self.diccionario_registro[direccion_sip].append(gmt_expires)
                if int(expires) == 0:
                    del self.diccionario_registro[direccion_sip]
        self.register2json()


if __name__ == "__main__":

    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("-SERVER ON-\r\n")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
