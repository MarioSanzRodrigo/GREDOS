#!/bin/bash 
while true
do
ping -c 3 $1 > /dev/null
if [ $? -eq 0 ]; then
  #echo Connection
  /usr/local/bin/ovs-vsctl show | grep tcp:$1:6633 > /dev/null
  if [ $? -eq 1 ]; then
    #Remote Pox
    /usr/local/bin/ovs-vsctl set-controller br0 tcp:$1:6633
  fi
else
  #echo ‘No connection’
  /usr/local/bin/ovs-vsctl show | grep tcp:$2:6633 > /dev/null
  if [ $? -eq 1 ]; then
    #Local Pox bk
    /usr/local/bin/ovs-vsctl set-controller br0 tcp:$2:6633
  fi
fi
    sleep 25
done
