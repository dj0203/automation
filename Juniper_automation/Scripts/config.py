from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
devices = {
    "172.20.20.2" : {"intf":"eth1"},
    "172.20.20.3" : {"intf":"eth1"},
}
lo_ip = "1.1.1"
iso_ip ="49.0001.0000.0000"

for count , (ip,params) in enumerate(devices.items(),start =1):
    lo_addr = f"{lo_ip}.{count}/32"
    iso_addr = f"{iso_ip}.000{count}.00"
    params["lo_ip"] = lo_addr
    params["iso_ip"] = iso_addr 
    print(f"Applying ISO & MPLS configuration on Devices with {ip} | Loopback address {params['lo_ip']} and ISO configurartion {params['iso_ip']} ")
    with Device (host = ip , user = username , passwd = password) as dev: 
        cu = Config(dev)
        cu.load(template_path="config.j2" , template_vars=params, format = "set")
        cu.commit()
