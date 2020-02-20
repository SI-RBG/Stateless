#################################################################################
## Configure the vSphere Provider
provider "vsphere" {
  user                 = var.vsphere_user
  password             = var.vsphere_password
  vsphere_server       = var.vsphere_server
  allow_unverified_ssl = true
}


# General Configrations

# Choose your DC 
data "vsphere_datacenter" "dc" {
  name = var.dc_name
}

# Choose your DC 
data "vsphere_datastore" "datastore" {
  name          = var.datastore_name
  datacenter_id = data.vsphere_datacenter.dc.id
}

# Use a resource pool "Requried for vcneter"
data "vsphere_resource_pool" "pool" {
  name          = var.resourcepool_name
  datacenter_id = data.vsphere_datacenter.dc.id
}

# Choose your network (aka port group)
data "vsphere_network" "network" {
  name          = var.network_name
  datacenter_id = data.vsphere_datacenter.dc.id
}

# Deploy vm from a template
data "vsphere_virtual_machine" "template" {
  name          = var.template_name
  datacenter_id = data.vsphere_datacenter.dc.id
}

resource "vsphere_folder" "parentfolder" {
  count = 4
  path          = "Team-${count.index}"
  type          = "vm"
  datacenter_id = data.vsphere_datacenter.dc.id
}

## Customize your vm
resource "vsphere_virtual_machine" "TEST-VM" {
  count = 4 //  .${count.index}  var.teams2[count.index]
  name              = "${var.hostname}_0${count.index}" // .${var.teams2[count.index]}
  resource_pool_id  = data.vsphere_resource_pool.pool.id
  datastore_id      = data.vsphere_datastore.datastore.id
  folder            = "Team-${count.index}"
  ## Uncomment below line if you use datastore clusters/RDS and comment out the line above.
  #datastore_cluster_id    = "${data.vsphere_datastore_cluster.datastore_cluster.id}"

  # Adjust the CPUs/Memory as needed
  num_cpus  = 2
  memory    = 2048
  guest_id  = data.vsphere_virtual_machine.template.guest_id
  scsi_type = data.vsphere_virtual_machine.template.scsi_type
  network_interface {
  network_id   = data.vsphere_network.network.id
  adapter_type = data.vsphere_virtual_machine.template.network_interface_types[0]
  }
disk {
  label            = "disk0"
  size             = data.vsphere_virtual_machine.template.disks[0].size
  eagerly_scrub    = data.vsphere_virtual_machine.template.disks[0].eagerly_scrub
  thin_provisioned = data.vsphere_virtual_machine.template.disks[0].thin_provisioned
  }

clone {
  template_uuid = data.vsphere_virtual_machine.template.id
  customize {
     linux_options {
       /* The name can contain alphanumeric characters and the hyphen (-) character.
       It cannot contain periods (.) or blank spaces and cannot be made up of digits only.
        Names are not case-sensitive.
        */
       host_name = "${var.hostname}-${count.index}"
       domain    = var.domain
     }
     network_interface {
       ipv4_address = "10.100.100.${count.index}"
       ipv4_netmask = "${var.netmask}"
     }
     ipv4_gateway    = "${var.gateway}"
     dns_server_list = "${var.dns}"
     }
  }
}


