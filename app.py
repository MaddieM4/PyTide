#!/usr/bin/python

import reg
from gtk.gdk import threads_init
from gui.statusicon import StatusIcon

threads_init()

r = reg.Registry()
r.newNetwork()

icon = StatusIcon(r)

