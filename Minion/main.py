#!/usr/bin/env python 


#Init Pins
######



#Init Connection
######
import httplib, urllib

params = urllib.urlencode({
    'isbn' : '9780131185838',
    'catalogId' : '10001',
    'schoolStoreId' : '15828',
    'search' : 'Search'
    })
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
conn = httplib.HTTPConnection("bkstr.com:80")
conn.request("POST", "/webapp/wcs/stores/servlet/BuybackSearch",
             params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()


#Running Loop
#######

while (off button == False){

check connection

if(pollrfid == True){

	try:
		success = sendRFIDtoserver(RFID)
	except:
		print "Network Error"
		

}

}
