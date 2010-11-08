"""
$Id: Base.py,v 1.12.2.10 2008/08/01 03:58:03 customdesigned Exp $

This file is part of the pydns project.
Homepage: http://pydns.sourceforge.net

This code is covered by the standard Python License.

    Base functionality. Request and Response classes, that sort of thing.
"""

import socket, string, types, time, select
import Type,Class,Opcode
import asyncore
#
# This random generator is used for transaction ids and port selection.  This
# is important to prevent spurious results from lost packets, and malicious
# cache poisoning.  This doesn't matter if you are behind a caching nameserver
# or your app is a primary DNS server only. To install your own generator,
# replace DNS.Base.random.  SystemRandom uses /dev/urandom or similar source.  
#
try:
  from random import SystemRandom
  random = SystemRandom()
except:
  import random

class DNSError(Exception): pass

# Lib uses DNSError, so import after defining.
import Lib

defaults= { 'protocol':'udp', 'port':53, 'opcode':Opcode.QUERY,
            'qtype':Type.A, 'rd':1, 'timing':1, 'timeout': 30 }

defaults['server']=[]

def ParseResolvConf(resolv_path="/etc/resolv.conf"):
    "parses the /etc/resolv.conf file and sets defaults for name servers"
    global defaults
    lines=open(resolv_path).readlines()
    for line in lines:
        line = string.strip(line)
        if not line or line[0]==';' or line[0]=='#':
            continue
        fields=string.split(line)
        if len(fields) < 2: 
            continue
        if fields[0]=='domain' and len(fields) > 1:
            defaults['domain']=fields[1]
        if fields[0]=='search':
            pass
        if fields[0]=='options':
            pass
        if fields[0]=='sortlist':
            pass
        if fields[0]=='nameserver':
            defaults['server'].append(fields[1])

def DiscoverNameServers():
    import sys
    if sys.platform in ('win32', 'nt'):
        import win32dns
        defaults['server']=win32dns.RegistryResolve()
    else:
        return ParseResolvConf()

class DnsRequest:
    """ high level Request object """
    def __init__(self,*name,**args):
        self.donefunc=None
        self.async=None
        self.defaults = {}
        self.argparse(name,args)
        self.defaults = self.args
        self.tid = 0

    def argparse(self,name,args):
        if not name and self.defaults.has_key('name'):
            args['name'] = self.defaults['name']
        if type(name) is types.StringType:
            args['name']=name
        else:
            if len(name) == 1:
                if name[0]:
                    args['name']=name[0]
        for i in defaults.keys():
            if not args.has_key(i):
                if self.defaults.has_key(i):
                    args[i]=self.defaults[i]
                else:
                    args[i]=defaults[i]
        if type(args['server']) == types.StringType:
            args['server'] = [args['server']]
        self.args=args

    def socketInit(self,a,b):
        self.s = socket.socket(a,b)

    def processUDPReply(self):
        if self.timeout > 0:
            r,w,e = select.select([self.s],[],[],self.timeout)
            if not len(r):
                raise DNSError, 'Timeout'
        (self.reply, self.from_address) = self.s.recvfrom(65535)
        self.time_finish=time.time()
        self.args['server']=self.ns
        return self.processReply()

    def processTCPReply(self):
        if self.timeout > 0:
            r,w,e = select.select([self.s],[],[],self.timeout)
            if not len(r):
                raise DNSError, 'Timeout'
        f = self.s.makefile('r')
        header = f.read(2)
        if len(header) < 2:
            raise DNSError,'EOF'
        count = Lib.unpack16bit(header)
        self.reply = f.read(count)
        if len(self.reply) != count:
            # FIXME: Since we are non-blocking, it could just be a large reply
            # that we need to loop and wait for.
            raise DNSError,'incomplete reply'
        self.time_finish=time.time()
        self.args['server']=self.ns
        return self.processReply()

    def processReply(self):
        self.args['elapsed']=(self.time_finish-self.time_start)*1000
        u = Lib.Munpacker(self.reply)
        r=Lib.DnsResult(u,self.args)
        r.args=self.args
        #self.args=None  # mark this DnsRequest object as used.
        return r
        #### TODO TODO TODO ####
