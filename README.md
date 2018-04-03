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
 - Memory: 4 GB RAM or more
 
 ## Scenarios
 
 - Clients scenario
 - Openstack scenario

 ## Usage

## Author

This project has been developed by [Carlos Vega García](https://es.linkedin.com/in/carlos-vega-garc%C3%ADa-449795150).

## References
