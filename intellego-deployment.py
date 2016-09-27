#!/usr/bin/env python

import sys
import six
import requests
import pyVmomi
import ssl

#print(sys.path)

#from pyVim.connect import SmartConnect, Disconnect
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim


#print('\n***** This script will be used to get arguments for creating vms ******\n')

# Handling Options Block
from optparse import OptionParser
parser = OptionParser()
parser.add_option('-p', '--project', action='store', type='string', dest='project',
                  help = 'A Project name. Ex: intellego')

def get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

parser.add_option('-i', '--ipaddresses', type='string', action='callback', callback = get_comma_separated_args,
                  dest = 'ipaddrs', help = 'Enclose list of IPs within double-quotes')

parser.add_option('-o', '--option', action = 'store', dest = 'option',
                  help = 'Example: single_plus_vmc, two_pair, four_pair, high_availability')

parser.add_option('-s', '--vcenterhost', action = 'store', dest = 'hostname',
                  help = 'vCenter Hostname')

parser.add_option('-u', '--username', action = 'store', dest = 'username',
                  help = 'Supply username to connect to vCenter')

parser.add_option('-a', '--password', action = 'store', dest = 'password',
                  help = 'Supply password to connect to vCenter')

(options, args) = parser.parse_args()

# End of handling options

# Make sure user supplied enough arguments
if not ( options.ipaddrs and options.option ):
    parser.print_help()
    print ('\n ERROR: IP addresses and/or deployment option missing!')
    sys.exit(1)

# Decide how many pairs to create
if ( options.option == 'single_plus_vmc'):
    if len(options.ipaddrs) is not 2:
        print('Error: Two IP addresses are required!')
        sys.exit(1)
    else:
        print('INFO: Ready to create nodes!')
elif (options.option == 'two_pair'):
    if len(options.ipaddrs) is not 4:
        print('Error: Four IP addresses are required!')
        sys.exit(1)
    else:
        print('INFO: Ready to create nodes!')
else:
    print('Unsupported option')
    parser.print_help()
    sys.exit(1)

# We have necessary IP's, project and options to create VM's at this point
def main():
    sslContext = None
    sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslContext.verify_mode = ssl.CERT_NONE

    print("Connecting to " + options.hostname + " with username " + options.username)
    si = None
    si = connect.SmartConnect(host=options.hostname, user=options.username, pwd=options.password, sslContext=sslContext)


    #si = connect.SmartConnect(host='10.0.155.52', user='skrishna@vsphere.local', pwd='Mchai2122')
    print("Time from vCenter: ")
    print(si.CurrentTime())

    print("Ready to create a vm for " + options.project)

    content = si.RetrieveContent()
    datacenter = content.rootFolder.childEntity[0]

    print(datacenter)


    # Disconnect once done
    connect.Disconnect(si)
    return

# Start
if __name__ == "__main__":
    main()