#        if protocol == 'tcp' and qtype == Type.AXFR:
#            while 1:
#                header = f.read(2)
#                if len(header) < 2:
#                    print '========== EOF =========='
#                    break
#                count = Lib.unpack16bit(header)
#                if not count:
#                    print '========== ZERO COUNT =========='
#                    break
#                print '========== NEXT =========='
#                reply = f.read(count)
#                if len(reply) != count:
#                    print '*** Incomplete reply ***'
#                    break
#                u = Lib.Munpacker(reply)
#                Lib.dumpM(u)

    def getSource(self):
        "Pick random source port to avoid DNS cache poisoning attack."
        while True:
            try:
                source_port = random.randint(1024,65535)
                self.s.bind(('', source_port))
                break
            except socket.error, msg: 
                # Error 98, 'Address already in use'
                if msg[0] != 98: raise

    def conn(self):
        self.getSource()
        self.s.connect((self.ns,self.port))

    def req(self,*name,**args):
        " needs a refactoring "
        self.argparse(name,args)
        #if not self.args:
        #    raise DNSError,'reinitialize request before reuse'
        protocol = self.args['protocol']
        self.port = self.args['port']
        self.tid = random.randint(0,65535)
        self.timeout = self.args['timeout']
        opcode = self.args['opcode']
        rd = self.args['rd']
        server=self.args['server']
        if type(self.args['qtype']) == types.StringType:
            try:
                qtype = getattr(Type, string.upper(self.args['qtype']))
            except AttributeError:
                raise DNSError,'unknown query type'
        else:
            qtype=self.args['qtype']
        if not self.args.has_key('name'):
            print self.args
            raise DNSError,'nothing to lookup'
        qname = self.args['name']
        if qtype == Type.AXFR:
            print 'Query type AXFR, protocol forced to TCP'
            protocol = 'tcp'
        #print 'QTYPE %d(%s)' % (qtype, Type.typestr(qtype))
        m = Lib.Mpacker()
        # jesus. keywords and default args would be good. TODO.
        m.addHeader(self.tid,
              0, opcode, 0, 0, rd, 0, 0, 0,
              1, 0, 0, 0)
        m.addQuestion(qname, qtype, Class.IN)
        self.request = m.getbuf()
        try:
            if protocol == 'udp':
                self.sendUDPRequest(server)
            else:
                self.sendTCPRequest(server)
        except socket.error, reason:
            raise DNSError, reason
        if self.async:
            return None
        else:
            if not self.response:
                raise DNSError,'no working nameservers found'
            return self.response

    def sendUDPRequest(self, server):
        "refactor me"
        self.response=None
        for self.ns in server:
            #print "trying udp",self.ns
            try:
                if self.ns.count(':'):
                    if hasattr(socket,'has_ipv6') and socket.has_ipv6:
                        self.socketInit(socket.AF_INET6, socket.SOCK_DGRAM)
                    else: continue
                else:
                    self.socketInit(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    # TODO. Handle timeouts &c correctly (RFC)
                    self.time_start=time.time()
                    self.conn()
                    if not self.async:
                        self.s.send(self.request)
                        r=self.processUDPReply()
                        # Since we bind to the source port and connect to the
                        # destination port, we don't need to check that here,
                        # but do make sure it's actually a DNS request that the
                        # packet is in reply to.
                        while r.header['id'] != self.tid        \
                                or self.from_address[1] != self.port:
                            r=self.processUDPReply()
                        self.response = r
                        # FIXME: check waiting async queries
                finally:
                    if not self.async:
                        self.s.close()
            except socket.error:
                continue
            break

    def sendTCPRequest(self, server):
        " do the work of sending a TCP request "
        self.response=None
        for self.ns in server:
            #print "trying tcp",self.ns
            try:
                if self.ns.count(':'):
                    if hasattr(socket,'has_ipv6') and socket.has_ipv6:
                        self.socketInit(socket.AF_INET6, socket.SOCK_STREAM)
                    else: continue
                else:
                    self.socketInit(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    # TODO. Handle timeouts &c correctly (RFC)
                    self.time_start=time.time()
                    self.conn()
                    buf = Lib.pack16bit(len(self.request))+self.request
                    # Keep server from making sendall hang
                    self.s.setblocking(0)
                    # FIXME: throws WOULDBLOCK if request too large to fit in
                    # system buffer
                    self.s.sendall(buf)
                    self.s.shutdown(socket.SHUT_WR)
                    r=self.processTCPReply()
                    if r.header['id'] == self.tid:
                        self.response = r
                        break
                finally:
                    self.s.close()
            except socket.error:
                continue

#class DnsAsyncRequest(DnsRequest):
class DnsAsyncRequest(DnsRequest,asyncore.dispatcher_with_send):
    " an asynchronous request object. out of date, probably broken "
    def __init__(self,*name,**args):
        DnsRequest.__init__(self, *name, **args)
        # XXX todo
        if args.has_key('done') and args['done']:
            self.donefunc=args['done']
        else:
            self.donefunc=self.showResult
        #self.realinit(name,args) # XXX todo
        self.async=1
    def conn(self):
        self.getSource()
        self.connect((self.ns,self.port))
        self.time_start=time.time()
        if self.args.has_key('start') and self.args['start']:
            asyncore.dispatcher.go(self)
    def socketInit(self,a,b):
        self.create_socket(a,b)
        asyncore.dispatcher.__init__(self)
        self.s=self
    def handle_read(self):
        if self.args['protocol'] == 'udp':
            self.response=self.processUDPReply()
            if self.donefunc:
                apply(self.donefunc,(self,))
    def handle_connect(self):
        self.send(self.request)
    def handle_write(self):
        pass
    def showResult(self,*s):
        self.response.show()

#
# $Log: Base.py,v $
# Revision 1.12.2.10  2008/08/01 03:58:03  customdesigned
# Don't try to close socket when never opened.
#
# Revision 1.12.2.9  2008/08/01 03:48:31  customdesigned
# Fix more breakage from port randomization patch.  Support Ipv6 queries.
#
# Revision 1.12.2.8  2008/07/31 18:22:59  customdesigned
# Wait until tcp response at least starts coming in.
#
# Revision 1.12.2.7  2008/07/28 01:27:00  customdesigned
# Check configured port.
#
# Revision 1.12.2.6  2008/07/28 00:17:10  customdesigned
# Randomize source ports.
#
# Revision 1.12.2.5  2008/07/24 20:10:55  customdesigned
# Randomize tid in requests, and check in response.
#
# Revision 1.12.2.4  2007/05/22 20:28:31  customdesigned
# Missing import Lib
#
# Revision 1.12.2.3  2007/05/22 20:25:52  customdesigned
# Use socket.inetntoa,inetaton.
#
# Revision 1.12.2.2  2007/05/22 20:21:46  customdesigned
# Trap socket error
#
# Revision 1.12.2.1  2007/05/22 20:19:35  customdesigned
# Skip bogus but non-empty lines in resolv.conf
#
# Revision 1.12  2002/04/23 06:04:27  anthonybaxter
# attempt to refactor the DNSRequest.req method a little. after doing a bit
# of this, I've decided to bite the bullet and just rewrite the puppy. will
# be checkin in some design notes, then unit tests and then writing the sod.
#
# Revision 1.11  2002/03/19 13:05:02  anthonybaxter
# converted to class based exceptions (there goes the python1.4 compatibility :)
#
# removed a quite gross use of 'eval()'.
#
# Revision 1.10  2002/03/19 12:41:33  anthonybaxter
# tabnannied and reindented everything. 4 space indent, no tabs.
# yay.
#
# Revision 1.9  2002/03/19 12:26:13  anthonybaxter
# death to leading tabs.
#
# Revision 1.8  2002/03/19 10:30:33  anthonybaxter
# first round of major bits and pieces. The major stuff here (summarised
# from my local, off-net CVS server :/ this will cause some oddities with
# the
#
# tests/testPackers.py:
#   a large slab of unit tests for the packer and unpacker code in DNS.Lib
#
# DNS/Lib.py:
#   placeholder for addSRV.
#   added 'klass' to addA, make it the same as the other A* records.
#   made addTXT check for being passed a string, turn it into a length 1 list.
#   explicitly check for adding a string of length > 255 (prohibited).
#   a bunch of cleanups from a first pass with pychecker
#   new code for pack/unpack. the bitwise stuff uses struct, for a smallish
#     (disappointly small, actually) improvement, while addr2bin is much
#     much faster now.
#
# DNS/Base.py:
#   added DiscoverNameServers. This automatically does the right thing
#     on unix/ win32. No idea how MacOS handles this.  *sigh*
#     Incompatible change: Don't use ParseResolvConf on non-unix, use this
#     function, instead!
#   a bunch of cleanups from a first pass with pychecker
#
# Revision 1.5  2001/08/09 09:22:28  anthonybaxter
# added what I hope is win32 resolver lookup support. I'll need to try
# and figure out how to get the CVS checkout onto my windows machine to
# make sure it works (wow, doing something other than games on the
# windows machine :)
#
# Code from Wolfgang.Strobl@gmd.de
# win32dns.py from
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66260
#
# Really, ParseResolvConf() should be renamed "FindNameServers" or
# some such.
#
# Revision 1.4  2001/08/09 09:08:55  anthonybaxter
# added identifying header to top of each file
#
# Revision 1.3  2001/07/19 07:20:12  anthony
# Handle blank resolv.conf lines.
# Patch from Bastian Kleineidam
#
# Revision 1.2  2001/07/19 06:57:07  anthony
# cvs keywords added
#
#
