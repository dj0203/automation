import os
import yaml
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Corrected base path based on your terminal output
BASE_PATH = "/home/deb/automation/Juniper_automation"
lo_ip_prefix = "1.1.1"
iso_ip_prefix = "49.0001.0000.0000"

def connect(ip):
    return Device(host=ip, user=username, passwd=password)

with open(f"{BASE_PATH}/inventory.yaml") as f:
    inventory = yaml.safe_load(f)

for count, device in enumerate(inventory["juniper_devices"], start=1):
    name = device["name"]
    mgmt_ip = device["ip"]
    role = device["role"]
    
    lo_addr = f"{lo_ip_prefix}.{count}/32"
    iso_addr = f"{iso_ip_prefix}.000{count}.00"
    
    print(f"\n⚡ Configuring {name} ({role})")

    try:
        with connect(mgmt_ip) as dev:
            cu = Config(dev)
            
            cu.load(f"set system host-name {name}", format="set")
            # 1. Load Loopback Configuration
            cu.load(template_path=f"{BASE_PATH}/Templates/loopback.j2", 
                    template_vars={"lo_ip": lo_addr}, 
                    format="set")
            
            # 2. Load Protocol Configuration (Only for non-CE routers)
            if role != "ce":
                # Find all links where this device is the source or target
                device_links = []
                for link in inventory.get("links", []):
                    if link["source"] == name:
                        device_links.append(link["source_intf"])
                    elif link["target"] == name:
                        device_links.append(link["target_intf"])

                for intf in device_links:
                    cu.load(template_path=f"{BASE_PATH}/Templates/protocols.j2",
                            template_vars={"iso_ip": iso_addr, "intf": intf},
                            format="set")
                    print(f"   - Added protocols for {intf}")

            # 3. Commit everything at once
            if cu.diff():
                print(f"   Pushing changes to {name}...")
                cu.commit()
                print(f"   ✅ {name} loopback and protocols configured.")
            else:
                print(f"   ℹ️ No changes needed for {name}.")

    except Exception as e:
        print(f"   ❌ Failed to configure {name}: {e}")

print("\n✨ Core Infrastructure Deployment Complete!")