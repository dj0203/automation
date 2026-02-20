from jnpr.junos import Device
nodes = {
    "172.20.20.3" :{"name" : "R2"},
    "172.20.20.2" :{"name" : "R1"},
}

for ip,params in nodes.items():
    print(f"\n Logging into device {params['name']}")
    with Device(host=ip,user ="root" , passwd ="Juniper") as dev: 
        output = dev.cli("show interfaces terse" ,warning =False)
        version = dev.cli("show version" ,warning =False) 
        print(output)
        print(version)