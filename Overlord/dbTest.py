#db_test.py
from dblayer import DBlayer

db = DBlayer(DEBUG=True)

admin = {
            'name' : 'badmin',
            'class' : 'admin',
            'ident' : '1337hax',
            'info' : 'plzdeleteme'
        }
db.addInitial(admin)

testUser =  {
                'ident' : '1d2fb3a4',
                'name' : 'Matt Ewing',
                'hours-used' : '23.4',
                'last' : '234562035',
                'rit-data' : 'tbd',
                'class' : 'admin',
                'admin-username' : 'makersauce',
                'admin-password' : 'letmein'
            }
        	
modUser =   {
                'ident' : '34kk43fg55',
                'last' : '635546035',
                'class' : 'admin',
                'admin-username' : 'facepour',
                'admin-password' : 'secret'
            }
            
testMachine =   {
                    'ident' : 'MET-40504',
                    'name' : 'Drill Press',
                    'address' : '192.168.1.169',
                    'occupied' : False,
                    'last-user' : '1d2fb3a4',
                    'last-time' : '234562035',
                    'hours' : '603.4',
                    'classes' : ['admin','cnc','user'],
                    'broken' : False
                }
            
modMachine =    {
                    'ident' : 'GCIS-3402',
                    'last' : '635546035',
                    'classes' : 'admin',
                    'broken' : True
                }


db.addUser(testUser,admin['ident'])
db.readUser(testUser['ident'])
db.readAllUsers()
db.updateUser(testUser['ident'],modUser,admin['ident'])
print "the following should throw an error:"

db.deleteUser(testUser['ident'],admin['ident'])
delid = db.readUser(modUser['ident'])['_id']
db.deleteUser(modUser['ident'],admin['ident'])

db.addMachine(testMachine,admin['ident'])
db.readMachine(testMachine['ident'])
db.readAllMachines()
db.updateMachine(testMachine['ident'],modMachine,admin['ident'])
print "the following should throw an error:"
db.deleteMachine(testMachine['ident'],admin['ident'])
db.deleteMachine(modMachine['ident'],admin['ident'])



