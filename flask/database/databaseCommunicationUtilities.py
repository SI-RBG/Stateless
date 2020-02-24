from database.databaseCommunication import *
from Utilities import *
from config import *
import sys
import pymysql, datetime, requests, shutil, json, time, sys, os, hashlib,random



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


def addEvent(BYUSER_VALUE, EVENT_NAME_VALUE, DESCRIPTIONS_VALUE = ""):
    try:
        BYUSER_VALUE = pymysql.escape_string(BYUSER_VALUE)
        EVENT_NAME_VALUE = pymysql.escape_string(EVENT_NAME_VALUE)
        DESCRIPTIONS_VALUE = pymysql.escape_string(DESCRIPTIONS_VALUE)
        q = "INSERT INTO events(BYUSER, EVENT_NAME, DESCRIPTIONS, CREATION_DATE) VALUES ('{}', '{}', '{}', '{}')".format(str(BYUSER_VALUE), str(EVENT_NAME_VALUE), str(DESCRIPTIONS_VALUE), str(time.strftime('%Y-%m-%d %H:%M:%S')))
        print("Adding an event: "+q, file=sys.stderr)
        mysqlExecute(q)
    except Exception as e:
        print(e, file=sys.stderr)
