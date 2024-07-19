`ifconfig`
`ip addr show`
`nmcli` on centos
`nmcli d show` show more info about devices
`ip route show`
`routel`
### OSI layers

![[Screenshot 2024-06-17 at 11.43.20.png]]

(binary)
A 0
B 10
C 110
D 1110
E 11110

![[Screenshot 2024-06-17 at 11.50.31.png]]

CIDR classless inter-domain routing

![[Screenshot 2024-06-17 at 11.53.13.png]]


# ARP

`ip n` show table (neighbor)

# DNS
### TLD top level domain

`dig -4 <domain>` ipv4
`dig -4 ... +trace`
`awk 'length($0)<50'` not greater than 50

# TCP

![[Screenshot 2024-06-17 at 12.06.30.png]]

SYN
SYN ACK
ACK, DATA

# DHCP

server udp 67
client udp 68

`/var/lib/dhclient/dhclient.leases`
`grep "DHCPOFFER" /var/log/messages`

Discover
Offer
Request
Ack

`ss -lunp | grep dhclient`
`dhclient -r` release ip
`dhclient` start it

### changing dhcp to static to dhcp
`nmcli`
`nmcli mod Wired\ connection\ 1 ipv4.method manual ipv4.address 192.168.51.191/24 ipv4.gateway 192.168.51.2`
`nmcli con down Wired\ conn...`
`nmcli con up`
`nmcli con mod Wired\ connection\1 ipv4.dns 192.168.5.2`
`nmcli con mod ... ipv4.method auto ipv4.address "" ipv4.dns "" ipv4.gateway ""`

`nmcli c show <connection> | grep ipv4` show v4 addresses

# Bonding and Teaming
`nmcli con mod ... ipv4.address 192.168.51.190/24,192.168.51.195/24`

### bonding
`nmcli con add type bond con-name bond0 ifname bond0 mode active-backup ip4 192.168.51.170/24`
`nmcli c` connections
`nmcli con add type bond-slave ifname ens33 master bond0`
`nmcli con add type bond-slave ifname ens38 master bond0`

`nmcli con up bond-slave-ens33`
`nmcli con up bond-slave-ens38`

`nmcli con mod bond0 ipv4.gateway 192.168.51.2`
`nmcli d show bond0`

### teaming
broadcast
round-robin
active-backup
loadbalance
lacp - 802.3ad

`nmcli con up bond-slave-ens33`

### link watchers
`ethtool`
`arp_ping`
`nsna_ping`

![[Screenshot 2024-06-17 at 13.00.21.png]]

`teamd`
`nmcli con add type team con-name Team0 ifname team0 team.config '{"runner":{"name": "activebackup"}, "link_watch": {"name": "ethtool"}}'`

`/usr/share/doc/teamd-1.27/example_configs/activebackup_ethtool_3.conf`
more examples there ^
`nmcli con add type team-slave con-name slave1 ifname eth1 master team 0`
`nmcli con add type team-slave con-name slave2 ifname eth2 master team 0`
`nmcli con show Team0 ipv4.address 10.0.1.15/24 ipv4.gateway 10.0.1.1 ipv4.method manual`
`nmcli con up slave1`
`nmcli con up slave2`
`nmcli con up team0`

`teamdctl team0 state`

`nmcli con dalete Team0`
`nmcli con dalete slave0`
`nmcli con dalete slave1`

`systemctl restart network`

### round robin
`nmcli con add type team con-name Team0 ifname team0`
`nmcli con mod Team0 ipv4.address 10.0.1.15/24 ipv4.gateway 10.0.1.1 ipv4.method manual`
`nmcli con add type team-slave con-name slave1 ifname eth1 master team0`
`nmcli con add type team-slave con-name slave2 ifname eth2 master team0`

`nmcli con up slave1`
`nmcli con up slave2`
`nmcli con up team0`

`ping -I team0 1.1.1.1`

## teaming has some advantages vs bonding



# routing
`route -n` deprecated 
`ip r` new
`ip route add prohibit 1.1.1.1` block ip
`ip route flush 1.1.1.1` remove block, unblock

`nmcli con up Wired...`
`ip route add 1.1.1.1 via 10.0.1.10 dev eth0`
`vim /etc/sysconfig/netowrk-scripts/route-eth0`

`ip link set eth1 down`
`ip r s` ip route show

`yum install bind-utils`
`host example.com`

# DNS
`bind-utils`
`/etc/hosts`
`getent ahosts <domain>`
`curl -I <domain>` show headers
`host <domain>`
`dig <domain>`
`/etc/nsswitch.conf` change order
`yum install links` cli browser
`links https://example.com`

### bind
`named-checkconf`
`named-checkzone`
`/usr/share/doc/bind-9.9.4/sample/var/named/named.empty`
`/etc/resolv.conf`
`bind-utils NetworkManager bash-completion`
`/etc/named.conf`
```conf
zone "example.com" IN {
	type slave;
	file "slaves/example.com.fwd";
	masters { 10.0.1.10; };
}
zone "10.0.10.in-addr.arpa" IN {
	type slave;
	masters { 10.0.1.10; };
}
```

