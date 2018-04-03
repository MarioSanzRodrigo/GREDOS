#!/bin/bash
 
  /sbin/iptables -t nat -A POSTROUTING -o eth2 -j MASQUERADE
  /sbin/iptables -A FORWARD -i eth2 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
  /sbin/iptables -A FORWARD -i eth2 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
