1. Containerlab Installation & Setup
Install Containerlab & Docker (One-Liner): curl -sL https://containerlab.dev/setup | sudo -E bash -s "all"

Add User to Docker Group: sudo usermod -aG docker $USER

Apply Group Changes: newgrp docker

Verify Installation: containerlab version

2. Docker Image Management
You have already successfully loaded your Juniper cRPD image into your local registry.

Load Arista cEOS: docker load -i cEOS-lab-4.35.0F.tar.xz

Load Juniper cRPD: docker load -i junos-routing-crpd-docker-amd64-23.4R1.9.tgz

Pull Nokia SR-Linux: docker pull ghcr.io/nokia/srlinux:latest

Pull FRR: docker pull frrouting/frr:latest

List Loaded Images: docker images

3. Git Repository Setup
You have linked your local ~/projects/automation folder to your GitHub repository: https://github.com/dj0203/automation.

Initialize Git: git init

Add Remote (SSH): git remote add origin git@github.com:dj0203/automation.git

Set Branch to Main: git branch -M main

Verify Remote URL: git remote -v

Check Status: git status

4. Git Workflow (Daily Use)
Stage Changes: git add .

Commit Changes: git commit -m "Your descriptive message here"

Push to GitHub: git push -u origin main

5. Ansible Installation
Since you are a Network Development Engineer focused on automation, this is your primary tool for pushing configurations.

Add Ansible PPA: sudo add-apt-repository --yes --update ppa:ansible/ansible

Install Ansible: sudo apt install ansible

Verify Ansible: ansible --version