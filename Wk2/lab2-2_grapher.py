#!/usr/bin/python
#import pysnmp

'''
File is used in conjunction with lab2-2_poller.py script.
Instructions:

1. lab2-2_poller.py should be run and allowed to run for 1 hour
    *can be achieved with command 'lab2-2_poller.py&'
    * This will allow the job to run in the background. Job will auto terminate after 1 hour
2. After lab2-2_poller.py script complets- datafile.dat will be created in same directory
3. This script "lab-2-2_grapher.py" can then be run from the same directory
4. lab2-2_grapher.py will unpack data from datafile.dat and create 2 graph files named "test1.svg" and "test2.svg" 
'''



from snmp_helper import snmp_get_oid_v3,snmp_extract
import pygal


####
#Takes input of dataPackage from readFromFile function and graphs it
#Graph looks like a straight line due to the large difference between input/output packets & octets
###
def graphData(packagedData):
    
    # Create empty arrays
    ifOutUcastPkts = []
    ifOutOctets = []
    ifInUcastPkts = []
    ifInOctets = []
    ifDescr = ""

    #Unpackages the data into rows of 5 values from readFromFile function
    #pushes new values onto each array below
    for dataRow in packagedData:
        ifOutUcastPkts.append(int(dataRow[0]))
        ifOutOctets.append(int(dataRow[1]))
        ifInUcastPkts.append(int(dataRow[2]))
        ifInOctets.append(int(dataRow[3]))
        if len(ifDescr) == 0:
            ifDescr = dataRow[4]

    # Create a Chart of type Line
    line_chart1 = pygal.Line()
    line_chart2 = pygal.Line()

    # Add Title to Graph
    line_chart1.title = 'Input/Output Octets'
    line_chart2.title = 'Input/Output Unicast Packets'

    # X-axis labels (samples were every five minutes)
    line_chart1.x_labels = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
    line_chart2.x_labels = line_chart1.x_labels

    # Add each one of the above lists into the graph as a line with corresponding title
    line_chart1.add('InOctets', ifInOctets)
    line_chart1.add('OutOctets',  ifOutOctets)
    line_chart2.add('InUcastPkts', ifInUcastPkts)
    line_chart2.add('OutUcastPkts', ifOutUcastPkts)

    # Create an output image file from this
    line_chart1.render_to_file('test1.svg')
    line_chart2.render_to_file('test2.svg')



#####
#Opens datafile which contains data in csv seperated values
#
def readFromFile():
    
    #Open data file "datafile.dat". This assumes the file exists by running the lab2-2_poller.py script
    data_file = open('datafile.dat', "rb")

    #Create Empty Array to store data in
    packagedData = []
        
    #Seperates the CSV data and stores them into the packagedData array
    for row in data_file:
        values = row.split(",")
        values[4] = values[4].rstrip()
        packagedData.append(values)

    #Close data file after reading values
    data_file.close()
    
    return packagedData

###
#main()
###

#Create empty array in main()

packagedData = []

packagedData = readFromFile()
graphData(packagedData)

