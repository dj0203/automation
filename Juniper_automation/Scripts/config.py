from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from dotenv import load_dotenv
import os
import yaml

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
lo_ip = "1.1.1"
iso_ip ="49.0001.0000.0000"

def connect(ip,username,password):
    return Device(host=ip,user=username,passwd=password)

with open("/home/deb/projects/automation/Juniper_automation/inventory.yaml") as f:
    inventory = yaml.safe_load(f)

for count , device in enumerate(inventory["juniper_devices"],start =1):
    name = device["name"]
    ip = device ["ip"]
    role = device["role"]
    lo_addr = f"{lo_ip}.{count}/32"
    iso_addr = f"{iso_ip}.000{count}.00"
    print(f"\n{name} → loopback {lo_addr} role {role}")
    
    with connect(ip, username, password) as dev:
        cu = Config(dev)
        cu.load(template_path="/home/deb/projects/automation/Juniper_automation/Templates/loopback.j2",template_vars={"lo_ip": lo_addr},format="set")
        cu.commit()
        print(f"  {name} loopback configured")
        
        if role != "ce":
            for intf in device["interfaces"]:
                with connect(ip, username, password) as dev:
                    cu = Config(dev)
                    cu.load(template_path="/home/deb/projects/automation/Juniper_automation/Templates/protocols.j2",
                        template_vars={"iso_ip": iso_addr, "intf": intf},
                        format="set")
                    cu.commit()
                    print(f"  {name} {intf} ISP protocols configured")
