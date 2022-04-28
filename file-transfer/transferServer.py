#! /usr/bin/env python3
# ######################
# File transfer server #
########################
# IMPORTS
import os, socket, sys, re
sys.path.append("../lib")       # for params
import params
from archiver import *

# flags to specify listenPort or print usage
switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
                         # s is a factory for connected sockets

conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('Connected by', addr)
while 1:
    trans_len = conn.recv(64).decode('utf-8')
    if trans_len:
        trans_len = int(trans_len)
        message = conn.recv(trans_len).decode('utf-8')
        new_file = "client_file_" + str(addr) + ".txt"
        unarchiveFile(new_file, message)
    data = conn.recv(1024).decode()

    if len(data) == 0:
        print("Zero length read, nothing to send, terminating")
        break

conn.shutdown(socket.SHUT_WR)
conn.close()

