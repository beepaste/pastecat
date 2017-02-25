#!/usr/bin/env python

"""
TODO:
    1.check if user connected with any data ( if no, then disconnect).
    2.add timeout
"""

import logging
import socket
import sys

import requests

from _thread import start_new_thread

HOST = '0.0.0.0'   # Symbolic name meaning all available interfaces
PORT = 1111  # Some Open port on server
PASTEBIN = 'https://beepaste.ir/api/create'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/var/log/pastecat.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def sendToLog(text="null"):
    if text != "null":
        logger.info(text)


def send_req(text="null"):
    if text != "null":
        r = requests.post(PASTEBIN, data={"text": "%s" % (text)}, verify=False)  # You can use stikked pastebin or my version of it!
        return r.text.encode("utf-8")[:-1]
    else:
        return "Sorry, You Must Enter Something To Paste."


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('Socket created')
sendToLog('Socket Created')

try:
    s.bind((HOST, PORT))
except OSError as err:
    err_no, err_msg = err.args
    # print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sendToLog('Bind failed. Error Code : ' + str(err_no) + ' Message ' + err_msg)
    sys.exit()

# print('Socket bind complete')
sendToLog('Socket bind complete')
s.listen(10)
# print('Socket now listening')
sendToLog('Socket now listening')


# Function for handling connections. This will be used to create threads
def clientthread(conn, ipaddr):
    # Receiving from client
    total_data = []
    while 1:
        data = conn.recv(1024)
        total_data.append(data)
        if not data:
            break
    reply = send_req(''.join(total_data))
    conn.sendall(reply + '\n')
    # print ("Send " + reply + " to " +  ipaddr)
    sendToLog("Send " + reply + " to " + ipaddr)
    conn.close()


# now keep talking with the client
while True:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    # print('Connected with ' + addr[0] + ':' + str(addr[1]))
    sendToLog('Connected with ' + addr[0] + ':' + str(addr[1]))
    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn, addr[0]))

s.close()
