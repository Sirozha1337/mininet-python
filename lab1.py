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

class NetworkTopo( Topo ):
    # Builds network topology
    def build( self, **_opts ):

        s1 = self.addSwitch ( 's1', failMode='standalone' )

        # Adding hosts
        d1 = self.addHost( 'd1', ip='192.168.0.1/28' )
        d2 = self.addHost( 'd2', ip='192.168.0.2/28' )
        d3 = self.addHost( 'd3', ip='192.168.0.3/28' )
        d4 = self.addHost( 'd4', ip='192.168.0.9/28' )
        d5 = self.addHost( 'd5', ip='192.168.0.10/28' )
        d6 = self.addHost( 'd6', ip='192.168.0.11/28' )
        
        # Connecting hosts to switches
        for d, s in [ (d1, s1), (d2, s1), (d3, s1)]:
            self.addLink( d, s )
        for d, s in [ (d4, s1), (d5, s1), (d6, s1)]:
            self.addLink( d, s )    


def run():

    topo = NetworkTopo()
    
    net = Mininet( topo=topo, controller=None )
    net.start()
    # Make Switch act like a normal switch
    #net['s1'].cmd('ovs-ofctl add-flow s1 action=normal')
    # Make Switch act like a hub
    #net['s1'].cmd('ovs-ofctl add-flow s1 action=flood')
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
