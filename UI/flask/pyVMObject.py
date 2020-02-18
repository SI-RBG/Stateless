"""



"""


class VM:
    def __init__(self, Competition_Uname, Team_Uname):
        self.Competition_Uname = None
        self.Team_Uname = None
        self.VM_Uname = None
        self.VM_ID = None
        self.Hostname = None
        self.CPU = None
        self.Memory = None
        self.Disk_Space = None
        self.ISO_Path = None
        self.IP_Address = None
        self.Guest_Type = None
        self.Template_Name = None
        self.Services = None


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
        if type(self.Competition_Uname) != str:
            return str(self.Competition_Uname)
        return self.Competition_Uname

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
        if type(self.Team_Uname) != str:
            return str(self.Team_Uname)
        return self.Team_Uname

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
        if type(self.VM_Uname) != str:
            return str(self.VM_Uname)
        return self.VM_Uname

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
        if type(self.VM_ID) != str:
            return str(self.VM_ID)
        return self.VM_ID

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
        if type(self.Hostname) != str:
            return str(self.Hostname)
        return self.Hostname

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
        if type(self.CPU) != str:
            return str(self.CPU)
        return self.CPU

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
        if type(self.Memory) != str:
            return str(self.Memory)
        return self.Memory

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
        if type(self.Disk_Space) != str:
            return str(self.Disk_Space)
        return self.Disk_Space

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
        if type(self.ISO_Path) != str:
            return str(self.ISO_Path)
        return self.ISO_Path

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
        if type(self.IP_Address) != str:
            return str(self.IP_Address)
        return self.IP_Address

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
        if type(self.Guest_Type) != str:
            return str(self.Guest_Type)
        return self.Guest_Type

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
        if type(self.Template_Name) != str:
            return str(self.Template_Name)
        return self.Template_Name

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
        if type(self.Services) != str:
            return str(self.Services)
        return self.Services


