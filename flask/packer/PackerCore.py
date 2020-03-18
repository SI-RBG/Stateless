#import packerpy
from packerpy import PackerExecutable
from packer.PackerUtilities import *
from packer.PackerConfig import *
from Utilities import *
import packer.pyPacker
from lib import pyTeamObject, pyCompetitionObject, pyVMObject, Stateless
import os, sys


def PackerCoreDeploy(pyCompOb):
    VMs = pyCompOb.get_sample_vms()

    vcenter_ip_env = os.environ.get('VCENTER_IP')
    vcenter_user_env = os.environ.get('VCENTER_USER')
    vcenter_password_env = os.environ.get('VCENTER_PASSWORD')
    debugMessage("Connecting to "+str(vcenter_ip_env)+" to start deploying")

    for vm in VMs:
        pp = packer.pyPacker.packerObject()
        pp.set_vsphere_server(vcenter_ip_env)
        pp.set_vsphere_user(vcenter_user_env)
        pp.set_vsphere_password(vcenter_password_env)
        pp.set_cluster("")
        pp.set_datacenter("")
        pp.set_resource_pool("")
        pp.set_host(pyCompOb.get_ESXI_HOST())
        pp.set_datastore(pyCompOb.get_datastore())
        pp.set_vm_name(vm.get_VM_Uname())
        pp.set_CPUs(vm.get_CPU())
        pp.set_RAM(vm.get_Memory())
        pp.set_network("Group100New")
        pp.set_disk_size(int(vm.get_Disk_Space()) * 1000)
        pp.set_guest_os_type(vm.get_Guest_Type())
        # For now, this should match the preseed.cfg file.
        pp.set_username("stateless")
        pp.set_password("stateless")
        #pp.set_username(vm.get_VM_Uname())
        #pp.set_password(vm.get_VM_Uname())


        if vm.shellinline_is_empty():
            pp.set_shellinline("ls /")
        else:
            pp.set_shellinline(vm.get_shellinline())

        template, template_vars = pp.get_Template_and_Template_Vars()
        debugMessage(str(template))
        if template is not None:

            (ret, out, err) = p.build(template, var=template_vars)
            s = str(out.decode("utf-8"))
            debugMessage(s)
            #ip = getIP(out)
            #print("The IP is :" + str(ip))


