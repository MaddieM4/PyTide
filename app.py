#!/usr/bin/python

import reg
from gtk.gdk import threads_init
from gui.statusicon import StatusIcon

threads_init()

r = reg.Registry()
r.newNetwork()

#print r.Network.connect("Campadrenaline@gmail.com","helpburn")
#r.newWaveList()

icon = StatusIcon(r)

