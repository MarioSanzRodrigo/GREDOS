apt-get install -y sshpass
vnx -f openstack_gredos.xml -v -t
vnx_config_nat ExtNet eno1
sleep 40
vnx -f openstack_gredos.xml -x start-all,load-img
vnx -f openstack_gredos.xml -x vlan-net,create-vMando
./scripts/del-connection
./scripts/create-connection 138.4.7.164
sshpass -p 'xxxx' scp -o StrictHostKeyChecking=no conf/controller/glance/Xenial-GREDOS.qcow2 root@controller:/tmp/images/
vnx -f openstack_gredos.xml -x create-img-local
vnx -f openstack_gredos.xml -x install-tacker
#vnx -f openstack_gredos.xml -x create-tacker
