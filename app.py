import reg
from gui.statusicon import StatusIcon

r = reg.Registry()
r.newNetwork()

#print r.Network.connect("Campadrenaline@gmail.com","helpburn")
#r.newWaveList()

icon = StatusIcon(r)

