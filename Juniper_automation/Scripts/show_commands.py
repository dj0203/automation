from jnpr.junos import Device
from dotenv import load_dotenv
import os
import yaml

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Load inventory file 
with open("/home/deb/projects/automation/Juniper_automation/inventory.yaml") as f: 
    inventory = yaml.safe_load(f) #becomes a dictionary

for devices in inventory["juniper_devices"] : #So `inventory["juniper_devices"]` gives the list of devices
    print(f"\n Logging into device {devices['name']}")
    with Device(host=devices['ip'],user = username , passwd =password) as dev: 
        output = dev.cli("show interfaces terse" ,warning =False)
        version = dev.cli("show version" ,warning =False)
        isis_up = dev.cli("show isis adjacency" ,warning=False)
        isis_interface = dev.cli("show isis interface" , warning=False)
        ldp_up = dev.cli("show ldp neighbor" ,warning =False)
        show_route = dev.cli("show route",warning = False)
        show_chassis = dev.cli("show chassis fpc" , warning = False)
        print(output)
        print(version)
        print(isis_up)
        print(isis_interface)
        print(ldp_up)
        print(show_route)
        print(show_chassis)