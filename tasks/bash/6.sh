#!/bin/bash

REPORT_FILE="system_report.txt"
CURRENT_DATE_TIME=$(date)
CURRENT_USER=$(whoami)
INTERNAL_IP=$(ifconfig | grep inet | head -n 1 | cut -d " " -f 2)
HOSTNAME=$(hostname)
EXTERNAL_IP=$(curl -s http://ipecho.net/plain; echo)
LINUX_DISTRO=$(uname -a)
SYSTEM_UPTIME=$(uptime)
DISK_USAGE=$(df -h / | awk 'NR==2 {print $3 " used, " $4 " free"}')
TOTAL_RAM=$(top -l 1 | grep -E "^Phys" | cut -d " " -f 2)
FREE_RAM=$(top -l 1 | grep -E "^Phys" | cut -d " " -f 8)
CPU_INFO=$(sysctl -a machdep.cpu.brand_string | cut -d " " -f 2-)

{
    echo "System Report"
    echo "============="
    echo "Date and Time: $CURRENT_DATE_TIME"
    echo "User: $CURRENT_USER"
    echo "Internal IP Address: $INTERNAL_IP"
    echo "Hostname: $HOSTNAME"
    echo "External IP Address: $EXTERNAL_IP"
    echo "Linux Distribution: $LINUX_DISTRO"
    echo "System Uptime: $SYSTEM_UPTIME"
    echo "Disk Usage: $DISK_USAGE"
    echo "Total RAM: $TOTAL_RAM"
    echo "Free RAM: $FREE_RAM"
    echo "CPU Info: $CPU_INFO"
} > $REPORT_FILE

echo "Report generated: $REPORT_FILE"