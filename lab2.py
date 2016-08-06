#!/usr/bin/python

from __future__ import print_function

import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Intf
from mininet.node import Controller

class LinuxRouter( Node ):
    # Turns host into IP router
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class NetworkTopo( Topo ):
    # Class that builds network topology consisting of four hosts, one router, three switches
    def build( self, **_opts ):

        router = self.addNode( 'r0', cls=LinuxRouter, ip='192.168.1.1/24' )

        s1 = self.addSwitch( 's1', failMode='standalone' )

        self.addLink( s1, router, intfName2='r0-eth1',
                      params2={ 'ip' : '192.168.1.1/24' } ) 

        self.addLink( s1, router, intfName2='r0-eth2',
                      params2={ 'ip' : '192.168.2.1/24' } )

        h1 = self.addHost( 'h1', ip='192.168.1.100/24',
                           defaultRoute='via 192.168.1.1' )
        
        h2 = self.addHost( 'h2', ip='192.168.2.100/24',
                           defaultRoute='via 192.168.2.1')

        h3 = self.addHost( 'h3', ip='192.168.1.101/24',
                           defaultRoute='via 192.168.1.1' )

        h4 = self.addHost( 'h4', ip='192.168.2.101/24',
                           defaultRoute='via 192.168.2.1' )

        for h, s in [ (h1, s1), (h2, s1), (h3, s1), (h4, s1) ]:
            self.addLink( h, s )

def run():

    topo = NetworkTopo()
    
    net = Mininet( topo=topo, controller=None )

    net.start()

    # Configure vlans on switch
    net[ 's1' ].cmd( './lab2.sh' )

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
