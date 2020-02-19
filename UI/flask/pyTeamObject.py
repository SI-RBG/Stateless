"""



"""
import pyVMObject
import ipaddress

class Team:

    def __init__(self, Competition_Uname, Team_Uname):
        self.Competition_Uname = Competition_Uname
        self.Team_Uname = Team_Uname
        self.Team_ID = None
        self.Domain_Name = None
        self.Subnet = None
        self.Gateway = None
        self.DNS1 = None
        self.DNS2 = None
        self.NICAKA_PortGropu = None
        self.NICAKA_PortGropuList = None
        self.VMs = []
        # List of ipaddress.IPv4Address('192.168.0.1')
        self.reservedIP = []


    def add_VM(self, VM):
        """
        Add a VM object to the list of VMs for this Team
        :param VM: VM object from pyVMObject
        :return: 1 for success
        """
        pass
        # TODO - Check if isinstance of VM class.
        try:
            self.VMs.append(VM)
            return 1
        except:
            return 0

    def get_VMs(self):
        """
        Get the object's VMs
        :return: object's VMs
        """
        return self.VMs

    def add_reservedIP(self, IP):
        """
        Add a IP string to the list of IPs for this Team.
        :return: object's VMs
        """
        pass
        # TODO - Check if isinstance of VM class.
        try:
            self.reservedIP.append(IP)
            return 1
        except:
            return 0

    def get_reservedIP(self):
        """
        Add a IP string to the list of IPs for this Team.
        :return: object's VMs
        """
        return self.reservedIP

    def set_Competition_Uname(self, Competition_Uname):
        """
        Set Competition_Uname
        :param Competition_Uname:
        :return: None
        """
        self.Competition_Uname = Competition_Uname

    def get_Competition_Uname(self):
        """
        Get the object's Competition_Uname
        :return: object's Competition_Uname
        """
        return self.Competition_Uname

    def Competition_Uname_is_empty(self):
        """
        Check if Competition_Uname has a value
        :return:
        """
        if self.Competition_Uname == None:
            return True
        return False

    def Competition_Uname_to_string(self):
        """
        Convert Competition_Uname value to a string and return it
        :return: string of Competition_Uname
        """
        return str(self.Competition_Uname)

    def set_Team_Uname(self, Team_Uname):
        """
        Set Team_Uname
        :param Team_Uname:
        :return: None
        """
        self.Team_Uname = Team_Uname

    def get_Team_Uname(self):
        """
        Get the object's Team_Uname
        :return: object's Team_Uname
        """
        return self.Team_Uname

    def Team_Uname_is_empty(self):
        """
        Check if Team_Uname has a value
        :return:
        """
        if self.Team_Uname == None:
            return True
        return False

    def Team_Uname_to_string(self):
        """
        Convert Team_Uname value to a string and return it
        :return: string of Team_Uname
        """
        return str(self.Team_Uname)

    def set_Team_ID(self, Team_ID):
        """
        Set Team_ID
        :param Team_ID:
        :return: None
        """
        self.Team_ID = Team_ID

    def get_Team_ID(self):
        """
        Get the object's Team_ID
        :return: object's Team_ID
        """
        return self.Team_ID

    def Team_ID_is_empty(self):
        """
        Check if Team_ID has a value
        :return:
        """
        if self.Team_ID == None:
            return True
        return False

    def Team_ID_to_string(self):
        """
        Convert Team_ID value to a string and return it
        :return: string of Team_ID
        """
        return str(self.Team_ID)

    def set_Domain_Name(self, Domain_Name):
        """
        Set Domain_Name
        :param Domain_Name:
        :return: None
        """
        self.Domain_Name = Domain_Name

    def get_Domain_Name(self):
        """
        Get the object's Domain_Name
        :return: object's Domain_Name
        """
        return self.Domain_Name

    def Domain_Name_is_empty(self):
        """
        Check if Domain_Name has a value
        :return:
        """
        if self.Domain_Name == None:
            return True
        return False

    def Domain_Name_to_string(self):
        """
        Convert Domain_Name value to a string and return it
        :return: string of Domain_Name
        """
        return str(self.Domain_Name)

    def set_Subnet(self, Subnet):
        """
        Set Subnet
        :param Subnet:
        :return: None
        """
        self.Subnet = Subnet

    def get_Subnet(self):
        """
        Get the object's Subnet
        :return: object's Subnet
        """
        return self.Subnet

    def Subnet_is_empty(self):
        """
        Check if Subnet has a value
        :return:
        """
        if self.Subnet == None:
            return True
        return False

    def Subnet_to_string(self):
        """
        Convert Subnet value to a string and return it
        :return: string of Subnet
        """
        return str(self.Subnet)

    def set_Gateway(self, Gateway):
        """
        Set Gateway
        :param Gateway:
        :return: None
        """
        self.Gateway = Gateway

    def get_Gateway(self):
        """
        Get the object's Gateway
        :return: object's Gateway
        """
        return self.Gateway

    def Gateway_is_empty(self):
        """
        Check if Gateway has a value
        :return:
        """
        if self.Gateway == None:
            return True
        return False

    def Gateway_to_string(self):
        """
        Convert Gateway value to a string and return it
        :return: string of Gateway
        """
        return str(self.Gateway)

    def set_DNS1(self, DNS1):
        """
        Set DNS1
        :param DNS1:
        :return: None
        """
        self.DNS1 = DNS1

    def get_DNS1(self):
        """
        Get the object's DNS1
        :return: object's DNS1
        """
        return self.DNS1

    def DNS1_is_empty(self):
        """
        Check if DNS1 has a value
        :return:
        """
        if self.DNS1 == None:
            return True
        return False

    def DNS1_to_string(self):
        """
        Convert DNS1 value to a string and return it
        :return: string of DNS1
        """
        return str(self.DNS1)

    def set_DNS2(self, DNS2):
        """
        Set DNS2
        :param DNS2:
        :return: None
        """
        self.DNS2 = DNS2

    def get_DNS2(self):
        """
        Get the object's DNS2
        :return: object's DNS2
        """
        return self.DNS2

    def DNS2_is_empty(self):
        """
        Check if DNS2 has a value
        :return:
        """
        if self.DNS2 == None:
            return True
        return False

    def DNS2_to_string(self):
        """
        Convert DNS2 value to a string and return it
        :return: string of DNS2
        """
        return str(self.DNS2)

    def set_NICAKA_PortGropu(self, NICAKA_PortGropu):
        """
        Set NICAKA_PortGropu
        :param NICAKA_PortGropu:
        :return: None
        """
        self.NICAKA_PortGropu = NICAKA_PortGropu

    def get_NICAKA_PortGropu(self):
        """
        Get the object's NICAKA_PortGropu
        :return: object's NICAKA_PortGropu
        """
        return self.NICAKA_PortGropu

    def NICAKA_PortGropu_is_empty(self):
        """
        Check if NICAKA_PortGropu has a value
        :return:
        """
        if self.NICAKA_PortGropu == None:
            return True
        return False

    def NICAKA_PortGropu_to_string(self):
        """
        Convert NICAKA_PortGropu value to a string and return it
        :return: string of NICAKA_PortGropu
        """
        return str(self.NICAKA_PortGropu)

    def set_NICAKA_PortGropuList(self, NICAKA_PortGropuList):
        """
        Set NICAKA_PortGropuList
        :param NICAKA_PortGropuList:
        :return: None
        """
        self.NICAKA_PortGropuList = NICAKA_PortGropuList

    def get_NICAKA_PortGropuList(self):
        """
        Get the object's NICAKA_PortGropuList
        :return: object's NICAKA_PortGropuList
        """
        return self.NICAKA_PortGropuList

    def NICAKA_PortGropuList_is_empty(self):
        """
        Check if NICAKA_PortGropuList has a value
        :return:
        """
        if self.NICAKA_PortGropuList == None:
            return True
        return False

    def NICAKA_PortGropuList_to_string(self):
        """
        Convert NICAKA_PortGropuList value to a string and return it
        :return: string of NICAKA_PortGropuList
        """
        return str(self.NICAKA_PortGropuList)

