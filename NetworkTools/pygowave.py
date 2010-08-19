import socket

def hello():
	print "Imported world"

def primitiveSTOMP(address, port):
	addr = (address, port)
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect(addr)
	while 1:
		print "\n----SEND:\n"
		send = ""
		while 1:
			inc = raw_input("")
			if inc=="//d":
				break
			else:
				send+=inc+"\n"
		if send=="done":
			break
		print "\n\nSENDING:",send
		# send the contents of the SEND variable
		sock.send(send+'\x00')
		print "\n\nReply:\n",sock.recv(2048)
