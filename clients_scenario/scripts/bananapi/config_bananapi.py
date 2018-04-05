#!usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, json
from time import sleep

config_file_path = '/etc/base.rc.local'
out_file_path = '/etc/rc.local'


def lauch():

        while True:

                os.system('clear')
                print '\n---Residential Gateway Configuration File Creator:'
                print '\n\tOptions:'
                print '\t1: Create a Configuration File'
                print '\t2: Exit'

                option = int(raw_input('\n\t*Select an Option:'))

                if option == 1:
                        os.system('clear')
                        TVlanID = raw_input('\n\t*Introduce the traffic VLAN ID')
                        trafficSubnet = raw_input('\n\t*Introduce the traffic subnet:')
                        OFVlanID = raw_input('\n\t*Introduce the OpenFlow VLAN ID:')
                        OFSubnet = raw_input('\n\t*Introduce the OpenFlow subnet:')

                        # Read in the file
                        with open(config_file_path, 'r') as file :
                          filedata = file.read()

                        # Replace the target string
                        filedata = filedata.replace('controllerIP', OFSubnet.split("0/24")[0]+"30")
                        filedata = filedata.replace('OFVlanID', OFVlanID)
                        filedata = filedata.replace('OFIP', OFSubnet.split("0/24")[0]+"87")
                        filedata = filedata.replace('gwIP', trafficSubnet.split("0/24")[0]+"254")
                        filedata = filedata.replace('br0IP', trafficSubnet.split("0/24")[0]+"1" )
                        filedata = filedata.replace('TVlanID', TVlanID)

                        # Write the file out again
                        with open(out_file_path, 'w') as file:
                          file.write(filedata)
                        os.chmod(out_file_path, 0777)

                elif option == 2:
                        os.system('clear')
                        sys.exit()

                else:
                        os.system('clear')
                        print '\n\t!!!!!!!!!! Invalid option, try again !!!!!!!!!!'
                        sleep(1)
#---------------------------------------------------------------------------------------------------------------

lauch()

