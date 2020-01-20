#!/bin/bash

/usr/sbin/iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
/usr/sbin/iptables -A INPUT -p tcp --dport 22 -j REJECT
/usr/sbin/knockd -d
/usr/sbin/sshd
/usr/bin/tail -f /var/log/knockd.log