from jnpr.junos import Device
from jnpr.junos.utils.config import Config 
nodes = {
    "172.20.20.3": {"intf" : "eth1" , "ip_address" : "10.1.1.1/24", "description" : "Link to R2"},
    "172.20.20.2": {"intf" : "eth1" , "ip_address" : "10.1.1.2/24", "description" : "Link to R1"}
}
for ip,params in nodes.items():
    print (f"Applying config to {ip}")
    with Device (host = ip , user = "root" , passwd = "Juniper") as dev: 
        cu = Config(dev)
        cu.load(template_path="interface_template.j2" , template_vars=params, format = "set")
        cu.commit()
print("Interface_Config Load done")
