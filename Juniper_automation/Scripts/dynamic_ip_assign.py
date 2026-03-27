import os 
import yaml
import ipaddress 
from dotenv import load_dotenv
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# 1. Load credentials
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# 2. Define IP Pools as iterators
# ISP Core uses /31, Customer Edge uses /30
ISP_POOL = ipaddress.ip_network("10.1.0.0/16").subnets(new_prefix=31)
CE_POOL = ipaddress.ip_network("172.16.0.0/16").subnets(new_prefix=30)

# 3. Load inventory (Adjust path if needed)
with open("../inventory.yaml") as f: 
    inventory = yaml.safe_load(f)

# 4. Create lookup table for roles and management IPs
device_info = {
    d["name"]: {"role": d["role"], "mgmt_ip": d["ip"]}
    for d in inventory["juniper_devices"]
}

# 5. Initialize the configuration plan storage
config_plan = {name: [] for name in device_info.keys()}
isp_iter = iter(ISP_POOL)
ce_iter = iter(CE_POOL)

print(f"✅ Loaded {len(device_info)} devices. Calculating IP assignments...")

# 6. Loop through links and assign IPs
for link in inventory["links"]:
    src, tgt = link["source"], link["target"]
    src_intf, tgt_intf = link["source_intf"], link["target_intf"]

    # Logic: Use CE pool if either side is a 'ce' role
    is_ce_link = (device_info[src]["role"] == "ce") or (device_info[tgt]["role"] == "ce")

    if is_ce_link:
        subnet = next(ce_iter)
        mask = "30"
        ips = list(subnet.hosts())
    else: 
        subnet = next(isp_iter)
        mask = "31"
        ips = [subnet[0], subnet[1]]

    # Store data for both sides of the link
    config_plan[src].append({"name": src_intf, "ip": f"{ips[0]}/{mask}"})
    config_plan[tgt].append({"name": tgt_intf, "ip": f"{ips[1]}/{mask}"})
    
    print(f"  Mapped: {src} <-> {tgt} | {subnet}")

# 7. Deployment Phase
print("\n🚀 Starting Deployment to Routers...")

for router, interfaces in config_plan.items():
    if not interfaces:
        continue

    mgmt_ip = device_info[router]["mgmt_ip"]
    print(f"Connecting to {router} ({mgmt_ip})...")

    try:
        with Device(host=mgmt_ip, user=USERNAME, passwd=PASSWORD) as dev:
            cu = Config(dev)
            
            for intf_data in interfaces:
                cu.load(
                    template_path="../Templates/interface_template.j2",
                    template_vars={
                        "intf": intf_data["name"], 
                        "ip_address": intf_data["ip"]
                    },
                    format="set"
                )

            if cu.diff():
                print(f"  Pushing configuration changes to {router}...")
                cu.commit(comment=f"Automated IP assignment via dj0203 script")
            else:
                print(f"  No changes needed for {router}.")

    except Exception as e:
        print(f"  ❌ Failed to configure {router}: {e}")

print("\n✅ IP configuration complete.")