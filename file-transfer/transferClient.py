#! /usr/bin/env python3
#######################
# Echo client program #
#######################
# IMPORTS
import os, socket, sys, re
sys.path.append("../lib")       # for params
import params
from archiver import *

# flags to specify serverHost:serverPort or print usage
switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

sending_file = True
while (sending_file):
    file_path = input("\nEnter File Path to Send...")
    if file_path == '' or file_path == 'quit':
        sending_file = False
        #break
    if os.path.exists(file_path):
        arched_file = archiveFile(file_path)
        file_len = len(arched_file)
        transfer_len = str(file_len).encode('utf-8')
        transfer_len += b' ' * (64 - len(transfer_len))
        s.send(transfer_len)
        s.send(arched_file)

s.shutdown(socket.SHUT_WR)      # no more output

print("Zero length read.  Closing")
s.close()
