from jnpr.junos import Device
import yaml
import os
from dotenv import load_dotenv

load_dotenv()
username= os.getenv("USERNAME")
password = os.getenv("PASSWORD")

def connect(ip,username,password):
    return Device(host=ip,user=username,passwd=password)

with open("/home/deb/projects/automation/Juniper_automation/inventory.yaml") as f:
    inventory=yaml.safe_load(f)

for devices in inventory["juniper_devices"]:
    print (f"Connecting to {devices['name']} and IP {devices['ip']}")
    with connect(devices['ip'],username,password)as dev:
        output = dev.cli("show version" , warning=False)
        print(output)

