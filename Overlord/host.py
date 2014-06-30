##TODO:
#
#getLog(day) FInish it
#machines new
#machines mod
#

import os
import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for
from dblayer import DBlayer

db = DBlayer(DEBUG=True)

app = Flask(__name__, static_folder='web/static', static_url_path='')
app.template_folder = "web"
SECURITYLOGS = "logs/"

ADMINIDENT = None

##START MAIN PAGE

@app.route("/")
def landing():
    now = datetime.datetime.now()
    log = getLog(now.strftime('%Y%m%d'))
    return render_template('landing.html', logs=log)

@app.route("/logs")
def logs():
    logList = getLogList()
    print logList
    return render_template('loglist.html',logList=logList)

@app.route('/logs/<logurl>')
def show_log(logurl):
    try:
        if os.path.isfile(os.path.join(SECURITYLOGS,logurl)):
            date = os.path.splitext(logurl)[0]
            logs = getLog(date)
            return render_template('log.html',logs=logs)
    except:
        return "<h1>Oops!</h1><p>Looks like there was an error retrieving that log.  Sorry about that.</p>"
       
@app.route("/users")
def users():
    categories = ['name','ident','class']
    users = db.readAllUsers()
    return render_template('users.html',users=users,categories=categories)
    
@app.route('/addUser',methods=['POST'])
def add_user():
    new = {}
    name = request.form['name']
    new['name'] = name
    ident = request.form['ident']
    new['ident'] = ident
    userclass = request.form['class']
    new['class'] = userclass
    try:
        hours = request.form['hours']
        new['hours'] = hours
    except:
        print 'no hours in form'
    try:
        last = request.form['last']
        new['last'] = last
    except:
        print 'no last in form'
    ##log ADDED USER xxx on XXXX
    added = db.addUser(new,'1337hax')
    return redirect(url_for('users'))
    
@app.route('/user-class',methods=['POST'])
def user_class():
    ident = request.form['ident']
    userClass = db.readUser(ident)['class']
    print "user class is {0}".format(userClass)
    ##log LOGIN ATTEMPT by XXXX at XXXX
    return jsonify(userClass=userClass)
  
@app.route("/machines")
def machines():
    categories = ['name','ident','classes','timeout']
    machines = db.readAllMachines()
    return render_template('machines.html',machines=machines,categories=categories)

@app.route('/addMachine',methods=['POST'])
def add_machine():
    new = {}
    name = request.form['name']
    new['name'] = name
    ident = request.form['ident']
    new['ident'] = ident
    classes = request.form['classes'].split(',')
    classes = [n.strip(' ') for n in classes]#Strip whitespace from classes
    new['classes'] = classes
    timeout = request.form['timeout']
    new['timeout'] = timeout
    try:
        hours = request.form['hours']
        new['hours'] = hours
    except:
        print 'no hours in form'
    try:
        last = request.form['last']
        new['last'] = last
    except:
        print 'no last in form'
    print new
    added = db.addMachine(new,'1337hax')
    ##log ADD machine XXXX at XXXX
    return redirect(url_for('machines'))
  
@app.route("/remove<string:index>")
def remove(index):
    print index
    if db.deleteUser(index,'1337hax'):
        print 'users'
        return redirect('/users')
    elif db.deleteMachine(index,'1337hax'):
        print 'machines'
        return redirect('/machines')
    return "<h1>Ooops!</h1>"
        

def getLog(day):
    f = day+'.log'
    if os.path.isfile(os.path.join(SECURITYLOGS,f)):
        ##PARSE LOG FILE
        log = [{'message':'hello','time':'1:30a'},{'message':'yes','time':'1:20a'},{'message':'fart','time':'1:40a'}]
        return log
    else:
        log = [{'message':'There has been no activity today'}]
        return log

def getLogList():
    try:
        onlyfiles = [ f for f in os.listdir(SECURITYLOGS) if os.path.isfile(os.path.join(SECURITYLOGS,f)) ]
        logList = []
        for f in onlyfiles:
            path = os.path.join(SECURITYLOGS,f)
            try:
                date = datetime.strptime(f, "%Y%m%d.log")
                filename = datetime.strftime(date, "%A %B %d, %Y")
            except:
                filename = f
            logList.append({'name':filename, 'path':path})
        return logList
    except:
        log = [{'message':'There has been no activity ever'}]
        return logList

