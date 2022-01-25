import subprocess
import optparse
import re
from getmac import get_mac_address


def argument():
    Parser = optparse.OptionParser()
    Parser.add_option("-n", "--network_interface", dest="network_interface", help="Name of the network interface of "
                                                                                  "which the MAC address has "
                                                                                  "to be changed")
    Parser.add_option("-c", "--new_mac", dest="new_mac", help="New MAC address")
    (option, arguments) = Parser.parse_args()
    if not option.network_interface:
        Parser.error("[-] Please specify a network interface. Use --help or -h for more info.")
    if not option.new_mac:
        Parser.error("[-] Please enter the new MAC address. Use --help or -h for more info.")
    while 1:
        if re.match(r"^[a-fA-F0-9]{2}[:][a-fA-F0-9]{2}[:][a-fA-F0-9]{2}[:][a-fA-F0-9]{2}[:][a-fA-F0-9]{2}[:]["
                    r"a-fA-F0-9]{2}", option.new_mac):
            break
        else:
            Parser.error("[-] You have specified an incorrect format for MAC address. Please Enter the MAC address in "
                         "the "
                         "format "
                         "xx:xx:xx:xx:xx:xx, where x is lower case alphabets from a-f or upper case alphabets from "
                         "A-F or "
                         "numbers from 0-9.")
            break
    while 1:
        if option.network_interface == "eth0":
            break
        if option.network_interface == "wlan0":
            break
        if option.network_interface == "lo":
            Parser.error("[-] This network interface does not have a MAC address")
            break
        else:
            Parser.error("[-] " + option.network_interface + " is not a valid network interface. Please specify a"
                                                             " valid network interface.")
            break
    return option


def mac(network_interface, new_mac):
    print("[+] MAC address of " + network_interface + " has been changed to " + new_mac)
    subprocess.call(["ifconfig", network_interface, "down"])
    subprocess.call(["ifconfig", network_interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", network_interface, "up"])


def check(interface):
    check_mac_address = get_mac_address(interface)
    return check_mac_address


options = argument()
check_mac = check(options.network_interface)
print("[+] Current MAC is ", check_mac)
mac(options.network_interface, options.new_mac)
check_mac = check(options.network_interface)
while 1:
    parser = optparse.OptionParser()
    if check_mac == options.new_mac:
        print("[+] The new MAC address is ", check_mac)
        break
    else:
        parser.error("[-] Failed to change the MAC address")
        break
