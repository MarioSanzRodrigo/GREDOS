#!/bin/bash
cd /root/

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
sed -i 's/^# exit 0/exit 0/g' /etc/networking/if-pre-up.d/swconfig

echo '--------------->Enable forwarding'
sed -i 's/^#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g' /etc/sysctl.conf

echo '--------------->Configuring WiFi AP'
apt-get update -y
apt-get install -y hostapd 
apt-get install -y hostapd-rtl
sed -i -e 's/^wpa_passphrase.*/wpa_passphrase=xxxxxxxx/g' /etc/hostapd/hostapd.conf 
sed -i -e 's/^bridge=.*/bridge=br0/g' /etc/hostapd/hostapd.conf 
sed -i -e 's/^ssid.*/ssid=BPI-R1/g' /etc/hostapd/hostapd.conf 
sed -i -e 's/^#DAEMON_CONF/DAEMON_CONF/g' /etc/default/hostapd 

echo '--------------->Moving scripts'
cp /root/GREDOS/openstack_scenario/scripts/bananapi/controllers.sh /root/controllers.sh
cp /root/GREDOS/openstack_scenario/scripts/bananapi/config_bananapi.py /root/config_bananapi.py
cp /root/GREDOS/openstack_scenario/scripts/bananapi/base.rc.local /etc/base.rc.local
chmod +x /root/controllers.sh config_bananapi.py

echo '--------------->Rebooting system'
sleep 3
reboot
