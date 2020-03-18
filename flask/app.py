import sys, ipaddress, os
from flask import Flask, flash, render_template, request, session, redirect, url_for, abort
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from auth import *
from database.databaseCommunication import *
from database.databaseCommunicationUtilities import *
from config import *
from lib import pyTeamObject, pyCompetitionObject, pyVMObject, Stateless
from packer.PackerCore import *

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


def debugMessage(q):
    """
    :param q: a string
    :return: None
    """
    print("Debug Message :" + str(q), file=sys.stderr)



# def get_all_undeployed_vms_by_competition_name(COMPETITION_NAME):
#     elements = mysqlExecuteAll("select * from wizard_vms where COMPETITION_NAME = '{}'".format(COMPETITION_NAME))
#     #elements = cleanSQLOutputs(elements)
#     return elements



def cleanSQLOutputs(outputs):
    """
    Takes a string
    returns a list of elements
    :param outputs:
    :return:
    """
    outputs = str(outputs)
    return [s.replace('(','').replace(')','').replace('\'','').strip() for s in outputs.split(',') if (len(str(s)) > 1)]


def test():
    mysqlExecuteAll("INSERT INTO templates(TEMPLATES_NAME, OTHER) VALUES ('Ubuntu18-Server', '11')")
    mysqlExecuteAll("INSERT INTO competitions(UNAME, TEAMS, CREATED_TEAMS, WIN_VMS, UNIX_VMS, TOTAL_VMS, TOTAL_CREATED_VMS, CREATED_FLAG, CREATED_FLAG_C) VALUES ('ISTS' , '2', '0' , '2', '2', '4', '0', '0', '0')")
    mysqlExecuteAll("INSERT INTO teams(COMPETITION_NAME, TEAM, DOMAIN_NAME, SUBNET, GATEWAY, DNS_SERVER1, NIC, CREATED_FLAG, CREATED_FLAG_C, CREATED_VMS_FLAG, CONFIGURED_VMS_FLAG) VALUES ('ISTS', 'Tigers1','Tigers1.com','10.1.1.0/24', '10.1.1.254', '1.1.1.1', 'g1','0','0','0','0')")
    mysqlExecuteAll("INSERT INTO teams(COMPETITION_NAME, TEAM, DOMAIN_NAME, SUBNET, GATEWAY, DNS_SERVER1, NIC, CREATED_FLAG, CREATED_FLAG_C, CREATED_VMS_FLAG, CONFIGURED_VMS_FLAG) VALUES ('ISTS', 'Tigers2','Tigers2.com','10.2.2.0/24', '10.2.2.254', '2.2.2.2', 'go2','0','0','0','0')")
    mysqlExecuteAll("INSERT INTO vms(COMPETITION_NAME, TEAM, VM_NAME, TEMPLATE_NAME, CPU, DISK, MEMORY, GUEST_OS_TYPE, CREATED_FLAG, CREATED_FLAG_C) VALUES ('ISTS', 'undefined', 'UServer', 'Ubuntu18-Server', '2','2', '1024', 'ubuntu64Guest', '0', '0')")



