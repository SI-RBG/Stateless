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