`firewall-cmd --permanent --add-service=dns && firewall-cmd --reload`
`sysctl enable named`
`cat /var/named/slaves/example.com.fwd`

`dig @10.0.1.11 server1.example.com`

`dig linuxacademy.com +nssearch`


# firewall
### netfilter
linux kernel framework

### iptables
`systemctl start iptables`
`tcpdump -i eth0 port 80`

`iptables -t filter -A INPUT -p tcp -dport 22 -j ACCEPT`
`iptables -I INPUT 5 -s 10.0.1.0/24 -j REJECT`

`cat /proc/net/nf_conntrack` raw connection tracking info
`conntrack -l`
`conntrack -L -p tcp --dport 80`
`conntrack -E -p tcp --dport 80` real time

`iptables -t filter -L` show filter rules
`iptables -t nat -L` show net rules
`iptables -t raw -L` show raw rules
`iptables -t mangle -L` show mangle rules

`iptables -L -v INPUT --line-numbers`

`iptables -I INPUT 5 -p tcp --dport 80 -j ACCEPT` add 80 accept

### firewalld
default zone - `public`
`/usr/lib/firewalld/zones/public.xml`

`firewall-cmd --list-all`
`firewall-cmd --get-active-zones`
`firewall-cmd --get-default-zone`
`firewall-cmd --get-zones`
`firewall-cmd --add-port=100/tcp`
`firewall-cmd --list-all`

`firewall-cmd --list-service[s]`
`firewall-cmd --list-ports`
`firewall-cmd --add-service=squid`
`firewall-cmd --list-all`
`/usr/lib/firewalld/services/` list services, create new
`firewall-cmd --reload`

to make changes persistant `--permanent`
`firewall-cmd --new-service=<name>`
`/etc/firewalld/services/<name>.xml`
`firewall-cmd --service=jmx --set-description "<desc>"`
`firewall-cmd --service=<service> --add-port=1400-1420/tcp`
`firewal-cmd --new-ipset=kiosk --type=hash:ip`
`firewall-cmd --ipset=kiosk --add-entry=10.0.1.11`
`firewall-cmd --ipset=kiosk --get-entries`

`firewall-cmd --ipset=kiosk --add-entries-from-file=<file>` add entries from file
`firewall-cmd --new-zone=kiosk`
`firewall-cmd --zone=kiosk --add-service=jmx`
`firewall-cmd --zone=kiosk --add-source=ipset:kiosk`

`man 5 firewalld.richlanguage`

`firewall-cmd --add-rich-rule'rule family=ipv4 source address=10.0.1.0/24 destination address=10.0.1.10/24 port port=8080-8090 protocol=tcp accept'`

`firewall-cmd --direct --add-rule ipv4 nat POSTROUTING 0 -o eth1 -j MASQUERADE` rather not use that

## troubleshooting
`iptables -vnL`
`vim /etc/sysconfig/iptables` edit iptables

`firewall-cmd --list-all`
`firewall-cmd --permanent --add-rich-rule='rule family=ipv4 source address=10.0.1.10/24 port port=80 protocol=tcp reject'`
`firewall-cmd --reload`
`firewall-cmd --permanent --add-rich-rule='rule family ipv4 source address = 10.0.1.11 port port=80 protocol=tcp accept'`
`firewall-cmd --permanent --remove-rich-rule='...'`

`iptables -I INPUT -p tcp -s 10.0.1.11 --dport 80 -j ACCEPT`
`service iptables save` save running config

`firewall-cmd --permanent --zone drop --add-source ipset:kiosk`


# Connection Troubleshooting
![[Screenshot 2024-06-19 at 11.47.54.png]]

`systemctl status {firewalld,iptables}`
`ip route add 10.0.1.0/24 dev eth1 tab 1`
`ip route add 10.0.1.0/24 dev eth2 tab 2`
`ip rule add from 10.0.1.0/24 tab 1`
`ip rule add from 10.0.1.0/24 tab 2`

`telnet`

`nc` netcat
`tcpdump`
`tcpdump port 80`
`tcpdump -i eth1 -n src host 10.0.1.11`
`tcpdump -i eth0 -w capture.pcap`
`tcpdump -i eth -w capture.pcap port not 22`
`tcpdump` or `tshark`

`tcpdump -n` drop name resolution DNS
`-i eth0` interface
`port not 22` omit ssh
`-A` ascii output
`-w capture.pcap` send to file
`-r capture.pcap` read file

`nohup` no hang up, run command in the background

# Port Forwarding
`iptables -nL`
`iptables -L. -t nat`
add to prerouting chain
`iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080`
`iptables -L --line-number`
`iptables -I INPUT 4 -p tcp -m state --state NEW -m tcp --dport 8080 -j ACCEPT`
`iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 10.0.1.20:80` redirect to another host, need to enable masquerade
`iptables -t nat -A POSTROUTING -j MASQUERADE`
`iptables -I FORWARD -p tcp -d 10.0.1.20 --dport 80 -m state --state NEW -j ACCEPT`
`iptables -I FORWARD -m state --state REPLATED,ESTABLISHED -j ACCEPT`