def from_MySQL_table_to_pyObject_Competition(pyCompOb, COMPETITION_NAME):
    """
    1 - This is a legendary function.
    2 - It pulls the data from MySQL databases to pythonObject/classes.
    3 - Thx CS1

    :param pyCompOb: a Competition object from pyCompetitionObject
    :param COMPETITION_NAME: a string - the name of the comp in the database.
    :return: the same object "pyCompObject"
    """
    try:
        try:
            comp_sql_elements = get_all_elements_comp2(COMPETITION_NAME)
        except Exception as e:
            if debug:
                debugMessage(e)
                debugMessage("Block #43214234231")

        try:
            """
                Current table structure
                ID INTEGER NOT NULL AUTO_INCREMENT,
                UNAME VARCHAR(50) NOT NULL,  -- HAS TO BE A unique names
                TEAMS INTEGER NOT NULL,
                CREATED_TEAMS INTEGER NOT NULL,
                WIN_VMS INTEGER NOT NULL,
                UNIX_VMS INTEGER NOT NULL,
                TOTAL_VMS INTEGER NOT NULL,
                TOTAL_CREATED_VMS INTEGER NOT NULL,
                CREATED_FLAG INTEGER NOT NULL,
                CREATED_FLAG_C INTEGER NOT NULL,
                """
            COMPETITION_ID = comp_sql_elements[0]
            UNAME = comp_sql_elements[1]
            TEAMS = comp_sql_elements[2]
            CREATED_TEAMS = comp_sql_elements[3]
            WIN_VMS = comp_sql_elements[4]
            UNIX_VMS = comp_sql_elements[5]
            TOTAL_VMS = comp_sql_elements[6]
            TOTAL_CREATED_VMS = comp_sql_elements[7]
            CREATED_FLAG = comp_sql_elements[8]
            CREATED_FLAG_C = comp_sql_elements[9]
            # This is an int
            pyCompOb.set_Competition_Teams(TEAMS)
            # This is an int
            pyCompOb.set_Total_VMs(TOTAL_VMS)
            # This is an int
            pyCompOb.set_Unix_VMs(UNIX_VMS)
            # This is an int
            pyCompOb.set_Win_VMs(WIN_VMS)
        except Exception as e:
            if debug:
                debugMessage(e)
                debugMessage("Block #435532443")

        try:
            # Get all team linked to this competition
            listOfTeams = get_all_teams_by_competition_name(COMPETITION_NAME)
        except Exception as e:
            if debug:
                debugMessage(e)
                debugMessage("Block #546654546")

        try:
            # Get all undeployed vms linked to this competition
            listOfVMs = get_all_undeployed_vms_by_competition_name(COMPETITION_NAME)
        except Exception as e:
            if debug:
                debugMessage(e)
                debugMessage("Block #1324235432")

        for team in listOfTeams:
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
            """
            TEAM_ID = team[0]
            # COMPETITION_NAME = team[1]
            TEAM_NAME = team[2]
            DOMAIN_NAME = team[3]
            SUBNET = team[4]
            GATEWAY = team[5]
            DNS_SERVER1 = team[6]
            NIC = team[7]
            CREATED_FLAG = team[8]
            CREATED_FLAG_C = team[9]
            CREATED_VMS_FLAG = team[10]
            CONFIGURED_VMS_FLAG = team[11]
            # Set
            pyTeamOb = pyTeamObject.Team(COMPETITION_NAME, TEAM_NAME)
            pyTeamOb.set_Competition_Uname(COMPETITION_NAME)
            pyTeamOb.set_Team_ID(TEAM_ID)
            pyTeamOb.set_Team_Uname(TEAM_NAME)
            pyTeamOb.set_DNS1(DNS_SERVER1)
            pyTeamOb.set_Domain_Name(DOMAIN_NAME)
            pyTeamOb.set_Gateway(GATEWAY)
            pyTeamOb.set_NICAKA_PortGropu(NIC)
            pyTeamOb.set_Subnet(SUBNET)

            # Add the team to comp object
            pyCompOb.add_Team(pyTeamOb)

            # try:
            #     pass
            # except Exception as e:
            #     if debug:
            #         debugMessage(e)
            #         debugMessage("Block #5432354543")

            for undeployed_vm in listOfVMs:
                """
                ID INTEGER NOT NULL AUTO_INCREMENT,
                COMPETITION_NAME VARCHAR(50) NOT NULL,
                TEAM VARCHAR(50) NOT NULL,
                VM_NAME VARCHAR(50) NOT NULL,
                CPU VARCHAR(50) NOT NULL,
                MEMORY VARCHAR(50) NOT NULL,
                GUEST_OS_TYPE VARCHAR(50),
                CREATED_FLAG INTEGER NOT NULL,
                CREATED_FLAG_C INTEGER NOT NULL,
                """
                VM_ID = undeployed_vm[0]
                COMPETITION_NAME = undeployed_vm[1]
                # TEAM_NAME = undeployed_vm[2] # We already have it
                VM_NAME = undeployed_vm[3]
                TEMPLATE_NAME = undeployed_vm[4]
                CPU = undeployed_vm[5]
                DISK = undeployed_vm[6]
                MEMORY = undeployed_vm[7]
                GUEST_OS_TYPE = undeployed_vm[8]
                CREATED_FLAG = undeployed_vm[9]
                CREATED_FLAG_C = undeployed_vm[10]
                # Set
                pyVMOb = pyVMObject.VM(COMPETITION_NAME, TEAM_NAME)
                pyVMOb.set_VM_ID(VM_ID)
                pyVMOb.set_VM_Uname(str(TEAM_NAME) + "_" + str(VM_NAME))
                pyVMOb.set_Domain_Name(DOMAIN_NAME)
                pyVMOb.set_CPU(CPU)
                pyVMOb.set_Memory(MEMORY)
                pyVMOb.set_Disk_Space(DISK)
                # pyVMOb.set_ISO_Path()

                # Check if an ip is used in the network of the current team.
                try:
                    ip = SUBNET.split('/')[0]
                    pyTeamOb.add_reservedIP(ip)
                    i = 1
                    while True:
                        ipo = ipaddress.IPv4Address(ip) + i
                        ipo_string = str(ipo)
                        i += 1
                        if (ipo_string in pyTeamOb.get_reservedIP()):
                            continue
                        break
                    pyVMOb.set_IP_Address(ipo_string)
                except Exception as e:
                    if debug:
                        debugMessage("Error #7387687341")
                        debugMessage(e)
                pyVMOb.set_Hostname(str(ipo_string).replace('.', '-'))
                pyVMOb.set_DNS1(DNS_SERVER1)
                pyVMOb.set_Gateway(GATEWAY)
                pyVMOb.set_Subnet(SUBNET)
                pyVMOb.set_Guest_Type(GUEST_OS_TYPE)
                pyVMOb.set_Template_Name(TEMPLATE_NAME)
                # pyVMOb.set_Services()
                # pyVMOb.set_NICAKA_PortGropu(NIC)

                # Add the vm to team object
                pyTeamOb.add_VM(pyVMOb)

        return pyCompOb
    except:
        debugMessage("Error #89238942389423")
        return None



def create_a_competition(pyCompOb):
    """
    This function gets a pyCompetitionObject object which should have all the information needed to deploy a comp.

    :param pyCompOb:
    :return:
    """
    debugMessage("WORKKKKKKKK")

    vcenter_ip_env = os.environ.get('VCENTER_IP')
    vcenter_user_env = os.environ.get('VCENTER_USER')
    vcenter_password_env = os.environ.get('VCENTER_PASSWORD')
    debugMessage("vcenter_ip_env:"+vcenter_ip_env)
    debugMessage("vcenter_user_env:" + vcenter_user_env)


    # Create StatelessObj
    so = Stateless.StatelessObj(vcenter_ip_env, vcenter_user_env, vcenter_password_env)
    # Set the changeable variables.
    so.set_datacenter("Datacenter")
    so.set_datastore("datastore3")
    so.set_cluster("CPTCCluster")
    so.set_RP("DevRP")

    # Login
    si = so.login()
    content = so.retrive_content(si)

    # Set the root path for pyCompOb
    rootpath = pyCompOb.Competition_Uname_to_string()+"/"


    # Get a list of pyTeamObjs
    listOfTeams = pyCompOb.get_Teams()
    if debug:
        debugMessage("Getting a list of teams that has a length of "+str(len(listOfTeams)))


    for teamObj in listOfTeams:
        teamUName = teamObj.Team_Uname_to_string()

        # Get a list of pyVMObjs
        VMs = teamObj.get_VMs()
        if debug:
            debugMessage("Getting a list of VMs, length of " + str(len(listOfTeams)))

        for vmObj in VMs:
            if vmObj.Template_Name_is_empty():
                pass
            # If it uses a template.
            else:
                #Competition_Uname = vmObj.get_Competition_Uname()
                Team_Uname = vmObj.Team_Uname_to_string()
                VM_Uname = vmObj.VM_Uname_to_string()
                Template_Name = vmObj.Template_Name_to_string()
                IP_Address = vmObj.IP_Address_to_string()
                Hostname = vmObj.Hostname_to_string()
                CPU = vmObj.CPU_to_string()
                Disk_Space = vmObj.Disk_Space_to_string()
                Memory = vmObj.Memory_to_string()
                Guest_Type = vmObj.get_Guest_Type()

                # Set the current path
                currentPath = rootpath+Team_Uname+"/"

                # Get last dir
                lastSubPath = Team_Uname

                # Create a folder
                if (so.test_create_folder(content, currentPath)):
                    if debug:
                        debugMessage(currentPath+" folder has been created")
                else:
                    if debug:
                        debugMessage(currentPath + " folder has NOT been created.\nError #79813923")

                # Clone a vm based on the given information.
                try:
                    code = so.clone_vm(content, VM_Uname, Template_Name, lastSubPath, "", "", "", "")
                    if debug:
                        if code == 1:
                            debugMessage("Kind of good so far!")
                        if code == 0:
                            debugMessage("Failed ")
                        if code == -1:
                            debugMessage("One of the inputs is None")
                except Exception as e:
                    if debug:
                        debugMessage(str(e)+"\nError #892378")

    so.logout(si)




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


@app.route("/create_templates", methods=['GET','POST'])
def create_templates():
    if 'username' in session:
        data = mysqlExecuteAll("SELECT * FROM templates")
        if debug:
            print("The data object: "+ str(data),file=sys.stderr)
        return render_template('templates.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()



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

                #CREATED_TEAMS = pymysql.escape_string(request.values.get('CREATED_TEAMS'))
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
                #raw_competitions_edit(UNAME, TEAMS, CREATED_TEAMS, WIN_VMS, UNIX_VMS, TOTAL_VMS,"0", ID)

                # First edit teams' names
                OLD_UNAME = mysqlExecute("select UNAME from competitions where id = '{}'".format(ID))
                OLD_UNAME = cleanSQLOutputs(OLD_UNAME)[0]
                mysqlExecute("UPDATE teams SET COMPETITION_NAME = '{}'  WHERE COMPETITION_NAME  = '{}'".format(UNAME,OLD_UNAME))
                # edit vms' names
                mysqlExecute("UPDATE vms SET COMPETITION_NAME = '{}'  WHERE COMPETITION_NAME  = '{}'".format(UNAME, OLD_UNAME))


                simple_competitions_edit(session, UNAME, TEAMS, WIN_VMS, UNIX_VMS, TOTAL_VMS, ID)


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
                raw_competitions_add(session, UNAME, TEAMS, "0", WIN_VMS, UNIX_VMS, TOTAL_VMS, TOTAL_CREATED_VMS, CREATED_FLAG, CREATED_FLAG_C)

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

                OLD_TEAM = mysqlExecute("select TEAM from teams where id = '{}'".format(ID))
                OLD_TEAM = cleanSQLOutputs(OLD_TEAM)[0]

                # Start by editing the vms to match the new name.
                mysqlExecute("UPDATE vms SET TEAM = '{}'  WHERE TEAM  = '{}'".format(TEAM, OLD_TEAM))

                # Create a competitions object and make an event
                simple_competitions_team_edit(COMPETITION_NAME,
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
                COMPS = mysqlExecuteAll("SELECT * FROM competitions")
                return render_template('competitions_team_edit.html', output_data = data, COMPS = COMPS, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                # TODO Add a error.html page where it just redirects to a url_for('url') like done.html
                data = mysqlExecuteAll("SELECT * FROM teams")
                return render_template('competitions_team.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()


def simple_competitions_team_edit(COMPETITION_NAME,
                                   TEAM,
                                   DOMAIN_NAME,
                                   SUBNET,
                                   GATEWAY,
                                   DNS_SERVER1,
                                   NIC,
                                   ID):
        q = "UPDATE teams SET " \
            "COMPETITION_NAME = '{}'," \
            "TEAM= '{}'," \
            "DOMAIN_NAME= '{}'," \
            "SUBNET= '{}'," \
            "GATEWAY= '{}'," \
            "DNS_SERVER1= '{}'," \
            "NIC= '{}' WHERE ID = '{}'".format(COMPETITION_NAME,
                                                                TEAM,
                                                                DOMAIN_NAME,
                                                                SUBNET,
                                                                GATEWAY,
                                                                DNS_SERVER1,
                                                                NIC,
                                                                ID)

        if debug:
            debugMessage("UPDATING " + q)
        mysqlExecute(q)
        addEvent(session['username'], "Team modification",
                 TEAM + " from competition " + COMPETITION_NAME + " has been updated")



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
                raw_competitions_team_add(session,
                                          COMPETITION_NAME,
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
            COMPS = mysqlExecuteAll("SELECT * FROM competitions")
            return render_template('competitions_team_add.html', username = session['username'], COMPS = COMPS, templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()


# VMs section

"""

