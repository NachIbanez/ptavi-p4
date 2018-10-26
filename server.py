#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    def register2json(self, diccionario_registro):
        usuarios = list(diccionario_registro)
        for usuario in usuarios:
            gmt_expires = diccionario_registro[usuario][1]
            gmt_actual = (time.strftime(' GMT %Y-%m-%d %H:%M:%S', time.gmtime(time.time())))
            if gmt_expires < gmt_actual:
                del diccionario_registro[usuario]
        file = open("registered.json", "w")
        file.write("{" + '\n\t"Registered Users"' + ": {\n\t\t")
        ultima_iteracion = len(diccionario_registro)
        iteracion = 1
        for usuario in diccionario_registro:
            file.write('\n\t\t"' + usuario + ' "' + ": {\n\t\t\t")
            lista = diccionario_registro[usuario]
            file.write('"address": ' + '"' + lista[0] + '",' + "\n\t\t\t")
            file.write('"expires": ' + '"' + lista[1] + '"')
            if ultima_iteracion == iteracion:
                file.write("\n\t\t}")
            else:
                file.write("\n\t\t},")
            iteracion += 1
        file.write("\n\t}\n}")

    def handle(self):
        for line in self.rfile:
            line_decoded = line.decode('utf-8')
            if line_decoded[:line_decoded.find(" ")] == "REGISTER":
                direccion_sip = line_decoded[line_decoded.find(" "):line_decoded.rfind(" ")]
                diccionario_registro[direccion_sip] = \
                    [self.client_address[0]]
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                self.host, self.port = self.client_address[:2]
                print("--" + line.decode('utf-8'), end="")
                print("Desde ip:puerto --> " + str(self.host) + ":" + str(self.port), "\n")
            elif line_decoded[:line_decoded.find(" ")] == "Expires:":
                expires = line_decoded[line_decoded.find(" "):][1:].replace(" ", "")
                gmt_expires = time.strftime(" GMT %Y-%m-%d %H:%M:%S", \
                                            time.gmtime(time.time() \
                                            + int(expires)))        
                expires_seconds_gmt = time.gmtime(time.time() + int(expires))
                diccionario_registro[direccion_sip].append(gmt_expires)
                if int(expires) == 0:
                    del diccionario_registro[direccion_sip]       
        SIPRegisterHandler.register2json(self, diccionario_registro)


if __name__ == "__main__":

    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    diccionario_registro = {}
    print("-SERVER ON-\r\n")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
