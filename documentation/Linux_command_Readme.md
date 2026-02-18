Networking & Connection
ip a: Displays all network interfaces and their assigned IP addresses. It is used to find the VM's IP for SSH connections.

sudo apt update: Refreshes the local package index so the system knows where to download the latest software from repositories.

sudo apt install openssh-server: Installs the SSH daemon (sshd), which is the bridge required for VS Code to connect to your Linux VM.

sudo systemctl status ssh: Checks if the SSH service is currently running and active.

ping google.com or ping 8.8.8.8: Tests for internet connectivity to ensure the VM can reach the external repositories.

Performance & System Monitoring
iostat -xz 1: Provides a real-time view of CPU and Disk utilization. We used this to identify that your VM was hitting a 1-CPU bottleneck.

cat /etc/apt/sources.list: Displays the list of repositories your system is using to find software packages.

sysctl -n hw.ncpu: (Mac Terminal) Shows the total number of CPU cores available on your MacBook Pro.

sysctl hw.perflevel0.ncpus hw.perflevel1.ncpus: (Mac Terminal) Breaks down your Mac's 12 cores into Performance (fast) and Efficiency (low power) counts.