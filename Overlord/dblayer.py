from pymongo import MongoClient
from bson.objectid import ObjectId
from time import strftime

class DBlayer(object):

    def __init__(self,uri='mongodb://localhost:27017/',db='securitydb',DEBUG=False):

        self.DEBUG = DEBUG

        if self.DEBUG:
            print "Starting DBlayer() INIT ..."

        self.dbclient = MongoClient(uri)
        self.db = self.dbclient[db]
        
        self.users = self.db['users']
        self.machines = self.db['machines']
        self.classes = self.db['classes']
        self.settings = self.db['settings']

        if self.DEBUG:
            print "DBlayer() INIT completed successfully."
            
    ##########
    #Users
    ##########
    
    def addUser(self, new, adder):
        """
        
        user = {
            'ident' : '1d2fb3a4',
            'name' : 'Matt Ewing',
            'hours-used' : '23.4',
            'last' : '234562035',
            'rit-data' : 'tbd',
            'class' : 'admin',
            'admin-username' : 'makersauce',
            'admin-password' : 'letmein'
        }
        
        """
        ##confirm adder is admin
        authorized = False
        try:
            authorized = self.users.find_one({'ident':adder})['class'] == 'admin'
        except Exception, e:
           if self.DEBUG:
               print "There was an error while authorizing adder:\n\n\t{0}".format(str(e))
               return False
               
        if authorized:
            if self.users.find_one({'ident':new['ident']}):
                if self.DEBUG:
                    print "Found user '{0}' already.  Consider updateUser() instead...".format(new['name'])
                return False
            
            if self.DEBUG:
                print "Adding user '{0}' to database ...".format(new['name'])
            
            success = False
            try:

                # add entity to the database
                if not 'hours' in new:
                    new['hours'] = 0
                if not 'last' in new:
                    new['last'] = str(strftime("%Y-%m-%d %H:%M:%S"))
                if not 'rit-data' in new:
                    new['rit-data'] = None##maybe find a way to get rit data
                if not 'here' in new:
                    new['here'] = False
                self.users.insert(new)
                success = True

            except Exception, e:
                if self.DEBUG:
                    print "There was an error while adding the user:\n\n\t{0}".format(str(e))

            return success

    def readUser(self, ident):
        try:
            user = self.users.find_one({'ident' : ident})
        except Exception, e:
                if self.DEBUG:
                    print "There was an error while reading the user:\n\n\t{0}".format(str(e))
                return False
                    
        if self.DEBUG:
            print "User Read Success\n{0}".format(user)
        
        return user
        ##readUser(ident)['class'] would return the class of the user
        
    def readAllUsers(self):
        try:
            users = list(self.users.find())
        except Exception, e:
                if self.DEBUG:
                    print "There was an error while reading the machine:\n\n\t{0}".format(str(e))
                return False
                    
        if self.DEBUG:
            print "Machine Read Success\n{0}".format(users)
        return users
        
    def updateUser(self, ident, new, updater):
 
        """
        new =   {
                        'ident' : '34kk43fg55',
                        'last' : '635546035',
                        'class' : 'admin',
                        'admin-username' : 'facepour',
                        'admin-password' : 'secret'
                    }
        """
        ##confirm adder is admin
        authorized = False
        try:
            authorized = self.users.find_one({'ident':updater})['class'] == 'admin'
        except Exception, e:
           if self.DEBUG:
               print "There was an error while authorizing updater:\n\n\t{0}".format(str(e))
               return False
               
        if authorized:
            if self.DEBUG:
                print "Updating user '{0}' ...".format(ident)

            success = False
            try:
                userId = self.users.find_one({'ident':ident})['_id']
                self.users.update({"_id": userId},{"$set": new})
                success = True

            except Exception, e:
               if self.DEBUG:
                   print "There was an error while updating the user:\n\n\t{0}".format(str(e))

            if self.DEBUG:
               print "User successfully updated."

            return success

    def deleteUser(self, idee, deleter):
        ##make sure deleter is admin
        idee = ObjectId(idee)
        authorized = False
        try:
            authorized = self.users.find_one({'ident':deleter})['class'] == 'admin'
        except Exception, e:
           if self.DEBUG:
               print "There was an error while authorizing deleter:\n\n\t{0}".format(str(e))
               return False
               
        if authorized:
            if not self.users.find_one({'_id' : idee}):
                if self.DEBUG:
                    print "There is no user with id {0}".format(idee)
                return False
            if self.DEBUG:
                print "Deleting User"
            self.users.remove({'_id' : idee},True)
            return True
		
    ##########
    #Machines
    ##########

    def addMachine(self, new, adder):
        """
        
        machine = {
            'ident' : 'MET-40504'
            'name' : 'Drill Press',
            'address' : '192.168.1.169',
            'occupied' : False,
            'last-user' : '1d2fb3a4',
            'last-time' : '234562035',
            'hours' : '603.4',
            'classes' : ['admin','cnc','user'],
            'broken' : False
        }
        
        """
        ##confirm adder is admin
        if (self.users.find_one({'ident':adder})['class'] == 'admin'):
            if self.users.find_one({'ident':new['ident']}):
                if self.DEBUG:
                    print "Machine '{0}' already exists. Try using updateMachine()...".format(new['ident'])
                return False
            
            if self.DEBUG:
                print "Adding machine '{0}' to database ...".format(new['ident'])
            
            success = False
            try:

                # add entity to the database
                new['occupied'] = False
                new['last-user'] = None
                new['last-time'] = str(strftime("%Y-%m-%d %H:%M:%S"))
                new['hours'] = 0
                new['broken'] = False
                self.machines.insert(new)
                success = True

            except Exception, e:
                if self.DEBUG:
                    print "There was an error while adding the machine:\n\n\t{0}".format(str(e))

            return success


    def readMachine(self, ident):
        try:
            machine = self.machines.find_one({'ident' : ident})
        except Exception, e:
                if self.DEBUG:
                    print "There was an error while reading the machine:\n\n\t{0}".format(str(e))
                return False
                    
        if self.DEBUG:
            print "Machine Read Success\n{0}".format(machine)
        return machine
        
    def readAllMachines(self):
        try:
            machines = list(self.machines.find())
        except Exception, e:
                if self.DEBUG:
                    print "There was an error while reading the machine:\n\n\t{0}".format(str(e))
                return False
                    
        if self.DEBUG:
            print "Machine Read Success\n{0}".format(machines)
        return machines
        
        
    def updateMachine(self, ident, new, updater):
 
        """
        new =       {
                        'ident' : 'GCIS-3402',
                        'last' : '635546035',
                        'classes' : 'admin',
                        'broken' : True
                    }
        """
        if (self.users.find_one({'ident':updater})['class'] == 'admin'):
            if self.DEBUG:
                print "Updating machine '{0}' ...".format(ident)

            success = False
            try:
                machineID = self.machines.find_one({'ident':ident})['_id']
                self.machines.update({"_id": machineID},{"$set": new})
                success = True

            except Exception, e:
               if self.DEBUG:
                   print "There was an error while updating the machine:\n\n\t{0}".format(str(e))

            if self.DEBUG:
               print "Machine successfully updated."

            return success

    def deleteMachine(self, idee, deleter):
        ##make sure deleter is admin
        authorized = False
        idee = ObjectId(idee)
        try:
            authorized = self.users.find_one({'ident':deleter})['class'] == 'admin'
        except Exception, e:
           if self.DEBUG:
               print "There was an error while authorizing deleter:\n\n\t{0}".format(str(e))
               return False
        if authorized:
            print idee
            if not self.machines.find_one({'_id' : idee}):
                if self.DEBUG:
                    print "There is no machine with id {0}".format(idee)
                return False
            if self.DEBUG:
                print "Deleting Machine"
            self.machines.remove({'_id' : idee},True)
            return True
           
    def sendFixReq(self, ident):
        ##Broken Machine Alert?
        return False

    def addInitial(self,init):
        
        success = False
                
        try:
            self.users.insert(init)
            success = True
            return success
        except:
            return success
        

    def _clearall(self):

        # blow away the entire database
        self.users.remove()
        self.machines.remove()
        self.classes.remove()
        self.settings.remove()

        return True




