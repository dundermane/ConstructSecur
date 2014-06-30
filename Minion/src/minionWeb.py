#!/usr/bin/env python 

import ast
import httplib, urllib


class webMinion(object):
    def __init__(self, addr,DEBUG=False):
    
        self.DEBUG = DEBUG
    
        if self.DEBUG:
            print "Connecting to Overlord..."
        try:
            self.conn = httplib.HTTPConnection(addr)
            params = urllib.urlencode({
                'ident' : 'pident232141'
                })
            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain"}
            self.conn.request("POST", "/machine-init",
                         params, headers)
            response = self.conn.getresponse()
            print response.status, response.reason
            data = ast.literal_eval(response.read())
            self.timeout = data['timeout']
            self.classes = data['classes']
            if self.DEBUG:
                print "Machine Security Initialized..."
        except Exception, e:
            if self.DEBUG:
                print "Connection Failed:\n\n\t{0}".format(str(e))
         
    def getUser(self, ident):
        
        if self.DEBUG:
            print "Looking up User {0}...".format(str(ident))
        try:
            params = urllib.urlencode({
                'ident' : ident
                })
            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain"}
            self.conn.request("POST", "/user-class",
                         params, headers)
            response = self.conn.getresponse()
            print response.status, response.reason
            data = ast.literal_eval(response.read())
            user_class = data['userClass']
            if self.DEBUG:
                print "Users Class: {0}...".format(str(user_class))
        except Exception, e:
            if self.DEBUG:
                print "User Lookup Failed:\n\n\t{0}".format(str(e))
        
    def close(self):
        self.conn.close()  ##Closes connection
