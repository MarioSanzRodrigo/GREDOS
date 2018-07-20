#!/bin/bash

#Check if configuration is done
if ovs-vsctl list-br | grep br0 > /dev/null; then
    echo The configuration is already done because br0 exists
    exit 0
else
    echo '--------------->Starting configuration'
fi

echo '--------------->Changing keyboard language to Spanish'
loadkeys es


echo '--------------->Changing root password to xxxx'
echo 'root:xxxx' | chpasswd
echo '--------------->Configuring initial network'
#echo auto eth0 >> /etc/network/interfaces 
#echo iface eth0 inet static >> /etc/network/interfaces
#echo address 138.4.7.225 >> /etc/network/interfaces
#echo netmask 255.255.255.0 >> /etc/network/interfaces
#echo gateway 138.4.7.129 >> /etc/network/interfaces
#service networking restart

echo '--------------->Updating packages'
apt-get update -y
echo '--------------->Installing build-essential'
apt-get install -y build-essential
echo '--------------->Installing openssl'
apt-get install -y openssl
echo '--------------->installing libcap-ng0 library'
apt-get install -y libcap-ng0

echo '--------------->Installing Python 2.7'
wget https://www.python.org/ftp/python/2.7/Python-2.7.tgz
tar -xzf Python-2.7.tgz
cd Python-2.7
./configure
make install
cd -

echo '--------------->Installing Library six for Python'
wget https://pypi.python.org/packages/b3/b2/238e2590826bfdd113244a40d9d3eb26918bd798fc187e2360a8367068db/six-1.10.0.tar.gz
tar -xzf six-1.10.0.tar.gz
cd six-1.10.0 
python setup.py install
cd -

echo '--------------->Installing OpenvSwitch'
wget http://openvswitch.org/releases/openvswitch-2.7.0.tar.gz
tar -xzf openvswitch-2.7.0.tar.gz
cd openvswitch-2.7.0
#./configure --with-linux=/lib/modules/$(uname -r)/build
./configure
make install
make modules_install
echo '--------------->Creating database of OpenvSwitch'
mkdir -p /usr/local/etc/openvswitch 
ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema
mkdir -p /usr/local/var/run/openvswitch
ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
                 --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
                 --private-key=db:Open_vSwitch,SSL,private_key \
                 --certificate=db:Open_vSwitch,SSL,certificate \
                 --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
                 --pidfile --detach --log-file

echo '--------------->Installing module VLAN'
apt-get install -y vlan
sed -i 's/^exit 0/#exit 0/g' /etc/network/if-pre-up.d/swconfig
sed -i '/vlan 101/d' /etc/network/if-pre-up.d/swconfig 
sed -i '/vlan 102/d' /etc/network/if-pre-up.d/swconfig
sed -i '/set apply/d' /etc/network/if-pre-up.d/swconfig

#TODO: Remove swconfig configuration and rename file
echo -e swconfig dev eth0 vlan 103 set ports \'3 8t\'>> /etc/network/if-pre-up.d/swconfig
echo -e swconfig dev eth0 vlan 104 set ports \'4 8t\'>> /etc/network/if-pre-up.d/swconfig
echo -e swconfig dev eth0 vlan 100 set ports \'0 8t\'>> /etc/network/if-pre-up.d/swconfig
echo -e swconfig dev eth0 vlan 101 set ports \'1 8t\'>> /etc/network/if-pre-up.d/swconfig
echo -e swconfig dev eth0 vlan 102 set ports \'2 8t\'>> /etc/network/if-pre-up.d/swconfig

echo 'swconfig dev eth0 port 0 pvid 100' >> /etc/network/if-pre-up.d/swconfig
echo 'swconfig dev eth0 port 1 pvid 101' >> /etc/network/if-pre-up.d/swconfig
echo 'swconfig dev eth0 port 2 pvid 102' >> /etc/network/if-pre-up.d/swconfig
echo 'swconfig dev eth0 port 3 pvid 103' >> /etc/network/if-pre-up.d/swconfig
echo 'swconfig dev eth0 port 4 pvid 104' >> /etc/network/if-pre-up.d/swconfig

echo 'swconfig dev eth0 set apply 1' >> /etc/network/if-pre-up.d/swconfig


#TODO: Remove ip configuration in interfaces. Only loopback
echo '--------------->Reconfiguring network'
sed -i '/auto eth0/d' /etc/network/interfaces
sed -i '/iface eth0/d' /etc/network/interfaces
sed -i '/138.4.7.225/d' /etc/network/interfaces
sed -i '/255.255.255.0/d' /etc/network/interfaces
sed -i '/138.4.7.129/d' /etc/network/interfaces

echo 'auto eth0.103' >> /etc/network/interfaces
echo 'iface eth0.103 inet static' >> /etc/network/interfaces
echo 'address 138.4.7.225' >> /etc/network/interfaces
echo 'gateway 138.4.7.129' >> /etc/network/interfaces
echo 'netmask 255.255.255.0' >> /etc/network/interfaces

