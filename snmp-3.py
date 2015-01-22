#!/usr/bin/python
#import pysnmp

from snmp_helper import snmp_get_oid,snmp_extract
from sys import argv

OIDs = { "run": "1.3.6.1.4.1.9.9.43.1.1.1.0", 
        "start": "1.3.6.1.4.1.9.9.43.1.1.3.0",
        "hostname": "1.3.6.1.2.1.1.5.0" }

def chk_saved(running, startup):
    if (startup == 0):
        print "Startup config has not been changed since last reboot"
    elif (startup >= running):
        print "Startup config is up to date"
    else:
        print "Startup config needs to be saved" 

COMMUNITY_STRING = "galileo"

for i in argv[1:len(argv)]:

    IP, SNMP_PORT  = i.split(':')

    a_device = (IP, COMMUNITY_STRING, SNMP_PORT)

    print snmp_extract(snmp_get_oid(a_device, oid=OIDs['hostname']))
    startup_value = snmp_get_oid(a_device, oid=OIDs['start'])
    startup_value = int(snmp_extract(startup_value))
    running_value = snmp_get_oid(a_device, oid=OIDs['run'])
    running_value = int(snmp_extract(running_value))

    chk_saved(running_value, startup_value)
    print
