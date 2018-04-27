# En reclamo
export OSM_HOSTNAME=`sudo lxc list | awk '($2=="SO-ub"){print $6}'`
export OSM_RO_HOSTNAME=`sudo lxc list | awk '($2=="RO"){print $6}'`
#osm vim-create --name openstack-site --user admin --password xxxx --auth_url http://10.0.10.11:35357/v3 --tenant admin --account_type openstack --config='{security_groups: default}'
# Para crear el NS hacerlo desde el dashboard

#Hay que meter en /etc/hosts en SO-ub 10.0.10.11 controller y en los demás lxc
