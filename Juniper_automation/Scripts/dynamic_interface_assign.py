from jnpr.junos import Device
from jnpr.junos.utils.config import Config 

devices = {
    "172.20.20.2" : {"intf":"eth1"}, 
    "172.20.20.3" : {"intf":"eth1"},
}
subnet = "10.1.1"
for count, (ip,params) in enumerate(devices.items(),start=1):
    ip_address= f"{subnet}.{count}/24"
    params["ip_address"] = ip_address
    print(f"Applying interface configuration on Device {ip} interface {params['intf']} gets {ip_address}")
    with Device (host = ip , user = "root" , passwd = "Juniper") as dev: 
        cu = Config(dev)
        cu.load(template_path="interface_template.j2" , template_vars=params, format = "set")
        cu.commit()

