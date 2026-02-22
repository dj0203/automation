# Python Reference — Lists, Dictionaries & YAML
> Based on your real Juniper automation scripts

---

## 1. List

A list is a collection of items in order. Each item has **no label** — just a value.

**When to use:** Multiple items of the same type.

```python
# A list of device IPs — just values, no labels
devices = ["192.168.0.100", "192.168.0.101", "192.168.0.102"]

# Access by position (starts at 0)
print(devices[0])  # → 192.168.0.100
print(devices[1])  # → 192.168.0.101

# Loop through a list
for ip in devices:
    print(ip)
```

> Think of it like a shopping list — "apples, bread, milk". Just values, no labels.

---

## 2. Dictionary

A dictionary stores data with **labels (keys)**. Every value has a name.

**When to use:** One item with multiple properties that have meaningful names.

```python
# A dictionary describing ONE device
device = {
    "name": "PE1",
    "ip":   "192.168.0.100",
    "role": "pe"
}

# Access by KEY (the label name)
print(device["name"])  # → PE1
print(device["ip"])    # → 192.168.0.100
print(device["role"])  # → pe
```

> Think of it like a form — "Name: PE1, IP: 192.168.0.100, Role: pe". Each field has a label.

---

## 3. List vs Dictionary

| | List `[]` | Dictionary `{}` |
|---|---|---|
| Brackets | Square `[]` | Curly `{}` |
| Items | No labels | Every item has a key |
| Access | By position `[0]` | By key `["name"]` |
| Use for | Collection of same type | One object with properties |
| Example | List of IPs | Device with name, ip, role |

---

## 4. List of Dictionaries — What Your Script Uses

You need BOTH — a list because you have multiple devices, a dictionary because each device has multiple properties.

```python
# The whole thing is a LIST (square brackets outside)
devices = [
    # Each item inside is a DICT (curly brackets)
    {"name": "PE1", "ip": "192.168.0.100", "role": "pe"},
    {"name": "P1",  "ip": "192.168.0.101", "role": "p"},
    {"name": "CE1", "ip": "192.168.0.104", "role": "ce"},
]

# Loop through the LIST, access the DICT inside
for device in devices:        # ← looping the list
    print(device["name"])     # ← accessing the dict
    print(device["ip"])
```

> Think of it like a spreadsheet — each ROW is a list item, each COLUMN is a dictionary key.

---

## 5. YAML — Why Use It?

YAML is a way to write your Python lists and dictionaries in a **separate file** instead of hardcoding them in your script. Same data, different format — cleaner and easier to edit.

**Why use YAML instead of hardcoding?**
When you have 6 devices today and 20 tomorrow, you edit the YAML file instead of your Python code.

### Your inventory.yaml

```yaml
juniper_devices:        # ← dictionary KEY
  - name: PE1           # ← dash means LIST item
    ip: 192.168.0.100   # ← dictionary keys inside each item
    role: pe
    junos: 21.4

  - name: P1            # ← second list item
    ip: 192.168.0.101
    role: p
    junos: 21.4

  - name: CE1           # ← third list item
    ip: 192.168.0.104
    role: ce
    junos: 14.1
```

**Key rule:** The dash `-` in YAML = a list item. The indented keys under it = a dictionary.

---

## 6. How It All Connects in show_commands.py

```python
import yaml

# Step 1 — load YAML file into Python
# yaml.safe_load() converts YAML → Python dictionary
with open("inventory.yaml") as f:
    inventory = yaml.safe_load(f)

# inventory is now:
# {"juniper_devices": [{"name": "PE1", "ip": "..."}, ...]}

# Step 2 — get the LIST of devices
# inventory["juniper_devices"] gives you the list
for device in inventory["juniper_devices"]:

    # Step 3 — access DICT keys for each device
    print(device["name"])   # → PE1
    print(device["ip"])     # → 192.168.0.100
    print(device["role"])   # → pe

    # Step 4 — use dict values to connect to device
    with Device(host=device["ip"], user=username, passwd=password) as dev:
        output = dev.cli("show interfaces terse", warning=False)
        print(output)
```

---

## Quick Reference

| Concept | Syntax | Access | Loop |
|---|---|---|---|
| List | `["a", "b"]` | `list[0]` | `for item in list` |
| Dictionary | `{"key": "value"}` | `dict["key"]` | `for k,v in dict.items()` |
| YAML list item | `- name: PE1` | After loading: `item["name"]` | Same as list |
| List of dicts | `[{"name": "PE1"}]` | `list[0]["name"]` | `for item in list` then `item["key"]` |