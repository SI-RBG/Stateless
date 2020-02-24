
from pyVmomi import vim
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
from pyVmomi import vmodl
import atexit
import argparse
import getpass
import ssl
import re
import sys
import time


"Static Inputs to connect to cptc-server"

INPUTS = {'vcenter_ip': 'cptc-vcenter.csec.rit.edu',
          'vcenter_user': 'cptc.local\\wow',
          'vcenter_password': 'weho!',
          'datacenter' : 'Datacenter',
          'datastore' : 'datastore1', 
          'cluster' : 'CPTCCluster',
          'RP' :    'DevRP', 
          'dea_name': 'Pf-Template',
          'new_clone_name': 'Pfsesne-wow',
          'new_clone_domain': 'cptc.local',
          'isDHCP' : False,
          'new_clone_ip': '10.0.1.44',
          'new_clone_netmask': '255.255.255.0',
          'new_clone_gateway': '10.0.1.1',
          'new_clone_dns': '10.0.0.1',
          'vSwitch' :    'Test_vSwitch123',
          'PG' : 'Test_PG123',
          'VlanID':     '1',
          "Template_Name" : "pfSense-2-2-4-Template", 
          'VM_Name':   "pfSense-2-2-4-clone"
          }


class StatelessObj():

    def __init__(self, vcenter_ip, vcenter_user, vcenter_password):
        self.vcenter_ip = vcenter_ip
        self.vcenter_user = vcenter_user
        self.vcenter_password = vcenter_password

    
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

    def wait_for_another_task(self,task,actionName='job', hideResult=False):
        while task.info.state == vim.TaskInfo.State.running:
            time.sleep(2)
    
        if task.info.state == vim.TaskInfo.State.success:
            if task.info.result is not None and not hideResult:
                out = '%s completed successfully, result: %s' % (actionName, task.info.result)
                print(out)
            else:
                out = '%s completed successfully.' % actionName
                print (out)
        else:
            out = '%s did not complete successfully: %s' % (actionName, task.info.error)
            raise task.info.error
            print (out)
        
        return task.info.result

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
        dc = self.get_obj(content, [vim.Datacenter], INPUTS['datacenter'])
        if (self.get_obj(content, [vim.Folder], INPUTS['folder_path'])):
            print("Folder '%s' already exists" % INPUTS['folder_path'])
            return 0
        else:
            self.create_folder(content, dc.hostFolder, INPUTS['folder_path'])
            print("Successfully created the host folder '%s'" % INPUTS['folder_path'])
            self.create_folder(content, dc.vmFolder, INPUTS['folder_path'])
            print("Successfully created the VM folder '%s'" % INPUTS['folder_path'])
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


    def Create_vSwitch(self, hosts, vswitch_Name):
        """
        create a virtual switch to the vcenter
        :param hosts: hosts to create virtual switch to
        :param vswitch_Name: the vswitch name 
        :return : N/A
        """
        for host in hosts:
            try:
                vswitch_spec = vim.host.VirtualSwitch.Specification()
                vswitch_spec.numPorts = 1024
                vswitch_spec.mtu = 1450
                host.configManager.networkSystem.AddVirtualSwitch(vswitch_Name,vswitch_spec)
            except vim.fault.AlreadyExists:
                print("vSwitch {} alredy exist".format(vswitch_Name))


    def Create_PortGroup(self,hosts, vswitch_Name, PG_Name, vlanId):
        """
        create a port group to the vcenter and add it to a virtual switch with a spesfic vlan ID 
        :param hosts: hosts to create virtual switch to
        :param vswitch_Name: the vswitch name 
        :param PG_Name: port group name
        :param vlanId: vlan id number
        :return : N/A
        """
        for host in hosts:
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


    
    def clone_vm(self,content, VM_Name, Template_Name, Folder_Path,IP_Address, Gateway,NetMask, DNS_Server):
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
        # if none git the first one
        datacenter = self.get_obj(content, [vim.Datacenter], INPUTS['datacenter'])

        
        destfolder = self.get_obj(content, [vim.Folder], Folder_Path)
        #destfolder = datacenter.vmFolder

        
        datastore = self.get_obj(content, [vim.Datastore], INPUTS['datastore'])
        

        # if None, get the first one
        cluster = self.get_obj(content, [vim.ClusterComputeResource], INPUTS['cluster'])

        resource_pool = self.get_obj(content, [vim.ResourcePool], INPUTS['RP'])
        
        TheTemplate = self.get_obj(content, [vim.VirtualMachine], Template_Name)

        #datastore = self.get_obj(content, [vim.Datastore], real_datastore_name)

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
        self.wait_for_task(task)
    
    def motd(self, content, message):
        """
        message of the day on vcenter
        :param message: message to be sent 
        :param content: service instance content
        """
        content.content.sessionManager.UpdateServiceMessage(message=message)

    def assign_IP(self,si, content):
        try:
            vm_name = INPUTS['VM_Name']      
            vm = self.get_obj(content, [vim.VirtualMachine], vm_name)

            if vm.runtime.powerState != 'poweredOff':
                print("WARNING:: Power off your VM before reconfigure")
                sys.exit()

            adaptermap = vim.vm.customization.AdapterMapping()
            globalip = vim.vm.customization.GlobalIPSettings()
            adaptermap.adapter = vim.vm.customization.IPSettings()
            
            isDHDCP = INPUTS['isDHCP']
            if not isDHDCP:
                """Static IP Configuration"""
                adaptermap.adapter.ip = vim.vm.customization.FixedIp()
                adaptermap.adapter.ip.ipAddress = INPUTS['new_clone_ip']
                adaptermap.adapter.subnetMask = INPUTS['new_clone_netmask']
                adaptermap.adapter.gateway = INPUTS['new_clone_gateway']  
                globalip.dnsServerList = INPUTS['new_clone_dns']
                
            else:
                """DHCP Configuration"""
                adaptermap.adapter.ip = vim.vm.customization.DhcpIpGenerator()
                
            adaptermap.adapter.dnsDomain = INPUTS['new_clone_domain']
            
            globalip = vim.vm.customization.GlobalIPSettings()
            
            #For Linux . For windows follow sysprep
            ident = vim.vm.customization.LinuxPrep(domain=INPUTS['new_clone_domain'], hostName=vim.vm.customization.FixedName(name=vm_name))        
            
            customspec = vim.vm.customization.Specification()
            #For only one adapter
            customspec.identity = ident
            customspec.nicSettingMap = [adaptermap]
            customspec.globalIPSettings = globalip
            
            #Configuring network for a single NIC
            #For multipple NIC configuration contact me.

            print("Reconfiguring VM Networks . . .")
            
            task = vm.Customize(spec=customspec)

            # Wait for Network Reconfigure to complete
            self.wait_for_another_task(task)        
                
        except vmodl.MethodFault as msg:
            print("Caught vmodl fault: {}".format(msg))
            return 1
        except Exception as msg:
            print("Caught exception: {}".format(msg))
            return 1

