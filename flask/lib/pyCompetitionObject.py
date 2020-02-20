"""
This class represents a competition object.

"""


class Competition:

    def __init__(self, Competition_Uname):
        self.Competition_Uname = Competition_Uname
        self.Competition_Teams = None
        self.Win_VMs = None
        self.Unix_VMs = None
        self.Total_VMs = None
        self.Resource_Pool = None
        self.Teams = []


    def add_Team(self, Team):
        """
        Add a Team object to the list of VMs for this Team
        :param VM: Team object from pyTeamObject
        :return: 1 for success
        """
        pass
        # TODO - Check if isinstance of VM class.
        try:
            self.Teams.append(Team)
            return 1
        except:
            return 0

    def get_Teams(self):
        """
        Get the object's Teams
        :return: object's Teams
        """
        return self.Teams

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

    def set_Competition_Teams(self, Competition_Teams):
        """
        Set Competition_Teams
        :param Competition_Teams:
        :return: None
        """
        self.Competition_Teams = Competition_Teams

    def get_Competition_Teams(self):
        """
        Get the object's Competition_Teams
        :return: object's Competition_Teams
        """
        return self.Competition_Teams

    def Competition_Teams_is_empty(self):
        """
        Check if Competition_Teams has a value
        :return:
        """
        if self.Competition_Teams == None:
            return True
        return False

    def Competition_Teams_to_string(self):
        """
        Convert Competition_Teams value to a string and return it
        :return: string of Competition_Teams
        """
        return str(self.Competition_Teams)

    def set_Win_VMs(self, Win_VMs):
        """
        Set Win_VMs
        :param Win_VMs:
        :return: None
        """
        self.Win_VMs = Win_VMs

    def get_Win_VMs(self):
        """
        Get the object's Win_VMs
        :return: object's Win_VMs
        """
        return self.Win_VMs

    def Win_VMs_is_empty(self):
        """
        Check if Win_VMs has a value
        :return:
        """
        if self.Win_VMs == None:
            return True
        return False

    def Win_VMs_to_string(self):
        """
        Convert Win_VMs value to a string and return it
        :return: string of Win_VMs
        """
        return str(self.Win_VMs)

    def set_Unix_VMs(self, Unix_VMs):
        """
        Set Unix_VMs
        :param Unix_VMs:
        :return: None
        """
        self.Unix_VMs = Unix_VMs

    def get_Unix_VMs(self):
        """
        Get the object's Unix_VMs
        :return: object's Unix_VMs
        """
        return self.Unix_VMs

    def Unix_VMs_is_empty(self):
        """
        Check if Unix_VMs has a value
        :return:
        """
        if self.Unix_VMs == None:
            return True
        return False

    def Unix_VMs_to_string(self):
        """
        Convert Unix_VMs value to a string and return it
        :return: string of Unix_VMs
        """
        return str(self.Unix_VMs)

    def set_Total_VMs(self, Total_VMs):
        """
        Set Total_VMs
        :param Total_VMs:
        :return: None
        """
        self.Total_VMs = Total_VMs

    def get_Total_VMs(self):
        """
        Get the object's Total_VMs
        :return: object's Total_VMs
        """
        return self.Total_VMs

    def Total_VMs_is_empty(self):
        """
        Check if Total_VMs has a value
        :return:
        """
        if self.Total_VMs == None:
            return True
        return False

    def Total_VMs_to_string(self):
        """
        Convert Total_VMs value to a string and return it
        :return: string of Total_VMs
        """
        return str(self.Total_VMs)

    def set_Resource_Pool(self, Resource_Pool):
        """
        Set Resource_Pool
        :param Resource_Pool:
        :return: None
        """
        self.Resource_Pool = Resource_Pool

    def get_Resource_Pool(self):
        """
        Get the object's Resource_Pool
        :return: object's Resource_Pool
        """
        return self.Resource_Pool

    def Resource_Pool_is_empty(self):
        """
        Check if Resource_Pool has a value
        :return:
        """
        if self.Resource_Pool == None:
            return True
        return False

    def Resource_Pool_to_string(self):
        """
        Convert Resource_Pool value to a string and return it
        :return: string of Resource_Pool
        """
        return str(self.Resource_Pool)