@app.route("/machine-init", methods=['POST'])
def machine_init():
    print request.method
    print request.form['ident']
    if request.method == "POST":
        machine = db.readMachine(request.form['ident'])
        timeout = machine['timeout']
        classes = machine['classes']
        response = jsonify(timeout=timeout,classes=classes)
        ##log "machine XXXX checked in at XXXXX"
        return response
    return 'Request did not POST'
	


@app.route("/login")
def login():
    ADMIN_IDENT="1337hax"
    print "logged in"

'''


@app.route('/_get_tweets')
def get_tweets():
    filter = request.args.get('filter', type=str)
    n = request.args.get('n', 0, type=int)
    if (filter=='none'):
        result = db.tweets.find().sort('created', -1)[n]
    else:
        result = db.tweets.find({'merchanthandle':filter}).sort('created', -1)[n]
    return jsonify(text=result['text'],created=result['created'],merchant=result['merchanthandle'])

@app.route('/_get_merchant')
def get_merchant():
    name = request.args.get('handle', type=str) ##finds the most recently updated merchants
    result = db.merchants.find_one({'twitterhandle':name})
    return jsonify(name=result['name'],description=result['description'],handle=result['twitterhandle'],tid=result['twitterid'],updated=result['lastupdated'],geo=result['lastgeo'],category=result['category'])

##END MAIN PAGE


##MAP

@app.route('/_recent_merchants')
def recent_merchants():
    n = request.args.get('n', 0, type=int) ##finds the most recently updated merchants
    result = db.merchants.find().sort('lastupdated', -1)[n]
    print result
    return jsonify(name=result['name'],description=result['description'],handle=result['twitterhandle'],tid=result['twitterid'],updated=result['lastupdated'],geo=result['lastgeo'],category=result['category'])
    
##END MAP


##ADMIN PAGE

@app.route('/admin/_add_merchant')
def add_vendor():
    name = request.args.get('name', 0, type=str)
    tline = request.args.get('tagline', 0, type=str)
    handle = request.args.get('twitterhandle', 0, type=str)
    category = request.args.get('category',type=str)
    new = {'name': name, 'category': category, 'twitterhandle': handle, 'description': tline}
    print new
    added = db.addmerchant(new)
    return jsonify(result=added)
    
#@app.route('/admin/_consume_tweets')
#def consume_tweets():
#    print 'im in'
#    cons = TweetConsumer()
#    print 'init'
#    new = cons.consume()
#    print 'nom'
#    return str(new)


@app.route('/admin/_add_category', methods=['POST'])
def catadd():
    if request.method == 'POST':
        name = request.form['catname']
        file = request.files['caticon']
        if not name: return jsonify({"success":False,"error":"No Name"})
        if not file: return jsonify({"success":False,"error":"No File"})
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['CATEGORY_ICON_DIR'], "%s.%s" % (name, file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            new = {'name': name, 'filename':filename}
            db.addcategory(new)
            return jsonify({"success":True})

@app.route('/admin/_preview_category', methods=['POST'])
def catpreview():
    if request.method == 'POST':
        file = request.files['caticon']
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['TEMP_UPLOAD'], "%s.%s" % (file.filename.rsplit('.', 1)[0], file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            return jsonify({"success":('/temp/'+(file.filename.rsplit('.', 1)[0] + '.' + file.filename.rsplit('.', 1)[1]))})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMAGES


@app.route('/_get_categories')
def get_categories():
    n = request.args.get('n', 0, type=int)
    result = db.categories.find().sort('name', -1)[n]
    return jsonify(name=result['name'],filename=result['filename'])
    


@app.route("/admin")
def admin():
    return render_template('admin.html')

##END ADMIN PAGE

@app.route("/vendor")
def vendor():
    return render_template('vendor.html')
'''
if __name__ == "__main__":
    app.run()

