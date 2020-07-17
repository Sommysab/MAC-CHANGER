#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    options, arguments = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    if not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options

def change_mac(i, new_mac):
    mac_address = re.search(r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", new_mac)
    
    if(mac_address):
        subprocess.call(["ifconfig", i,  "down"])
        subprocess.call(["ifconfig", i, 'hw', 'ether', new_mac])
        subprocess.call(["ifconfig", i, "up"])
    else: 
        print("[-] Could not change MAC address. Make sure to type the correct format")
    

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_address_search_result = re.search(r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", ifconfig_result)
    
    if(mac_address_search_result):
        return mac_address_search_result.group(0)
    else: 
        print("[-] Could not read MAC address.")

# Input collector
options = get_arguments()

# Get Existing Mac
current_mac = get_current_mac(options.interface)
print("current Mac = " + str(current_mac))

# Update New Mac
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac==options.new_mac:
    print("[+] MAC address was successfully changed to ==> " + current_mac)
else:
    print("[-] MAC address did not get changed")


