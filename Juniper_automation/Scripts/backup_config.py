from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import yaml
from dotenv import load_dotenv
import os
from datetime import datetime
import subprocess

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
BASE = "/home/deb/automation/Juniper_automation"
BKP_DIR = f"{BASE}/Backups"
os.makedirs(BKP_DIR, exist_ok=True)

with open(f"{BASE}/inventory.yaml") as f: 
    inv = yaml.safe_load(f)
print("Pulling latest configs from Device")

for dev_info in inv["juniper_devices"]:
    name,ip = dev_info["name"], dev_info["ip"]
    try:
        with Device(host=ip,user=USERNAME,passwd=PASSWORD) as dev: 
            config = dev.rpc.get_config(options={'format': 'text'})
            with open(f"{BKP_DIR}/{name}.conf","w") as f:
                f.write(config.text)
            print(f" {name} backed up.")
    except Exception as e: 
        print(f" {name} failed: {e}")

print("\n☁️ Pushing to dj0203/automation...")
os.chdir(BASE)
try:
    subprocess.run(["git", "add", "Backups/"], check=True)
    subprocess.run(["git", "commit", "-m", f"Backup {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("Success! Your lab is now safe in the cloud.")
except Exception as e:
    print(f" Git push failed: {e}")
