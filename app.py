import reg
from gui.statusicon import StatusIcon

r = reg.Registry()
r.newWaveList()

icon = StatusIcon(r)

# No longer needed with StatusIcon main loop
#z = raw_input("Press Enter (or any other key, really) to quit.\n")
