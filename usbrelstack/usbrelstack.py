# Optokey, Inc.
# All Rights Reserved

# IMPORTANT: Certain libraries need to be preinstalled, as described in the file relayctl.py

# IMPORTANT: There is no distinction between identical USB relay boards. Use testing routine to verify relay numbering.

import usb.core
import usb.util
import time
import sys

import relayctl

# Defines 8 channel relays by SMAKN
Vendor = 0x0403
Product = 0x6001
Stacks = 0

# Stores USB devices with vendor/product id's specified
devs = []


def loadDevices():
    devices = usb.core.find(find_all=True, idVendor = Vendor, idProduct = Product)
    countEm = 0
    for dev in devices:
        if dev.idVendor == 1027 and dev.idProduct == 24577:
            devs.append(dev)
            countEm += 1
    return countEm

def isItOnOrOff(number):
    if number == 0:
        return "OFF"
    else:
        return "ON"  

def returnValue(value):
    return value

# Main program
# Load devices
Stacks = loadDevices()

# Lists information on all relays available
if len(sys.argv) > 1 and str(sys.argv[1]) == 'list':
    print("Available devices:")
    countDevices = 0
    for dev in devs:
        print 'Device', countDevices, '= idVendor:', hex(dev.idVendor), '(', dev.idVendor, ') idProduct:', hex(dev.idProduct), '(', dev.idProduct, ') Address:', dev.address, ' Bus:', dev.bus
        countDevices += 1

# Tests order of relays and switches all off
if len(sys.argv) > 1 and str(sys.argv[1]) == 'test':
    print("Testing 1 through 24")
    for d in range(Stacks):
        dev = devs[d]
        for i in range(1, 9):
            relayctl.switchon(dev, i)
            time.sleep(0.1)
            relayctl.switchoff(dev, i)

# Displays status of all relays or a particular one
if len(sys.argv) > 1 and str(sys.argv[1]) == 'status':
    if len(sys.argv) > 2:
	channel = int(sys.argv[2])
	dev = devs[(channel-1)//8]
	relay = (channel-1)%8 + 1
	print ("Channel " + str(channel) + " is " + isItOnOrOff(relayctl.getstatus(dev, relay)))
        returnValue(relayctl.getstatus(dev, relay))
    else:
    	for d in range(Stacks):
            dev = devs[d]
            for i in range(1, 9):
            	print("Channel "+str(i)+" on device " + str(d) + " is "+isItOnOrOff(relayctl.getstatus(dev, i)))


if len(sys.argv) > 1 and str(sys.argv[1]) == 'on':
    if int(sys.argv[2]) > 0 and int(sys.argv[2]) < 25:
        channel = int(sys.argv[2])
        dev = devs[(channel-1)//8]
        relay = (channel-1)%8 + 1
        relayctl.switchon(dev, relay)

if len(sys.argv) > 1 and str(sys.argv[1]) == 'off':
    if int(sys.argv[2]) > 0 and int(sys.argv[2]) < 25:
        channel = int(sys.argv[2])
        dev = devs[(channel-1)//8]
        relay = (channel-1)%8 + 1
        relayctl.switchoff(dev, relay)

if len(sys.argv) == 1:
    print("Examples:")
    print("sudo python usbrelstack.py list")
    print("        This command will list all available USB relays")
    print("sudo python usbrelstack.py status")
    print("        This command will show status of relays")
    print("sudo python usbrelstack.py status 2")
    print("	   This command will show the status of relay 2 and also return 1/0")
    print("sudo python usbrelstack.py test")
    print("        This command will turn ON relay relays starting from 1 sequentially to 24")
    print("sudo python usbrelstack.py on 1")
    print("        This command will turn ON relay 1")
    print("sudo python usbrelstack.py off 5")
    print("        This command will turn OFF relay 5")
