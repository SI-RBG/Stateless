"""
File name: pyVMObject.py
Purpose: This class represents a VM object.

"""


class VM:
    def __init__(self, Competition_Uname, Team_Uname):
        self.Competition_Uname = Competition_Uname
        self.Team_Uname = Team_Uname
        self.VM_Uname = None
        self.VM_ID = None
        self.Hostname = None
        self.CPU = None
        self.Memory = None
        self.Disk_Space = None
        self.IP_Address = None
        self.Domain_Name = None
        self.Subnet = None
        self.Gateway = None
        self.DNS1 = None
        self.DNS2 = None
        self.ISO_Path = None
        self.Guest_Type = None
        self.Guest_Name = None
        self.Template_Name = None
        self.NICAKA_PortGropu = None
        self.NICAKA_PortGropuList = None
        self.Services = None

        self.ssh_username = None
        self.ssh_password = None
        self.disk_controller_type = None
        self.disk_thin_provisioned = None
        self.network_card = None
        self.Services = None
        self.shellinline = None

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

    def set_VM_Uname(self, VM_Uname):
        """
        Set VM_Uname
        :param VM_Uname:
        :return: None
        """
        self.VM_Uname = VM_Uname

    def get_VM_Uname(self):
        """
        Get the object's VM_Uname
        :return: object's VM_Uname
        """
        return self.VM_Uname

    def VM_Uname_is_empty(self):
        """
        Check if VM_Uname has a value
        :return:
        """
        if self.VM_Uname == None:
            return True
        return False

    def VM_Uname_to_string(self):
        """
        Convert VM_Uname value to a string and return it
        :return: string of VM_Uname
        """
        return str(self.VM_Uname)

    def set_VM_ID(self, VM_ID):
        """
        Set VM_ID
        :param VM_ID:
        :return: None
        """
        self.VM_ID = VM_ID

    def get_VM_ID(self):
        """
        Get the object's VM_ID
        :return: object's VM_ID
        """
        return self.VM_ID

    def VM_ID_is_empty(self):
        """
        Check if VM_ID has a value
        :return:
        """
        if self.VM_ID == None:
            return True
        return False

    def VM_ID_to_string(self):
        """
        Convert VM_ID value to a string and return it
        :return: string of VM_ID
        """
        return str(self.VM_ID)

    def set_Hostname(self, Hostname):
        """
        Set Hostname
        :param Hostname:
        :return: None
        """
        self.Hostname = Hostname

    def get_Hostname(self):
        """
        Get the object's Hostname
        :return: object's Hostname
        """
        return self.Hostname

    def Hostname_is_empty(self):
        """
        Check if Hostname has a value
        :return:
        """
        if self.Hostname == None:
            return True
        return False

    def Hostname_to_string(self):
        """
        Convert Hostname value to a string and return it
        :return: string of Hostname
        """
        return str(self.Hostname)

    def set_CPU(self, CPU):
        """
        Set CPU
        :param CPU:
        :return: None
        """
        self.CPU = CPU

    def get_CPU(self):
        """
        Get the object's CPU
        :return: object's CPU
        """
        return self.CPU

    def CPU_is_empty(self):
        """
        Check if CPU has a value
        :return:
        """
        if self.CPU == None:
            return True
        return False

    def CPU_to_string(self):
        """
        Convert CPU value to a string and return it
        :return: string of CPU
        """
        return str(self.CPU)

    def set_Memory(self, Memory):
        """
        Set Memory
        :param Memory:
        :return: None
        """
        self.Memory = Memory

    def get_Memory(self):
        """
        Get the object's Memory
        :return: object's Memory
        """
        return self.Memory

    def Memory_is_empty(self):
        """
        Check if Memory has a value
        :return:
        """
        if self.Memory == None:
            return True
        return False

    def Memory_to_string(self):
        """
        Convert Memory value to a string and return it
        :return: string of Memory
        """
        return str(self.Memory)

    def set_Disk_Space(self, Disk_Space):
        """
        Set Disk_Space
        :param Disk_Space:
        :return: None
        """
        self.Disk_Space = Disk_Space

    def get_Disk_Space(self):
        """
        Get the object's Disk_Space
        :return: object's Disk_Space
        """
        return self.Disk_Space

    def Disk_Space_is_empty(self):
        """
        Check if Disk_Space has a value
        :return:
        """
        if self.Disk_Space == None:
            return True
        return False

    def Disk_Space_to_string(self):
        """
        Convert Disk_Space value to a string and return it
        :return: string of Disk_Space
        """
        return str(self.Disk_Space)

    def set_IP_Address(self, IP_Address):
        """
        Set IP_Address
        :param IP_Address:
        :return: None
        """
        self.IP_Address = IP_Address

    def get_IP_Address(self):
        """
        Get the object's IP_Address
        :return: object's IP_Address
        """
        return self.IP_Address

    def IP_Address_is_empty(self):
        """
        Check if IP_Address has a value
        :return:
        """
        if self.IP_Address == None:
            return True
        return False

    def IP_Address_to_string(self):
        """
        Convert IP_Address value to a string and return it
        :return: string of IP_Address
        """
        return str(self.IP_Address)

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

    def set_ISO_Path(self, ISO_Path):
        """
        Set ISO_Path
        :param ISO_Path:
        :return: None
        """
        self.ISO_Path = ISO_Path

    def get_ISO_Path(self):
        """
        Get the object's ISO_Path
        :return: object's ISO_Path
        """
        return self.ISO_Path

    def ISO_Path_is_empty(self):
        """
        Check if ISO_Path has a value
        :return:
        """
        if self.ISO_Path == None:
            return True
        return False

    def ISO_Path_to_string(self):
        """
        Convert ISO_Path value to a string and return it
        :return: string of ISO_Path
        """
        return str(self.ISO_Path)

    def set_Guest_Type(self, Guest_Type):
        """
        Set Guest_Type
        :param Guest_Type:
        :return: None
        """
        self.Guest_Type = Guest_Type

    def get_Guest_Type(self):
        """
        Get the object's Guest_Type
        :return: object's Guest_Type
        """
        return self.Guest_Type

    def Guest_Type_is_empty(self):
        """
        Check if Guest_Type has a value
        :return:
        """
        if self.Guest_Type == None:
            return True
        return False

    def Guest_Type_to_string(self):
        """
        Convert Guest_Type value to a string and return it
        :return: string of Guest_Type
        """
        return str(self.Guest_Type)

    def set_Template_Name(self, Template_Name):
        """
        Set Template_Name
        :param Template_Name:
        :return: None
        """
        self.Template_Name = Template_Name

    def get_Template_Name(self):
        """
        Get the object's Template_Name
        :return: object's Template_Name
        """
        return self.Template_Name

    def Template_Name_is_empty(self):
        """
        Check if Template_Name has a value
        :return:
        """
        if self.Template_Name == None:
            return True
        return False

    def Template_Name_to_string(self):
        """
        Convert Template_Name value to a string and return it
        :return: string of Template_Name
        """
        return str(self.Template_Name)

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

    def set_Services(self, Services):
        """
        Set Services
        :param Services:
        :return: None
        """
        self.Services = Services

    def get_Services(self):
        """
        Get the object's Services
        :return: object's Services
        """
        return self.Services

    def Services_is_empty(self):
        """
        Check if Services has a value
        :return:
        """
        if self.Services == None:
            return True
        return False

    def Services_to_string(self):
        """
        Convert Services value to a string and return it
        :return: string of Services
        """
        return str(self.Services)

    def set_shellinline(self, shellinline):
        """
        Set shellinline
        :param shellinline:
        :return: None
        """
        self.shellinline = shellinline

    def get_shellinline(self):
        """
        Get the object's shellinline
        :return: object's shellinline
        """
        return self.shellinline

    def shellinline_is_empty(self):
        """
        Check if shellinline has a value
        :return:
        """
        if self.shellinline == None:
            return True
        return False

    def shellinline_to_string(self):
        """
        Convert shellinline value to a string and return it
        :return: string of shellinline
        """
        return str(self.shellinline)

    def set_Guest_Name(self, Guest_Name):
        """
        Set Guest_Name
        :param Guest_Name:
        :return: None
        """
        self.Guest_Name = Guest_Name
    def get_Guest_Name(self):
        """
        Get the object's Guest_Name
        :return: object's Guest_Name
        """
        return self.Guest_Name
    def Guest_Name_is_empty(self):
        """
        Check if Guest_Name has a value
        :return:
        """
        if self.Guest_Name == None:
            return True
        return False
    def Guest_Name_to_string(self):
        """
        Convert Guest_Name value to a string and return it
        :return: string of Guest_Name
        """
        return str(self.Guest_Name)
