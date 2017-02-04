#!/usr/bin/python
# -*- Coding: utf-8 -*-

"""
TODO:
    1.check if user connected with any data ( if no, then disconnect).
    2.add timeout
    3.add multithread [DONE]
"""

import socket, sys
from thread import *

HOST = '0.0.0.0'   # Symbolic name meaning all available interfaces
PORT = 1111 # Some Open port on server
PASTEBIN = 'https://beepaste.ir/api/create'

def send_req(text="null"):
    if text != "null":
        r = requests.post(PASTEBIN, data={"text":"%s" %(text)}, verify=False) # You can use stikked pastebin or my version of it!
        return r.text.encode("utf-8")[:-1]
    else:
        return "Sorry, You Must Enter Something To Paste."

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn, ipaddr):
    #Receiving from client
    total_data = []
    while 1:
        data = conn.recv(1024)
        total_data.append(data)
        if not data:
            break
    reply = send_req(''.join(total_data))
    conn.sendall(reply + '\n')
    print "Send " + reply + " to " +  ipaddr
    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn, addr[0]))

s.close()
