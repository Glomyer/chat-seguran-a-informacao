import socket
import pickle
from common_classes import ChatMessage
import copy
from threading import Thread

import nacl.utils
from nacl.public import PrivateKey, Box

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
SERVER_PORT_KEY = 5003
server_key = PrivateKey.generate()
server_public_key = server_key.public_key

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
sk = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
sk.bind((SERVER_HOST, SERVER_PORT_KEY))

sk.listen(12)
s.listen(12)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT_KEY}")

def listen_for_client(cs):

    while True:
        try:
            loaded_message = pickle.loads(cs.recv(1024))
            key = loaded_message.key
            message = loaded_message.message
            receive_box = Box(server_key, key)
            decripted_message = receive_box.decrypt(message)
            loaded_message.key = server_public_key
            loaded_message.message = decripted_message

        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)

        else:
            for client_socket in client_sockets:
                
                new_message = copy.deepcopy(loaded_message)
                key = new_message.key
                message = new_message.message
                send_box = Box(server_key, client_socket[1])
                new_message.message = send_box.encrypt(message)
                serialized_data = pickle.dumps(new_message)
                client_socket[0].sendall(serialized_data)

            del(loaded_message)

while True:
    client_socket_key, client_address_key = sk.accept()
    client_socket, client_address = s.accept()
    client_public_key = pickle.loads(client_socket_key.recv(1024))
    client_socket_key.send(pickle.dumps(server_public_key))
    #print(f"[+] {client_address} conectou.\nChave: {client_public_key}\n")
    client_sockets.add((client_socket, client_public_key))
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

# close client sockets
for cs in client_sockets:
    cs[0].close()
# close server socket
s.close()