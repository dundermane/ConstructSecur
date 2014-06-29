#!/usr/bin/env python 
import time
from minionWeb import webMinion


def swipe():
    return 'neo'

#Init some Pins
##########

while True:
    addr = '127.0.0.1:5000'
    minion = webMinion(addr, DEBUG=True)
    try:
        print minion.timeout
        print minion.classes
    except:
        print 'Couldnt find the server'

    ident = swipe()
    minion.getUser(ident)

    minion.close()
    time.sleep(5)

