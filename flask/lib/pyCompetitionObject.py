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
        self.datastore = None
        self.vSphereFolder = None
        self.ResourcePool = None
        self.ESXI_HOST = None
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


    def set_datastore(self, datastore):
        """
        Set datastore
        :param datastore:
        :return: None
        """
        self.datastore = datastore

    def get_datastore(self):
        """
        Get the object's datastore
        :return: object's datastore
        """
        return self.datastore

    def datastore_is_empty(self):
        """
        Check if datastore has a value
        :return:
        """
        if self.datastore == None:
            return True
        return False

    def datastore_to_string(self):
        """
        Convert datastore value to a string and return it
        :return: string of datastore
        """
        return str(self.datastore)

    def set_vSphereFolder(self, vSphereFolder):
        """
        Set vSphereFolder
        :param vSphereFolder:
        :return: None
        """
        self.vSphereFolder = vSphereFolder

    def get_vSphereFolder(self):
        """
        Get the object's vSphereFolder
        :return: object's vSphereFolder
        """
        return self.vSphereFolder

    def vSphereFolder_is_empty(self):
        """
        Check if vSphereFolder has a value
        :return:
        """
        if self.vSphereFolder == None:
            return True
        return False

    def vSphereFolder_to_string(self):
        """
        Convert vSphereFolder value to a string and return it
        :return: string of vSphereFolder
        """
        return str(self.vSphereFolder)

    def set_ResourcePool(self, ResourcePool):
        """
        Set ResourcePool
        :param ResourcePool:
        :return: None
        """
        self.ResourcePool = ResourcePool

    def get_ResourcePool(self):
        """
        Get the object's ResourcePool
        :return: object's ResourcePool
        """
        return self.ResourcePool

    def ResourcePool_is_empty(self):
        """
        Check if ResourcePool has a value
        :return:
        """
        if self.ResourcePool == None:
            return True
        return False

    def ResourcePool_to_string(self):
        """
        Convert ResourcePool value to a string and return it
        :return: string of ResourcePool
        """
        return str(self.ResourcePool)



    def get_sample_vms(self):
        if len(self.Teams) > 0:
            return self.Teams[0].get_VMs()
        else:
            return None

    
    def set_ESXI_HOST(self, ESXI_HOST):
        """
        Set ESXI_HOST
        :param ESXI_HOST:
        :return: None
        """
        self.ESXI_HOST = ESXI_HOST
    def get_ESXI_HOST(self):
        """
        Get the object's ESXI_HOST
        :return: object's ESXI_HOST
        """
        return self.ESXI_HOST
    def ESXI_HOST_is_empty(self):
        """
        Check if ESXI_HOST has a value
        :return:
        """
        if self.ESXI_HOST == None:
            return True
        return False
    def ESXI_HOST_to_string(self):
        """
        Convert ESXI_HOST value to a string and return it
        :return: string of ESXI_HOST
        """
        return str(self.ESXI_HOST)

