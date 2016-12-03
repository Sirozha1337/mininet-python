# Copyright 2016 Chernyaev Sergey
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This component is an L2 Learning switch with VLAN access and dot1q support 
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet

log = core.getLogger()



class L2Switch (object):
  """
  A L2Switch object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection
      
    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Use this table to keep track of which ethernet address is on
    # which switch port (keys are MACs, values are ports).
    self.mac_to_port = {}

    self.vlan_to_port = {}
    log.debug( self.connection.dpid )
    if self.connection.dpid == 1:
      self.vlan_to_port[1] = 10
      self.vlan_to_port[2] = 20
      self.vlan_to_port[3] = 20
      self.vlan_to_port[4] = 1 # dot1q
      self.vlan_to_port[65534] = 0 # ignore 

    if self.connection.dpid == 2:
      self.vlan_to_port[1] = 1
      self.vlan_to_port[2] = 10
      self.vlan_to_port[3] = 20
      self.vlan_to_port[65534] = 0
      

  def resend_packet (self, packet_in, out_ports):
    """
    Instructs the switch to resend a packet that it had sent to us.
    "packet_in" is the ofp_packet_in object the switch had sent to the
    controller due to a table-miss.
    """
    log.debug( "Sending out: %s" % out_ports )

    msg = of.ofp_packet_out()
    msg.data = packet_in
    
    # Add actions for each out port
    for out_port in out_ports:
      # If port is dot1q put on vlan tag
      if self.vlan_to_port[out_port] == 1:
        action = of.ofp_action_vlan_vid(vlan_vid = self.vlan_to_port[packet_in.in_port])
      # Else strip vlan tag
      else:
        action = of.ofp_action_strip_vlan()
      msg.actions.append(action)
      
      # Send the packet out of the specified port
      action = of.ofp_action_output(port = out_port)
      msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)
    log.debug("Packet sent out: %s" % out_ports )
    

  def act_like_switch (self, packet, packet_in):
    """
    Implement switch-like behavior.
    """

    # Here's some psuedocode to start you off implementing a learning
    # switch.  You'll need to rewrite it as real Python code.
    log.debug("DPID: %s" % self.connection.dpid)

    # Learn source vlan of the packet
    if packet.type == ethernet.VLAN_TYPE:
      src_vlan = packet.find('vlan').id
    else:
      src_vlan = self.vlan_to_port[packet_in.in_port]

    log.debug("Source VLAN: %s" % src_vlan) 

    # Learn the port for the source MAC
    self.mac_to_port[packet.src] = packet_in.in_port # add or update mac table entry

    # Ports to send out the packet
    out_ports = []

    #if the port associated with the destination MAC of the packet is known
    if packet.dst in self.mac_to_port: 
      log.debug("Mac is in table")

      dst_vlan = self.vlan_to_port[self.mac_to_port[packet.dst]]

      #if the port is in the same vlan as sending port
      if src_vlan == dst_vlan or dst_vlan == 1:

        # Send packet out the associated port
        out_ports.append(self.mac_to_port[packet.dst])
        self.resend_packet(packet_in, out_ports)
        
        log.debug("Installing flow. Source port: %s. Destination port: %s.", packet_in.in_port, self.mac_to_port[packet.dst])

        # Install the flow table entry
        msg = of.ofp_flow_mod()

        ## Set fields to match received packet
        msg.match = of.ofp_match(dl_dst = packet.dst)
        
        #< Set other fields of flow_mod (timeouts? buffer_id?) >
        msg.idle_timeout = 60
        
        # Add action to add vlan tag or strip it
        if dst_vlan == 1:
          action = of.ofp_action_vlan_vid(vlan_vid = src_vlan)
        else:
          action = of.ofp_action_strip_vlan()
        msg.actions.append(action)

        # Add action to resend packet out of the specified port
        msg.actions.append(of.ofp_action_output(port = self.mac_to_port[packet.dst]))
        self.connection.send(msg)
        
    else:
      # Sending to all ports in same vlan as the input port or dot1q port, ignore port connected to controller
      log.debug("Adress is not in table, flooding: ")
      for port in self.connection.ports:
        if port != packet_in.in_port and (self.vlan_to_port[port] == src_vlan or self.vlan_to_port[port] == 1):
           out_ports.append(port)
      log.debug(out_ports)
      if len(out_ports) > 0:
        self.resend_packet(packet_in, out_ports)


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.

    self.act_like_switch(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug( event.connection.ports )
    log.debug("Controlling %s" % (event.connection,))
    L2Switch(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
