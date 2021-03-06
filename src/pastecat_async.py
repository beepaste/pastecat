import asyncio
import json
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket

import requests

HOST = '0.0.0.0'   # Symbolic name meaning all available interfaces
PORT = 1111  # Some Open port on server
PASTEBIN = 'https://beepaste.io/api'
API_KEY = ''


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


# TODO: better to do this with aiohttp?
def get_response_text(text):
    response = requests.post(PASTEBIN, json={'api-key': API_KEY, 'pasteRaw': text, 'pasteLanguage': 'text'})
    if response.status_code == 201:
        return json.loads(response.text)['url'] + "\n"
    else:
        return "An error accoured. Please try again later. \n"


async def echo_handler(client):
    with client:
        total_data = []
        while True:
            data = await loop.sock_recv(client, 10000)
            if not data:
                break
            total_data.append(data.decode('utf-8'))
        text = ''.join(total_data)
        to_send = bytes(get_response_text(text).encode('utf-8'))
        await loop.sock_sendall(client, to_send)
    print('Connection Closed!')

loop.create_task(echo_server((HOST, PORT)))
loop.run_forever()
