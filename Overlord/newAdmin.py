#!/usr/bin/env python

from dblayer import DBlayer
import getpass

db = DBlayer(DEBUG=True)

print 'so you want to add an admin, eh?'
name = raw_input("full name: ")
usern = raw_input("user name: ")
trys = 0
while True:
    pw = getpass.getpass("password: ")
    pw2 = getpass.getpass("re-type password: ")
    if pw == pw2:
	    print 'hey, great password, btw.'
	    break
    else:
	    print 'passwords didn\'t match... try again'
    if trys > 2:
        print 'get better soon.'
        exit(0)
    trys += 1
trys = 0
while True:
    swipe = getpass.getpass("swipe card and press enter: ")
    swipe2 = getpass.getpass("re-swipe card and press enter: ")
    if swipe == swipe2:
	    print 'swipe worked.'
	    break
    else:
	    print 'swipe didn\'t work... try again'
    if trys > 2:
        print 'get a better card.'
        exit(0)
    trys += 1




admin = {
            'name' : name,
            'admin-user' : usern,
            'admin-pw' : pw,
            'class' : 'admin',
            'ident' : swipe
        }

db.addInitial(admin)

