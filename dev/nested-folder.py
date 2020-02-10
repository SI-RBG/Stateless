#!/usr/bin/env python


from __future__ import print_function
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import ssl
import argparse
import atexit
import getpass


host1 = "vcenter.layer0.xyz"
user1 = 'layer0.xyz\deployer'
password1 = "PleaseWork1!"
port1 = 443
datacenter1 = "Moonlight"
folder1 = "son"   


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def create_folder(content, host_folder, folder_name):
    host_folder.CreateFolder(folder_name)


def main():
    context = ssl._create_unverified_context()
    si = SmartConnect(host=host1,
                      user=user1,
                      pwd=password1,
                      port=int(port1), sslContext=context)
    if not si:
        print("Could not connect to the specified host using specified "
              "username and password")
        return -1

    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    print(content)
    dc = get_obj(content, [vim.Datacenter], datacenter1)
    print(dc)
    if (get_obj(content, [vim.Folder], folder1)):
        print("Folder '%s' already exists" % folder1)
        return 0
    create_folder(content, dc.hostFolder, folder1)
    print("Successfully created the host folder '%s'" % folder1)
    create_folder(content, dc.vmFolder, folder1)
    print("Successfully created the VM folder '%s'" % folder1)
    return 0

# Start program
if __name__ == "__main__":
    main()
