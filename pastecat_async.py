import asyncio
from socket import (AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket)

import requests

HOST = '0.0.0.0'   # Symbolic name meaning all available interfaces
PORT = 1111  # Some Open port on server
PASTEBIN = 'https://beepaste.ir/api/create'


loop = asyncio.get_event_loop()

async def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)
    while True:
        client, addr = await loop.sock_accept(sock)
        print('connection from', addr)
        loop.create_task(echo_handler(client))

async def echo_handler(client):
    with client:
        while True:
            data = await loop.sock_recv(client, 10000)
            if not data:
                break
            await loop.sock_sendall(client, requests.post(PASTEBIN, data={'text': data}, verify=False).text.encode("utf-8")[:-1] + b'\n')
            break
    print('Connection Closed!')

loop.create_task(echo_server((HOST, PORT)))
loop.run_forever()
