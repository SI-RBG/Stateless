from flask import Flask, flash, jsonify, render_template, request, session, redirect, url_for, abort
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymysql, datetime, requests, shutil, json, time, sys, os, hashlib,random
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import requests
from auth import *
from databaseCommunication import *
from databaseCommunicationUtilities import *
from Utilities import *
from SQLFunctions import *
from config import *
import sys


# Wait
time.sleep(2)

# Get the dir name
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# Flask app
app = Flask(__name__, static_url_path='/static', template_folder='templates')

# Connect to MYSQL
mysqlConn= pymysql.connect('mysql', 'root', 'root', 'db')
mysqlConnCursor = mysqlConn.cursor()

# Rate limit
limiter = Limiter (
    app,
    key_func=get_remote_address,
    default_limits=["28000 per day", "1000 per hour", "1000 per minute"]
)

# Creating Sessions
secretKey = os.urandom(24)
app.secret_key = secretKey

# Configure CORS
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

# # Create a user
# user1 = 'admin'
# user1hashedpass = generate_password_hash('admin')
# mysqlConnCursor.execute("INSERT INTO users(Username, HashedPass, CreationDate) VALUES ('{}', '{}', '{}')".format(user1, user1hashedpass, datetime.datetime.now().strftime('%Y-%m-%d')))
# mysqlConnCursor.close()
# mysqlConn.commit()
# mysqlConn.close()

# @app.errorhandler(500)
# def internal_error(error):
#     return home()

def test_add_date_1():
    raw_competitions_add("GODS_COMP", "4")
    raw_competitions_add("KIDS_COMP", "2")
    raw_competitions_add("WHATEVER_COMP", "4")
    raw_competitions_team_add("GODS_COMP", "Team1", "Team1.com", "192.168.1.0/24", "192.168.1.254", "8.8.8.8", "Group100", "2", "4", "6", "0", "0")
    raw_competitions_team_add("GODS_COMP", "Team2", "Team2.com", "192.168.2.0/24", "192.168.2.254", "8.8.8.8", "Group100", "2", "4", "6", "0", "0")
    raw_competitions_team_add("GODS_COMP", "Team2", "Team2.com", "192.168.2.0/24", "192.168.2.254", "8.8.8.8", "Group100", "2", "4", "6", "0", "0")
    raw_competitions_team_add("GODS_COMP", "Team3", "Team3.com", "192.168.3.0/24", "192.168.3.254", "8.8.8.8", "Group100", "2", "4", "6", "0", "0")



def mysqlExecute(q):
    # Connect to MYSQL
    result = ""
    try:
        if debug:
            print("Executing :"+str(q), file=sys.stderr)
        mysqlConn= pymysql.connect('mysql', 'root', 'root', 'db')
        mysqlConnCursor = mysqlConn.cursor()
        mysqlConnCursor.execute(str(q))
        result = mysqlConnCursor.fetchone()
        mysqlConn.commit()
        mysqlConnCursor.close()
        mysqlConn.close()
        if debug:
            print("Output :"+str(result), file=sys.stderr)
    except Exception as e:
        if debug:
            print(e, file=sys.stderr)
        else:
            pass
    try:
        return str(result)
    except:
        return result


def mysqlExecuteAll(q):
    # Connect to MYSQL
    mysqlConn= pymysql.connect('mysql', 'root', 'root', 'db')
    mysqlConnCursor = mysqlConn.cursor()
    mysqlConnCursor.execute(str(q))
    result = mysqlConnCursor.fetchall()
    if debug:
        print("Executing: "+q+"\nOutput: "+str(result),file=sys.stderr)
    mysqlConn.commit()
    mysqlConnCursor.close()
    mysqlConn.close()
    return result




@app.route("/")
def root():
    if 'username' in session:
        return home()
    return render_template('login.html')