echo 'auto eth0.104' >> /etc/network/interfaces
echo 'iface eth0.104 inet manual' >> /etc/network/interfaces

echo 'auto eth0.100' >> /etc/network/interfaces
echo 'iface eth0.100 inet manual' >> /etc/network/interfaces

echo 'auto eth0.101' >> /etc/network/interfaces
echo 'iface eth0.101 inet manual' >> /etc/network/interfaces

echo 'auto eth0.102' >> /etc/network/interfaces
echo 'iface eth0.102 inet manual' >> /etc/network/interfaces

echo 'auto wlan0' >> /etc/network/interfaces
echo 'iface wlan0 inet manual' >> /etc/network/interfaces

echo 'auto br0' >> /etc/network/interfaces
echo 'iface br0 inet static' >> /etc/network/interfaces
echo 'address 192.168.2.1' >> /etc/network/interfaces
echo 'gateway 192.168.2.1' >> /etc/network/interfaces
echo 'netmask 255.255.255.0' >> /etc/network/interfaces

echo '--------------->Enable forwarding'
sed -i 's/^#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g' /etc/sysctl.conf


#TODO: Not needed DHCP Server
echo '--------------->Configurating DHCP'
apt-get install -y dnsmasq
echo -e '\ninterface=br0' >> /etc/dnsmasq.conf
echo 'dhcp-range=192.168.2.10,192.168.2.30,1h' >> /etc/dnsmasq.conf
echo -e DNSMASQ_OPTS=\"--conf-file=/etc/dnsmasq.conf\" >> /etc/default/dnsmasq

#TODO: Not needed change rc.local -> use configuration script
echo '--------------->Changing booting file'
sed -i 's/^exit 0/#exit 0/g' /etc/rc.local
echo 'loadkeys es' >> /etc/rc.local
echo '/etc/init.d/dnsmasq restart' >> /etc/rc.local
echo '/usr/local/share/openvswitch/scripts/ovs-ctl start'>> /etc/rc.local

echo 'service networking restart' >> /etc/rc.local
echo 'ifconfig eth0.100 up' >> /etc/rc.local
echo 'ifconfig eth0.101 up' >> /etc/rc.local
echo 'ifconfig eth0.102 up' >> /etc/rc.local
echo 'ifconfig eth0.104 up' >> /etc/rc.local
echo 'ifconfig wlan0 up' >> /etc/rc.local

echo echo '1 > /proc/sys/net/ipv4/ip_forward' >> /etc/rc.local
echo iptables -A INPUT -i br0 -j ACCEPT >> /etc/rc.local
echo iptables -t nat -A POSTROUTING -o eth0.103 -j MASQUERADE >> /etc/rc.local
echo iptables -A INPUT -i lo -j ACCEPT >> /etc/rc.local
echo iptables -A FORWARD -i br0 -o eth0.103 -j ACCEPT >> /etc/rc.local
echo iptables -A FORWARD -i eth0.103 -o br0 -j ACCEPT >> /etc/rc.local
echo /usr/local/share/openvswitch/scripts/ovs-ctl status > /var/log/network.log >> /etc/rc.local
echo '/usr/local/bin/ovs-vsctl add-br br0 || true' >> /etc/rc.local
echo /usr/local/bin/ovs-vsctl set-controller br0 tcp:192.168.2.13:6633 >> /etc/rc.local

echo ifconfig br0 up >> /etc/rc.local
echo ifconfig br0 192.168.2.1/24 >> /etc/rc.local
echo 'echo ifconfig >> /var/log/network.log' >> /etc/rc.local

echo '/usr/local/bin/ovs-vsctl add-port br0 eth0.100 || true' >> /etc/rc.local
echo '/usr/local/bin/ovs-vsctl add-port br0 eth0.101 || true' >> /etc/rc.local
echo '/usr/local/bin/ovs-vsctl add-port br0 eth0.102 || true' >> /etc/rc.local
echo '/usr/local/bin/ovs-vsctl add-port br0 eth0.104 || true' >> /etc/rc.local
echo '/usr/local/bin/ovs-vsctl add-port br0 wlan0 || true' >> /etc/rc.local

echo 'service hostapd stop' >> /etc/rc.local
echo 'service hostapd restart' >> /etc/rc.local


echo '--------------->Configuring WiFi AP'
apt-get update -y
apt-get install -y hostapd 
apt-get install -y hostapd-rtl
sed -i -e 's/^wpa_passphrase.*/wpa_passphrase=xxxxxxxx/g' /etc/hostapd/hostapd.conf 
sed -i -e 's/^bridge=.*/bridge=br0/g' /etc/hostapd/hostapd.conf 
sed -i -e 's/^ssid.*/ssid=BPI-R1/g' /etc/hostapd/hostapd.conf 
sed -i -e 's/^#DAEMON_CONF/DAEMON_CONF/g' /etc/default/hostapd 


#TODO: Download github repository and remove not needed parts
reboot
