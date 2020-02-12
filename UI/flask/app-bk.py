from flask import Flask, flash, jsonify, render_template, request, session, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymysql, datetime, requests, shutil, json, time, sys, os
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Wait
time.sleep(10)


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


# Create users
user2 = 'admin2'
user2hashedpass = generate_password_hash('admin2')
mysqlConnCursor.execute("INSERT INTO users(Username, HashedPass, VideoCount, CreationDate) VALUES ('{}', '{}', 0, '{}')".format(user2, user2hashedpass, datetime.datetime.now().strftime('%Y-%m-%d')))
user1 = 'admin'
user1hashedpass = generate_password_hash('admin')
mysqlConnCursor.execute("INSERT INTO users(Username, HashedPass, VideoCount, CreationDate) VALUES ('{}', '{}', 0, '{}')".format(user1, user1hashedpass, datetime.datetime.now().strftime('%Y-%m-%d')))
mysqlConnCursor.close()
mysqlConn.commit()
mysqlConn.close()


# @app.errorhandler(500)
# def internal_error(error):
#     return home()


@app.route("/")
def home():
    return render_template('login.html')

@app.route("/upload", methods=['GET','POST'])
def upload():
    mysqlConn= pymysql.connect('mysql', 'root', 'root', 'db')
    mysqlConnCursor = mysqlConn.cursor()
    if 'username' in session:
        if request.method == 'POST':
            target = os.path.join(APP_ROOT, "static")
            link = request.form.get('linkupload', None)
            if link != "" and link is not None:
                localfile = link.split('/')[-1]
                destination = "/".join([target, localfile])
                r = requests.get(link, stream=True)
                with open(destination, 'wb') as f:
                    destination = "/".join([target, localfile])
                    shutil.copyfileobj(r.raw, f)
                    mysqlConnCursor.execute("SELECT UID FROM users WHERE Username='{}'".format((session['username'])))
                    UID = mysqlConnCursor.fetchone()
                    mysqlConnCursor.execute("INSERT INTO video(UID, VideoTitle, VideoOwner, VideoURL, DateUploaded) VALUES \
                            ('{}', '{}', '{}', '{}', '{}')".format(UID[0], localfile, \
                                                                   str(destination), session['username'],
                                                                   datetime.datetime.now().strftime('%Y-%m-%d')))
                    mysqlConnCursor.execute("UPDATE users SET VideoCount = VideoCount + \
                            1 WHERE Username = '{}'".format(str(session['username'])))
                    mysqlConn.commit()
                    mysqlConnCursor.close()
                    mysqlConn.close()
                    return render_template('executehtml', username=session['username'])
            else:
                for f in request.files.getlist("file"):
                    filename = f.filename
                    destination = "/".join([target, filename])
                    print("Storing in database . . . " + destination, sys.stderr)
                    f.save(destination)
                    mysqlConnCursor.execute("SELECT UID FROM users WHERE Username='{}'".format((session['username'])))
                    UID = mysqlConnCursor.fetchone()
                    mysqlConnCursor.execute("INSERT INTO video(UID, VideoTitle, VideoURL, VideoOwner, DateUploaded) VALUES \
                            ('{}', '{}', '{}', '{}', '{}')".format(UID[0], filename, \
                                                                   str(destination), session['username'],
                                                                   datetime.datetime.now().strftime('%Y-%m-%d')))
                    mysqlConnCursor.execute("UPDATE users SET VideoCount = VideoCount + \
                            1 WHERE Username = '{}'".format(str(session['username'])))
                    mysqlConn.commit()
                    mysqlConnCursor.close()
                    mysqlConn.close()
                    return render_template('upload.html', username=session['username'])
        mysqlConnCursor.close()
        mysqlConn.close()
        return render_template('upload.html', username=session['username'])
    else:
        mysqlConnCursor.close()
        mysqlConn.close()
    return redirect(url_for('login'))


@app.route("/view")
def view():
    mysqlConn= pymysql.connect('mysql', 'root', 'root', 'db')
    mysqlConnCursor = mysqlConn.cursor()
    if 'username' in session:
        return render_template('view.html', username = session['username'])
    else:
        mysqlConnCursor.close()
        mysqlConn.close()
    return redirect(url_for('login'))


