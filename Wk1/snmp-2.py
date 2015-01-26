#!/usr/bin/python
#import pysnmp

from snmp_helper import snmp_get_oid,snmp_extract
from sys import argv



for i in argv[1:len(argv)]:

    COMMUNITY_STRING = "galileo"
    IP, SNMP_PORT  = i.split(':')

    a_device = (IP, COMMUNITY_STRING, SNMP_PORT)

    OIDs = { "1.3.6.1.2.1.1.1.0", "1.3.6.1.2.1.1.5.0" }

    for j in OIDs:
        snmp_data = snmp_get_oid(a_device, oid=j)
        output = snmp_extract(snmp_data)
        if j == "1.3.6.1.2.1.1.5.0":
            print output.upper() + '\n'
        else:
            print output + '\n'
