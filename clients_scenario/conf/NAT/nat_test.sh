#!/bin/bash
 
  /sbin/iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE
#  /sbin/iptables -A FORWARD -i eth3 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
#  /sbin/iptables -A FORWARD -i eth1 -o eth3 -j ACCEPT