@app.route("/login", methods=['GET','POST'])
@limiter.limit("14400/day;600/hour;1000/minute")
def login():
    try:
        mysqlConn= pymysql.connect('mysql', 'root', 'root', 'db')
        mysqlConnCursor = mysqlConn.cursor()
        if request.method == 'GET':
            return home()
        username = request.form['username']
        password = request.form['password']
        hashedpass = generate_password_hash(password)
        q = "SELECT HashedPass FROM users WHERE Username=" + "'" + str(username) + "'"
        print(q)
        mysqlConnCursor.execute(q)
        userpass = mysqlConnCursor.fetchone()
        q = "SELECT Username FROM users WHERE Username=" + "'" + str(username) + "'"
        print(q)
        mysqlConnCursor.execute(q)
        username = mysqlConnCursor.fetchone()
        username = str(username).replace('(','').replace(')','').replace("'",'').replace(" ",'').replace(",",'')
        mysqlConnCursor.close()
        mysqlConn.close()
        if userpass == None:
            return invalid_user()
        elif check_password_hash(userpass[0], password):
            if "'" in username:
                username = str(username).split("'")[0]
            session['username'] = username
            return redirect(url_for('homepage'))
        return invalid_password()
    except:
        home()



@app.route("/logout", methods=['GET','POST'])
def logout():
    session.pop('username', None)
    flash('You were logged out.')
    return redirect(url_for('login'))


@app.route("/home", methods=['GET','POST'])
def homepage():
    mysqlConn= pymysql.connect('mysql', 'root', 'root', 'db')
    mysqlConnCursor = mysqlConn.cursor()
    if 'username' in session:
        if request.method == 'POST':
            target = os.path.join(APP_ROOT, "static")

            link = request.form.get('linkupload', None)
            if link != "" and link is not None:
                localfile = link.split('/')[-1]
                print(localfile + link, sys.stderr)
                destination = "/".join([target, localfile])
                r = requests.get(link, stream=True)
                with open(destination, 'wb') as f:
                    if not localfile.endswith(".mp4"):
                        flash("Please upload a file with .mp4 extension.")
                        return render_template('home.html', username = session['username'])
                    destination = "/".join([target, localfile])
                    print("Storing in database . . . " + destination, sys.stderr)
                    shutil.copyfileobj(r.raw, f)
                    mysqlConnCursor.execute("SELECT UID FROM users WHERE Username='{}'".format((session['username'])))
                    UID = mysqlConnCursor.fetchone()
                    print(UID, sys.stderr)
                    mysqlConnCursor.execute("INSERT INTO video(UID, VideoTitle, VideoOwner, VideoURL, DateUploaded) VALUES \
                        ('{}', '{}', '{}', '{}', '{}')".format(UID[0], localfile, \
                        str(destination), session['username'], datetime.datetime.now().strftime('%Y-%m-%d')))
                    mysqlConnCursor.execute("UPDATE users SET VideoCount = VideoCount + \
                        1 WHERE Username = '{}'".format(str(session['username'])))
                    mysqlConn.commit()
                    mysqlConnCursor.close()
                    mysqlConn.close()
                    return render_template('home.html', username = session['username'])
            else:
                for f in request.files.getlist("file"):
                    filename = f.filename
                    if not filename.endswith(".mp4"):
                        flash("Please upload a file with .mp4 extension.")
                        return render_template('home.html', username = session['username'])
                    destination = "/".join([target, filename])
                    print("Storing in database . . . " + destination, sys.stderr)
                    f.save(destination)
                    mysqlConnCursor.execute("SELECT UID FROM users WHERE Username='{}'".format((session['username'])))
                    UID = mysqlConnCursor.fetchone()
                    mysqlConnCursor.execute("INSERT INTO video(UID, VideoTitle, VideoURL, VideoOwner, DateUploaded) VALUES \
                        ('{}', '{}', '{}', '{}', '{}')".format(UID[0], filename, \
                        str(destination), session['username'], datetime.datetime.now().strftime('%Y-%m-%d')))
                    mysqlConnCursor.execute("UPDATE users SET VideoCount = VideoCount + \
                        1 WHERE Username = '{}'".format(str(session['username'])))
                    mysqlConn.commit()
                    mysqlConnCursor.close()
                    mysqlConn.close()
                    return render_template('home.html', username = session['username'])
        mysqlConnCursor.close()
        mysqlConn.close()
        return render_template('home.html', username = session['username'])
    else:
        mysqlConnCursor.close()
        mysqlConn.close()
    return redirect(url_for('login'))


@app.route('/getcount', methods=['GET', 'POST'])
def getcount():
    e = 'Any'
    # select VideoCount from users where Username ='admin'
    if 'username' in session:
        try:
            mysqlConn = pymysql.connect('mysql', 'root', 'root', 'db')
            mysqlConnCursor = mysqlConn.cursor()
            if request.method == 'POST':
                username = request.args.post('username')
            if request.method == 'GET':
                username = request.args.get('username')
            mysqlConnCursor.execute("SELECT VideoCount FROM users WHERE Username='{}'".format(username))
            rows = mysqlConnCursor.fetchall()
            row_headers = [x[0] for x in mysqlConnCursor.description]
            json_data = []
            for result in rows:
                json_data.append(dict(zip(row_headers, result)))
            print(json_data, sys.stderr)
            mysqlConnCursor.close()
            mysqlConn.close()
            return jsonify(json_data)
        except Exception as e:
            print("type error: " + str(e))
            e = str(e)
            print(e)
    #return home()


