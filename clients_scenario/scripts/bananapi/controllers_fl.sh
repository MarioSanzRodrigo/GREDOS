#!/bin/bash 
while true
do
ping -c 3 $1 > /dev/null
if [ $? -eq 0 ]; then
  #echo conecta
  /usr/local/bin/ovs-vsctl show | grep tcp:$1:6633 > /dev/null
  if [ $? -eq 1 ]; then
    /usr/local/bin/ovs-vsctl set-controller br0 tcp:$1:6633
  fi
else
  #echo ‘No conecta’
  /usr/local/bin/ovs-vsctl show | grep tcp:$2:6633 > /dev/null
  if [ $? -eq 1 ]; then
    /usr/local/bin/ovs-vsctl set-controller br0 tcp:$2:6633
  fi
fi
    sleep 25
done

