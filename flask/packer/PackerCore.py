"""
File name: PackerCore.py
Purpose: Provide the necessary functionalities to communicate with Paker.
"""

#import packerpy
from packerpy import PackerExecutable
from packer.PackerUtilities import *
from packer.PackerConfig import *
from Utilities import *
import packer.pyPacker
from lib import pyTeamObject, pyCompetitionObject, pyVMObject, Stateless
import os, sys, threading



def packerBuild(pyVMObject, pyPackerObject, template, template_vars):
    """
    This function builds a VM/VM_Template from a json packer template.
    :param pyVMObject: This is a VM object type.
    :param pyPackerObject: This is an packerObject object type.
    :param template: json
    :param template_vars: changeable variables in template
    :return:
    """
    try:
        (ret, out, err) = p.build(template, var=template_vars)
        ip = getIP(out)
        debugMessage("Assigning {} to VM".format(ip))
        pyVMObject.set_IP_Address(ip)
        s = str(out.decode("utf-8"))
        debugMessage(s)
    except:
        debugMessage("Failed")
        debugMessage("Error #89237236789")


def createPlayground():
    pass


def PackerCoreDeploy(pyCompOb):
    """
    This function deploys the play gerund team.
    :param pyCompOb: This is a pyCompObject object type.
    :return: True or False
    """
    # Get env vars
    vcenter_ip_env = os.environ.get('VCENTER_IP')
    vcenter_user_env = os.environ.get('VCENTER_USER')
    vcenter_password_env = os.environ.get('VCENTER_PASSWORD')
    debugMessage("vcenter_ip_env:"+vcenter_ip_env)
    debugMessage("vcenter_user_env:" + vcenter_user_env)

    # Create StatelessObj
    so = Stateless.StatelessObj(vcenter_ip_env, vcenter_user_env, vcenter_password_env)
    # Login
    si = so.login()

    # Create a vSwitch for
    so.Create_vSwitch(vcenter_ip_env,"StatelessPlaygroundvSwitch")
    # Create a PortGroup
    so.Create_PortGroup(vcenter_ip_env, "StatelessPlaygroundvSwitch", "StatelessPlaygroundvPG", 0)
    # Logout
    so.logout(si)

    # Create an upstream for the playground LAN.
    # Check if the VM already exists
    # If exists turn it on
    # If it doesn't exist create it and make sure it's on all the time.

    # Get a sample for just one team.
    VMs = pyCompOb.get_sample_vms()

    debugMessage("Connecting to "+str(vcenter_ip_env)+" to start deploying")
    debugMessage(str(len(VMs))+" VMs will be created")

    try:
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
            pp.set_disk_size(int(vm.get_Disk_Space()) * 1024)
            pp.set_guest_os_type(vm.get_Guest_Type())
            pp.set_guest_os_name(vm.get_Guest_Name())
            pp.set_iso_paths(vm.get_ISO_Path())
            # For now, this should match the preseed.cfg file.
            pp.set_username("stateless")
            pp.set_password("stateless")
            #pp.set_username(vm.get_VM_Uname())
            #pp.set_password(vm.get_VM_Uname())


            if vm.shellinline_is_empty():
                pp.set_shellinline("whoami")
            else:
                pp.set_shellinline(vm.get_shellinline())

            template, template_vars = pp.get_Template_and_Template_Vars()
            debugMessage(str(template))
            if template is not None:
                threading.Thread(target=packerBuild, args=(vm, pp, template, template_vars,)).start()
                #ip = getIP(out)
                #print("The IP is :" + str(ip))
        return True
    except:
        return False

