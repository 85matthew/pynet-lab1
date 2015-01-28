Directions for labs 2-1 and 2-2





1. Using SNMPv3 create a script that detects changes to the running configuration. If the running configuration is changed, then send an email notification to yourself identifying the router that changed and the time that it changed.

Note, the running configuration of pynet-rtr2 is changing every 15 minutes (roughly at 0, 15, 30, and 45 minutes after the hour).  This will allow you to test your script in the lab environment. I will continue to do this for at least the next week.

In this exercise, you will possibly need to save data to an external file. One way you can accomplish this is by using a pickle file, see:   
    http://youtu.be/ZJOJjyhhEvM  

A pickle file lets you save native Python data structures (dictionaries, lists, objects) directly to a file.


2. Using SNMPv3 create two SVG image files.  The first image file should graph input and output octets on interface FA4 on pynet-rtr1 every five minutes for an hour.  Use the pygal library to create the SVG graph file.  

The second SVG graph file should be the same as the first except graph unicast packets received and transmitted.

The relevant OIDs are as follows:

('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5')
('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5')
('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5')
('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')


Note, you should be able to scp (secure copy) your image file off the lab server. You can then open up the file using a browser.  For example, on MacOs I did the following (from the MacOs terminal):

scp kbyers@pylab.twb-tech.com:SNMP/class2/test.svg .

This copied the file from ~kbyers/SNMP/class2/test.svg to the current directory on my MAC.  

The format of the command is:

scp <remote-username>@<remote-hostname>:<remote_path>/<remote_file> .

The period at the end indicates copy it to the current directory on the local machine.




EXTRA:

Graphing SNMP Data

For graphing, I am using the pygal SVG graphics library:
http://pygal.org/

You can use this library to create SVG images.  SVG images should generally work with newer browsers (Chrome, Firefox, Safari, IE9+):

SVG Browser support:
http://caniuse.com/#feat=svg



The below code creates an SVG image using pygal from SNMP interface data.

>>>> CODE <<<<

import pygal

fa4_in_octets = [5269, 5011, 6705, 5987, 5011, 5071, 6451, 5011, 
                                5011, 6181, 5281, 5011]
fa4_out_octets =[5725, 5783, 7670, 6783, 5398, 5783, 9219, 3402, 
                                5783, 6953, 5668, 5783]

fa4_in_packets = [24, 21, 40, 32, 21, 21, 49, 9, 21, 34, 24, 21]
fa4_out_packets = [24, 21, 40, 32, 21, 21, 49, 9, 21, 34, 24, 21]

# Create a Chart of type Line
line_chart = pygal.Line()

# Title
line_chart.title = 'Input/Output Packets and Bytes'

# X-axis labels (samples were every five minutes)
line_chart.x_labels = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']

# Add each one of the above lists into the graph as a line with corresponding title
line_chart.add('InPackets', fa4_in_packets)
line_chart.add('OutPackets',  fa4_out_packets)
line_chart.add('InBytes', fa4_out_octets)
line_chart.add('OutBytes', fa4_in_octets)

# Create an output image file from this
line_chart.render_to_file('test.svg')

>>>> END CODE <<<<

You can view the image that was created at:
https://pynet.twb-tech.com/static/img/snmp_interfaces.svg

