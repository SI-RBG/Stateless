"""
This a class to hold values for terraform templates.


"""

class terraformObject:

    def __init__(self):
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

    def set_dc_name(self, dc_name):
        """
        Set dc_name
        :param dc_name:
        :return: None
        """
        self.dc_name = dc_name

    def get_dc_name(self):
        """
        Get the object's dc_name
        :return: object's dc_name
        """
        return self.dc_name

    def dc_name_is_empty(self):
        """
        Check if dc_name has a value
        :return:
        """
        if self.dc_name == None:
            return True
        return False

    def dc_name_to_string(self):
        """
        Convert dc_name value to a string and return it
        :return: string of dc_name
        """
        if type(self.dc_name) != str:
            return str(self.dc_name)
        return self.dc_name

    def set_datastore_name(self, datastore_name):
        """
        Set datastore_name
        :param datastore_name:
        :return: None
        """
        self.datastore_name = datastore_name

    def get_datastore_name(self):
        """
        Get the object's datastore_name
        :return: object's datastore_name
        """
        return self.datastore_name

    def datastore_name_is_empty(self):
        """
        Check if datastore_name has a value
        :return:
        """
        if self.datastore_name == None:
            return True
        return False

    def datastore_name_to_string(self):
        """
        Convert datastore_name value to a string and return it
        :return: string of datastore_name
        """
        if type(self.datastore_name) != str:
            return str(self.datastore_name)
        return self.datastore_name

    def set_resourcepool_name(self, resourcepool_name):
        """
        Set resourcepool_name
        :param resourcepool_name:
        :return: None
        """
        self.resourcepool_name = resourcepool_name

    def get_resourcepool_name(self):
        """
        Get the object's resourcepool_name
        :return: object's resourcepool_name
        """
        return self.resourcepool_name

    def resourcepool_name_is_empty(self):
        """
        Check if resourcepool_name has a value
        :return:
        """
        if self.resourcepool_name == None:
            return True
        return False

    def resourcepool_name_to_string(self):
        """
        Convert resourcepool_name value to a string and return it
        :return: string of resourcepool_name
        """
        if type(self.resourcepool_name) != str:
            return str(self.resourcepool_name)
        return self.resourcepool_name

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

    def set_domain(self, domain):
        """
        Set domain
        :param domain:
        :return: None
        """
        self.domain = domain

    def get_domain(self):
        """
        Get the object's domain
        :return: object's domain
        """
        return self.domain

    def domain_is_empty(self):
        """
        Check if domain has a value
        :return:
        """
        if self.domain == None:
            return True
        return False

    def domain_to_string(self):
        """
        Convert domain value to a string and return it
        :return: string of domain
        """
        if type(self.domain) != str:
            return str(self.domain)
        return self.domain

    def set_network_name(self, network_name):
        """
        Set network_name
        :param network_name:
        :return: None
        """
        self.network_name = network_name

    def get_network_name(self):
        """
        Get the object's network_name
        :return: object's network_name
        """
        return self.network_name

    def network_name_is_empty(self):
        """
        Check if network_name has a value
        :return:
        """
        if self.network_name == None:
            return True
        return False

    def network_name_to_string(self):
        """
        Convert network_name value to a string and return it
        :return: string of network_name
        """
        if type(self.network_name) != str:
            return str(self.network_name)
        return self.network_name

    def set_template_name(self, template_name):
        """
        Set template_name
        :param template_name:
        :return: None
        """
        self.template_name = template_name

    def get_template_name(self):
        """
        Get the object's template_name
        :return: object's template_name
        """
        return self.template_name

    def template_name_is_empty(self):
        """
        Check if template_name has a value
        :return:
        """
        if self.template_name == None:
            return True
        return False

    def template_name_to_string(self):
        """
        Convert template_name value to a string and return it
        :return: string of template_name
        """
        if type(self.template_name) != str:
            return str(self.template_name)
        return self.template_name

    def set_hostname(self, hostname):
        """
        Set hostname
        :param hostname:
        :return: None
        """
        self.hostname = hostname

    def get_hostname(self):
        """
        Get the object's hostname
        :return: object's hostname
        """
        return self.hostname

    def hostname_is_empty(self):
        """
        Check if hostname has a value
        :return:
        """
        if self.hostname == None:
            return True
        return False

    def hostname_to_string(self):
        """
        Convert hostname value to a string and return it
        :return: string of hostname
        """
        if type(self.hostname) != str:
            return str(self.hostname)
        return self.hostname

    def set_ipaddress(self, ipaddress):
        """
        Set ipaddress
        :param ipaddress:
        :return: None
        """
        self.ipaddress = ipaddress

    def get_ipaddress(self):
        """
        Get the object's ipaddress
        :return: object's ipaddress
        """
        return self.ipaddress

    def ipaddress_is_empty(self):
        """
        Check if ipaddress has a value
        :return:
        """
        if self.ipaddress == None:
            return True
        return False

    def ipaddress_to_string(self):
        """
        Convert ipaddress value to a string and return it
        :return: string of ipaddress
        """
        if type(self.ipaddress) != str:
            return str(self.ipaddress)
        return self.ipaddress

    def set_netmask(self, netmask):
        """
        Set netmask
        :param netmask:
        :return: None
        """
        self.netmask = netmask

    def get_netmask(self):
        """
        Get the object's netmask
        :return: object's netmask
        """
        return self.netmask

    def netmask_is_empty(self):
        """
        Check if netmask has a value
        :return:
        """
        if self.netmask == None:
            return True
        return False

    def netmask_to_string(self):
        """
        Convert netmask value to a string and return it
        :return: string of netmask
        """
        if type(self.netmask) != str:
            return str(self.netmask)
        return self.netmask

    def set_gateway(self, gateway):
        """
        Set gateway
        :param gateway:
        :return: None
        """
        self.gateway = gateway

    def get_gateway(self):
        """
        Get the object's gateway
        :return: object's gateway
        """
        return self.gateway

    def gateway_is_empty(self):
        """
        Check if gateway has a value
        :return:
        """
        if self.gateway == None:
            return True
        return False

    def gateway_to_string(self):
        """
        Convert gateway value to a string and return it
        :return: string of gateway
        """
        if type(self.gateway) != str:
            return str(self.gateway)
        return self.gateway

    def set_dns(self, dns):
        """
        Set dns
        :param dns:
        :return: None
        """
        self.dns = dns

    def get_dns(self):
        """
        Get the object's dns
        :return: object's dns
        """
        return self.dns

    def dns_is_empty(self):
        """
        Check if dns has a value
        :return:
        """
        if self.dns == None:
            return True
        return False

    def dns_to_string(self):
        """
        Convert dns value to a string and return it
        :return: string of dns
        """
        if type(self.dns) != str:
            return str(self.dns)
        return self.dns

