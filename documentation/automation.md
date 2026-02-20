How Network Automation Works
// Start here — the big picture
Before touching any code, let's understand what we're actually doing when we "automate" a network device.

Without automation: You SSH into a device, type commands one by one, and repeat for every device. 10 devices = 10x the work. A typo on device 7 means inconsistency.

With automation: You write a Python script once. It connects to all 10 devices, sends the correct config, and confirms it worked — in seconds.
Think of it like a mail merge in Word — you write one template letter, fill in names from a list, and print 1000 personalised letters automatically. Your Python script is the mail merge, and your devices are the recipients.
The 3-Step Pattern (used by ALL vendors)
1
Connect — Your Python script opens a connection to the device (SSH, NETCONF, or API depending on vendor)
2
Send Config — The script pushes configuration, either as raw CLI commands or structured data (XML/JSON)
3
Confirm & Close — Commit/save, verify it worked, disconnect cleanly
How Each Vendor Speaks
Vendor	Connection Method	Python Library	Config Format
Juniper cRPD	NETCONF (XML over SSH)	junos-eznc (PyEZ)	Junos "set" commands or XML
Cisco IOL	SSH (CLI)	netmiko	IOS CLI commands
Nokia SR Linux	gNMI or JSON-RPC	requests / pygnmi	JSON
The concepts are identical across all vendors. Only the library and syntax change. Once you understand one, the others click quickly.

// Quick Check
What Python library did you use to automate your Juniper device?
netmiko
junos-eznc (PyEZ)
paramiko
ncclient


Python Basics You Need:

// Only the parts used in your script — nothing extra
You don't need to learn all of Python. Your automation scripts use just 4 Python concepts. Let's cover them now.

1. Variables — storing information
A variable is just a labelled box. You put something in the box and refer to it by its label later.
python
copy
# A variable called "ip" holding a text value (string)
ip = "172.20.20.3"

# A variable called "port" holding a number
port = 22

# Now you can use the variable anywhere
print(ip)   # prints: 172.20.20.3
2. Dictionaries — storing related data together
A dictionary is like a form. "Name: John, Age: 30, City: Dublin". Each field (key) has a value. In Python: {"name": "John", "age": 30}
python
copy
# A dictionary holding info about ONE device
device = {
    "intf": "eth1",
    "ip_address": "10.1.1.1/24"
}

# Access a value using its key
print(device["intf"])       # prints: eth1
print(device["ip_address"])  # prints: 10.1.1.1/24
3. Nested Dictionaries — your "nodes" structure
In your script, nodes is a dictionary inside a dictionary — the key is the device IP, the value is another dict of params.

python
copy
# Outer key = device IP address
# Inner value = another dict with intf + ip_address
nodes = {
    "172.20.20.3": {"intf": "eth1", "ip_address": "10.1.1.1/24"},
    "172.20.20.2": {"intf": "eth1", "ip_address": "10.1.1.2/24"}
}

# Access: nodes[ip][key]
print(nodes["172.20.20.3"]["intf"])  # prints: eth1
4. For Loop — repeating for each device
A for loop says "for every item in this list, do this thing". It's how your script automatically handles 2 devices — or 200 — without you changing the code.
python
copy
# .items() gives you the key AND value on each loop
# ip    = "172.20.20.3"  (the key)
# params = {"intf": "eth1", ...}  (the value)
for ip, params in nodes.items():
    print(f"Connecting to {ip}")
    print(f"Interface: {params['intf']}")

# Output:
# Connecting to 172.20.20.3
# Interface: eth1
# Connecting to 172.20.20.2
# Interface: eth1


Your Juniper Script — Line by Line

// Click any line to understand what it does
● Juniper cRPD — PyEZ + NETCONF
You already ran this script successfully. Now let's understand every single line. Click each line to expand the explanation.

from jnpr.junos import Device
▶ click to explain
from jnpr.junos.utils.config import Config
▶ click to explain
nodes = {"172.20.20.3": {"intf": "eth1", "ip_address": "10.1.1.1/24"}, ...}
▶ click to explain
for ip, params in nodes.items():
▶ click to explain
    with Device(host=ip, user="root", passwd="Juniper") as dev:
▶ click to explain
        cu = Config(dev)
▶ click to explain
        cu.load(template_path="interface_template.j2", template_vars=params, format="set")
▶ click to explain
        cu.commit()
▶ click to explain
Your Jinja2 Template
interface_template.j2
copy
# {{ }} = placeholder — gets replaced by the value from params
set interfaces {{intf}} unit 0 family inet address {{ip_address}}

# When params = {"intf": "eth1", "ip_address": "10.1.1.1/24"}, this becomes:
set interfaces eth1 unit 0 family inet address 10.1.1.1/24

Cisco IOL — Same Idea, Different Library
// Using Netmiko — SSH-based CLI automation
● Cisco IOL — Netmiko + SSH
Cisco IOL doesn't support NETCONF out of the box like Juniper does. Instead, we use Netmiko — a Python library that SSH's into the device and sends CLI commands, exactly like you would manually.

