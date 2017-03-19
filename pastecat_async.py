import asyncio
from socket import (AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket)

import requests
import json

HOST = '0.0.0.0'   # Symbolic name meaning all available interfaces
PORT = 1111  # Some Open port on server
PASTEBIN = 'https://beepaste.io/api'
apikey = 'YWRlMGJjOGQ0OTIyY2Q0MWUyMTIwNzRk'


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
        total_data = []
        while True:
            data = await loop.sock_recv(client, 10000)
            if not data:
                break
            total_data.append(data.decode('utf-8'))
        text = ''.join(total_data)
        await loop.sock_sendall(client, (json.loads(requests.post(PASTEBIN, json={'api-key': apikey, 'pasteRaw': text, 'pasteLanguage': 'text'}).text)['url'] + '\n').encode('utf-8'))
    print('Connection Closed!')

loop.create_task(echo_server((HOST, PORT)))
loop.run_forever()
