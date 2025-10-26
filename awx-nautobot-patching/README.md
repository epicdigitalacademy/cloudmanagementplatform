# AWX + Nautobot Patching Project

This project integrates **Ansible AWX** with **Nautobot** to perform automated OS patching and post-patch health checks.

### Components
- `inventories/nautobot_inventory.py`: dynamic inventory from Nautobot API
- `playbooks/patch.yml`: OS patch automation
- `playbooks/healthcheck.yml`: post-patch verification

### Environment Variables for AWX
```
NAUTOBOT_URL=https://nautobot.local
NAUTOBOT_TOKEN=<your_token>
ROLE=server
```

### Usage
1. Create AWX Project pointing to this Git repo.
2. Add Inventory → Source → “Sourced from Project” → select `inventories/nautobot_inventory.py`.
3. Add Job Templates:
   - **Patch Servers** → playbook: `playbooks/patch.yml`
   - **Health Check** → playbook: `playbooks/healthcheck.yml`
4. Optionally, schedule or trigger via Camunda.
