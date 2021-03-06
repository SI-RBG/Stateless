"""
File name: Stateless.py
Purpose: Hold vSphere common variables like Admin credentials, Datacenter, Datastore, Cluster and Resources pool.
"""

from pyVmomi import vim
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
import atexit
import argparse
import getpass
import ssl
import re



class StatelessObj():

    def __init__(self, vcenter_ip, vcenter_user, vcenter_password):
        """
        :param vcenter_ip: ip address ,Type: string
        :param vcenter_user: username ,Type: string
        :param vcenter_password: password ,Type: string
        """
        self.vcenter_ip = vcenter_ip
        self.vcenter_user = vcenter_user
        self.vcenter_password = vcenter_password

        # Changeable
        self.datacenter = None
        self.datastore = None
        self.cluster = None
        self.RP = None

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

    def set_RP(self, RP):
        """
        Set RP
        :param RP:
        :return: None
        """
        self.RP = RP

    def get_RP(self):
        """
        Get the object's RP
        :return: object's RP
        """
        return self.RP

    def RP_is_empty(self):
        """
        Check if RP has a value
        :return:
        """
        if self.RP == None:
            return True
        return False

    def RP_to_string(self):
        """
        Convert RP value to a string and return it
        :return: string of RP
        """
        return str(self.RP)

    
    def login(self):
        """
        login function take vcenter ip, user, password and sign in to retrive a service instance.
        :param vcenter_ip: vcenter ip address
        :param vcenter_user:  vcenter username 
        :param vcenter_password: vcenter password
        :return: service instance content object
        """
        #Connectin to vCenter
        context = ssl._create_unverified_context()
        serviceInstance = SmartConnect(host=self.vcenter_ip,
                            user=self.vcenter_user,
                            pwd=self.vcenter_password,
                            port=int(443), sslContext=context)
        if not serviceInstance:
            print("Could not connect to the specified host using specified "
                    "username and password")
            return -1
        atexit.register(Disconnect, serviceInstance)
        return serviceInstance


    def logout(self, si):
        """
        logout function to logout 
        :param si: service instance
        :return: N/A
        """
        si.content.sessionManager.Logout()


    def retrive_content(self, si):
        """
        retrive content from a service instance
        :param si: service instance
        :return: service instance content 
        """
        content = si.RetrieveContent()
        return content


    def get_obj(self,content, vimtype, name):
        """
        take the content and type of vim and name and return the object
        :param content: service instance content
        :param vimtype: the type of vim
        :param the name of the object
        :return: The object in question 
        """
        obj = None
        container = content.viewManager.CreateContainerView(
            content.rootFolder, vimtype, True)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj


    def wait_for_task(self,task):
        """
        wait for a vCenter task to finish 
        :param task: task to be waited for
        :return N/A
        """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                return task.info.result

            if task.info.state == 'error':
                print("there was an error")
                task_done = True


    def mkdir_task(self, base_obj, dir_name):
        """
        helper function takes the base object and dir name and creat the folder with dir name
        :param base_obj: base object
        :param dir_name: folder name
        :returns: the base object
        """
        try:
            return base_obj.CreateFolder(dir_name)
        except (vim.fault.InvalidName) as e:
            print(e)
            import sys


    def create_folder(self, content, base_obj, folder_path):
        """
        takes the content, base object and nested folder pathe and creats that folder dirctory
        :param content: service instance content
        :param base_obj: base object
        :param folder_path: nested path e.g. /folder1/folder2/folder3
        :return : N/A
        """
        folder_path_parts = folder_path.strip('/').split('/')
        for path_part in folder_path_parts:
            if base_obj.childEntity:
                for y, child_obj in enumerate(base_obj.childEntity):
                    if child_obj.name == path_part:
                        base_obj = child_obj
                        break
                    elif y >= len(base_obj.childEntity)-1:
                        base_obj = self.mkdir_task(base_obj, path_part)
                        break
            else:
                base_obj = self.mkdir_task(base_obj, path_part)


    def test_create_folder(self,content, folder_path):
        """
        test the functionality of create_folder and check whether the folder exist or not
        :param content: service instance content
        :param folder_path: nested path e.g. /folder1/folder2/folder3
        """
        try:
            dc = self.get_obj(content, [vim.Datacenter], self.datacenter)
            if (self.get_obj(content, [vim.Folder], folder_path)):
                print("Folder '%s' already exists" % folder_path)
                return 1
            else:
                #self.create_folder(content, dc.hostFolder, folder_path)
                #print("Successfully created the host folder '%s'" % folder_path)
                self.create_folder(content, dc.vmFolder, folder_path)
                print("Successfully created the VM folder '%s'" % folder_path)
                return 1
        except:
            return 0



    def GetVMHosts(self,content):
        """
        get VM hosts view
        :param content: service instance content
        :return object of VM hosts
        """
        host_view = content.viewManager.CreateContainerView(content.rootFolder,[vim.HostSystem],True)
        obj = [host for host in host_view.view]
        host_view.Destroy()
        return obj


    def Create_vSwitch(self, vcenter, vswitch_Name):
        """
        create a virtual switch to the vcenter
        :param hosts: hosts to create virtual switch to
        :param vswitch_Name: the vswitch name 
        :return : N/A
        """
        for host in vcenter:
            try:
                vswitch_spec = vim.host.VirtualSwitch.Specification()
                vswitch_spec.numPorts = 1024
                vswitch_spec.mtu = 1450
                host.configManager.networkSystem.AddVirtualSwitch(vswitch_Name,vswitch_spec)
            except vim.fault.AlreadyExists:
                print("vSwitch {} alredy exist".format(vswitch_Name))


    def Create_PortGroup(self,vcenter, vswitch_Name, PG_Name, vlanId):
        """
        create a port group to the vcenter and add it to a virtual switch with a spesfic vlan ID
        :param hosts: hosts to create virtual switch to
        :param vswitch_Name: the vswitch name 
        :param PG_Name: port group name
        :param vlanId: vlan id number
        :return : N/A
        """
        for host in vcenter:
            try:
                portgroup_spec = vim.host.PortGroup.Specification()
                portgroup_spec.vswitchName = vswitch_Name
                portgroup_spec.name = PG_Name
                portgroup_spec.vlanId = int(vlanId)
                network_policy = vim.host.NetworkPolicy()
                network_policy.security = vim.host.NetworkPolicy.SecurityPolicy()
                network_policy.security.allowPromiscuous = True
                network_policy.security.macChanges = False
                network_policy.security.forgedTransmits = False
                portgroup_spec.policy = network_policy
                host.configManager.networkSystem.AddPortGroup(portgroup_spec)
            except vim.fault.AlreadyExists:
                    print("Port group {} alredy exist in vSwitch {} ".format(PG_Name, vswitch_Name))        


    def add_nic(self,content, VM, PG_Name):
        """
        create a network interface card for a specfic vm and attach it to a port group
        :param content: service instance content
        :param VM: the vm to add the nic to  
        :param PG_Name: port group name
        :return : N/A
        """
        spec = vim.VM.ConfigSpec()
        nic_changes = []

        nic_spec = vim.VM.device.VirtualDeviceSpec()
        nic_spec.operation = vim.VM.device.VirtualDeviceSpec.Operation.add

        nic_spec.device = vim.VM.device.VirtualE1000()

        nic_spec.device.deviceInfo = vim.Description()
        nic_spec.device.deviceInfo.summary = 'vCenter API test'

        network = self.get_obj(content, [vim.Network], PG_Name)
        if isinstance(network, vim.OpaqueNetwork):
            nic_spec.device.backing = vim.VM.device.VirtualEthernetCard.OpaqueNetworkBackingInfo()
            nic_spec.device.backing.opaqueNetworkType = network.summary.opaqueNetworkType
            nic_spec.device.backing.opaqueNetworkId = network.summary.opaqueNetworkId
        else:
            nic_spec.device.backing = vim.VM.device.VirtualEthernetCard.NetworkBackingInfo()
            nic_spec.device.backing.useAutoDetect = False
            nic_spec.device.backing.deviceName = network.name

        nic_spec.device.connectable = vim.VM.device.VirtualDevice.ConnectInfo()
        nic_spec.device.connectable.startConnected = True
        nic_spec.device.connectable.allowGuestControl = True
        nic_spec.device.connectable.connected = False
        nic_spec.device.connectable.status = 'untried'
        nic_spec.device.wakeOnLanEnabled = True
        nic_spec.device.addressType = 'assigned'

        nic_changes.append(nic_spec)
        spec.deviceChange = nic_changes
        #e = VM.ReconfigVM_Task(spec=spec)
        print("NIC CARD ADDED")


    
    def clone_vm(self,content, VM_Name, Template_Name, Folder_Path, IP_Address, Gateway,NetMask, DNS_Server):
        """
        clone a virtual machine from a template
        :param content: service instance content
        :param VM_Name: the virtual machine name
        :param Template_Name: template name to be cloned
        :param IP_Address: ip adress of the VM
        :param Gateway: the Gateway of the virtual machine
        :param NetMask: network mask
        :param DNS_Server: the DNS server
        :return N/A
        """

        if self.datacenter == None:
            return -1
        if self.datastore == None:
            return -1
        if self.RP == None:
            return -1

        try:
            # if none git the first one
            datacenter = self.get_obj(content, [vim.Datacenter], self.datacenter)

            destfolder = self.get_obj(content, [vim.Folder], Folder_Path)
            # destfolder = datacenter.vmFolde
            datastore = self.get_obj(content, [vim.Datastore], self.datastore)

            # if None, get the first one
            cluster = self.get_obj(content, [vim.ClusterComputeResource], self.cluster)

            resource_pool = self.get_obj(content, [vim.ResourcePool], self.RP)

            TheTemplate = self.get_obj(content, [vim.VirtualMachine], Template_Name)

            # datastore = self.get_obj(content, [vim.Datastore], real_datastore_name)

            vmconf = vim.vm.ConfigSpec()

            # if datastorecluster_name:
            #     podsel = vim.storageDrs.PodSelectionSpec()
            #     pod = get_obj(content, [vim.StoragePod], datastorecluster_name)
            #     podsel.storagePod = pod

            #     storagespec = vim.storageDrs.StoragePlacementSpec()
            #     storagespec.podSelectionSpec = podsel
            #     storagespec.type = 'create'
            #     storagespec.folder = destfolder
            #     storagespec.resourcePool = resource_pool
            #     storagespec.configSpec = vmconf

            try:
                rec = content.storageResourceManager.RecommendDatastores(
                    storageSpec=storagespec)
                rec_action = rec.recommendations[0].action[0]
                real_datastore_name = rec_action.destination.name
            except:
                real_datastore_name = TheTemplate.datastore[0].info.name

            # set relospec
            relospec = vim.vm.RelocateSpec()
            relospec.datastore = datastore
            relospec.pool = resource_pool

            clonespec = vim.vm.CloneSpec()
            clonespec.location = relospec
            clonespec.powerOn = True

            print("cloning VM...")
            task = TheTemplate.Clone(folder=destfolder, name=VM_Name, spec=clonespec)


            #self.wait_for_task(task)

            return 1
        except Exception as e:
            print("Stateless Debug Message :" + str(e), file=sys.stderr)
            return 0


    def motd(self, content, message):
        """
        message of the day on vcenter
        :param message: message to be sent 
        :param content: service instance content
        """
        content.content.sessionManager.UpdateServiceMessage(message=message)

