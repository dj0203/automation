The Role of .items()
In Python, a dictionary consists of Keys and Values.

Keys: Your management IPs ("172.20.20.3").

Values: The inner dictionary containing the interface details ({"intf": "eth1", ...}).

When you call nodes.items(), you are telling Python to "unpack" the dictionary into a list of pairs (tuples) so you can look at the Key and the Value at the same time. Without .items(), a standard for x in nodes: loop would only give you the IP addresses and ignore the configuration data.

The Role of ip and params
These are temporary variables that exist only inside the loop. Think of them as placeholders for the current "row" the script is processing:

ip: This takes the Key from your dictionary.

It is used in Device(host=ip) to tell the script exactly which container to SSH into.

params: This takes the Value associated with that key.

In your code, params is itself a small dictionary (e.g., {"intf": "eth1", "ip_address": "10.1.1.1/24"}).

This is passed into template_vars=params.

How they interact with the Jinja2 Template ? 
This is where the magic happens for your automation. When you pass params into the cu.load() function, the Jinja2 engine looks inside that variable to find the labels you used in your .j2 file.

Variable in Python (params),Placeholder in Template (.j2),Resulting Configuration
"""intf"": ""eth1""",{{ intf }},set interfaces eth1...
"""ip_address"": ""10.1.1.1/24""",{{ ip_address }},...address 10.1.1.1/24