`iptables -I INPUT 4 -p tcp -m state --state NEW --dport 80 -j ACCEPT`
`cat /proc/sys/net/ipv4/ip_forward` -> echo 1 to this to enable

`firewall-cmd --add-forward-port=port=80:proto=tcp:toport=8080`
`firewall-cmd --add-forward-port=port=8080:proto=tcp:toport=80:toaddr=10.0.1.20`
`firewall-cmd --remove-forward-port='...'`
`firewall-cmd --add-masquerade`


# SSH Tunnel
local - access remote content (if no direct access to port)
`ssh -L 8080:Server2:80 cloud_user@Server1`

remote - show local port on remote machine
`ssh -R 8080:localhost:80 cloud_user@Server1`

dynamic - kind of proxy
`ssh -D 8080 cloud_user@Server1`

`/etc/ssh/sshd_config` -> `GatewayPorts yes`

# Proxy Servers
### squid - most popular linux caching proxy
`firewall-cmd --permanent --add-service=squid`, default port 3128
`cat /etc/squid/squid.conf | grep "^[^#]"` show conf files without comments

`export http_proxy="http://10.0.1.10:3128"` set proxy on linux
`/var/log/squid/access.log` logs of using proxy

example rule
`acl blacklist dstdomain .apache.org .linuxacademy.com`
`http_access deny blacklist`
`systemctl restart squid`

changing bandwidth rules
`acl kiosk_128k src 10.0.1.10/24`
`delay_pools 1`
`delay_class 1 3`
`delay_access 1 allow kiosk_128k`
`delay_access 1 deny all`
`delay_parameters 1 64000/64000 -1/-1 16000/64000`
restart

# Load Balancing
[Cool Post with animations](https://samwho.dev/load-balancing/)
Round Robin
Least Connections
Source / IP Hash

session persistance/sticky sessions
nginx
HXProxy

### HAProxy
`/etc/haproxy/haproxy.cfg`
```conf
frontend demo_app
	bind *:80
	mode http
	default_backend apache_nodes

backend apache_nodes
	mode https
	balance roundrobin
	option forwardfor # X-Forwarded-For
	server node1 10.0.1.20:8080 check
	server node2 10.0.1.30:8080 check
```

`sysctl restart haproxy`
`for i in {1..10}; do curl localhost; done`

`balance source` apply best effort stickiness

### NGINX
`yum install -y epel-release`
`yum install -y nginx`

`/etc/nginx/nginx.conf`
```conf
http {
	upstream demoapp {
		server 10.0.1.20;
		server 10.0.1.30;
	}
	server {
		listen 80;
		location / {
			proxy_pass http://demoapp
		}
	}
}
```

default is round robin
`ip_hash` to use source ip balancing

# VPN
`yum install epel-release`
`yum install openvpn`

`firewall-cmd --permanent --add-port 1194/tcp`
`firewall-cmd --permanent --add-masquerade`
reload

`yum install easy-rsa`

`mkdir /etc/openvpn/easy-rsa`
`PATH=$PATH:/usr/share/easy-rsa/3.0.3/`

`easyrsa init-pki`
`easyrsa build-ca`
`easyrsa gen-dh`

`easyrsa gen-req server nopass`
`easyrsa sign-req server server` `yes`
`easyrsa gen-req client nopass`
`easyrsa sign-req client client`

`cd /etc/openvpn`
`openvpn --genkey --secret pfs.key`
`less /usr/share/doc/openvpn.../sample/sample-config-files/{server,client}.conf` examples

![[Screenshot 2024-06-19 at 14.30.40.png]]

`/etc/openvpn`
`systemctl start openvpn@server.service`

copy keys
![[Pasted image 20240619143252.png]]
```bash
# [root@Server1]# vim keys.sh
cd /etc/openvpn
mkdir -p server1/keys
cp pfs.key server1/keys
cp easy-rsa/pki/dh.pem server1/keys
cp easy-rsa/pki/ca.crt server1/keys
cp easy-rsa/pki/private/ca.key server1/keys
cp easy-rsa/pki/private/client.key server1/keys
cp easy-rsa/pki/issued/client.crt server1/keys
tar cvzf /tmp/keys.tgz server1/
```

client config
![[Pasted image 20240619143418.png]]

`systemctl start openvpn@client`
`ip route add 10.0.1.20 dev tun0`

# IDS - intrusion detection system
## IPS - intrusion prevention system

SNORT - open source IPS/IDS maintained by Cisco
could be used as packet sniffer, packet logger, or IPS

community rules

**SNORT** rule engine
**BARNYARD2** output parser
**SNORBY** web gui

example rules
`alert tcp any 80 <> $HOME_NET any (msg:"HTTP Request"; sid:10000001; rev:001;)`
`systemctl restart snortd`
`/var/log/snort/alert` logs stored here
`alert tcp any any -> $HOME_NET 80 (msg:"Incoming HTTP Request"; sid:1000002; rev:001;)`
`alert tcp 10.0.4.10 any <> $HOME_NET any (msg:"Bad Actor Request"; sid:1000003; rev:001;)`


