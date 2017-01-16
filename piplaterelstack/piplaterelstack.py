# Optokey, Inc.
# All Rights Reserved

# IMPORTANT: Install libraries recommended by pi-plates
# sudo apt-get update
# sudo apt-get install python-pip
# sudo pip install pi-plates

# Enable SPI in RP3 configuration
# download and install: sudo apt-get install python-spidev

# This routine performs the same function as usbrelstack.py but with pi-plates based relays
# Controls 2 pi plates, so 14 channels in total (works only with 7 relay plates)

# top plate is Address 7, bottom plate is address 6

import sys
import time
import piplates.RELAYplate as RELAY

# Defines address for Pi-Plates, start with the address of the top plate and then go down
plateAddress = [7,6]

def returnValue(value):
    return value

# Turns relay ON (1-14)
if len(sys.argv) > 1 and str(sys.argv[1]) == 'on':
    if int(sys.argv[2]) > 0 and int(sys.argv[2]) < 15:
        channel = int(sys.argv[2])
        address = plateAddress((channel-1)//7)
        relay = (channel-1)%7 + 1
        RELAY.relayON(address, relay)

# Turns relay OFF (1-14)
if len(sys.argv) > 1 and str(sys.argv[1]) == 'off':
    if int(sys.argv[2]) > 0 and int(sys.argv[2]) < 15:
        channel = int(sys.argv[2])
        address = plateAddress((channel-1)//7)
        relay = (channel-1)%7 + 1
        RELAY.relayOFF(address, relay)

# Either gives the status of each relay or a particular one (also returns 0/1 in that case)
if len(sys.argv) > 1 and str(sys.argv[1]) == 'status':
    if len(sys.argv) > 2:
        channel = int(sys.argv[2])
        address = plateAddress((channel-1)//7)
        relay = (channel-1)%7 + 1
        mask = 1
        mask = mask << (relay-1)
        rstate = RELAY.relaySTATE(address)
        if (rstate & mask) != 0:
            print 'Channel ' + str(channel) + ' is ON'
            returnValue(1)
        else:
            print 'Channel ' + str(channel) + ' is OFF'
            returnValue(0)
    else:
        rr = 0
        for ad in plateAddress:
            mask = 1
            rstate = RELAY.relaySTATE(ad)
            for i in range(7):
                rr = rr + 1
                if (rstate & mask) != 0:
                    print 'Channel ' + str(rr) + ' is ON'
                else:
                    print 'Channel ' + str(rr) + ' is OFF'
                mask = mask << 1

# Tests order of relays and switches all off
if len(sys.argv) > 1 and str(sys.argv[1]) == 'test':
    print("Testing 1 through 24")
    for ad in plateAddress:
        for i in range(6):
            RELAY.relayON(ad, i + 1)
            time.sleep(0.1)
            RELAY.relayOFF(ad, i + 1)

      
if len(sys.argv) == 1:
    print("Examples:")
    print("python piplatesrelstack.py status")
    print("        This command will show status of relays")
    print("python ppiplatesrelstack.pyy status 2")
    print("	   This command will show the status of relay 2 and also return 1/0")
    print("sudo python usbrelstack.py test")
    print("        This command will turn ON relay relays starting from 1 sequentially to 14")
    print("sudo python usbrelstack.py on 1")
    print("        This command will turn ON relay 1")
    print("sudo python usbrelstack.py off 5")
    print("        This command will turn OFF relay 5")
