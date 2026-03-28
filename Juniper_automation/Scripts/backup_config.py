import os
import yaml
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from jnpr.junos import Device

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
BASE = "/home/deb/automation/Juniper_automation"
BKP_DIR = f"{BASE}/Backups"

os.makedirs(BKP_DIR, exist_ok=True)

with open(f"{BASE}/inventory.yaml") as f:
    inv = yaml.safe_load(f)

print(f"📡 Starting backup of {len(inv['juniper_devices'])} devices...")

for dev_info in inv["juniper_devices"]:
    name, ip = dev_info["name"], dev_info["ip"]
    
    try:
        with Device(host=ip, user=USERNAME, passwd=PASSWORD, gather_facts=False) as dev:
            print(f"🚀 Connecting to {name} ({ip})...")
            
            # CE Routers (14.1) don't support 'set' format via RPC
            # So we use 'text' for CEs and 'set' for the rest
            fmt = 'text' if 'CE' in name else 'set'
            
            config_data = dev.rpc.get_config(options={'format': fmt})
            
            if config_data is not None and hasattr(config_data, 'text'):
                config_text = config_data.text
                with open(f"{BKP_DIR}/{name}.conf", "w") as f:
                    f.write(config_text)
                print(f"  ✅ {name} backed up ({fmt} format).")
            else:
                print(f"  ⚠️  {name} returned no data.")
                
    except Exception as e:
        print(f"  ❌ {name} failed: {e}")

# 4. GitHub Sync
print("\n☁️ Pushing to GitHub...")
os.chdir(BASE)
try:
    # First, add the modified script itself and the backups
    subprocess.run(["git", "add", "Scripts/backup_config.py", "Backups/"], check=True)
    
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    # Check if there are actually changes to commit to avoid exit status 1
    status = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if status.returncode != 0:
        subprocess.run(["git", "commit", "-m", f"Backup {ts}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🚀 Success! Lab is safe in the cloud.")
    else:
        print("ℹ️ No changes to commit.")
except Exception as e:
    print(f"  ⚠️ Git sync failed: {e}")