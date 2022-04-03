#!/usr/bin/env python3

import sys
import os
from laumio import *
import time

r = None
g = None
b = None
try: 
    r = int(sys.argv[1])
    g = int(sys.argv[2])
    b = int(sys.argv[3])
except ValueError:
    print_usage()

listeIp = ["192.168.1.24", "192.168.1.26", "192.168.1.28", "192.168.1.21", "192.168.1.29", "192.168.1.31", "192.168.1.25", "192.168.1.27", "192.168.1.30", "192.168.1.23"]

for lumIP in listeIp:
    print(lumIP)
    l = Laumio(lumIP)
    print(l)
    l.wipeOut()

for lumIP in listeIp:
    l = Laumio(lumIP)
    l.colorWipe(r, g, b, 50)
    time.sleep(1)
    l = Laumio(lumIP)
    l.colorWipe(0, 0, 0, 50)
    time.sleep(2)
