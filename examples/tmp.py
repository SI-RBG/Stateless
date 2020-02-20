

string = """
        self.vsphere_server = None
        self.dc_name = None
        self.datastore_name = None
        self.resourcepool_name = None
        self.vsphere_user = None
        self.vsphere_password = None
        self.domain = None
        self.network_name = None
        self.template_name = None
        self.hostname = None
        self.ipaddress = None
        self.netmask = None
        self.gateway = None
        self.dns = None
"""

string = """
        self.Competition_Uname = Competition_Uname
        self.Competition_Teams = None
        self.Win_VMs = None
        self.Unix_VMs = None
        self.Total_VMs = None
        self.Resource_Pool = None
"""


string = string.replace(".",";").replace("=",";").split(';')
new_string = []

for line in string:
    if "self" in line:
        continue
    if "None" in line:
        continue
    if "#" in line:
        continue
    new_string.append(line)


sss = """


    def set_vsphere_server(self, vsphere_server):
        \"\"\"
        Set vsphere_server
        :param vsphere_server:
        :return: None
        \"\"\"
        self.vsphere_server = vsphere_server


    def get_vsphere_server(self):
        \"\"\"
        Get the object's vsphere_server
        :return: object's vsphere_server
        \"\"\"
        return self.vsphere_server


    def vsphere_server_is_empty(self):
        \"\"\"
        Check if vsphere_server has a value
        :return:
        \"\"\"
        if self.vsphere_server == None:
            return True
        return False


    def vsphere_server_to_string(self):
        \"\"\"
        Convert vsphere_server value to a string and return it
        :return: string of vsphere_server
        \"\"\"
        return str(self.vsphere_server)


        """


for e in new_string:
    s = sss.replace("vsphere_server",e.strip())
    print(s)
