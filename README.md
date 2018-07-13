# GREDOS Project scenarios
***

This repository develop several scenarios to deploy the research project GREDOS using [Virtual Networks over linuX (VNX)](http://www.dit.upm.es/~vnx/).

Index:
- [Summary](https://github.com/carlosv5/GREDOS#summary)
- [Requirements](https://github.com/carlosv5/GREDOS#requirements)
- [Scenarios](https://github.com/carlosv5/GREDOS#scenarios)
- [Banana Pi configuration](https://github.com/carlosv5/GREDOS#BananaPi)
- [Author](https://github.com/carlosv5/GREDOS#author)
- [References](https://github.com/carlosv5/GREDOS#references)


## Summary
Research project GREDOS is developed by Departamento de Ingeniería de Sistemas Telemáticos (DIT) of Escuela Técnica Superior de Ingenieros de Telecomunicación (ETSIT).GREDOS is focused on evolving residential networks to an user-centric software architecture, so, each client of a telecommunications operator can control and modify his home network using mobile applications.

These scenarios deploy residential network architecture based on SDN and NFV.The scenarios define network’s components:residential network, access network implemented with optical technologies and operator’s infrastructure (cloud) where services are deployed. For this purpose, innovative technologies as SDN, NFV, cloud computing and optical equipment have been used.

![Objective](https://github.com/carlosv5/GREDOS/blob/master/img/objective.png)


## Requirements

 - VNX installed [(VNX Installation Guide)](http://web.dit.upm.es/vnxwiki/index.php/Vnx-install)
 - Operating System: Tested in Ubuntu 16.04
 - Hard Drive: 5 GB avaible space (Filesystems size)
 - Memory: 8 GB RAM or more
 - Banana Pi with GREDOS's image installed and configuration
 
 ## Scenarios
  - [Scenario 1: Pox as SDN controller and Banana Pi as Residential Gateway](https://github.com/carlosv5/GREDOS/wiki/pox_scenario): this scenario deploy clients and cloud side except from the Banana Pi (physical). Uses the module l2_learning of Pox as SDN controller.
   - [Scenario 2: Floodlight as SDN controller and OVS as Residential Gateway](https://github.com/carlosv5/GREDOS/wiki/floodlight_all_virtual_scenario): this scenario deploy clients and cloud side and the residential gateway OVS. Uses the GREDOS project's network application in Floodlight as SDN controller.
   - [Scenario 3: Floodlight as SDN controller and Banana Pi as Residential Gateway](https://github.com/carlosv5/GREDOS/wiki/floodlight_scenario): this scenario deploy clients and cloud side except from the Banana Pi (physical). Uses the GREDOS project's network application in Floodlight as SDN controller.      
 - [Scenario 4: OpenStack as ISP Cloud](https://github.com/carlosv5/GREDOS/wiki/openstack_gredos): this scenario deploy cloud and client sides except from the Banana Pi (physical). Cloud side is deployed with OpenStack.
 
 ## BananaPi
You need to understand the Banana Pi's configuration in order to deploy the scenarios 1,3 and 4. 

[Here](https://github.com/carlosv5/GREDOS/wiki/BananaPi) there is an explanation.
 
## Author

This project has been developed by [Carlos Vega García](https://es.linkedin.com/in/carlos-vega-garc%C3%ADa-449795150) as a result of a Master's thesis in Universidad Politécnica de Madrid.

## References
* http://oa.upm.es/50230/ - Ricardo Flores's phd thesis with GREDOS's architecture design

