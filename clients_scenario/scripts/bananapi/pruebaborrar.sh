#!/bin/bash
controller_ip=$1
br0_ip=$2
while true
do
ping -c 3 $controller_ip > /dev/null
  if [ $? -eq 0 ]; then
    echo conecta
    /usr/local/bin/ovs-vsctl show | grep tcp:$controller_ip > /dev/null
    if [ $? -eq 1 ];then 
      nc -zv $controller_ip 6633
      if [ $? -eq 0 ];then 
        echo Conecta a pox
        /usr/local/bin/ovs-vsctl set-controller br0 tcp:$controller_ip:6633
      else
        echo Conecta a Fl
        /usr/local/bin/ovs-vsctl set-controller br0 tcp:$controller_ip:6653
      fi
    fi
  else
    echo 'no conecta'
    /usr/local/bin/ovs-vsctl show | grep tcp:$br0_ip:6633 > /dev/null
    if [ $? -eq 1 ];then 
      #Conecta a pox local
      /usr/local/bin/ovs-vsctl set-controller br0 tcp:$br0_ip:6633
    fi
  fi
  sleep 1
done 


#Parameters 
# $1 controller_ip
# $2 br0_ip
