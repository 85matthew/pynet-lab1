#!/usr/bin/python
#import pysnmp


'''
File is used in conjunction with lab2-2_grapher.py script.
Instructions:

1. This script "lab2-2_poller.py" should be run and allowed to run for 1 hour
    *can be achieved with command 'lab2-2_poller.py&'
    * This will allow the job to run in the background. Job will auto terminate after 1 hour
2. After lab2-2_poller.py script complets- datafile.dat will be created in same directory(contains csv data)

3. The user may then run script "lab-2-2_grapher.py" from the same directory
4. lab2-2_grapher.py will unpack data from datafile.dat and create 2 graph files named "test1.svg" and "test2.svg" 
'''

from snmp_helper import snmp_get_oid_v3,snmp_extract
from time import sleep


######
#SNMP Parameters
#####
snmp_host= ("50.242.94.227", 7961)
a_user = "pysnmp" 
auth_key = "galileo1"
encrypt_key = "galileo1"
snmp_user = (a_user, auth_key, encrypt_key)

####
#OID Information
#####
OIDs = { 'ifDescr_fa4': '1.3.6.1.2.1.2.2.1.2.5',
        'ifInOctets_fa4': '1.3.6.1.2.1.2.2.1.10.5',
        'ifInUcastPkts_fa4': '1.3.6.1.2.1.2.2.1.11.5',
        'ifOutOctets_fa4': '1.3.6.1.2.1.2.2.1.16.5',
        'ifOutUcastPkts_fa4': '1.3.6.1.2.1.2.2.1.17.5',
        }

####
#Queries snmp device for specified OIDs. These values are saved in the "query_value" list
####
def querySNMPv3(snmp_user, snmp_host, OIDs):

    #Create empty dict value 
    query_value = {}
    #Initialize count to 0
    count = 0

    #Query SNMP device for each OID value, extract the value, store in query_value Array
    for eachKey in OIDs:

        query_value[count]  = snmp_get_oid_v3(snmp_host, snmp_user, OIDs[eachKey]) 
        query_value[count] = snmp_extract(query_value[count])
        count = count + 1
    return query_value, count

#####
#Write the returned SNMP values to a file in CSV format
####
def writeToFile(returnedValues, count):
    
    #Open datafile "datafile.dat" in binary/append mode. If it does not exist it will be created automatically
    #Only last data item per row should have newline character
    data_file = open('datafile.dat', "ab")
        
    index = 0
    for index in range(0, count):
        if index != count - 1:
            data_file.write(returnedValues[index] + ',')

        else:
            data_file.write(returnedValues[index] + '\n')
    #Close the text file
    data_file.close()



#Create empty dict value
returnedValues = {}

#Initialize count variable- used to count rows of data in file
count = 0

#Initialize variable- used to count how many times the script has been executed between sleep() function
#We want to run it 12 times (every 5 minutes for 1 hour)
runTimeCount = 0

while runTimeCount < 12:

    returnedValues, count = querySNMPv3(snmp_user, snmp_host, OIDs)
    writeToFile(returnedValues, count)
    runTimeCount = runTimeCount + 1
    if runTimeCount == 12:
        #If we have already executed 12 times, break the while loop
        break;
    else:
        #sleep() for 5 minutes until the next polling
        sleep(300)