Key difference from Juniper: With PyEZ, you pushed structured config (XML/set format). With Netmiko, you're sending raw CLI strings — the exact same commands you'd type in the terminal.
Step 1 — Install Netmiko
bash — run once in your terminal
copy
pip install netmiko
Step 2 — Create the script
Save this as ~/projects/automation/Cisco/interface_config.py

interface_config.py — Cisco IOL
copy
# ── Same pattern as Juniper ──────────────────────────────
# Step 1: Import the library
from netmiko import ConnectHandler

# Step 2: Define your devices (same nodes dict as Juniper!)
nodes = {
    "172.20.20.10": {"intf": "GigabitEthernet1", "ip_address": "10.1.1.1", "subnet": "255.255.255.0"},
    "172.20.20.11": {"intf": "GigabitEthernet1", "ip_address": "10.1.1.2", "subnet": "255.255.255.0"},
}

# Step 3: Loop through devices — same as Juniper
for ip, params in nodes.items():
    print(f"Applying config to {ip}")

    # Connection details — Cisco-specific device_type
    device = {
        "device_type": "cisco_ios",   # tells Netmiko what kind of device
        "host": ip,
        "username": "admin",
        "password": "admin",
    }

    # Connect — same "with" pattern as Juniper
    with ConnectHandler(**device) as net_connect:

        # Build the CLI commands using params (like your Jinja2 template)
        commands = [
            f"interface {params['intf']}",
            f"ip address {params['ip_address']} {params['subnet']}",
            "no shutdown",
        ]

        # Send config commands — equivalent to cu.load() + cu.commit()
        output = net_connect.send_config_set(commands)
        print(output)

print("Interface Config Done")
Side-by-Side: Juniper vs Cisco
Action	Juniper (PyEZ)	Cisco (Netmiko)
Import	from jnpr.junos import Device	from netmiko import ConnectHandler
Connect	Device(host=ip, user=..., passwd=...)	ConnectHandler(device_type="cisco_ios", host=ip, ...)
Send config	cu.load(template_path=...)	net_connect.send_config_set([commands])
Activate	cu.commit()	Automatic (IOS applies immediately)
Format	Junos "set" commands / XML	Plain IOS CLI strings
Notice the nodes dict and for loop are identical between Juniper and Cisco. The only thing that changes is the library name and how you send commands. Same recipe, different kitchen.
Verify it worked — inside the script
Add this after send_config_set
copy
# Check the interface after configuring it
output = net_connect.send_command(f"show interface {params['intf']}")
print(output)

Nokia SR Linux — JSON over HTTP
// Using the built-in JSON-RPC API — no extra library needed
● Nokia SR Linux — JSON-RPC API
Nokia SR Linux is a modern network OS designed from the ground up for automation. Instead of SSH/CLI, it has a built-in HTTP API that accepts JSON — like a web server for your router.

What's JSON? JSON is just a structured data format — very similar to the Python dict you already know.

Python dict:  {"name": "eth1", "ip": "10.1.1.1"}
JSON:         {"name": "eth1", "ip": "10.1.1.1"}

They look identical. Python converts between them automatically.
Step 1 — No extra install needed
We use Python's built-in requests library (for HTTP calls) and json (built in).

bash
copy
pip install requests
Step 2 — Create the script
Save as ~/projects/automation/Nokia/interface_config.py

interface_config.py — Nokia SR Linux
copy
# ── Same pattern as Juniper and Cisco ───────────────────
import requests
import json
import urllib3
urllib3.disable_warnings()  # suppress SSL warnings in lab

# Same nodes dict — same pattern!
nodes = {
    "172.20.20.20": {"intf": "ethernet-1/1", "ip_address": "10.1.1.1", "prefix_len": 24},
    "172.20.20.21": {"intf": "ethernet-1/1", "ip_address": "10.1.1.2", "prefix_len": 24},
}

# Same loop — same pattern!
for ip, params in nodes.items():
    print(f"Applying config to {ip}")

    # SR Linux JSON-RPC endpoint — it's just a URL
    url = f"https://{ip}:443/jsonrpc"

    # The config as JSON (like a Jinja2 template but in Python dict form)
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "set",
        "params": {
            "commands": [{
                "path": f"/interface[name={params['intf']}]/subinterface[index=0]/ipv4/address[ip-prefix={params['ip_address']}/{params['prefix_len']}]",
                "value": {}
            }]
        }
    }

    # Send it — like cu.load() + cu.commit() in one step
    response = requests.post(
        url,
        json=payload,
        auth=("admin", "NokiaSrl1!"),
        verify=False
    )

    print(f"Status: {response.status_code}")
    print(response.json())

print("Interface Config Done")
Full 3-Vendor Comparison
Concept	Juniper	Cisco	Nokia
Protocol	NETCONF (XML)	SSH (CLI)	HTTP (JSON)
Library	junos-eznc	netmiko	requests
Connect	Device(host, user, passwd)	ConnectHandler(device_type, host, ...)	requests.post(url, auth=...)
Send config	cu.load(template)	send_config_set([cmds])	POST JSON payload
Commit	cu.commit()	Not needed (IOS auto-applies)	Not needed (JSON-RPC applies immediately)
nodes dict	✓ Same	✓ Same	✓ Same
for loop	✓ Same	✓ Same	✓ Same
← Back
