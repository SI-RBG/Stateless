#import packerpy
from packerpy import PackerExecutable
from packer.PackerUtilities import *
from packer.PackerConfig import *
from Utilities import *
import packer.pyPacker
from lib import pyTeamObject, pyCompetitionObject, pyVMObject, Stateless
import os, sys


# template_vars = {'vc_server': 'vc.mohad.red'
#     , 'vc_username': 'controller@vsphere.local'
#     , 'vc_password': '07xAD!07xAD!*&'
#
#                  # This is the type of this template
#     , 'guest_os_type': 'ubuntu64Guest'
#
#     , 'host': 'mikasa.mohammed.red'
#     , 'vm_name': 'example-ubuntu2'
#     , 'datastore': 'datastore2'
#     , 'network': 'Group200'
#     , 'username': 'testuser'
#     , 'password': 'testuser'
#     , 'CPUs': 2
#     , 'RAM': 2048
#     , 'disk_size': 32768
#     , 'shellinline': 'ls /'
#                  }





def PackerCoreDeploy(pyCompOb):
    VMs = pyCompOb.get_sample_vms()

    vcenter_ip_env = os.environ.get('VCENTER_IP')
    vcenter_user_env = os.environ.get('VCENTER_USER')
    vcenter_password_env = os.environ.get('VCENTER_PASSWORD')

    for vm in VMs:
        pp = packer.pyPacker.packerObject()
        pp.set_vsphere_server(vcenter_ip_env)
        pp.set_vsphere_user(vcenter_user_env)
        pp.set_vsphere_password(vcenter_password_env)
        pp.set_host(pyCompOb.get_ESXI_HOST())
        pp.set_datastore(pyCompOb.get_datastore())
        pp.set_vm_name(vm.get_VM_Uname())
        pp.set_CPUs(vm.get_CPU())
        pp.set_RAM(vm.get_Memory())
        pp.set_network("Group200")
        pp.set_disk_size(int(vm.get_Disk_Space()) * 1000)
        pp.set_guest_os_type(vm.get_Guest_Type())
        # For now
        pp.set_username(vm.get_VM_Uname())
        pp.set_password(vm.get_VM_Uname())

        if vm.shellinline_is_empty():
            pp.set_shellinline("ls /")
        else:
            pp.set_shellinline(vm.get_shellinline())

        template, template_vars = pp.get_Template_and_Template_Vars()
        debugMessage(str(template))
        if template is not None:

            (ret, out, err) = p.build(template, var=template_vars)
            ip = getIP(out)
            print("The IP is :" + str(ip))