@app.route('/getvideos', methods=['GET', 'POST'])
def getvideos():
    mysqlConn= pymysql.connect('mysql', 'root', 'root', 'db')
    mysqlConnCursor = mysqlConn.cursor()
    if 'username' in session:
        username = request.get_json()
        username = username['username']
        print("username is " + str(username), sys.stderr)
        mysqlConnCursor.execute("SELECT UID FROM users WHERE Username='{}'".format(username))
        UID = mysqlConnCursor.fetchone()
        if "'" in str(UID[0]):
            UID[0] = UID[0].split("'")[0]
        mysqlConnCursor.execute("SELECT * FROM video WHERE UID={}".format(UID[0]))
        rows = mysqlConnCursor.fetchall()
        row_headers=[x[0] for x in mysqlConnCursor.description]
        json_data=[]
        for result in rows:
            json_data.append(dict(zip(row_headers,result)))
        print(json_data, sys.stderr)
        mysqlConnCursor.close()
        mysqlConn.close()
        return jsonify(json_data)
    mysqlConnCursor.close()
    mysqlConn.close()
    return redirect(url_for('login'))


@app.route('/getvideos2', methods=['GET', 'POST'])
def getvideos2():
    mysqlConn= pymysql.connect('mysql', 'root', 'root', 'db')
    mysqlConnCursor = mysqlConn.cursor()
    if 'username' in session:
        username = request.get_json()
        username = username['username']
        mysqlConnCursor.execute("SELECT UID FROM users WHERE Username='{}'".format(username))
        UID = mysqlConnCursor.fetchone()
        mysqlConnCursor.execute("SELECT * FROM video WHERE UID!={}".format(UID[0]))
        rows = mysqlConnCursor.fetchall()
        row_headers=[x[0] for x in mysqlConnCursor.description]
        json_data=[]
        for result in rows:
            json_data.append(dict(zip(row_headers,result)))
        print(json_data, sys.stderr)
        mysqlConnCursor.close()
        mysqlConn.close()
        return jsonify(json_data)
    mysqlConnCursor.close()
    mysqlConn.close()
    return redirect(url_for('login'))



@app.route('/del/<VID>')
def delete(VID):
    mysqlConn= pymysql.connect('mysql', 'root', 'root', 'db')
    mysqlConnCursor = mysqlConn.cursor()
    print(VID, sys.stderr)
    mysqlConnCursor.execute("SELECT VideoOwner FROM video WHERE VID={}".format(VID))
    tempVideoOwner = mysqlConnCursor.fetchone()[0]
    if 'username' in session:
        if session['username'] != tempVideoOwner:
            mysqlConnCursor.close()
            mysqlConn.close()
            return redirect(url_for('homepage'))
        mysqlConnCursor.execute("SELECT VideoTitle FROM video WHERE VID={}".format(VID))
        fileNameTmp = mysqlConnCursor.fetchone()
        fileNameTmp = fileNameTmp[0]
        print(fileNameTmp, sys.stderr)
        if fileNameTmp == '':
            return redirect(url_for('homepage'))
        mysqlConnCursor.execute("SELECT VideoOwner FROM video WHERE VID={}".format(VID))
        tempVideoOwner = mysqlConnCursor.fetchone()[0]
        if session['username'] != tempVideoOwner:
            flash('Cannot delete video uploaded by someone else')
            mysqlConn.commit()
            mysqlConnCursor.close()
            mysqlConn.close()
            return redirect(url_for('homepage'))
        mysqlConnCursor.execute("DELETE FROM video WHERE VID={}".format(VID))
        mysqlConnCursor.execute("SELECT UID FROM users WHERE Username='{}'".format((session['username'])))
        UID = mysqlConnCursor.fetchone()
        mysqlConnCursor.execute("UPDATE users SET VideoCount = VideoCount - \
                    1 WHERE Username = '{}'".format(str(session['username'])))
        mysqlConn.commit()
        command = "rm " + APP_ROOT + "/static/" + fileNameTmp
        os.system(command)
        mysqlConnCursor.close()
        mysqlConn.close()
        return redirect(url_for('homepage'))
    mysqlConnCursor.close()
    mysqlConn.close()
    return redirect(url_for('login'))


@app.route('/vids/<title>')
def videos(title):
    return app.send_static_file(title)




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


if __name__ == "__main__":
    app.run(host='0.0.0.0')

