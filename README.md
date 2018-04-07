# GREDOS Project scenarios
***

This repository develop several scenarios to deploy GREDOS project using [Virtual Networks over linuX (VNX)](http://www.dit.upm.es/~vnx/).

Index:
- [Summary](https://github.com/carlosv5/GREDOS#summary)
- [Requirements](https://github.com/carlosv5/GREDOS#requirements)
- [Scenarios](https://github.com/carlosv5/GREDOS#scenarios)
- [Usage](https://github.com/carlosv5/GREDOS#usage)
- [Notes](https://github.com/carlosv5/GREDOS#notes)
- [Author](https://github.com/carlosv5/GREDOS#author)
- [References](https://github.com/carlosv5/GREDOS#references)


## Summary

Investigation project GREDOS is developed by Departamento de Ingeniería de Sistemas Telemáticos (DIT) of Escuela Técnica Superior de Ingenieros de Telecomunicación (ETSIT). GREDOS is focused on evolving residential networks to an user centralized software architecture, so, each client of a telecommunications operator could control and modify his home network. For that purpose, residential networks are split in two components: on the one hand, a client application to control the network and devices connected to it, and on the other hand, the server component, based on SDN and NFV technologies.

These scenarios deploy residential network architecture based on SDN and NFV. The scenarios define network’s components: access network, transport network implemented with optical technologies, and operator’s infrastructure (cloud) where services are deployed. The cloud infrastructure is built with OpenStack and runs the SDN controllers which switches the traffic. It also hosts the user network functions: routing, NAT, DHCP, etc, letting change the specialized residential gateway for a white-box switch with OpenvSwitch that understands the SDN controller orders and switch packages in the network.

## Requirements

 - VNX installed [(VNX Installation Guide)](http://web.dit.upm.es/vnxwiki/index.php/Vnx-install)
 - Operating System: Ubuntu 14.04 / Ubuntu 16.04 / Ubuntu 17.04
 - Hard Drive: 5 GB avaible space (Filesystems size)
 - Memory: 8 GB RAM or more
 - Banana Pi with GREDOS's image installed and configuration
 
 ## Scenarios
 - Clients scenario
     * [Pox scenario](https://github.com/carlosv5/GREDOS/wiki/pox_scenario): this scenario deploy clients and cloud side except from the Banana Pi (physical). Uses Pox as SDN controllers. Beware of interfaces connections
      * [Floodlight scenario without Banana Pi](https://github.com/carlosv5/GREDOS/wiki/floodlight_all_virtual_scenario): this scenario deploy clients and cloud side and Banana Pi OVS. Uses Floodlight as SDN controllers
      * [Floodlight scenario](https://github.com/carlosv5/GREDOS/wiki/floodlight_scenario): this scenario deploy clients and cloud side except from the Banana Pi (physical). Uses Floodlight as SDN controllers. Beware of interfaces connections
      * [Clients scenario with OpenStack](https://github.com/carlosv5/GREDOS/wiki/openstack_clients_scenario): this scenario deploy clients side except from the Banana Pi (physical). Beware of interfaces connections. It must run with OpenStack scenario at the same time.
 - [Openstack scenario](https://github.com/carlosv5/GREDOS/wiki/openstack_gredos): this scenario deploy cloud side. Beware of interfaces connections. It must run with the previous scenario at the same time.

 ## Usage

In order to run an scenario you must follow this commands:
 - Create an scenario `sudo vnx -f file.xml -v -t`
 - Destroy an scenario `sudo vnx -f file.xml -v --destroy`
 
## Author

This project has been developed by [Carlos Vega García](https://es.linkedin.com/in/carlos-vega-garc%C3%ADa-449795150).

## References