@app.route("/home")
def home():
    if 'username' in session:
        return render_template('home.html', templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return render_template('login.html')


@app.route("/install", methods=['get', 'post'])
def install():
    # Check the data base for config entry.
    result = mysqlExecute("select * from config")
    # returns this example: (1, 'VSPHERE_SERVER1', 'VSPHERE_SERVER2', 'VSPHERE_SERVER3')
    if debug:
        print(result, file=sys.stderr)
    if len(str(result)) > 10:
        return "You have configured me already!"
    else:
        # If it does not exist, add this:
        vcip = dcname = domain = "VSPHERE_SERVER1"
        if request.method == 'POST':
            # Escape
            vcip = request.values.get('vcip')
            vcip = pymysql.escape_string(vcip)
            dcname = request.values.get('dcname')
            dcname = pymysql.escape_string(dcname)
            domain = request.values.get('domain')
            domain = pymysql.escape_string(domain)
            result = mysqlExecute("INSERT INTO config(VSPHERE_SERVER, DC_NAME, DOMAIN) VALUES ('{}', '{}', '{}')".format(vcip, dcname, domain))
            if debug:
                print("INSERTED! ", file=sys.stderr)
        return render_template("install.html")


"""
This is /login where it takes username and password
TODO LIST:
    Handle some errors, like when the user does not install() before trying to login. (Real handling not try catch)
"""
@app.route("/login", methods=['GET','POST'])
@limiter.limit("14400/day;600/hour;1000/minute")
def login():
    # If submitting data
    if request.method == 'POST':
        session['username'] = request.form['username']
        # This is too much ,later
        # HASHEDPASSWORD = hashlib.sha224(password).hexdigest()
        # mysqlExecute("INSERT INTO logged(USERNAME, HASHEDPASSWORD, CREATIONDATE) VALUES ('{}', '{}', '{}')".format(username, HASHEDPASSWORD, datetime.datetime.now().strftime('%Y-%m-%d')))
        # session["username"] = username
        # session["H"] = HASHEDPASSWORD
        return redirect(url_for('home'))

        try:
            # Fitch for current vSphere IP
            # More info https://vdc-download.vmware.com/vmwb-repository/dcr-public/1cd28284-3b72-4885-9e31-d1c6d9e26686/71ef7304-a6c9-43b3-a3cd-868b2c236c81/doc/operations/com/vmware/vcenter/vm.list-operation.html
            try:
                VSPHERE_SERVER = mysqlExecute("select VSPHERE_SERVER from config")
                VSPHERE_SERVER = str(VSPHERE_SERVER).replace('(','').replace(')','').replace("'",'').replace(" ",'').replace(",",'')
            except:
                return root()
            # IF there is no IP
            # TODO Test this! - Does it really work?
            if len(VSPHERE_SERVER) < 1 or VSPHERE_SERVER == None:
                install()

            # TODO - Escape
            username = request.form['username']
            password = request.form['password']
            success = vCenterAuth(VSPHERE_SERVER,username, password)

            # If no username posted
            if username == None:
                return invalid_user()
            # If no password posted
            elif password == None:
                return invalid_password()
            # IF vCenterAuth logged in
            elif success:
                # Create a session
                # This is called security :)
                session['username'] = username
                # This is too much ,later
                # HASHEDPASSWORD = hashlib.sha224(password).hexdigest()
                # mysqlExecute("INSERT INTO logged(USERNAME, HASHEDPASSWORD, CREATIONDATE) VALUES ('{}', '{}', '{}')".format(username, HASHEDPASSWORD, datetime.datetime.now().strftime('%Y-%m-%d')))
                # session["username"] = username
                # session["H"] = HASHEDPASSWORD
                return redirect(url_for('home'))

            # Else, fuck off !
            return invalid_password()
        except:
            pass
    return root()



@app.route("/templates", methods=['GET','POST'])
def templates():
    if 'username' in session:
        data = mysqlExecuteAll("SELECT * FROM templates")
        if debug:
            print("The data object: "+ str(data),file=sys.stderr)
        return render_template('templates.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()


@app.route("/add_templates", methods=['POST'])
def add_templates():
    if 'username' in session:
        if request.method == 'POST':
            try:
                TEMPLATES_NAME = pymysql.escape_string(request.values.get('TEMPLATES_NAME'))
                OTHER = pymysql.escape_string(request.values.get('OTHER'))
                mysqlExecute("INSERT INTO templates(TEMPLATES_NAME, OTHER) VALUES ('{}', '{}')".format(TEMPLATES_NAME, OTHER))
                time.sleep(1)
                addEvent(session['username'], "Template creation", "A template's information has been added")
                time.sleep(1)
                return render_template('done.html', url = url_for('templates'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except Exception as e:
                print(e, file=sys.stderr)

    # TODO
    # Add more descriptive error with parameters!
    return abort(500, 'add_templates error...')


def getTemplatesLength():
    if 'username' in session:
        try:
            data = mysqlExecuteAll("SELECT * FROM templates")
            length = int(data[-1][0])
        except:
            length = 0
        return length
    return root()

def getEventsLength():
    if 'username' in session:
        try:
            data = mysqlExecuteAll("SELECT * FROM events")
            length = int(data[-1][0])
        except:
            length = 0
        return length
    return root()


def addEvent(BYUSER_VALUE, EVENT_NAME_VALUE, DESCRIPTIONS_VALUE = ""):
    if 'username' in session:
        try:
            BYUSER_VALUE = pymysql.escape_string(BYUSER_VALUE)
            EVENT_NAME_VALUE = pymysql.escape_string(EVENT_NAME_VALUE)
            DESCRIPTIONS_VALUE = pymysql.escape_string(DESCRIPTIONS_VALUE)
            q = "INSERT INTO events(BYUSER, EVENT_NAME, DESCRIPTIONS, CREATION_DATE) VALUES ('{}', '{}', '{}', '{}')".format(str(BYUSER_VALUE), str(EVENT_NAME_VALUE), str(DESCRIPTIONS_VALUE), str(time.strftime('%Y-%m-%d %H:%M:%S')))
            print("Adding an event: "+q, file=sys.stderr)
            mysqlExecute(q)
        except Exception as e:
            print(e, file=sys.stderr)
    return root()



@app.route("/tasks", methods=['GET','POST'])
def tasks():
    if 'username' in session:
        events = mysqlExecuteAll("SELECT * FROM events")
        if debug:
            print("The events object: "+ str(events),file=sys.stderr)
        return render_template('tasks.html', output_events = events, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()



@app.route("/settings", methods=['GET','POST'])
def settings():
    return "settings"



@app.route("/logout", methods=['GET','POST'])
def logout():
    session.pop('username', None)
    flash('You were logged out.')
    return redirect(url_for('login'))


@app.route("/home", methods=['GET','POST'])
def homepage():
    pass


@app.route("/invalid_user")
def invalid_user():
    return """
        <!DOCTYPE html>
    <html>
    <head>
      <title>Invalid Username</title>
    </head>
      <body>The username used does not exist</body>
    </html>
    """


@app.route("/invalid_password")
def invalid_password():
    return """
        <!DOCTYPE html>
    <html>
    <head>
      <title>Invalid password</title>
    </head>
      <body>Invalid password</body>
    </html>
    """




@app.route("/competitions", methods=['GET'])
def competitions():
    if 'username' in session:
        data = mysqlExecuteAll("SELECT * FROM competitions")
        return render_template('competitions.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()


@app.route("/competitions_edit", methods=['GET','POST'])
def competitions_edit():
    if 'username' in session:
        if request.method == 'POST':
            try:
                error_message = ""
                ID = pymysql.escape_string(request.values.get('ID'))
                UNAME = pymysql.escape_string(request.values.get('UNAME'))
                TEAMS = pymysql.escape_string(request.values.get('TEAMS'))

                CREATED_TEAMS = pymysql.escape_string(request.values.get('CREATED_TEAMS'))
                UNIX_VMS = pymysql.escape_string(request.values.get('UNIX_VMS'))
                if len(UNIX_VMS) < 1:
                    if debug:
                        error_message = "Missing CREATED_TEAMS"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())


                WIN_VMS = pymysql.escape_string(request.values.get('WIN_VMS'))
                if len(WIN_VMS) < 1:
                    if debug:
                        error_message = "Missing WIN_VMS"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                UNIX_VMS = pymysql.escape_string(request.values.get('UNIX_VMS'))
                if len(UNIX_VMS) < 1:
                    if debug:
                        error_message = "Missing UNIX_VMS"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())


                TOTAL_VMS = str(int(WIN_VMS) + int(UNIX_VMS))

                # Edit a comp and make an event
                raw_competitions_edit(UNAME, TEAMS, CREATED_TEAMS, WIN_VMS, UNIX_VMS, TOTAL_VMS,"0", ID)



                return render_template('done.html', url = url_for('competitions'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                # TODO Add a error.html page where it just redirects to a url_for('url') like done.html
                data = mysqlExecuteAll("SELECT * FROM competitions")
                return render_template('competitions.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
        else:
            try:
                COMP_ID = pymysql.escape_string(request.args.get('COMP_ID'))
                data = mysqlExecuteAll("SELECT * FROM competitions WHERE ID={}".format(COMP_ID))
                return render_template('competitions_edit.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                # TODO Add a error.html page where it just redirects to a url_for('url') like done.html
                data = mysqlExecuteAll("SELECT * FROM competitions")
                return render_template('competitions.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()



@app.route("/competitions_add", methods=['GET','POST'])
def competitions_add():
    if 'username' in session:
        if request.method == 'POST':
            try:
                # TODO Check for UNAME and TEAMS
                UNAME = pymysql.escape_string(request.values.get('UNAME'))
                TEAMS = pymysql.escape_string(request.values.get('TEAMS'))


                WIN_VMS = pymysql.escape_string(request.values.get('WIN_VMS'))
                if len(WIN_VMS) < 1:
                    if debug:
                        error_message = "Missing WIN_VMS"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                UNIX_VMS = pymysql.escape_string(request.values.get('UNIX_VMS'))
                if len(UNIX_VMS) < 1:
                    if debug:
                        error_message = "Missing UNIX_VMS"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())


                TOTAL_VMS = str(int(WIN_VMS) + int(UNIX_VMS))
                CREATED_FLAG = CREATED_FLAG_C = TOTAL_CREATED_VMS = "0"


                # Create a comp and make an event
                raw_competitions_add(UNAME, TEAMS, "0", WIN_VMS, UNIX_VMS, TOTAL_VMS, TOTAL_CREATED_VMS, CREATED_FLAG, CREATED_FLAG_C)

                return render_template('done.html', url = url_for('competitions'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                pass
        return render_template('competitions_add.html', username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()




def check_competition_existence(COMPETITION_NAME):
    try:
        q = "select UNAME from competitions where UNAME = '{}'".format(COMPETITION_NAME)
        result = mysqlExecute(q)
        if debug:
            print("Testing "+COMPETITION_NAME, file=sys.stderr)
            print("Mysql output: "+result, file=sys.stderr)
        if len(result) <= 1:
            return 0
    except:
        if debug:
            print("check_competition_existence() Error #82382", file=sys.stderr)
        return 0
    return 1

def check_team_existence(COMPETITION_NAME, TEAM):
    try:
        q = "select ID from teams where TEAM = '{}' and COMPETITION_NAME ='{}'".format(TEAM, COMPETITION_NAME)
        result = mysqlExecute(q)
        if debug:
            print("Testing "+COMPETITION_NAME, file=sys.stderr)
            print("Mysql output: "+result, file=sys.stderr)
        if len(result) <= 1:
                return 0
    except:
        if debug:
            print("check_competition_existence() Error #82382", file=sys.stderr)
        return 0
    return 1


# Teams section.

@app.route("/competitions_team", methods=['GET'])
def competitions_team():
    if 'username' in session:
        data = mysqlExecuteAll("SELECT * FROM teams")
        return render_template('competitions_team.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()



@app.route("/competitions_team_edit", methods=['GET','POST'])
def competitions_team_edit():
    if 'username' in session:
        if request.method == 'POST':
            try:

                COMPETITION_NAME = pymysql.escape_string(request.values.get('COMPETITION_NAME'))

                # First check if the COMPETITION_NAME exist.
                error_message = 'The selected competition ('+ COMPETITION_NAME +') doesn\'t exist'
                try:
                    q = "select UNAME from competitions where UNAME = '{}'".format(COMPETITION_NAME)
                    result = str(mysqlExecute(q))

                    if debug:
                        print("Testing "+COMPETITION_NAME, file=sys.stderr)
                        print("Mysql output: "+result, file=sys.stderr)
                    if len(result) <= 1:
                        return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
                except:
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                # If the selected competition "COMPETITION_NAME" exist update it
                ID = pymysql.escape_string(request.values.get('ID'))
                TEAM = pymysql.escape_string(request.values.get('TEAM'))
                if len(TEAM) < 1:
                    if debug:
                        error_message = "Missing TEAM"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                DOMAIN_NAME = pymysql.escape_string(request.values.get('DOMAIN_NAME'))
                if len(DOMAIN_NAME) < 1:
                    if debug:
                        error_message = "Missing DOMAIN_NAME"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                SUBNET = pymysql.escape_string(request.values.get('SUBNET'))
                if len(SUBNET) < 1:
                    if debug:
                        error_message = "Missing SUBNET"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                GATEWAY = pymysql.escape_string(request.values.get('GATEWAY'))
                if len(GATEWAY) < 1:
                    if debug:
                        error_message = "Missing GATEWAY"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                DNS_SERVER1 = pymysql.escape_string(request.values.get('DNS_SERVER1'))
                if len(DNS_SERVER1) < 1:
                    if debug:
                        error_message = "Missing DNS_SERVER1"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                NIC = pymysql.escape_string(request.values.get('NIC'))
                if len(NIC) < 1:
                    if debug:
                        error_message = "Missing NIC"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())


                # Create a competitions object and make an event
                raw_competitions_team_edit(COMPETITION_NAME,
                                           TEAM,
                                           DOMAIN_NAME,
                                           SUBNET,
                                           GATEWAY,
                                           DNS_SERVER1,
                                           NIC,
                                           ID)


                return render_template('done.html', url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                error_message = "Unknown problem in competitions_team_edit"
                print("Error: "+error_message, file=sys.stderr)
                return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
        else:
        # if request.method is 'GET'
            try:
                TEAM_ID = pymysql.escape_string(request.args.get('TEAM_ID'))
                if len(TEAM_ID) < 1:
                    if debug:
                        error_message = "Missing TEAM_ID"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                data = mysqlExecuteAll("SELECT * FROM teams WHERE ID={}".format(TEAM_ID))
                return render_template('competitions_team_edit.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                # TODO Add a error.html page where it just redirects to a url_for('url') like done.html
                data = mysqlExecuteAll("SELECT * FROM teams")
                return render_template('competitions_team.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()



def raw_competitions_team_edit(COMPETITION_NAME,
                               TEAM,
                               DOMAIN_NAME,
                               SUBNET,
                               GATEWAY,
                               DNS_SERVER1,
                               NIC,
                               CREATED_FLAG,
                               CREATED_FLAG_C,
                               CREATED_VMS_FLAG,
                               CONFIGURED_VMS_FLAG,
                               ID):
    q = "UPDATE teams SET " \
        "COMPETITION_NAME = '{}'," \
        "TEAM= '{}'," \
        "DOMAIN_NAME= '{}'," \
        "SUBNET= '{}'," \
        "GATEWAY= '{}'," \
        "DNS_SERVER1= '{}'," \
        "NIC= '{}'," \
        "CREATED_FLAG = '{}'," \
        "CREATED_FLAG_C = '{}'," \
        "CREATED_VMS_FLAG = '{}'," \
        "CONFIGURED_VMS_FLAG = '{}' WHERE ID = '{}'".format(COMPETITION_NAME,
                                                 TEAM,
                                                 DOMAIN_NAME,
                                                 SUBNET,
                                                 GATEWAY,
                                                 DNS_SERVER1,
                                                 NIC,
                                                 CREATED_FLAG,
                                                 CREATED_FLAG_C,
                                                 CREATED_VMS_FLAG,
                                                 CONFIGURED_VMS_FLAG,
                                                 ID)

    if debug:
        print("UPDATING "+q, file=sys.stderr)
    mysqlExecute(q)
    addEvent(session['username'], "Team modification", TEAM+" from competition "+COMPETITION_NAME+" has been updated")




@app.route("/competitions_team_add", methods=['GET','POST'])
def competitions_team_add():
    if 'username' in session:
        if request.method == 'POST':
            try:
                # Check
                COMPETITION_NAME = pymysql.escape_string(request.values.get('COMPETITION_NAME'))

                # First check if the COMPETITION_NAME exist.
                error_message = 'The selected competition ('+ COMPETITION_NAME +') doesn\'t exist'
                try:
                    q = "select UNAME from competitions where UNAME = '{}'".format(COMPETITION_NAME)
                    result = mysqlExecute(q)

                    if debug:
                        print("Testing "+COMPETITION_NAME, file=sys.stderr)
                        print("Mysql output: "+result, file=sys.stderr)
                    if len(str(result)) <= 1:
                        return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
                except:
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                TEAM = pymysql.escape_string(request.values.get('TEAM'))
                if len(TEAM) < 1:
                    if debug:
                        error_message = "Missing TEAM"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                DOMAIN_NAME = pymysql.escape_string(request.values.get('DOMAIN_NAME'))
                if len(DOMAIN_NAME) < 1:
                    if debug:
                        error_message = "Missing DOMAIN_NAME"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                SUBNET = pymysql.escape_string(request.values.get('SUBNET'))
                if len(SUBNET) < 1:
                    if debug:
                        error_message = "Missing SUBNET"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                GATEWAY = pymysql.escape_string(request.values.get('GATEWAY'))
                if len(GATEWAY) < 1:
                    if debug:
                        error_message = "Missing GATEWAY"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                DNS_SERVER1 = pymysql.escape_string(request.values.get('DNS_SERVER1'))
                if len(DNS_SERVER1) < 1:
                    if debug:
                        error_message = "Missing DNS_SERVER1"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                NIC = pymysql.escape_string(request.values.get('NIC'))
                if len(NIC) < 1:
                    if debug:
                        error_message = "Missing NIC"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                CREATED_FLAG = "0"
                CREATED_FLAG_C = "0"

                # Create a team and make an event
                raw_competitions_team_add(COMPETITION_NAME,
                                          TEAM,
                                          DOMAIN_NAME,
                                          SUBNET,
                                          GATEWAY,
                                          DNS_SERVER1,
                                          NIC,
                                          CREATED_FLAG,
                                          CREATED_FLAG_C)


                return render_template('done.html', url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                error_message = "Unknown problem in competitions_team_add()"
                print("Error: "+error_message, file=sys.stderr)
                return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
        else:
            # if request.method == 'GET':
            return render_template('competitions_team_add.html', username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()


# VMs section

@app.route("/competitions_vm", methods=['GET'])
def competitions_vm():
    if 'username' in session:
        data = mysqlExecuteAll("SELECT * FROM vms")
        return render_template('competitions_vm.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()


@app.route("/competitions_vm_edit", methods=['GET','POST'])
def competitions_vm_edit():
    if 'username' in session:
        if request.method == 'POST':
            try:
                ID = pymysql.escape_string(request.values.get('ID'))
                COMPETITION_NAME = pymysql.escape_string(request.values.get('COMPETITION_NAME'))
                TEAM = pymysql.escape_string(request.values.get('TEAM'))
                VM_NAME = pymysql.escape_string(request.values.get('VM_NAME'))
                CPU = pymysql.escape_string(request.values.get('CPU'))
                MEMORY = pymysql.escape_string(request.values.get('MEMORY'))
                GUEST_OS_TYPE = pymysql.escape_string(request.values.get('GUEST_OS_TYPE'))
                CREATED_FLAG = CREATED_FLAG_C = "0"

                # Edit a comp and make an event
                raw_competitions_vm_edit(COMPETITION_NAME, TEAM, VM_NAME, CPU, MEMORY, GUEST_OS_TYPE, CREATED_FLAG, CREATED_FLAG_C, ID)

                return render_template('done.html', url = url_for('competitions_vm'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                # TODO Add a error.html page where it just redirects to a url_for('url') like done.html
                data = mysqlExecuteAll("SELECT * FROM vms")
                return render_template('competitions_vm.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
        else:

            # IF 'GET'
            try:
                VM_ID = pymysql.escape_string(request.args.get('VM_ID'))
                data = mysqlExecuteAll("SELECT * FROM vms WHERE ID={}".format(VM_ID))
                return render_template('competitions_vm_edit.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                # TODO Add a error.html page where it just redirects to a url_for('url') like done.html
                data = mysqlExecuteAll("SELECT * FROM vms")
                return render_template('competitions_vm.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()

"""

"""
def raw_competitions_vm_edit(COMPETITION_NAME, TEAM, VM_NAME, CPU, MEMORY, GUEST_OS_TYPE, CREATED_FLAG, CREATED_FLAG_C, ID):
    mysqlExecute("UPDATE vms SET CPU = '{}', MEMORY = '{}', CREATED_FLAG = '{}', CREATED_FLAG_C = '{}' WHERE ID = '{}'".format(CPU, MEMORY, CREATED_FLAG, CREATED_FLAG_C, ID))
    addEvent(session['username'], "VM modification", VM_NAME+" VM for team "+TEAM+" in competition "+COMPETITION_NAME+" has been modified")



def raw_competitions_vm_add(COMPETITION_NAME, TEAM, VM_NAME, CPU, MEMORY, GUEST_OS_TYPE, CREATED_FLAG, CREATED_FLAG_C):
    mysqlExecute("INSERT INTO vms(COMPETITION_NAME,"
                 " TEAM,"
                 " VM_NAME,"
                 " CPU,"
                 " MEMORY,"
                 " GUEST_OS_TYPE,"
                 " CREATED_FLAG,"
                 " CREATED_FLAG_C) VALUES ('{}', '{}', '{}', '{}','{}', '{}', '{}', '{}')"
                 .format(COMPETITION_NAME,
                         TEAM,
                         VM_NAME,
                         CPU,
                         MEMORY,
                         GUEST_OS_TYPE,
                         CREATED_FLAG,
                         CREATED_FLAG_C))
    if debug:
        print("A vm has been created "+str(VM_NAME), file=sys.stderr)
    addEvent(session['username'], "VM addition",VM_NAME+" VM has been created for team "+TEAM+" in competition "+COMPETITION_NAME)




@app.route("/competitions_vm_add", methods=['GET','POST'])
def competitions_vm_add():
    if 'username' in session:
        if request.method == 'POST':
            try:
                """
                    ID INTEGER NOT NULL AUTO_INCREMENT,
                    COMPETITION_NAME VARCHAR(50) NOT NULL,  -- A unique name
                    TEAM VARCHAR(50) NOT NULL,
                    VM_NAME VARCHAR(50) NOT NULL, -- This is "Name" and "Hostname"
                    CPU VARCHAR(50) NOT NULL,
                    MEMORY VARCHAR(50) NOT NULL,
                    GUEST_OS_TYPE VARCHAR(50),
                    CREATED_FLAG INTEGER NOT NULL,
                    CREATED_FLAG_C INTEGER NOT NULL,
                """
                COMPETITION_NAME = pymysql.escape_string(request.values.get('COMPETITION_NAME'))
                if len(COMPETITION_NAME) < 1:
                    if debug:
                        error_message = "Missing COMPETITION_NAME"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                TEAM = pymysql.escape_string(request.values.get('TEAM'))
                if len(TEAM) < 1:
                    if debug:
                        error_message = "Missing TEAM"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                VM_NAME = pymysql.escape_string(request.values.get('VM_NAME'))
                if len(VM_NAME) < 1:
                    if debug:
                        error_message = "Missing VM_NAME"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                CPU = pymysql.escape_string(request.values.get('CPU'))
                if len(CPU) < 1:
                    if debug:
                        error_message = "Missing CPU"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                MEMORY = pymysql.escape_string(request.values.get('MEMORY'))
                if len(MEMORY) < 1:
                    if debug:
                        error_message = "Missing MEMORY"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                GUEST_OS_TYPE = pymysql.escape_string(request.values.get('GUEST_OS_TYPE'))
                if len(GUEST_OS_TYPE) < 1:
                    if debug:
                        error_message = "Missing GUEST_OS_TYPE"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                CREATED_FLAG = CREATED_FLAG_C = "0"

                # Create a vm and make an event
                raw_competitions_vm_add(COMPETITION_NAME, TEAM, VM_NAME, CPU, MEMORY, GUEST_OS_TYPE, CREATED_FLAG, CREATED_FLAG_C)

                return render_template('done.html', url = url_for('competitions_vm'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                pass
        return render_template('competitions_vm_add.html', username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()




@app.route("/competitions_wizard", methods=['GET', 'POST'])
def competitions_wizard():
    if 'username' in session:
        # Note that we are not calling this function plain "random()" because random
        # is the name of a package we imported.
        # Step 1, Create a comp

        if "step" not in request.form:
            """
            Doesn't take anything
            Sends a page where users can send the application back a new comp data.
            """
            debugMessage("Redirect #1278313")
            return render_template("wizard.html", step="PAGE_CREATE_COMP")
        elif request.form["step"] == "PAGE_2":
            """
            When it's PAGE_2, it gets:
            UNAME, TEAMS, WIN_VMS, UNIX_VMS.
            
            It redirects it to PAGE_3.
            """
            try:
                error_message = ""

                UNAME = pymysql.escape_string(str(request.form['UNAME']))
                TEAMS = pymysql.escape_string(str(request.form['TEAMS']))

                # If some of them is empty.
                if (len(UNAME) < 1 or len(TEAMS) < 1):
                    pass

                WIN_VMS = pymysql.escape_string(request.values.get('WIN_VMS'))
                if len(WIN_VMS) < 1:
                    if debug:
                        error_message = "Missing WIN_VMS"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                UNIX_VMS = pymysql.escape_string(request.values.get('UNIX_VMS'))
                if len(UNIX_VMS) < 1:
                    if debug:
                        error_message = "Missing UNIX_VMS"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())


                TOTAL_VMS = str(int(WIN_VMS) + int(UNIX_VMS))
                CREATED_FLAG = CREATED_FLAG_C = CREATED_TEAMS = TOTAL_CREATED_VMS = "0"


                # Create a COMPETITION
                raw_competitions_add(UNAME, TEAMS, CREATED_TEAMS, WIN_VMS, UNIX_VMS, TOTAL_VMS, TOTAL_CREATED_VMS, CREATED_FLAG, CREATED_FLAG_C)

                # Add teams objects to mysql so we use get_competition_teams(COMPETITION_NAME) in step "PAGE_3_PICK"
                for i in range(int(TEAMS)):
                    TEAM_tmp = "Team_"+str(i+1)
                    raw_competitions_team_add(UNAME,
                                              TEAM_tmp,
                                              "0",
                                              "0",
                                              "0",
                                              "0",
                                              "0",
                                              "0",
                                              "0")


                # Move to the next page which is editing teams in step 2 template
                TEAMS = get_competition_teams(UNAME)
                debugMessage("Redirect #813613")
                return render_template("wizard.html", step="PAGE_3_PICK", UNAME=UNAME, TEAMS = TEAMS)
            except Exception as ex:
                if debug:
                    debugMessage("Couldn't create a comp")
                    debugMessage("Error: "+str(ex))
                    debugMessage("Block #134233")
        # Step 3, where we can create teams
        elif request.form["step"] == "PAGE_CREATE_TEAM":
            """
            PAGE_CREATE_TEAM, it helps creating teams using UNAME.
            
            """
            try:
                """
                This block tris to get some parameters that step "PAGE_3_PICK" should submit.
                If it didn't get all the parameters that means something went wrong, thus redirect to step "PAGE_3_PICK"
                """
                # Sanitize
                COMPETITION_NAME = UNAME = pymysql.escape_string(str(request.form['UNAME']))
                TEAM = pymysql.escape_string(str(request.form['TEAM']))


                # Get all elements of a comp
                # elements = get_all_elements_comp(UNAME)
                # debugMessage("Getting all elements: "+str(elements))
                # TEAMS = elements[2]
                # CREATED_TEAMS = elements[3]
                # if debug:
                #     debugMessage("Comparing "+str(TEAMS)+" and "+str(CREATED_TEAMS))
                #     debugMessage("Checking if we need more teams, TEAMS:" + str(TEAMS) + " > CREATED_TEAMS:" + str(
                #         CREATED_TEAMS) + " ?")
                # # Check if we need to create a new team.
                # if int(TEAMS) > int(CREATED_TEAMS):
                #     debugMessage("Redirect #841611")
                #     # Send it back to itself.
                return render_template("wizard.html", step="PAGE_CREATE_TEAM", UNAME=UNAME, TEAM=TEAM)
            except Exception as e:
                if debug:
                    debugMessage(e)
                    debugMessage("Error #72521 ")
                    debugMessage("Block #77823")

        elif request.form["step"] == "TAKE_PARAMETERS":
            """
            This block gets the values coming from PAGE_CREATE_TEAM and process it.
            Then redirect back to PAGE_3_PICK
            """
            try:
                COMPETITION_NAME = UNAME = pymysql.escape_string(str(request.form['UNAME']))
                TEAM = pymysql.escape_string(request.values.get('TEAM'))


                if len(TEAM) < 1:
                    if debug:
                        error_message = "Missing TEAM"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                DOMAIN_NAME = pymysql.escape_string(request.values.get('DOMAIN_NAME'))
                if len(DOMAIN_NAME) < 1:
                    if debug:
                        error_message = "Missing DOMAIN_NAME"
                        debugMessage(error_message)
                    DOMAIN_NAME = TEAM + ".com"

                SUBNET = pymysql.escape_string(request.values.get('SUBNET'))
                if len(SUBNET) < 1:
                    if debug:
                        error_message = "Missing SUBNET"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                GATEWAY = pymysql.escape_string(request.values.get('GATEWAY'))
                if len(GATEWAY) < 1:
                    if debug:
                        error_message = "Missing GATEWAY"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                DNS_SERVER1 = pymysql.escape_string(request.values.get('DNS_SERVER1'))
                if len(DNS_SERVER1) < 1:
                    if debug:
                        error_message = "Missing DNS_SERVER1"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                NIC = pymysql.escape_string(request.values.get('NIC'))
                if len(NIC) < 1:
                    if debug:
                        error_message = "Missing NIC"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                CREATED_FLAG = CREATED_VMS_FLAG = CONFIGURED_VMS_FLAG = "0"
                CREATED_FLAG_C = "1" # So the team object knows that it has been edited

                """
                Since the team has been created in the past step we need to edit this.
                Edit a team and make an event.
                """
                safe_competitions_team_edit_by_name(COMPETITION_NAME,
                                                    TEAM,
                                                    DOMAIN_NAME,
                                                    SUBNET,
                                                    GATEWAY,
                                                    DNS_SERVER1,
                                                    NIC,
                                                    CREATED_FLAG,
                                                    CREATED_FLAG_C,
                                                    CREATED_VMS_FLAG,
                                                    CONFIGURED_VMS_FLAG)

                # Update
                update_CREATED_TEAMS_comp(COMPETITION_NAME)


                """
                In this stage they are two ways it can end up with.
                one - we still have teams to create.
                    How to go with that
                        Get the comp teams and created_teams and according to that move.
                        
                    What it will happen
                        Goes back to PAGE_3_PICK
                Two - we don't have teams to create
                    How to go with that
                        
                    What it will happen
                        move forward to step "PAGE_3_PICK_VMS"
                
                """

                elements = get_all_elements_comp(UNAME)
                TEAMS = elements[2]
                CREATED_TEAMS = elements[3]


                if int(TEAMS) > int(CREATED_TEAMS):
                    debugMessage("Redirect #841611")
                    # Send it back to pick another team to create/edit.
                    TEAMS = get_competition_teams(UNAME)
                    return render_template("wizard.html", step="PAGE_3_PICK", UNAME=UNAME, TEAMS = TEAMS)
                else:
                    """
                    At this point we need to start creating VMs for each team.
                    """
                    debugMessage("Redirect #98181")
                    # Get all teams
                    # Check if any team has no VMS
                    teams = next_unedited_vm(COMPETITION_NAME)
                    i = 0
                    for team in teams:
                        """
                        ID INTEGER NOT NULL AUTO_INCREMENT,
                        COMPETITION_NAME VARCHAR(50) NOT NULL,  -- A unique name
                        TEAM VARCHAR(50) NOT NULL,
                        DOMAIN_NAME VARCHAR(50) NOT NULL,
                        SUBNET VARCHAR(50) NOT NULL,
                        GATEWAY VARCHAR(50) NOT NULL,
                        DNS_SERVER1 VARCHAR(50) NOT NULL,
                        NIC VARCHAR(50) NOT NULL,
                        CREATED_FLAG INTEGER NOT NULL,
                        CREATED_FLAG_C INTEGER NOT NULL, -- Created/Edited flag
                        CREATED_VMS_FLAG INTEGER NOT NULL, -- I don't need it anymore
                        CONFIGURED_VMS_FLAG INTEGER NOT NULL, --
                        CONSTRAINT users_pk PRIMARY KEY(ID)
                        """
                        debugMessage(str(i)+"- "+str(team))

                    return render_template("wizard.html", step="PAGE_CREATE_VM", UNAME=UNAME)

            except Exception as e:
                if debug:
                    debugMessage(e)
                    debugMessage("NOTE: We don't need to config a tame ")
                    debugMessage("Block #1987823")
        elif request.form["step"] == "PAGE_3_PROCESS":
            pass
        elif request.form["step"] == "step_f":
            pass
        else:
            print("None of these steps is valid", file=sys.stderr)
            debugMessage("Redirect #1337912")
            return root()
    debugMessage("No session competitions_wizard()")
    debugMessage("Redirect #812323613")
    return root()




@app.route("/competition_summary", methods=['GET'])
def competition_summary():
    return render_template('competition_summary.html',competition_data = get_competition_data("co1"))








def raw_competitions_add(UNAME, TEAMS, CREATED_TEAMS, WIN_VMS, UNIX_VMS, TOTAL_VMS, TOTAL_CREATED_VMS, CREATED_FLAG, CREATED_FLAG_C):
    """

    :param UNAME:
    :param TEAMS:
    :param CREATED_TEAMS:
    :param WIN_VMS:
    :param UNIX_VMS:
    :param TOTAL_VMS:
    :param TOTAL_CREATED_VMS:
    :param CREATED_FLAG:
    :param CREATED_FLAG_C:
    :return:
    """
    mysqlExecute("INSERT INTO competitions("
                 "UNAME, "
                 "TEAMS, "
                 "CREATED_TEAMS, " \
                 "WIN_VMS, "
                 "UNIX_VMS, "
                 "TOTAL_VMS, "
                 "TOTAL_CREATED_VMS, "
                 "CREATED_FLAG, "
                 "CREATED_FLAG_C) VALUES ('{}' , '{}', '{}' , '{}', '{}', '{}', '{}', '{}', '{}')"
                 .format(
                    UNAME,
                    TEAMS,
                    CREATED_TEAMS,
                    WIN_VMS,
                    UNIX_VMS,
                    TOTAL_VMS,
                    TOTAL_CREATED_VMS,
                    CREATED_FLAG,
                    CREATED_FLAG_C))
    addEvent(session['username'], "Competition addition", UNAME+" competition has been created with "+TEAMS+" teams")





def raw_competitions_edit(UNAME, TEAMS, CREATED_TEAMS, WIN_VMS, UNIX_VMS, TOTAL_VMS, TOTAL_CREATED_VMS, ID):
    """

    :param UNAME:
    :param TEAMS:
    :param CREATED_TEAMS:
    :param WIN_VMS:
    :param UNIX_VMS:
    :param TOTAL_VMS:
    :param TOTAL_CREATED_VMS:
    :param ID:
    :return:
    """
    mysqlExecute("UPDATE competitions SET "
                 " UNAME = '{}',"
                 " TEAMS= '{}',"
                 " CREATED_TEAMS= '{}',"
                 " WIN_VMS= '{}',"
                 " UNIX_VMS= '{}',"
                 " TOTAL_VMS= '{},'"
                 " TOTAL_CREATED_VMS= '{}'"
                 " WHERE ID = '{}'"
                 .format(UNAME,
                         TEAMS,
                         CREATED_TEAMS,
                         WIN_VMS,
                         UNIX_VMS,
                         TOTAL_VMS,
                         TOTAL_CREATED_VMS,
                         ID))
    addEvent(session['username'], "Competition modification", UNAME+" competition has been modified")




def safe_competitions_team_edit_by_name(COMPETITION_NAME,
                                        TEAM,
                                        DOMAIN_NAME,
                                        SUBNET,
                                        GATEWAY,
                                        DNS_SERVER1,
                                        NIC,
                                        CREATED_FLAG,
                                        CREATED_FLAG_C,
                                        CREATED_VMS_FLAG,
                                        CONFIGURED_VMS_FLAG):
    """
    This function never changes COMPETITION_NAME and TEAM.
    :param COMPETITION_NAME:
    :param TEAM:
    :param DOMAIN_NAME:
    :param SUBNET:
    :param GATEWAY:
    :param DNS_SERVER1:
    :param NIC:
    :param CREATED_FLAG:
    :param CREATED_FLAG_C:
    :param CREATED_VMS_FLAG:
    :param CONFIGURED_VMS_FLAG:
    :return:
    """
    q = "UPDATE teams SET " \
        "DOMAIN_NAME= '{}'," \
        "SUBNET= '{}'," \
        "GATEWAY= '{}'," \
        "DNS_SERVER1= '{}'," \
        "NIC= '{}'," \
        "CREATED_FLAG = '{}'," \
        "CREATED_FLAG_C = '{}'," \
        "CREATED_VMS_FLAG = '{}'," \
        "CONFIGURED_VMS_FLAG = '{}' WHERE TEAM = '{}' and COMPETITION_NAME = '{}'".format(
                                                            DOMAIN_NAME,
                                                            SUBNET,
                                                            GATEWAY,
                                                            DNS_SERVER1,
                                                            NIC,
                                                            CREATED_FLAG,
                                                            CREATED_FLAG_C,
                                                            CREATED_VMS_FLAG,
                                                            CONFIGURED_VMS_FLAG,
                                                            TEAM,
                                                            COMPETITION_NAME)
    if debug:
        print("UPDATING "+q, file=sys.stderr)
    mysqlExecute(q)
    addEvent(session['username'], "Team modification", TEAM+" from competition "+COMPETITION_NAME+" has been updated")


def safe_competitions_team_edit(COMPETITION_NAME,TEAM,
                               DOMAIN_NAME,
                               SUBNET,
                               GATEWAY,
                               DNS_SERVER1,
                               CREATED_FLAG,
                               CREATED_FLAG_C,
                               CREATED_VMS_FLAG,
                               CONFIGURED_VMS_FLAG):

    elements = get_all_elements_team(TEAM,COMPETITION_NAME)
    old_ID = elements[0]
    old_COMPETITION_NAME = elements[1]
    old_TEAM = elements[2]
    old_DOMAIN_NAME = elements[3]
    old_SUBNET = elements[4]
    old_GATEWAY = elements[5]
    old_DNS_SERVER1 = elements[6]
    old_NIC = elements[7]
    old_CREATED_FLAG = elements[8]
    old_CREATED_FLAG_C = elements[9]
    old_CREATED_VMS_FLAG = elements[10]
    old_CONFIGURED_VMS_FLAG = elements[11]
    raw_competitions_team_edit(old_COMPETITION_NAME,
                               TEAM,
                               DOMAIN_NAME,
                               SUBNET,
                               GATEWAY,
                               DNS_SERVER1,
                               old_NIC,
                               CREATED_FLAG,
                               CREATED_FLAG_C,
                               CREATED_VMS_FLAG,
                               CONFIGURED_VMS_FLAG,
                               old_ID)



def raw_competitions_team_add(COMPETITION_NAME,
                              TEAM,
                              DOMAIN_NAME,
                              SUBNET,
                              GATEWAY,
                              DNS_SERVER1,
                              NIC,
                              CREATED_FLAG = "0",
                              CREATED_FLAG_C = "0" ,
                              CREATED_VMS_FLAG = "0",
                              CONFIGURED_VMS_FLAG = "0"):
    """

    :param COMPETITION_NAME:
    :param TEAM:
    :param DOMAIN_NAME:
    :param SUBNET:
    :param GATEWAY:
    :param DNS_SERVER1:
    :param NIC:
    :param CREATED_FLAG:
    :param CREATED_FLAG_C:
    :param CREATED_VMS_FLAG:
    :param CONFIGURED_VMS_FLAG:
    :return:

    MYSQL:
    ID INTEGER NOT NULL AUTO_INCREMENT,
	COMPETITION_NAME VARCHAR(50) NOT NULL,  -- A unique name
	TEAM VARCHAR(50) NOT NULL,
	DOMAIN_NAME VARCHAR(50) NOT NULL,
	SUBNET VARCHAR(50) NOT NULL,
	GATEWAY VARCHAR(50) NOT NULL,
	DNS_SERVER1 VARCHAR(50) NOT NULL,
	NIC VARCHAR(50) NOT NULL,
	CREATED_FLAG INTEGER NOT NULL,
	CREATED_FLAG_C INTEGER NOT NULL,
	CREATED_VMS_FLAG INTEGER NOT NULL, -- I don't need it anymore
	CONFIGURED_VMS_FLAG INTEGER NOT NULL,
    """
    q = "INSERT INTO teams(" \
        "COMPETITION_NAME," \
        " TEAM," \
        " DOMAIN_NAME," \
        " SUBNET," \
        " GATEWAY," \
        " DNS_SERVER1," \
        " NIC," \
        " CREATED_FLAG," \
        " CREATED_FLAG_C," \
        " CREATED_VMS_FLAG," \
        " CONFIGURED_VMS_FLAG) VALUES ('{}', '{}','{}','{}', '{}', '{}', '{}','{}','{}','{}','{}')" \
        .format(COMPETITION_NAME,
                TEAM,
                DOMAIN_NAME,
                SUBNET,
                GATEWAY,
                DNS_SERVER1,
                NIC,
                CREATED_FLAG,
                CREATED_FLAG_C,
                CREATED_VMS_FLAG,
                CONFIGURED_VMS_FLAG)
    mysqlExecute(q)
    if debug:
        print("A team has been created: "+str(TEAM), file=sys.stderr)
    addEvent(session['username'], "Team addition", TEAM+" has been added to competition "+COMPETITION_NAME)






def get_competition_data(COMPETITION_NAME):
    data = {}
    teams = get_competition_teams(COMPETITION_NAME)
    for TEAM in teams:
        vms = get_team_vms(TEAM)
        data[TEAM] = vms
        if debug:
            print("Team :"+str(TEAM)+" has "+str(vms), file=sys.stderr)
    return data



def get_competition_teams(COMPETITION_NAME):
    teams = mysqlExecuteAll("select TEAM from teams where COMPETITION_NAME = '{}'".format(COMPETITION_NAME))
    teams = cleanSQLOutputs(teams)
    return teams


def get_team_vms(TEAM):
    vms = mysqlExecuteAll("select VM_NAME from vms where TEAM = '{}'".format(TEAM))
    vms = cleanSQLOutputs(vms)
    return vms


def has_configured_vms(TEAM):
    boo = mysqlExecuteAll("select CONFIGURED_VMS_FLAG from teams where TEAM = '{}'".format(TEAM))
    boo = cleanSQLOutputs(boo)
    if boo == '1' or int(boo) == 1:
        return True
    return False

"""
mysql> select * from teams where TEAM = 'co110';
+----+------------------+-------+-------------+-------------+------------+-------------+-------+--------------+----------------+
| ID | COMPETITION_NAME | TEAM  | DOMAIN_NAME | SUBNET      | GATEWAY    | DNS_SERVER1 | NIC   | CREATED_FLAG | CREATED_FLAG_C |
+----+------------------+-------+-------------+-------------+------------+-------------+-------+--------------+----------------+
|  1 | co11             | co110 | co110.com   | 10.1.1.0/24 | 10.1.1.254 | 1.1.1.1     | go100 |            0 |              0 |
+----+------------------+-------+-------------+-------------+------------+-------------+-------+--------------+----------------+
"""
def get_all_elements_team(COMPETITION_NAME, TEAM):
    elements = mysqlExecuteAll("select * from teams where TEAM = '{}' and COMPETITION_NAME = '{}'".format(TEAM, COMPETITION_NAME))
    elements = cleanSQLOutputs(elements)
    return elements


def get_all_teams_by_competition_name(COMPETITION_NAME):
    elements = mysqlExecuteAll("select * from teams where COMPETITION_NAME = '{}'".format(COMPETITION_NAME))
    #elements = cleanSQLOutputs(elements)
    return elements



def get_all_elements_team_ordered(COMPETITION_NAME, TEAM):
    """
    This function needs to be updated if MYSQL table changed
    TAG: Table-dependent

    Usage:
    ID, COMPETITION_NAME, TEAM, DOMAIN_NAME, SUBNET, GATEWAY, DNS_SERVER1, NIC, CREATED_FLAG, CREATED_FLAG_C, CREATED_VMS_FLAG, CONFIGURED_VMS_FLAG = get_all_elements_team_ordered(TEAM)

    :return:
    """
    all_elements = get_all_elements_team(COMPETITION_NAME, TEAM)
    ID = all_elements[0]
    COMPETITION_NAME = all_elements[1]
    TEAM = all_elements[2]
    DOMAIN_NAME = all_elements[3]
    SUBNET = all_elements[4]
    GATEWAY = all_elements[5]
    DNS_SERVER1 = all_elements[6]
    NIC = all_elements[7]
    CREATED_FLAG = all_elements[8]
    CREATED_FLAG_C = all_elements[9]
    CREATED_VMS_FLAG = all_elements[10]
    CONFIGURED_VMS_FLAG = all_elements[11]
    return ID, COMPETITION_NAME, TEAM, DOMAIN_NAME, SUBNET, GATEWAY, DNS_SERVER1, NIC, CREATED_FLAG, CREATED_FLAG_C, CREATED_VMS_FLAG, CONFIGURED_VMS_FLAG




def get_all_elements_comp(COMPETITION_NAME):
    """

    :param COMPETITION_NAME:
    :return:
    :example of what it can return:
    Two teams, 0 created teams, 2 win vms, 2 linux vms, total vms, ...etc.
    returning :['comp2', '2', '0', '2', '2', '4', '0', '0']
    """
    elements = mysqlExecute("select * from competitions where UNAME = '{}'".format(COMPETITION_NAME))
    elements = cleanSQLOutputs(elements)
    return elements



def update_CONFIGURED_VMS_FLAG(TEAM):
    CONFIGURED_VMS_FLAG = mysqlExecute("select CONFIGURED_VMS_FLAG from teams where TEAM = '{}'".format(TEAM))
    CONFIGURED_VMS_FLAG = cleanSQLOutputs(CONFIGURED_VMS_FLAG)
    CONFIGURED_VMS_FLAG = (int(CONFIGURED_VMS_FLAG) + 1)
    CONFIGURED_VMS_FLAG = str(CONFIGURED_VMS_FLAG)
    mysqlExecute("UPDATE teams SET CONFIGURED_VMS_FLAG= '{}' WHERE TEAM = '{}'"
                 .format(CONFIGURED_VMS_FLAG,TEAM))
    addEvent(session['username'], "CONFIGURED_VMS_FLAG has been updated for team ("+TEAM+")")


def update_CREATED_TEAMS_comp(COMPETITION_NAME):
    CREATED_TEAMS = mysqlExecute("select CREATED_TEAMS from competitions where UNAME = '{}'".format(COMPETITION_NAME))
    CREATED_TEAMS = CREATED_TEAMS.replace("(","").replace(")","").replace(",","")
    CREATED_TEAMS = (int(str(CREATED_TEAMS)) + 1)
    CREATED_TEAMS = str(CREATED_TEAMS)
    mysqlExecute("UPDATE competitions SET CREATED_TEAMS= '{}' WHERE UNAME = '{}'"
                 .format(CREATED_TEAMS,COMPETITION_NAME))
    addEvent(session['username'], "CREATED_TEAMS has been updated for competition ("+COMPETITION_NAME+")")







def next_unedited_vm(COMPETITION_NAME):
    """
    Database schema sensitive --> Which means this will break if you change he database structure for "competitions" table.
    :param COMPETITION_NAME:
    :return:
    """
    if debug:
        debugMessage("Executing next_unedited_vm()")
    teams = get_all_teams_by_competition_name(COMPETITION_NAME)
    return teams



def get_vms_comp(COMPETITION_NAME):
    """
    This function needs to be updated if MYSQL table changed
    TAG: Table-dependent

    :param COMPETITION_NAME:
    :return:
    """
    elements = get_all_elements_comp(COMPETITION_NAME)
    WIN_VMS = elements[4]
    UNIX_VMS = elements[5]
    TOTAL_VMS = elements[6]
    TOTAL_CREATED_VMS = elements[7]
    return WIN_VMS, UNIX_VMS, TOTAL_VMS, TOTAL_CREATED_VMS




def get_next_team_to_configure(COMPETITION_NAME):
    """
    This function needs to be updated if MYSQL table changed
    TAG: Table-dependent

    :param COMPETITION_NAME:
    :return:
    """
    teams = get_competition_teams(COMPETITION_NAME)
    for team in teams:
        # If any team hasn't finished configuring its VMs
        if has_configured_vms(team):
            """
            +----+------------------+-------+-------------+-------------+------------+-------------+-------+--------------+----------------+
            | ID | COMPETITION_NAME | TEAM  | DOMAIN_NAME | SUBNET      | GATEWAY    | DNS_SERVER1 | NIC   | CREATED_FLAG | CREATED_FLAG_C |
            +----+------------------+-------+-------------+-------------+------------+-------------+-------+--------------+----------------+
            |  1 | co11             | co110 | co110.com   | 10.1.1.0/24 | 10.1.1.254 | 1.1.1.1     | go100 |            0 |              0 |
            +----+------------------+-------+-------------+-------------+------------+-------------+-------+--------------+----------------+
            """
            elements = get_all_elements_team(COMPETITION_NAME, team)
            COMPETITION_NAME = elements[1]
            TEAM = elements[2]
            CREATED_TEAMS = elements[3]
            DOMAIN_NAME = elements[4]
            SUBNET = elements[5]
            GATEWAY = elements[6]
            DNS_SERVER1 = elements[7]
            NIC = elements[8]
            return COMPETITION_NAME, TEAM, CREATED_TEAMS, DOMAIN_NAME, DOMAIN_NAME, SUBNET, GATEWAY, DNS_SERVER1, DNS_SERVER1, NIC
    return None, None, None, None, None, None, None, None, None, None





def cleanSQLOutputs(outputs):
    """
    Takes a string
    returns a list of elements
    :param outputs:
    :return:
    """
    outputs = str(outputs)
    return [s.replace('(','').replace(')','').replace('\'','').strip() for s in outputs.split(',') if (len(str(s)) > 1)]



def debugMessage(q):
    """
    :param q: a string
    :return: None
    """
    print("Debug Message :" + str(q), file=sys.stderr)


if __name__ == "__main__":
    app.run(host='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))


