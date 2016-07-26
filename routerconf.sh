# Make a new bridge and add interfaces to it
ip link add name br0 type bridge
ip link set br0 up
ip link set r0-eth1 up
ip link set r0-eth1 master br0
ip link set r0-eth2 up
ip link set r0-eth2 master br0

# Add two subinterfaces to the bridge
ip link add link br0 name br0.10 type vlan id 10
ip link add link br0 name br0.20 type vlan id 20

# Bring those interfaces up
ip link set br0.10 up
ip link set br0.20 up

# Delete IPs from interfaces we already 
# connected through the bridge
ifconfig r0-eth1 0
ifconfig r0-eth2 0

# Add IP addresses to bridge subinterfaces
ip addr add 192.168.1.1/24 dev br0.10
ip addr add 192.168.2.1/24 dev br0.20
