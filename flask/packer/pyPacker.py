"""
File name: pyPacker.py
Purpose: This a class to hold values for packer templates.
"""


from packerpy import PackerExecutable
from Utilities import *

class packerObject:

    def __init__(self):
        # Config
        self.vsphere_server = None
        self.vsphere_user = None
        self.vsphere_password = None
        self.insecure_connection = None

        # Common
        self.vm_name = None
        self.host = None
        self.datastore = None
        self.network = None
        self.cluster = None
        self.datacenter = None
        self.resource_pool = None
        self.guest_os_type = None
        self.guest_os_name = None
        self.CPUs = None
        self.RAM = None
        self.RAM_reserve_all = None
        self.disk_controller_type = None
        self.disk_size = None
        self.disk_thin_provisioned = None
        self.network_card = None

        self.iso_paths = None
        self.floppy_files = None
        self.boot_command = None

        # Linux communicator
        self.username = None
        self.password = None


        # Communicator
        # Not needed so far
        #self.communicator = None
        #self.winrm_username = None
        #self.winrm_password = None

        # provisioners
        self.type = None
        self.shellinline = None


    def get_Template_and_Template_Vars(self):
        items = [self.vsphere_server,
                self.vsphere_user,
                self.vsphere_password,
                self.cluster,
                self.datacenter,
                self.resource_pool,
                self.guest_os_type,
                self.guest_os_name,
                self.host,
                self.vm_name,
                self.datastore,
                self.network,
                self.username,
                self.password,
                self.CPUs,
                self.RAM,
                self.disk_size,
                self.iso_paths,
                self.shellinline]
        # Check if any item is missing
        for i in range(len(items)):
            item = items[i]
            if item is None:
                debugMessage(str(i)+" is missing")
                return None, None

        # Ubuntu server
        if self.guest_os_type == "ubuntu64Guest":
            template = '/flask/packer/templates/ubuntu/{}/template.json'.format(self.guest_os_name)
            template_vars = {'vc_server': self.vsphere_server
                , 'vc_username': self.vsphere_user
                , 'vc_password': self.vsphere_password

                , 'datacenter': self.datacenter
                , 'cluster': self.cluster
                , 'resource_pool': self.resource_pool

                             # This is the type of this template
                , 'guest_os_type': self.guest_os_type

                , 'host': self.host
                , 'vm_name': self.vm_name
                , 'datastore': self.datastore
                , 'network': self.network
                , 'username': self.username
                , 'password': self.password
                , 'CPUs': int(self.CPUs)
                , 'RAM': int(self.RAM)
                , 'disk_size': self.disk_size
                , 'os_iso_path': self.iso_paths
                , 'shellinline': self.shellinline
                             }

            return template, template_vars

        # Windows 2019
        if self.guest_os_type == "windows9Server64Guest":
            template = '/flask/packer/templates/windows/{}/template.json'.format(self.guest_os_name)
            template_vars = {'vc_server': self.vsphere_server
                , 'vc_username': self.vsphere_user
                , 'vc_password': self.vsphere_password

                , 'datacenter': self.datacenter
                , 'cluster': self.cluster
                , 'resource_pool': self.resource_pool

                # This is the type of this template
                , 'guest_os_type': self.guest_os_type

                , 'host': self.host
                , 'vm_name': self.vm_name
                , 'datastore': self.datastore
                , 'network': self.network
                #, 'username': self.username # In windows it's always going to be Administrator
                #, 'password': self.password  # If we will enable this, we need to edit its XML file to they match otherwise winrm will not be able to connect
                , 'CPUs': int(self.CPUs)
                , 'RAM': int(self.RAM)
                , 'disk_size': self.disk_size
                , 'os_iso_path': self.iso_paths
                , 'shellinline': self.shellinline
                }

            return template, template_vars


    def set_vsphere_server(self, vsphere_server):
        """
        Set vsphere_server
        :param vsphere_server:
        :return: None
        """
        self.vsphere_server = vsphere_server

    def get_vsphere_server(self):
        """
        Get the object's vsphere_server
        :return: object's vsphere_server
        """
        return self.vsphere_server

    def vsphere_server_is_empty(self):
        """
        Check if vsphere_server has a value
        :return:
        """
        if self.vsphere_server == None:
            return True
        return False

    def vsphere_server_to_string(self):
        """
        Convert vsphere_server value to a string and return it
        :return: string of vsphere_server
        """
        if type(self.vsphere_server) != str:
            return str(self.vsphere_server)
        return self.vsphere_server

    def set_vsphere_user(self, vsphere_user):
        """
        Set vsphere_user
        :param vsphere_user:
        :return: None
        """
        self.vsphere_user = vsphere_user

    def get_vsphere_user(self):
        """
        Get the object's vsphere_user
        :return: object's vsphere_user
        """
        return self.vsphere_user

    def vsphere_user_is_empty(self):
        """
        Check if vsphere_user has a value
        :return:
        """
        if self.vsphere_user == None:
            return True
        return False

    def vsphere_user_to_string(self):
        """
        Convert vsphere_user value to a string and return it
        :return: string of vsphere_user
        """
        if type(self.vsphere_user) != str:
            return str(self.vsphere_user)
        return self.vsphere_user

    def set_vsphere_password(self, vsphere_password):
        """
        Set vsphere_password
        :param vsphere_password:
        :return: None
        """
        self.vsphere_password = vsphere_password

    def get_vsphere_password(self):
        """
        Get the object's vsphere_password
        :return: object's vsphere_password
        """
        return self.vsphere_password

    def vsphere_password_is_empty(self):
        """
        Check if vsphere_password has a value
        :return:
        """
        if self.vsphere_password == None:
            return True
        return False

    def vsphere_password_to_string(self):
        """
        Convert vsphere_password value to a string and return it
        :return: string of vsphere_password
        """
        if type(self.vsphere_password) != str:
            return str(self.vsphere_password)
        return self.vsphere_password

    def set_insecure_connection(self, insecure_connection):
        """
        Set insecure_connection
        :param insecure_connection:
        :return: None
        """
        self.insecure_connection = insecure_connection

    def get_insecure_connection(self):
        """
        Get the object's insecure_connection
        :return: object's insecure_connection
        """
        return self.insecure_connection

    def insecure_connection_is_empty(self):
        """
        Check if insecure_connection has a value
        :return:
        """
        if self.insecure_connection == None:
            return True
        return False

    def insecure_connection_to_string(self):
        """
        Convert insecure_connection value to a string and return it
        :return: string of insecure_connection
        """
        if type(self.insecure_connection) != str:
            return str(self.insecure_connection)
        return self.insecure_connection

    def set_vm_name(self, vm_name):
        """
        Set vm_name
        :param vm_name:
        :return: None
        """
        self.vm_name = vm_name

    def get_vm_name(self):
        """
        Get the object's vm_name
        :return: object's vm_name
        """
        return self.vm_name

    def vm_name_is_empty(self):
        """
        Check if vm_name has a value
        :return:
        """
        if self.vm_name == None:
            return True
        return False

    def vm_name_to_string(self):
        """
        Convert vm_name value to a string and return it
        :return: string of vm_name
        """
        if type(self.vm_name) != str:
            return str(self.vm_name)
        return self.vm_name

    def set_host(self, host):
        """
        Set host
        :param host:
        :return: None
        """
        self.host = host

    def get_host(self):
        """
        Get the object's host
        :return: object's host
        """
        return self.host

    def host_is_empty(self):
        """
        Check if host has a value
        :return:
        """
        if self.host == None:
            return True
        return False

    def host_to_string(self):
        """
        Convert host value to a string and return it
        :return: string of host
        """
        if type(self.host) != str:
            return str(self.host)
        return self.host

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
        if type(self.datastore) != str:
            return str(self.datastore)
        return self.datastore

    def set_network(self, network):
        """
        Set network
        :param network:
        :return: None
        """
        self.network = network

    def get_network(self):
        """
        Get the object's network
        :return: object's network
        """
        return self.network

    def network_is_empty(self):
        """
        Check if network has a value
        :return:
        """
        if self.network == None:
            return True
        return False

    def network_to_string(self):
        """
        Convert network value to a string and return it
        :return: string of network
        """
        if type(self.network) != str:
            return str(self.network)
        return self.network

    def set_guest_os_type(self, guest_os_type):
        """
        Set guest_os_type
        :param guest_os_type:
        :return: None
        """
        self.guest_os_type = guest_os_type

    def get_guest_os_type(self):
        """
        Get the object's guest_os_type
        :return: object's guest_os_type
        """
        return self.guest_os_type

    def guest_os_type_is_empty(self):
        """
        Check if guest_os_type has a value
        :return:
        """
        if self.guest_os_type == None:
            return True
        return False

    def guest_os_type_to_string(self):
        """
        Convert guest_os_type value to a string and return it
        :return: string of guest_os_type
        """
        if type(self.guest_os_type) != str:
            return str(self.guest_os_type)
        return self.guest_os_type

    def set_CPUs(self, CPUs):
        """
        Set CPUs
        :param CPUs:
        :return: None
        """
        self.CPUs = CPUs

    def get_CPUs(self):
        """
        Get the object's CPUs
        :return: object's CPUs
        """
        return self.CPUs

    def CPUs_is_empty(self):
        """
        Check if CPUs has a value
        :return:
        """
        if self.CPUs == None:
            return True
        return False

    def CPUs_to_string(self):
        """
        Convert CPUs value to a string and return it
        :return: string of CPUs
        """
        if type(self.CPUs) != str:
            return str(self.CPUs)
        return self.CPUs

    def set_RAM(self, RAM):
        """
        Set RAM
        :param RAM:
        :return: None
        """
        self.RAM = RAM

    def get_RAM(self):
        """
        Get the object's RAM
        :return: object's RAM
        """
        return self.RAM

    def RAM_is_empty(self):
        """
        Check if RAM has a value
        :return:
        """
        if self.RAM == None:
            return True
        return False

    def RAM_to_string(self):
        """
        Convert RAM value to a string and return it
        :return: string of RAM
        """
        if type(self.RAM) != str:
            return str(self.RAM)
        return self.RAM

    def set_RAM_reserve_all(self, RAM_reserve_all):
        """
        Set RAM_reserve_all
        :param RAM_reserve_all:
        :return: None
        """
        self.RAM_reserve_all = RAM_reserve_all

    def get_RAM_reserve_all(self):
        """
        Get the object's RAM_reserve_all
        :return: object's RAM_reserve_all
        """
        return self.RAM_reserve_all

    def RAM_reserve_all_is_empty(self):
        """
        Check if RAM_reserve_all has a value
        :return:
        """
        if self.RAM_reserve_all == None:
            return True
        return False

    def RAM_reserve_all_to_string(self):
        """
        Convert RAM_reserve_all value to a string and return it
        :return: string of RAM_reserve_all
        """
        if type(self.RAM_reserve_all) != str:
            return str(self.RAM_reserve_all)
        return self.RAM_reserve_all

    def set_disk_controller_type(self, disk_controller_type):
        """
        Set disk_controller_type
        :param disk_controller_type:
        :return: None
        """
        self.disk_controller_type = disk_controller_type

    def get_disk_controller_type(self):
        """
        Get the object's disk_controller_type
        :return: object's disk_controller_type
        """
        return self.disk_controller_type

    def disk_controller_type_is_empty(self):
        """
        Check if disk_controller_type has a value
        :return:
        """
        if self.disk_controller_type == None:
            return True
        return False

    def disk_controller_type_to_string(self):
        """
        Convert disk_controller_type value to a string and return it
        :return: string of disk_controller_type
        """
        if type(self.disk_controller_type) != str:
            return str(self.disk_controller_type)
        return self.disk_controller_type

    def set_disk_size(self, disk_size):
        """
        Set disk_size
        :param disk_size:
        :return: None
        """
        self.disk_size = disk_size

    def get_disk_size(self):
        """
        Get the object's disk_size
        :return: object's disk_size
        """
        return self.disk_size

    def disk_size_is_empty(self):
        """
        Check if disk_size has a value
        :return:
        """
        if self.disk_size == None:
            return True
        return False

    def disk_size_to_string(self):
        """
        Convert disk_size value to a string and return it
        :return: string of disk_size
        """
        if type(self.disk_size) != str:
            return str(self.disk_size)
        return self.disk_size

    def set_disk_thin_provisioned(self, disk_thin_provisioned):
        """
        Set disk_thin_provisioned
        :param disk_thin_provisioned:
        :return: None
        """
        self.disk_thin_provisioned = disk_thin_provisioned

    def get_disk_thin_provisioned(self):
        """
        Get the object's disk_thin_provisioned
        :return: object's disk_thin_provisioned
        """
        return self.disk_thin_provisioned

    def disk_thin_provisioned_is_empty(self):
        """
        Check if disk_thin_provisioned has a value
        :return:
        """
        if self.disk_thin_provisioned == None:
            return True
        return False

    def disk_thin_provisioned_to_string(self):
        """
        Convert disk_thin_provisioned value to a string and return it
        :return: string of disk_thin_provisioned
        """
        if type(self.disk_thin_provisioned) != str:
            return str(self.disk_thin_provisioned)
        return self.disk_thin_provisioned

    def set_network_card(self, network_card):
        """
        Set network_card
        :param network_card:
        :return: None
        """
        self.network_card = network_card

    def get_network_card(self):
        """
        Get the object's network_card
        :return: object's network_card
        """
        return self.network_card

    def network_card_is_empty(self):
        """
        Check if network_card has a value
        :return:
        """
        if self.network_card == None:
            return True
        return False

    def network_card_to_string(self):
        """
        Convert network_card value to a string and return it
        :return: string of network_card
        """
        if type(self.network_card) != str:
            return str(self.network_card)
        return self.network_card

    def set_iso_paths(self, iso_paths):
        """
        Set iso_paths
        :param iso_paths:
        :return: None
        """
        self.iso_paths = iso_paths

    def get_iso_paths(self):
        """
        Get the object's iso_paths
        :return: object's iso_paths
        """
        return self.iso_paths

    def iso_paths_is_empty(self):
        """
        Check if iso_paths has a value
        :return:
        """
        if self.iso_paths == None:
            return True
        return False

    def iso_paths_to_string(self):
        """
        Convert iso_paths value to a string and return it
        :return: string of iso_paths
        """
        if type(self.iso_paths) != str:
            return str(self.iso_paths)
        return self.iso_paths

    def set_floppy_files(self, floppy_files):
        """
        Set floppy_files
        :param floppy_files:
        :return: None
        """
        self.floppy_files = floppy_files

    def get_floppy_files(self):
        """
        Get the object's floppy_files
        :return: object's floppy_files
        """
        return self.floppy_files

    def floppy_files_is_empty(self):
        """
        Check if floppy_files has a value
        :return:
        """
        if self.floppy_files == None:
            return True
        return False

    def floppy_files_to_string(self):
        """
        Convert floppy_files value to a string and return it
        :return: string of floppy_files
        """
        if type(self.floppy_files) != str:
            return str(self.floppy_files)
        return self.floppy_files

    def set_boot_command(self, boot_command):
        """
        Set boot_command
        :param boot_command:
        :return: None
        """
        self.boot_command = boot_command

    def get_boot_command(self):
        """
        Get the object's boot_command
        :return: object's boot_command
        """
        return self.boot_command

    def boot_command_is_empty(self):
        """
        Check if boot_command has a value
        :return:
        """
        if self.boot_command == None:
            return True
        return False

    def boot_command_to_string(self):
        """
        Convert boot_command value to a string and return it
        :return: string of boot_command
        """
        if type(self.boot_command) != str:
            return str(self.boot_command)
        return self.boot_command

    def set_username(self, username):
        """
        Set username
        :param username:
        :return: None
        """
        self.username = username

    def get_username(self):
        """
        Get the object's username
        :return: object's username
        """
        return self.username

    def username_is_empty(self):
        """
        Check if username has a value
        :return:
        """
        if self.username == None:
            return True
        return False

    def username_to_string(self):
        """
        Convert username value to a string and return it
        :return: string of username
        """
        if type(self.username) != str:
            return str(self.username)
        return self.username

    def set_password(self, password):
        """
        Set password
        :param password:
        :return: None
        """
        self.password = password

    def get_password(self):
        """
        Get the object's password
        :return: object's password
        """
        return self.password

    def password_is_empty(self):
        """
        Check if password has a value
        :return:
        """
        if self.password == None:
            return True
        return False

    def password_to_string(self):
        """
        Convert password value to a string and return it
        :return: string of password
        """
        if type(self.password) != str:
            return str(self.password)
        return self.password

    def set_communicator(self, communicator):
        """
        Set communicator
        :param communicator:
        :return: None
        """
        self.communicator = communicator

    def get_communicator(self):
        """
        Get the object's communicator
        :return: object's communicator
        """
        return self.communicator

    def communicator_is_empty(self):
        """
        Check if communicator has a value
        :return:
        """
        if self.communicator == None:
            return True
        return False

    def communicator_to_string(self):
        """
        Convert communicator value to a string and return it
        :return: string of communicator
        """
        if type(self.communicator) != str:
            return str(self.communicator)
        return self.communicator

    def set_winrm_username(self, winrm_username):
        """
        Set winrm_username
        :param winrm_username:
        :return: None
        """
        self.winrm_username = winrm_username

    def get_winrm_username(self):
        """
        Get the object's winrm_username
        :return: object's winrm_username
        """
        return self.winrm_username

    def winrm_username_is_empty(self):
        """
        Check if winrm_username has a value
        :return:
        """
        if self.winrm_username == None:
            return True
        return False

    def winrm_username_to_string(self):
        """
        Convert winrm_username value to a string and return it
        :return: string of winrm_username
        """
        if type(self.winrm_username) != str:
            return str(self.winrm_username)
        return self.winrm_username

    def set_winrm_password(self, winrm_password):
        """
        Set winrm_password
        :param winrm_password:
        :return: None
        """
        self.winrm_password = winrm_password

    def get_winrm_password(self):
        """
        Get the object's winrm_password
        :return: object's winrm_password
        """
        return self.winrm_password

    def winrm_password_is_empty(self):
        """
        Check if winrm_password has a value
        :return:
        """
        if self.winrm_password == None:
            return True
        return False

    def winrm_password_to_string(self):
        """
        Convert winrm_password value to a string and return it
        :return: string of winrm_password
        """
        if type(self.winrm_password) != str:
            return str(self.winrm_password)
        return self.winrm_password

    def set_type(self, type):
        """
        Set type
        :param type:
        :return: None
        """
        self.type = type

    def get_type(self):
        """
        Get the object's type
        :return: object's type
        """
        return self.type

    def type_is_empty(self):
        """
        Check if type has a value
        :return:
        """
        if self.type == None:
            return True
        return False

    def type_to_string(self):
        """
        Convert type value to a string and return it
        :return: string of type
        """
        if type(self.type) != str:
            return str(self.type)
        return self.type

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
        if type(self.shellinline) != str:
            return str(self.shellinline)
        return self.shellinline

    def set_cluster(self, cluster):
        """
        Set cluster
        :param cluster:
        :return: None
        """
        self.cluster = cluster

    def get_cluster(self):
        """
        Get the object's cluster
        :return: object's cluster
        """
        return self.cluster

    def cluster_is_empty(self):
        """
        Check if cluster has a value
        :return:
        """
        if self.cluster == None:
            return True
        return False

    def cluster_to_string(self):
        """
        Convert cluster value to a string and return it
        :return: string of cluster
        """
        return str(self.cluster)

    def set_datacenter(self, datacenter):
        """
        Set datacenter
        :param datacenter:
        :return: None
        """
        self.datacenter = datacenter

    def get_datacenter(self):
        """
        Get the object's datacenter
        :return: object's datacenter
        """
        return self.datacenter

    def datacenter_is_empty(self):
        """
        Check if datacenter has a value
        :return:
        """
        if self.datacenter == None:
            return True
        return False

    def datacenter_to_string(self):
        """
        Convert datacenter value to a string and return it
        :return: string of datacenter
        """
        return str(self.datacenter)

    def set_resource_pool(self, resource_pool):
        """
        Set resource_pool
        :param resource_pool:
        :return: None
        """
        self.resource_pool = resource_pool

    def get_resource_pool(self):
        """
        Get the object's resource_pool
        :return: object's resource_pool
        """
        return self.resource_pool

    def resource_pool_is_empty(self):
        """
        Check if resource_pool has a value
        :return:
        """
        if self.resource_pool == None:
            return True
        return False

    def resource_pool_to_string(self):
        """
        Convert resource_pool value to a string and return it
        :return: string of resource_pool
        """
        return str(self.resource_pool)


    def set_guest_os_name(self, guest_os_name):
        """
        Set guest_os_name
        :param guest_os_name:
        :return: None
        """
        self.guest_os_name = guest_os_name
    def get_guest_os_name(self):
        """
        Get the object's guest_os_name
        :return: object's guest_os_name
        """
        return self.guest_os_name
    def guest_os_name_is_empty(self):
        """
        Check if guest_os_name has a value
        :return:
        """
        if self.guest_os_name == None:
            return True
        return False
    def guest_os_name_to_string(self):
        """
        Convert guest_os_name value to a string and return it
        :return: string of guest_os_name
        """
        return str(self.guest_os_name)