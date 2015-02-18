#!/usr/bin/env python

'''
Run command from CLI with python and script name "ie- python eapi_vlan.py --name matt_w 666"

Valid Options:
    --name      example: python eapi_vlan.py --name "VLAN_NAME" "VLAN_NUMBER"
    --remove    example: python eapi_vlan.py --remove "VLAN_NUMBER"


EXAMPLE-    python eapi_vlan.py --name matt_w 666
            python eapi_vlan.py --remove 666


Script uses .eapi.conf file for device connection information, currently configured to be in ~/.eapi.conf

Current Contents

[connection:router]         (VARIABLE "router" in configuration is referencing this connection info)
username: eapi
password: 99saturday
transport: https
enablepwd: ""
port: 8243
host: 50.242.94.227
'''

from jsonrpclib import Server
import sys
#import time
import argparse
from pprint import pprint
import pyeapi
#import json



######
# Runs show command
#   Returns 2 values: ('Exists'= to if the vlan exists  - True/False
#                       'vlan_name' = Name of the Vlan if it exists Value/None as a string)
######################################
def show_cmd(vlan_id):
    try:
        device = pyeapi.connect_to('router')
    except:
        print "Couldn't connect to device"
        return False, None

    cmds = [ "show vlan {}".format(vlan_id) ]

    try:
        results = device.enable([cmds])
        fixed_dict = results[0]

    except:
        print "VLAN does not exist in switch..."
        return False, None

    try:
        vlan_name = get_vlan_name(fixed_dict, vlan_id)
        return True, vlan_name
    except:
        print "something broke"
        print sys.exc_info()[0] 
        return False, None

#####
# Grabs VLAN name from data returned
#   Returns VLAN name as string
######################################
def get_vlan_name(fixed_dict, vlan_id):
    return fixed_dict['result']['vlans'][str(vlan_id)]['name']

#####
# adds a VLAN to the switch and configures the VLAN name
#   Returns nothing
######################################
def add_vlan(vlan_id, vlan_name):
    try:
        device = pyeapi.connect_to('router')
    except:
        print "Error connecting to device"
        return True

    cmds = [ "vlan {}".format(vlan_id) ,  "name {}".format(vlan_name) ]

    try:
        results = device.config(cmds)

    except:
        print sys.exc_info()[0] 
    return

####
# removes a VLAN from the switching using vlan_id
#   Returns nothing
######################################
def rem_vlan(vlan_id):
    
    try:
        device = pyeapi.connect_to('router')
    except:
        print "Couldn't connect to device"
        return True
    cmds = [ "no vlan {}".format(vlan_id) ]

    try:
        results = device.config(cmds)

    except:
        print "VLAN does not exist in switch!"
        print sys.exc_info()[0]
    return

####
# Parses Arguments from command line call
#   Returns Args - after parsing for correct input and notifying user of any errors
######################################
def arg_parse(args):
    vlan_name = ""
    addVlan= False
    remVlan = False


    parser = argparse.ArgumentParser(
        description="Idempotent addition/removal of VLAN to Arista switch"
    )
    parser.add_argument("vlan_id", help="VLAN number to create or remove", action="store", type=int)
    parser.add_argument(
        "--name",
        help="Specify VLAN name",
        action="store",
        dest="vlan_name",
        type=str
    )
    parser.add_argument("--remove", help="Remove the given VLAN ID", action="store_true")

    args = parser.parse_args()
    remove = args.remove
    vlan_name = args.vlan_name 

    if remove == True and vlan_name != None:
        parser.error("add and remove tags are mutually exclusive")

    return args


####
# MAIN
######################################
def main(args):

    args = arg_parse(args)

    exists, existing_vlan_name = show_cmd(args.vlan_id)

    if args.remove and exists == True:
        rem_vlan(args.vlan_id)
        print "Removed VLAN"
    elif args.remove and exists != True:
        print "Unable to delete"
    elif args.vlan_name == existing_vlan_name:
        print "VLAN already configured with this name"
    elif args.vlan_name and exists == True:
        print "VLAN already exists."
    elif args.vlan_name and exists == False:
        add_vlan(args.vlan_id, args.vlan_name)
        print "Successfully created new VLAN"
    else:
        print "Something went wrong"
         
if __name__ == "__main__":
    main(sys.argv)
