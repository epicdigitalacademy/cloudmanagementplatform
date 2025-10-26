#!/usr/bin/env python3
import requests, json, os, sys

NAUTOBOT_URL = os.environ.get("NAUTOBOT_URL", "https://nautobot.local")
NAUTOBOT_TOKEN = os.environ.get("NAUTOBOT_TOKEN", "")
ROLE = os.environ.get("ROLE", "server")

if not NAUTOBOT_TOKEN:
    print("Error: Missing NAUTOBOT_TOKEN environment variable", file=sys.stderr)
    sys.exit(1)

headers = {"Authorization": f"Token {NAUTOBOT_TOKEN}"}
url = f"{NAUTOBOT_URL}/api/dcim/devices/?role={ROLE}&status=active"
resp = requests.get(url, headers=headers, verify=False)
data = resp.json()

inventory = {"_meta": {"hostvars": {}}, "all": {"hosts": []}}

for device in data.get("results", []):
    name = device["name"]
    ip = None
    if device.get("primary_ip4"):
        ip = device["primary_ip4"]["address"].split("/")[0]
    inventory["all"]["hosts"].append(name)
    inventory["_meta"]["hostvars"][name] = {
        "ansible_host": ip,
        "os_type": device.get("custom_fields", {}).get("os_type", "unknown"),
        "owner_email": device.get("custom_fields", {}).get("owner_email", "unknown"),
        "business_unit": device.get("custom_fields", {}).get("business_unit", "unassigned"),
    }

print(json.dumps(inventory, indent=2))
