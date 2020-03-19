#import packerpy
from packerpy import PackerExecutable
from packer.PackerUtilities import *
from packer.PackerConfig import *
from Utilities import *
import os, sys
import packer.pyPacker

def PackerCoreDeploy(guest_os_type,guest_os_name,iso_path):
    vcenter_ip_env = os.environ.get('VCENTER_IP')
    vcenter_user_env = os.environ.get('VCENTER_USER')
    vcenter_password_env = os.environ.get('VCENTER_PASSWORD')
    print("connecting to " + str(vcenter_ip_env))
    pp = packer.pyPacker.packerObject()
    pp.set_vsphere_server(vcenter_ip_env)
    pp.set_vsphere_user(vcenter_user_env)
    pp.set_vsphere_password(vcenter_password_env)
    pp.set_cluster("")
    pp.set_datacenter("")
    pp.set_resource_pool("")
    pp.set_host("mikasa.mohammed.red")
    pp.set_datastore("datastore2")
    pp.set_vm_name("AAA_en_windows_server_2019_x64")
    pp.set_CPUs("4")
    pp.set_RAM(str(1024*4))
    pp.set_network("Group100New")
    pp.set_disk_size("32768")
    pp.set_guest_os_type(guest_os_type)
    pp.set_guest_os_name(guest_os_name)
    pp.set_iso_paths(iso_path)
    # For now
    pp.set_username("stateless")
    pp.set_password("stateless")

    pp.set_shellinline("whoami")

    template, template_vars = pp.get_Template_and_Template_Vars()
    print(str(template))
    if template is not None:
        (ret, out, err) = p.build(template, var=template_vars)
        s = str(out.decode("utf-8")).split("\n")
        print(s)
        #ip = getIP(out)
        #print("The IP is :" + str(ip))

def test():
    #PackerCoreDeploy("windows9Server64Guest","en_windows_server_2019_x64","[datastore2] ISOs/Windows_2019/en_windows_server_2019_x64_dvd_3c2cf1202.iso")
    PackerCoreDeploy("windows9Server64Guest", "en_windows_server_2019_x64",
                     "[datastore2] ISOs/Windows_2019/en_windows_server_2019_x64_dvd_3c2cf1202.iso")



if __name__ == '__main__':
    test()