"""
def raw_competitions_vm_edit(COMPETITION_NAME, TEAM, VM_NAME, CPU, DISK, MEMORY, GUEST_OS_TYPE, CREATED_FLAG, CREATED_FLAG_C, ID):
    mysqlExecute("UPDATE vms SET CPU = '{}', DISK = '{}', MEMORY = '{}', CREATED_FLAG = '{}', CREATED_FLAG_C = '{}' WHERE ID = '{}'".format(CPU, DISK, MEMORY, CREATED_FLAG, CREATED_FLAG_C, ID))
    addEvent(session['username'], "VM modification", VM_NAME+" VM for team "+TEAM+" in competition "+COMPETITION_NAME+" has been modified")



def raw_competitions_vm_add(COMPETITION_NAME, TEAM, VM_NAME,TEMPLATE_NAME, CPU, DISK, MEMORY, GUEST_OS_TYPE, CREATED_FLAG, CREATED_FLAG_C):
    mysqlExecute("INSERT INTO vms("
                 "COMPETITION_NAME,"
                 " TEAM,"
                 " VM_NAME,"
                 " TEMPLATE_NAME,"
                 " CPU,"
                 " DISK,"
                 " MEMORY,"
                 " GUEST_OS_TYPE,"
                 " CREATED_FLAG,"
                 " CREATED_FLAG_C) VALUES ('{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}')"
                 .format(
                        COMPETITION_NAME,
                        TEAM,
                        VM_NAME,
                        TEMPLATE_NAME,
                        CPU,
                        DISK,
                        MEMORY,
                        GUEST_OS_TYPE,
                        CREATED_FLAG,
                        CREATED_FLAG_C))
    if debug:
        print("A vm has been created "+str(VM_NAME), file=sys.stderr)
    addEvent(session['username'], "VM addition",VM_NAME+" VM has been created for team "+TEAM+" in competition "+COMPETITION_NAME)



def raw_competitions_wizard_vm_add(COMPETITION_NAME, TEAM, VM_NAME, TEMPLATE_NAME, CPU, DISK, MEMORY, GUEST_OS_TYPE, CREATED_FLAG, CREATED_FLAG_C):
    mysqlExecute("INSERT INTO wizard_vms(COMPETITION_NAME,"
                 " TEAM,"
                 " VM_NAME,"
                 " TEMPLATE_NAME,"
                 " CPU,"
                 " DISK,"
                 " MEMORY,"
                 " GUEST_OS_TYPE,"
                 " CREATED_FLAG,"
                 " CREATED_FLAG_C) VALUES ('{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}')"
                 .format(COMPETITION_NAME,
                         TEAM,
                         VM_NAME,
                         TEMPLATE_NAME,
                         CPU,
                         DISK,
                         MEMORY,
                         GUEST_OS_TYPE,
                         CREATED_FLAG,
                         CREATED_FLAG_C))
    if debug:
        debugMessage("A generic vm has been created "+str(VM_NAME)+" raw_competitions_vm_add() ")
    addEvent(session['username'], "Generic VM addition",VM_NAME+" VM has been created for competition "+COMPETITION_NAME+" read to be deployed")



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
                DISK = pymysql.escape_string(request.values.get('DISK'))
                MEMORY = pymysql.escape_string(request.values.get('MEMORY'))
                GUEST_OS_TYPE = pymysql.escape_string(request.values.get('GUEST_OS_TYPE'))
                CREATED_FLAG = CREATED_FLAG_C = "0"

                # Edit a comp and make an event
                raw_competitions_vm_edit(COMPETITION_NAME, TEAM, VM_NAME, CPU, DISK, MEMORY, GUEST_OS_TYPE, CREATED_FLAG, CREATED_FLAG_C, ID)

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
                if debug:
                    debugMessage("Getting COMPETITION_NAME on competitions_vm_add()")
                COMPETITION_NAME = pymysql.escape_string(request.values.get('COMPETITION_NAME'))
                if COMPETITION_NAME == None:
                    if debug:
                        error_message = "Missing COMPETITION_NAME"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                if debug:
                    debugMessage("Getting TEAM on competitions_vm_add()")
                TEAM = pymysql.escape_string(request.values.get('TEAM'))
                if TEAM == None:
                    if debug:
                        error_message = "Missing TEAM"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                if debug:
                    debugMessage("Getting VM_NAME on competitions_vm_add()")
                VM_NAME = pymysql.escape_string(request.values.get('VM_NAME'))
                if VM_NAME == None:
                    if debug:
                        error_message = "Missing VM_NAME"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                if debug:
                    debugMessage("Getting CPU on competitions_vm_add()")
                CPU = pymysql.escape_string(request.values.get('CPU'))
                if CPU == None:
                    if debug:
                        error_message = "Missing CPU"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                if debug:
                    debugMessage("Getting DISK on competitions_vm_add()")
                DISK = pymysql.escape_string(request.values.get('DISK'))
                if CPU == None:
                    if debug:
                        error_message = "Missing DISK"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                if debug:
                    debugMessage("Getting TEMPLATE_NAME on competitions_vm_add()")
                TEMPLATE_NAME = pymysql.escape_string(request.values.get('TEMPLATE_NAME'))
                if TEMPLATE_NAME == None:
                    if debug:
                        error_message = "Missing TEMPLATE_NAME"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                if debug:
                    debugMessage("Getting MEMORY on competitions_vm_add()")
                MEMORY = pymysql.escape_string(request.values.get('MEMORY'))
                if MEMORY == None:
                    if debug:
                        error_message = "Missing MEMORY"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                if debug:
                    debugMessage("Getting GUEST_OS_TYPE on competitions_vm_add()")
                GUEST_OS_TYPE = pymysql.escape_string(request.values.get('GUEST_OS_TYPE'))
                if GUEST_OS_TYPE == None:
                    if debug:
                        error_message = "Missing GUEST_OS_TYPE"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('competitions_team'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())


                CREATED_FLAG = CREATED_FLAG_C = "0"

                # Create a vm and make an event
                #raw_competitions_vm_add(COMPETITION_NAME, TEAM, VM_NAME, CPU, MEMORY, GUEST_OS_TYPE, CREATED_FLAG, CREATED_FLAG_C)
                raw_competitions_vm_add(COMPETITION_NAME, "undefined", VM_NAME, TEMPLATE_NAME, CPU, DISK, MEMORY, GUEST_OS_TYPE, CREATED_FLAG,
                                        CREATED_FLAG_C)

                return render_template('done.html', username = session['username'], url = url_for('competitions_vm'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except Exception as ex:
                if debug:
                    debugMessage("Error: "+str(ex))
                    debugMessage("Error #873216812")
        COMPS = mysqlExecuteAll("SELECT * FROM competitions")
        TEAMS = mysqlExecuteAll("SELECT * FROM teams")
        TEMPLATES = mysqlExecuteAll("SELECT * FROM templates")
        return render_template('competitions_vm_add.html', username = session['username'], TEMPLATES = TEMPLATES, COMPS = COMPS, TEAMS = TEAMS, templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()




@app.route("/competitions_deployment", methods=['GET','POST'])
def competitions_deployment():
    if 'username' in session:
        try:
            """
            Get all undeployed competitions which are known by CREATED_FLAG 
            if CREATED_FLAG = 1 that means it has been deployed.
            if CREATED_FLAG = 0 that means it has NOT been deployed.
            """
            try:
                vmsObjects =[]
                ToBeSentList = []
                # Get Comp ID
                COMP_ID = pymysql.escape_string(str(request.args.get('COMP_ID')))
                debugMessage("competitions_deployment() "+str(COMP_ID)+" length: "+str(len(COMP_ID)))

                # If it's not a number
                if type(int(COMP_ID)) != int:
                    undeployed_comps = mysqlExecuteAll("select * from competitions where CREATED_FLAG = 0")

                    return render_template('competitions_deployment.html', output_data=undeployed_comps,
                                           username=session['username'],
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                # Start looking for all the variables for this comp and add them to a comp object

                # Get COMPETITION_NAME by ID submitted
                COMPETITION_NAME = mysqlExecute("select UNAME from competitions where id = '{}'".format(COMP_ID))
                COMPETITION_NAME = cleanSQLOutputs(COMPETITION_NAME)[0]

                # Create a pyCompetitionObject object
                pyCompOb = pyCompetitionObject.Competition(COMPETITION_NAME)

                try:
                    # Fill the object
                    pyCompOb = from_MySQL_table_to_pyObject_Competition(pyCompOb, COMPETITION_NAME)
                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #32423412312")

                try:
                    listOfTeams = pyCompOb.get_Teams()
                    listOfListofvmsObjects = [team.get_VMs() for team in listOfTeams]
                    ToBeSentList = []
                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #3451453")

                try:
                    for vmsOfATeam in listOfListofvmsObjects:
                    # https://dockertester.mohad.red:5000/competitions_deployment?COMP_ID=1
                        for vm in vmsOfATeam:
                            debugMessage(str(vm.get_VM_ID()) + " "+str(vm.get_VM_Uname()))
                            ToBeSentList.append([vm.VM_ID_to_string(),
                                                 vm.get_Competition_Uname(),
                                                 vm.Team_Uname_to_string(),
                                                 vm.VM_Uname_to_string(),
                                                 vm.Template_Name_to_string(),
                                                 vm.IP_Address_to_string(),
                                                 vm.Hostname_to_string(),
                                                 vm.CPU_to_string(),
                                                 vm.Disk_Space_to_string(),
                                                 vm.Memory_to_string(),
                                                 vm.get_Guest_Type()
                                                 ])
                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #1324421354")
                if debug:
                    debugMessage("Redirecting to competitions_deployment_1.html")
                    debugMessage("Passing "+str(COMP_ID))
                return render_template('competitions_deployment_1.html', output_data=ToBeSentList, COMP_ID = COMP_ID, username=session['username'])
            except Exception as e:
                if debug:
                    debugMessage(e)
                debugMessage("No COMP_ID")

            # IF get GET
            undeployed_comps = mysqlExecuteAll("select * from competitions where CREATED_FLAG = 0")

            return render_template('competitions_deployment.html', output_data=undeployed_comps,
                                   username=session['username'],
                                   templates_length=getTemplatesLength(), tasks_length=getEventsLength())
        except:
            debugMessage("Error #98239823")
    return root()



@app.route("/competitions_deployment_post", methods=['GET','POST'])
def competitions_deployment_post():
    if 'username' in session:
        try:
            pass
            if request.method == 'POST':
                try:
                    COMP_ID_V = request.form.get('COMPID')
                    if COMP_ID_V == None:
                        debugMessage("Error #98289293")
                        return root()
                    COMP_ID = pymysql.escape_string(str(COMP_ID_V))

                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #3234675665")

                # Get COMPETITION_NAME by ID submitted
                COMPETITION_NAME = mysqlExecute("select UNAME from competitions where id = '{}'".format(COMP_ID))
                COMPETITION_NAME = cleanSQLOutputs(COMPETITION_NAME)[0]

                # Create a pyCompetitionObject object
                pyCompOb = pyCompetitionObject.Competition(COMPETITION_NAME)

                try:
                    # Fill the object
                    pyCompOb = from_MySQL_table_to_pyObject_Competition(pyCompOb, COMPETITION_NAME)
                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #8239732981")

                debugMessage("create_a_competition(pyCompOb) TIME!!!!!")
                #
                # TODO   - Add more teste here!!!!
                create_a_competition(pyCompOb)
        except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Error #345154323")
    return root()



@app.route("/something", methods=['GET'])
def something():
    vcenter_ip_env = os.environ.get('VCENTER_IP')
    vcenter_user_env = os.environ.get('VCENTER_USER')
    vcenter_password_env = os.environ.get('VCENTER_PASSWORD')
    debugMessage("vcenter_ip_env:"+vcenter_ip_env)
    debugMessage("vcenter_user_env:" + vcenter_user_env)


    # Create StatelessObj
    so = Stateless.StatelessObj(vcenter_ip_env, vcenter_user_env, vcenter_password_env)
    # Set the changeable variables.
    so.set_datacenter("Datacenter")
    so.set_datastore("datastore")
    so.set_cluster("CPTCCluster")
    so.set_RP("DevRP")

    # Login
    si = so.login()
    content = so.retrive_content(si)


    currentPath = "test100/test200"

    # Create a folder
    if (so.test_create_folder(content, currentPath)):
        if debug:
            debugMessage(currentPath + " folder has been created")
    else:
        if debug:
            debugMessage(currentPath + " folder has NOT been created.\nError #79813923")

    # Get last dir
    lastSubPath = currentPath.split('/')[-1]

    try:
        code = so.clone_vm(content, "US234", "Ubuntu18-Server", "test200", "", "", "","")
        if debug:
            if code == 1:
                debugMessage("Kind of good so far!")
            if code == 0:
                debugMessage("Failed ")
            if code == -1:
                debugMessage("One of the inputs is None")
    except Exception as e:
        if debug:
           debugMessage(str(e)+"\nError #892378")
    return "GOOD! "+str(code)





@app.route("/guest_type_templates", methods=['GET'])
def guest_type_templates():
    if 'username' in session:
        data = mysqlExecuteAll("SELECT * FROM gt_templates")
        return render_template('gt_templates.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()




@app.route("/guest_type_templates_edit", methods=['GET','POST'])
def guest_type_templates_edit():
    if 'username' in session:
        if request.method == 'POST':
            try:
                error_message = ""
                ID = pymysql.escape_string(request.values.get('ID'))



                GUEST_TYPE = pymysql.escape_string(request.values.get('GUEST_TYPE'))
                if len(GUEST_TYPE) < 1:
                    if debug:
                        error_message = "Missing GUEST_TYPE"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('guest_type_templates'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())


                ISO_PATH = pymysql.escape_string(request.values.get('ISO_PATH'))
                if len(ISO_PATH) < 1:
                    if debug:
                        error_message = "Missing ISO_PATH"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('guest_type_templates'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())


                # Edit a gt_templates
                # TODO make an event
                mysqlExecute("UPDATE gt_templates SET "
                             " GUEST_TYPE = '{}',"
                             " ISO_PATH = '{}' WHERE ID = '{}'"
                             .format(GUEST_TYPE,
                                     ISO_PATH,
                                     ID))


                return render_template('done.html', url = url_for('guest_type_templates'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                debugMessage("Error #094290023")
        else:
            try:
                ID = pymysql.escape_string(request.args.get('ID'))
                data = mysqlExecuteAll("SELECT * FROM gt_templates WHERE ID={}".format(ID))
                return render_template('gt_templates_edit.html', output_data = data, username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                debugMessage("Error #023132873")
    return root()




@app.route("/guest_type_templates_add", methods=['GET','POST'])
def guest_type_templates_add():
    if 'username' in session:
        if request.method == 'POST':
            try:

                GUEST_TYPE = pymysql.escape_string(request.values.get('GUEST_TYPE'))
                if len(GUEST_TYPE) < 1:
                    if debug:
                        error_message = "Missing GUEST_TYPE"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('guest_type_templates'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())

                ISO_PATH = pymysql.escape_string(request.values.get('ISO_PATH'))
                if len(ISO_PATH) < 1:
                    if debug:
                        error_message = "Missing ISO_PATH"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url = url_for('guest_type_templates'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())


                # Create a gt template.
                # TODO make an event.
                mysqlExecute("INSERT INTO gt_templates("
                             "GUEST_TYPE, "
                             "ISO_PATH) VALUES ('{}' , '{}')"
                    .format(
                    GUEST_TYPE,
                    ISO_PATH))

                return render_template('done.html', url = url_for('guest_type_templates'), templates_length = getTemplatesLength(), tasks_length = getEventsLength())
            except:
                pass
        return render_template('gt_templates_add.html', username = session['username'], templates_length = getTemplatesLength(), tasks_length = getEventsLength())
    return root()



@app.route("/competitions_deployment_packer", methods=['GET','POST'])
def competitions_deployment_packer():
    if 'username' in session:
        try:
            """
            
            """
            try:
                vmsObjects =[]
                ToBeSentList = []
                # Get Comp ID
                COMP_ID = pymysql.escape_string(str(request.args.get('COMP_ID')))
                debugMessage("competitions_deployment_packer() "+str(COMP_ID)+" length: "+str(len(COMP_ID)))

                # If it's not a number
                if type(int(COMP_ID)) != int:
                    undeployed_comps = mysqlExecuteAll("select * from competitions where CREATED_FLAG = 0")

                    return render_template('competitions_deployment_packer.html', output_data=undeployed_comps,
                                           username=session['username'],
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                # Start looking for all the variables for this comp and add them to a comp object

                # Get COMPETITION_NAME by ID submitted
                COMPETITION_NAME = mysqlExecute("select UNAME from competitions where id = '{}'".format(COMP_ID))
                COMPETITION_NAME = cleanSQLOutputs(COMPETITION_NAME)[0]

                # Create a pyCompetitionObject object
                pyCompOb = pyCompetitionObject.Competition(COMPETITION_NAME)

                try:
                    # Fill the object
                    pyCompOb = from_MySQL_table_to_pyObject_Competition(pyCompOb, COMPETITION_NAME)
                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #32423412312")

                try:
                    listOfTeams = pyCompOb.get_Teams()
                    listOfListofvmsObjects = [team.get_VMs() for team in listOfTeams]
                    ToBeSentList = []
                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #3451453")

                try:
                    for vmsOfATeam in listOfListofvmsObjects:
                    # https://dockertester.mohad.red:5000/competitions_deployment?COMP_ID=1
                        for vm in vmsOfATeam:
                            debugMessage(str(vm.get_VM_ID()) + " "+str(vm.get_VM_Uname()))
                            ToBeSentList.append([vm.VM_ID_to_string(),
                                                 vm.get_Competition_Uname(),
                                                 vm.Team_Uname_to_string(),
                                                 vm.VM_Uname_to_string(),
                                                 vm.Template_Name_to_string(),
                                                 vm.IP_Address_to_string(),
                                                 vm.Hostname_to_string(),
                                                 vm.CPU_to_string(),
                                                 vm.Disk_Space_to_string(),
                                                 vm.Memory_to_string(),
                                                 vm.get_Guest_Type()
                                                 ])
                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #1324421354")
                if debug:
                    debugMessage("Redirecting to competitions_deployment_packer_1.html")
                    debugMessage("Passing "+str(COMP_ID))
                return render_template('competitions_deployment_packer_1.html', output_data=ToBeSentList, COMP_ID = COMP_ID, username=session['username'])
            except Exception as e:
                if debug:
                    debugMessage(e)
                debugMessage("No COMP_ID")

            # IF get GET
            undeployed_comps = mysqlExecuteAll("select * from competitions where CREATED_FLAG = 0")

            return render_template('competitions_deployment_packer.html', output_data=undeployed_comps,
                                   username=session['username'],
                                   templates_length=getTemplatesLength(), tasks_length=getEventsLength())
        except:
            debugMessage("Error #98239823")
    return root()



@app.route("/competitions_deployment_packer_post", methods=['GET','POST'])
def competitions_deployment_packer_post():
    if 'username' in session:
        try:
            pass
            if request.method == 'POST':
                try:
                    COMP_ID_V = request.form.get('COMPID')
                    if COMP_ID_V == None:
                        debugMessage("Error #98289293")
                        return root()
                    COMP_ID = pymysql.escape_string(str(COMP_ID_V))

                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #3234675665")

                # Get COMPETITION_NAME by ID submitted
                COMPETITION_NAME = mysqlExecute("select UNAME from competitions where id = '{}'".format(COMP_ID))
                COMPETITION_NAME = cleanSQLOutputs(COMPETITION_NAME)[0]

                # Create a pyCompetitionObject object
                pyCompOb = pyCompetitionObject.Competition(COMPETITION_NAME)

                try:
                    # Fill the object
                    pyCompOb = from_MySQL_table_to_pyObject_Competition(pyCompOb, COMPETITION_NAME)
                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #8239732981")

                # Deploy
                pyCompOb.set_datastore("datastore2")
                pyCompOb.set_ESXI_HOST("mikasa.mohammed.red")


                debugMessage("Executing PackerCoreDeploy()")
                # Deploy
                try:
                    PackerCoreDeploy(pyCompOb)
                except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Block #834431181")


        except Exception as e:
                    if debug:
                        debugMessage(e)
                        debugMessage("Error #345154323")
    return root()





def create_a_competition_gt(pyCompOb):
    """
    This function gets a pyCompetitionObject object which should have all the information needed to deploy a comp.

    :param pyCompOb:
    :return:
    """
    pass





if __name__ == "__main__":
    app.run(host='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))


