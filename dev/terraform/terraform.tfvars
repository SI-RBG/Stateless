# The vSphere server hostname or IP to connect to. Example: "vsphere.customer.com"
vsphere_server = "vc.mohammed.local"

# The name of the datacenter you will be deploying pTFE into. Example: "DC1"
dc_name = "Datacenter0"

# The name of the datastore you want to use. Example: "datastore1". Comment this line out if you use datastore clusters
datastore_name = "datastore2"

# If you use datastore clusters (RDS) please use this variable instaed of datastore_name
#datastore_cluster_name = ""

# Comment out if you do not use resource pools if you use resource pools
resourcepool_name = "Resource1"

# The user of the pTFE host. Example: "administtor@layer0.xyz"
vsphere_user = "controller@mohammed.local"

#password of the usertodeploy for quick testing
vsphere_password = "pasword"

# The domain mame of the pTFE server. Example: "customer.com"
domain = "mohammed.red"

# The name of the vm network where you want to deploy pTFE. Example "VM Network". AKA PortGroup
network_name = "Group100"

# The name of the template you will use as a base for pTFE. Example "ubuntu_template".
template_name = "Ubuntu 18 Test"

# The name of the pTFE host, without the domain. Example: "ptfe"
hostname = "Example-VM"

# The IP Address of the server. Example: "10.0.0.100"
ipaddress = "10.100.100.88"

# The netmask of the server. Example: "24"
netmask = "24"

# The Gateway address of the server. Example: "10.0.0.1"
gateway = "10.100.100.254"

# DNS Servers to use. Example: ["1.1.1.1","1.0.0.1"]
dns = ["10.0.1.1", "1.1.1.1"]
