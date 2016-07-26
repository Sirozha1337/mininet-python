# Turn openv switches into legacy switches
ovs-vsctl set-fail-mode s1 standalone
ovs-vsctl set-controller s1
ovs-vsctl set-fail-mode s2 standalone
ovs-vsctl set-controller s2

# Set up VLANs
ovs-vsctl set port s1-eth2 tag=10
ovs-vsctl set port s1-eth3 tag=20
ovs-vsctl set port s2-eth2 tag=10
ovs-vsctl set port s2-eth3 tag=20
ovs-vsctl set port s1-eth1 vlan_mode=native-tagged
ovs-vsctl set port s2-eth1 vlan_mode=native-tagged
