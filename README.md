# mininet-python
mynet.py -- here's the net I'm trying to connect to the internet

test.py -- an example of mininet host connecting to the internet

routerconf.sh, switchconf.sh -- configuration for router and switchs, should be placed in home directory

stp1.py -- topology that consists of 6 hosts and 3 switches with a loop

stp2.py -- topology from stp1 but without loops

stp3.py -- topology with a loop and stp enabled 

savedtopo.mn -- example of miniedit save file format

savedtopo.py -- topology made in miniedit and saved as python script

lab2.py -- a network with two vlans connected by router

lab2.sh -- configures vlan on switch, should be placed in home directory before launching lab2.py

topo_for_vlan_access_test.py -- topology consists of two switches and four hosts which are divided into two separate vlans

vlan_access_controller.py -- controller with L2 learning and vlan capabilities

topo_for_vlan_dot1q_test.py -- topology consists of two switches and five hosts which are divided into two separate vlans

vlan_dot1q_controller.py -- controller with L2 learning and dot1q support