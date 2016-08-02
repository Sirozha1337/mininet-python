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
    # Builds network topology with a loop 
    def build( self, **_opts ):

        # Adding legacy switches
        s1, s2, s3 = [ self.addSwitch( s, failMode='standalone' ) 
                   for s in ( 's1', 's2', 's3' ) ]
        
        # Creating links
        self.addLink( s1, s2 )
        self.addLink( s2, s3 )
        self.addLink( s3, s1 )

        # Adding hosts
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )
        h4 = self.addHost( 'h4' )
        h5 = self.addHost( 'h5' )
        h6 = self.addHost( 'h6' )
        
        # Connecting hosts to switches
        for h, s in [ (h1, s1), (h2, s1), (h3, s2), (h4, s2), (h5, s3), (h6, s3) ]:
            self.addLink( h, s )


def run():

    topo = NetworkTopo()
    
    net = Mininet( topo=topo, controller=None )
    net.start()
    net['s1'].cmd('ovs-vsctl set bridge s1 stp-enable=true')
    net['s2'].cmd('ovs-vsctl set bridge s2 stp-enable=true')
    net['s3'].cmd('ovs-vsctl set bridge s3 stp-enable=true')
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
