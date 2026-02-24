import yaml
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from dotenv import load_dotenv
import os
import ipaddress

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

ce_subnets =list(ipaddress.ip_network("172.16.0.0/16").subnets(new_prefix=30))
isp_subnets = list(ipaddress.ip_network("10.1.0.0/16").subnets(new_prefix=30))

ce_counter = 0
isp_counter =0

def connect(ip,username,password): 
    return Device(host=ip,user = username , passwd = password)
with open("/home/deb/projects/automation/Juniper_automation/inventory.yaml") as f:
    inventory = yaml.safe_load(f)

role_map={}
ip_map = {}
for device in inventory["juniper_devices"]:
    role_map[device["name"]] = device["role"]
    ip_map[device["name"]] = device["ip"]

for link in inventory["links"]:
    source_device = link["source"]
    source_interface = link["source_intf"]
    target_device = link["target"]
    target_interface = link["target_intf"]
    source_role = role_map[source_device]
    target_role = role_map[target_device]
    if source_role == "ce" or target_role == "ce":
        subnet = ce_subnets[ce_counter]
        ce_counter +=1
    else:
        subnet_type = "isp"
        subnet = isp_subnets[isp_counter]
        isp_counter +=1
    
    hosts = list(subnet.hosts())
    source_ip = f"{hosts[0]}/30"
    target_ip = f"{hosts[1]}/30"

    print (f"{source_device} {source_interface}:{source_ip}")
    print (f"{target_device} {target_interface}:{target_ip}")

    #Push the config on source interface
    with connect(ip_map[source_device],username,password) as dev:
        cu = Config(dev)
        cu.load(template_path="/home/deb/projects/automation/Juniper_automation/Templates/interface_template.j2",template_vars={"intf": source_interface, "ip_address": source_ip},format="set")
        cu.commit()
        print(f"{source_device} configured")
   #Push the config on target interface 
    with connect(ip_map[target_device],username,password) as dev:
        cu = Config(dev)
        cu.load(template_path="/home/deb/projects/automation/Juniper_automation/Templates/interface_template.j2",template_vars={"intf": target_interface, "ip_address": target_ip},format="set")
        cu.commit()
        print(f"{target_device} configured")
    



