#!/usr/bin/python

"""
This script creates the network environment for Lab4:
- 5 routers, 7 switches and 2 hosts interconnected according to Fig 1 of Lab4
- Quagga service enabled in all routers
- IPv4 and IPv6 addressing given via zebra
- XTerm window launched for all devices.
"""
# Needed to patch Mininet's isShellBuiltin module
import sys

# Run commands when you exit the python script
import atexit

# patch isShellBuiltin (suggested by MiniNExT's authors)
import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

# Loads the default controller for the switches
# We load the OVSSwitch to use openflow v1.3
from mininet.node import Controller, OVSSwitch

# Needed to set logging level and show useful information during script execution.
from mininet.log import setLogLevel, info

# To launch xterm for each node
from mininet.term import makeTerms

# Provides the mininext> prompt
from mininext.cli import CLI

# Primary constructor for the virtual environment.
from mininext.net import MiniNExT

# We import the topology class for Lab4
from lab4_topo import Lab4Topo

# Variable initialization
net = None
hosts = None


def run():
    " Creates the virtual environment, by starting the network and configuring debug information "
    info('** Creating an instance of Lab4 network topology\n')
    topo = Lab4Topo()

    info('** Starting the network\n')
    global net
    global hosts
    # We use mininext constructor with the instance of the network, the default controller and the openvswitch
    net = MiniNExT(topo, controller=Controller, switch=OVSSwitch)
    net.start()
    
    info('** Executing custom commands\n')
    ##############################################
    # Space to add any customize command before prompting command line
    # We provide an example on how to assign IPv6 addresses to hosts h1 and h2 as they 
    # are not configured through Quagga
    # If required, you can add any extra logic to it
    
    # We gather only the hosts created in the topology (no switches nor controller)
    hosts = [ net.getNodeByName( h ) for h in topo.hosts() ]
    info('** Adding IPv6 address to hosts\n')
    for host in hosts:
        if host.name is 'h1':
            host.cmd('ip -6 addr add 2001:1:0:11::10/64 dev h1-eth1')
            host.cmd('ip -6 route add default via 2001:1:0:11::1')
        elif host.name is 'h2':            
            host.cmd('ip -6 addr add 2001:1:0:22::20/64 dev h2-eth1')
            host.cmd('ip -6 route add default via 2001:1:0:22::2')

    info('** Enabling xterm for all hosts\n')
    makeTerms( hosts, 'node' )
 

    ##############################################    
	# Enable the mininext> prompt 
    info('** Running CLI\n')
    CLI(net)

# Cleanup function to be called when you quit the script
def stopNetwork():
    "stops the network, cleans logs"

    if net is not None:
        info('** Tearing down Quagga network\n')
        # For sanity, when leaving the python script, we clean the logs again
        info('** Deleting logs and closing terminals for hosts\n')
        for host in hosts:
            if host.name in ['h1','h2']:
                pass
            else :
                host.cmd( "sh configs/%s/clean.sh" ) % host.name
        
    # This command stops the simulation
    net.stop()

if __name__ == '__main__':
    # Execute the cleanup function
    atexit.register(stopNetwork)
    # Set the log level on terminal
    setLogLevel('info')
    
    # Execute the script
    run()
