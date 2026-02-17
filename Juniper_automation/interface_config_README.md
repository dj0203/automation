The Automation Engine (Python & Jinja2)
The script follows a Source of Truth model, separating data (the dictionary) from logic (the script) and structure (the template).

The Loop Logic Explained
The code iterates through the nodes dictionary using .items() to unpack your data:

nodes.items(): This method converts the dictionary into a list of pairs so Python can handle both the Key and Value simultaneously.

ip (The Key): Acts as the destination address for the Device(host=ip) connection.

params (The Value): A sub-dictionary containing the variables (intf, ip_address) that are passed into the Jinja2 template.

Deployment Script (interface_config.py)
Python
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# DATA: Source of Truth
nodes = {
    "172.20.20.3": {"intf": "eth1", "ip_address": "10.1.1.1/24"},
    "172.20.20.2": {"intf": "eth1", "ip_address": "10.1.1.2/24"}
}

# LOGIC: Execution Loop
for ip, params in nodes.items():
    print(f"Applying config to {ip}")
    with Device(host=ip, user="root", passwd="YourPassword") as dev:
        cu = Config(dev)
        # Pass 'params' into 'template_vars' to fill the {{ placeholders }}
        cu.load(template_path="interface_template.j2", template_vars=params, format="set")
        cu.commit()
The Template (interface_template.j2)
Code snippet
set interfaces {{ intf }} unit 0 family inet address {{ ip_address }}