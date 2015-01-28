#!/usr/bin/python
#import pysnmp

from snmp_helper import snmp_get_oid_v3,snmp_extract
#from sys import argv
import smtplib
import pickle
from email.mime.text import MIMEText
import time



######
#SNMP Parameters
#####
snmp_host= ("50.242.94.227", 8061)

a_user = "pysnmp" 
auth_key = "galileo1"
encrypt_key = "galileo1"
snmp_user = (a_user, auth_key, encrypt_key)

oid_run_chg = "1.3.6.1.4.1.9.9.43.1.1.1.0"
oid_hostname = "1.3.6.1.2.1.1.5.0"
oid_sysuptime = "1.3.6.1.2.1.1.3.0"
pickle_file = "pickle.dat"



def chk_file(hostname, oid_running_value, pickle_file):
    # Verifies proper pickle.dat file & creates if necessary

    fileNotFound = False
    try:
        pickle.load (open (pickle_file, "rb") )
    except IOError:
        #Catch error of "file not found", create the file and write a value
        fileNotFound = True 
        print "File not found... Creating file"
        pickle.dump ( oid_running_value, open( pickle_file, "wb") )
        return True

    if fileNotFound == False:
        #File exists so load the value from the file
        file_value = pickle.load( open(pickle_file, "rb") )

        #Check if the current value is newer than the value written to file
        if float(file_value) < float(oid_running_value):
            #Current value is newer so write to file
            pickle.dump ( oid_running_value, open(pickle_file, "wb") )
            return True
    
def calc_datetime(oid_running_value, oid_sysuptime):
    # Uses passed values to calculate the time of the last running config change

    currentTime = time.time()

    # Converts OID sysuptime timestamp from Tics to seconds (divide by 100)
    oid_sysuptime = oid_sysuptime / 100

    # Converts OID running-config-change timestamp from Tics to seconds (divide by 100)
    oid_running_value = float(oid_running_value) / 100

    #Calculate time of last change and return value
    timeChanged = currentTime - (float(oid_sysuptime) - float(oid_running_value))
    return timeChanged 
  

def send_email(sender, recipient, hostname, timeChanged):
    # Sends an email with change hostname and time

    message = MIMEText(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timeChanged)) + " Configuration changed on " + hostname)
    message['Subject'] = hostname + " Config Changed:"
    message['From'] = sender
    message['To'] = recipient

    # Create SMTP connection object to localhost
    smtp_conn = smtplib.SMTP('localhost')

    # Send the email
    smtp_conn.sendmail(sender, recipient, message.as_string())

    # Close SMTP connection
    smtp_conn.quit()

#main()
#parses OID Values
#####    
oid_running_value  = snmp_get_oid_v3(snmp_host, snmp_user, oid_run_chg)
hostname = snmp_get_oid_v3(snmp_host, snmp_user, oid_hostname)
oid_sysuptime = snmp_get_oid_v3(snmp_host, snmp_user, oid_sysuptime)
oid_running_value = snmp_extract(oid_running_value)
hostname = snmp_extract(hostname)
oid_sysuptime = snmp_extract(oid_sysuptime)
oid_sysuptime = float(oid_sysuptime)

# Calculate time for last running config change
timeChanged = calc_datetime(oid_running_value, oid_sysuptime)

#Check if running config has been changed. If so, send an email with changed information
if chk_file(hostname, oid_running_value, pickle_file):
    send_email("bogus@gmail.com", "mwilkerson@trace3.com", hostname, timeChanged) 
