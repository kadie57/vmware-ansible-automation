# Ansible EDA with VMware vCenter Lab
This repository showcases a **simple lab project** that integrates two powerful tools:

- **Ansible Event-Driven Automation (EDA)** → provides the **automation engine** that reacts to events (e.g., VM creation/deletion).  
- **NetBox** → serves as the **infrastructure source of truth**, keeping track of virtual machines and resources.  



## Features
- Detect when a new Virtual Machine (VM) is created in vCenter logs.  
- Trigger an Ansible EDA **rulebook** to automatically run a playbook.  
- Playbook action: add the newly created VM into **NetBox** inventory.  
- Example Python **plugin source** for reading logs and extracting VM names.  


## Repository Structure
```
ansible-eda-vcenter-lab/
│── README.md 
│── docs/
│ └── workflow.png #
│── ansible/
│ ├── playbooks/
│ │ └── add_vm_to_netbox.yml
│ ├── rulebooks/
│ │ └── detect_new_vm.yml
│ └── roles/
│ └── netbox_vm/...
│── plugins/
│ └── sources/
│ └── vcenter_log.py # Custom source plugin
│── examples/
│ └── demo_log.txt # Sample log file

```


## Architecture
![architecture](docs/workflow.png)

- **VMware ESXi + vCenter**: virtualization platform.  
- **Ubuntu Ansible Control Node**: runs Ansible & EDA.  (I used Ubuntu 24.04) 
- **NetBox**: acts as the source of truth for infrastructure inventory.  
> In this lab, events are collected using a simple Python log reader.  
> In a production environment, this component could be replaced by a log management system such as **Graylog**, **VMware Log Insight**, or **ELK stack**.



## Requirements
- VMware vCenter (lab environment)  
- Ansible 2.15+  
- ansible-rulebook (EDA)  
- Python 3.9+  
- NetBox API (for demo integration)  

## Installation

### 1. Turn on SSH on Ubuntu
```
sudo apt install openssh-server
sudo systemctl enable ssh
sudo ufw allow ssh
sudo systemctl status ssh
sudo systemctl start ssh
```

### 2. Install Ansible
On Ubuntu control node:
```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible
```

### 3. Install Python & pip
```
sudo apt install -y python3 python3-pip
python3 --version
pip3 --version
```

### 4. Install Ansible Rulebook (EDA)
```
pip install ansible-rulebook
```

### 5. Install VMware & NetBox collections
```
ansible-galaxy collection install community.vmware
ansible-galaxy collection install netbox.netbox
```

### 6. Install additional Python modules
```
pip install requests
pip install pyvmomi
```

### 7. Verify installation
```
ansible --version
ansible-rulebook --version
```

### 8. Run EDA rulebook
```
ansible-rulebook -r ansible/rulebooks/detect_new_vm.yml -i inventory.yml
```

## Conclusion

In real-world environments, this solution can be expanded further:  
- Replace **Ansible** with **AWX/Ansible Automation Platform** for centralized job management.  
- Replace the simple **Python log reader** with enterprise log platforms such as **Graylog**, **VMware Log Insight**, or **ELK**.  
- Extend automation to more use cases, e.g.:  
  - Auto-assigning IP addresses or VLANs from NetBox  
  - Triggering monitoring updates in Prometheus/Grafana  
  - Managing VM lifecycle policies (power, snapshots, scaling)  

This lab is just a starting point to explore how **event-driven automation** and a **source of truth** can work together to simplify infrastructure operations.

Thanks for visiting my repo! ✨