def main():
    print("Starting main!")
    #Connectin to vCenter
    StatelessObj1 = StatelessObj(INPUTS['vcenter_ip'],INPUTS['vcenter_user'],INPUTS['vcenter_password'])
    si = StatelessObj1.login()
    content = StatelessObj1.retrive_content(si)
    
    #Test Folder creating
    #StatelessObj1.test_create_folder(content,INPUTS['folder_path'])

    #Test vSwitch_Creat
    #Hosts  =  StatelessObj1.GetVMHosts(content)
    #StatelessObj1.Create_vSwitch(Hosts,INPUTS['vSwitch'])

    #Test PGroup Creation 
    #StatelessObj1.Create_PortGroup(Hosts, INPUTS['vSwitch'], INPUTS['PG'], INPUTS['VlanID'])

    #Test adding NIC to a vim
    #vm = StatelessObj1.get_obj(content, [vim.VirtualMachine], "TheWorking_VM2")
    #StatelessObj1.add_nic(content, vm, INPUTS['PG'])


    #Test clonning "GOD Speed"
    Folder_Path = "Admin"
    StatelessObj1.clone_vm(content, INPUTS['VM_Name'], INPUTS['Template_Name'],Folder_Path, INPUTS['new_clone_ip'], INPUTS['new_clone_gateway'],INPUTS['new_clone_netmask'], INPUTS['new_clone_dns'])

    #Assign fixed IP addres
    #StatelessObj1.assign_IP(si,content)
    #Logout
    StatelessObj1.logout(si)


# start this thing
if __name__ == "__main__":
    main()
