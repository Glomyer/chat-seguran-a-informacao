from email import message
import socket
import pickle
import sys
import traceback
import copy
from threading import Thread

import nacl.utils
from nacl.public import PrivateKey, Box

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
SERVER_PORT_KEY = 5003

#2 party

# initialize list/set of all connected client's sockets
client_sockets = set()
s = socket.socket()
sk = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
sk.bind((SERVER_HOST, SERVER_PORT_KEY))

sk.listen(4)
s.listen(4)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT_KEY}")


def broadcast_message(message):
    for client_socket in client_sockets():
        new_message = copy.deepcopy(message)
        serialized_data = pickle.dumps(new_message)
        client_socket[0].sendall(serialized_data)
    del(new_message)

def exchange_keys(csk, key):
    for client_socket_key in client_sockets():
        if(client_socket_key[1] is not csk):
            new_key = copy.deepcopy(key)
            serialized_data = pickle.dumps(new_key)
            client_socket_key[1].sendall(serialized_data)
    del(new_key)

def listen_for_client_keys(csk):
    while True:
        try:
            key = pickle.loads(csk.recv(1024))
            print(key)
            exchange_keys(csk, key)

        except Exception as e:
            print(f"[!] Error: {e}")

def listen_for_client_messages(cs):
    while True:
        try:
            loaded_message = pickle.loads(cs.recv(1024))
            print(loaded_message)
            broadcast_message(loaded_message)

        except Exception as e:
            print(f"[!] Error: {e}")
  

def close_connections():

    for client_socket in client_sockets:
        client_socket[0].close()
    s.close()

while True:
    try: 
        client_socket_key, client_address_key = sk.accept()
        client_socket, client_address = s.accept()
        client_public_key = pickle.loads(client_socket_key.recv(1024))
        #client_socket_key.send(pickle.dumps(server_public_key))
        print(f"[+] {client_address} conectou.\nChave: {client_public_key}\n")
        client_sockets.add((client_socket, client_public_key))

        t = Thread(target=listen_for_client_messages, args=(client_socket,))
        t.daemon = True
        t.start()
        
    except Exception as e:
        print(f"[!] Error: {e}")
        print(sys.exc_info())

