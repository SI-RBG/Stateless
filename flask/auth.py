"""
File name: auth.py
Purpose: To be used when we need to check for valid creds
"""

import requests


# Function to get the vCenter server session
def get_vc_session(s,vcip,username,password):
    result = s.post('https://'+vcip+'/rest/com/vmware/cis/session',auth=(username,password))
    return result


# 'controller@mohammed.red'
def vCenterAuth(VSPHERE_SERVER,username, password):
    s=requests.Session()
    s.verify=False
    session_id = get_vc_session(s,VSPHERE_SERVER,username, password)
    session_id = session_id.json()
    if ("unauthenticated'" in session_id):
        return 0
    else:
        try:
            session = str(session_id['value'])
            if (len(session) == 32):
                return 1
        except:
            return 0
    print(session_id)