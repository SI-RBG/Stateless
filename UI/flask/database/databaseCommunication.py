from database.databaseCommunicationUtilities import *
from Utilities import *
from config import *
import sys


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


def simple_competitions_edit(UNAME, TEAMS, WIN_VMS, UNIX_VMS, TOTAL_VMS, ID):
    """

    :param UNAME:
    :param TEAMS:
    :param WIN_VMS:
    :param UNIX_VMS:
    :param TOTAL_VMS:
    :param ID:
    :return:
    """
    mysqlExecute("UPDATE competitions SET "
                 " UNAME = '{}',"
                 " TEAMS= '{}',"
                 " WIN_VMS= '{}',"
                 " UNIX_VMS= '{}',"
                 " TOTAL_VMS= '{}'"
                 " WHERE ID = '{}'"
                 .format(UNAME,
                         TEAMS,
                         WIN_VMS,
                         UNIX_VMS,
                         TOTAL_VMS,
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

def get_all_elements_team2(COMPETITION_NAME, TEAM):
    elements = mysqlExecuteAll("select * from teams where TEAM = '{}' and COMPETITION_NAME = '{}'".format(TEAM, COMPETITION_NAME))
    elements = cleanSQLOutputs(elements)
    return elements


def get_all_teams_by_competition_name(COMPETITION_NAME):
    elements = mysqlExecuteAll("select * from teams where COMPETITION_NAME = '{}'".format(COMPETITION_NAME))
    #elements = cleanSQLOutputs(elements)
    return elements


def get_all_vms_by_competition_name(COMPETITION_NAME):
    elements = mysqlExecuteAll("select * from vms where COMPETITION_NAME = '{}' ".format(COMPETITION_NAME))
    #elements = cleanSQLOutputs(elements)
    return elements

def get_all_undeployed_vms_by_competition_name(COMPETITION_NAME):
    elements = mysqlExecuteAll("select * from vms where COMPETITION_NAME = '{}' and TEAM = 'Undefined' ".format(COMPETITION_NAME))
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


def get_all_elements_comp2(COMPETITION_NAME):
    """

    :param COMPETITION_NAME:
    :return:
    :example of what it can return:
    Two teams, 0 created teams, 2 win vms, 2 linux vms, total vms, ...etc.
    returning :['comp2', '2', '0', '2', '2', '4', '0', '0']
    """
    elements = mysqlExecute("select * from competitions where UNAME = '{}'".format(COMPETITION_NAME))
    return elements




def update_CONFIGURED_VMS_FLAG(TEAM):
    """
    This function updates "CONFIGURED_VMS_FLAG" in the mysql database for a "TEAM"
    It also adds/logs an event.


    TODO - Needs more testing

    :param TEAM:
    :return:
    """
    CONFIGURED_VMS_FLAG = mysqlExecute("select CONFIGURED_VMS_FLAG from teams where TEAM = '{}'".format(TEAM))
    CONFIGURED_VMS_FLAG = cleanSQLOutputs(CONFIGURED_VMS_FLAG)
    CONFIGURED_VMS_FLAG = (int(CONFIGURED_VMS_FLAG) + 1)
    CONFIGURED_VMS_FLAG = str(CONFIGURED_VMS_FLAG)
    mysqlExecute("UPDATE teams SET CONFIGURED_VMS_FLAG= '{}' WHERE TEAM = '{}'"
                 .format(CONFIGURED_VMS_FLAG,TEAM))
    addEvent(session['username'], "CONFIGURED_VMS_FLAG has been updated for team ("+TEAM+")")



def update_CREATED_VMS_FLAG_comp_team(COMPETITION_NAME,TEAM):
    """
    This function updates "CREATED_VMS_FLAG" in the mysql database for a "TEAM"
    It also adds/logs an event.


    :param TEAM:
    :return:
    """
    CREATED_VMS_FLAG = mysqlExecute("select CREATED_VMS_FLAG from teams where TEAM = '{}' and COMPETITION_NAME = '{}'".format(TEAM,COMPETITION_NAME))
    CREATED_VMS_FLAG = CREATED_VMS_FLAG.replace("(","").replace(")","").replace(",","")
    CREATED_VMS_FLAG = (int(str(CREATED_VMS_FLAG)) + 1)
    CREATED_VMS_FLAG = str(CREATED_VMS_FLAG)
    mysqlExecute("UPDATE teams SET CREATED_VMS_FLAG= '{}' WHERE TEAM = '{}'"
                 .format(CREATED_VMS_FLAG,TEAM))
    addEvent(session['username'], "CREATED_VMS_FLAG has been updated for team ("+TEAM+")")




def update_CREATED_TEAMS_comp(COMPETITION_NAME):
    """
    This function updates "CREATED_TEAMS" in the mysql database for a "COMPETITION_NAME"
    It also adds/logs an event.


    :param COMPETITION_NAME:
    :return:
    """
    CREATED_TEAMS = mysqlExecute("select CREATED_TEAMS from competitions where UNAME = '{}'".format(COMPETITION_NAME))
    CREATED_TEAMS = CREATED_TEAMS.replace("(","").replace(")","").replace(",","")
    CREATED_TEAMS = (int(str(CREATED_TEAMS)) + 1)
    CREATED_TEAMS = str(CREATED_TEAMS)
    mysqlExecute("UPDATE competitions SET CREATED_TEAMS= '{}' WHERE UNAME = '{}'"
                 .format(CREATED_TEAMS,COMPETITION_NAME))
    addEvent(session['username'], "CREATED_TEAMS has been updated for competition ("+COMPETITION_NAME+")")



def update_TOTAL_CREATED_VMS_comp(COMPETITION_NAME):
    """
    This function updates "TOTAL_CREATED_VMS" in the mysql database for a "COMPETITION_NAME"
    It also adds/logs an event.


    :param COMPETITION_NAME:
    :return:
    """
    TOTAL_CREATED_VMS = mysqlExecute("select TOTAL_CREATED_VMS from competitions where UNAME = '{}'".format(COMPETITION_NAME))
    TOTAL_CREATED_VMS = TOTAL_CREATED_VMS.replace("(","").replace(")","").replace(",","")
    TOTAL_CREATED_VMS = (int(str(TOTAL_CREATED_VMS)) + 1)
    TOTAL_CREATED_VMS = str(TOTAL_CREATED_VMS)
    mysqlExecute("UPDATE competitions SET TOTAL_CREATED_VMS= '{}' WHERE UNAME = '{}'"
                 .format(TOTAL_CREATED_VMS,COMPETITION_NAME))
    addEvent(session['username'], "TOTAL_CREATED_VMS has been updated for competition ("+COMPETITION_NAME+")")




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

