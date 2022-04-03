#/usr/bin/env python3

import socket
import urllib.request

class Laumio:
    """ Laumio's abstraction layer

    ip -- Laumio's IP
    """

    def init(self, ip):
        self.ip = ip
        self.url = 'http://'+str(ip)+'/api/'

    def wipeOut(self):
        """ Shut down all the LED """
        rgb = [0,0,0]
        self.setPixelColor(9,rgb = [0,0,0])
        return self.fillColor(rgb)


    def fillColor(self, rgb):
        """ Set the color of all the leds in the Laumio
        r -- red byte
        g -- green byte
        b -- blue byte
        """
        payload = bytearray([ 255, rgb[0],rgb[1],rgb[2] ])
        return self._send(payload)

    def fillRing(self, ringid, rgb):
        """ Set the color of all the leds of ring ringid in the Laumio
        ringid -- Ring ID (0~2)
        r -- red byte
        g -- green byte
        b -- blue byte
        """
        payload = bytearray([ 1, ringid, rgb[0],rgb[1],rgb[2] ])
        return self._send(payload)

    def fillColumn(self, columnid, rgb):
        """ Set the color of all the leds of column columnid in the Laumio
        columnid -- Column ID (0~3)
        r -- red byte
        g -- green byte
        b -- blue byte
        """
        payload = bytearray([ 2, columnid, rgb[0],rgb[1],rgb[2] ])
        return self._send(payload)

    def setPixelColor(self, pixel, rgb):
        """ Set the color of all the leds pixel of the Laumio
        pixel -- LED ID (0~12)
        r -- red byte
        g -- green byte
        b -- blue byte
        """
        payload = bytearray([ 0, pixel, rgb[0],rgb[1],rgb[2] ])
        return self._send(payload)

    def rainbow(self):
        """ Start Rainbow animation """
        payload = bytearray([ 0x0a ])
        return self._send(payload)

    def status(self):
        """ Get the JSON Laumio status """
        return urllib.request.urlopen(self.url).read().decode()

    def _send(self, payload):
        """ Proxy to socket.socket.sendto w/ minimal error-handling """
        try:
            sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
            sock.sendto(payload, (self.ip, 6969))
            return 0
        except socket.error:
            return 1
    def fillColorProjecteur(self, port, rgb):
        """ Proxy to socket.socket.sendto w/ minimal error-handling """
        try:
            sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
            sock.sendto(bytearray([ 255, rgb[0],rgb[1],rgb[2] ]), (self.__ip, port))
            return 0
        except socket.error:
            return