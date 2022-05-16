from asyncio.windows_events import NULL
import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import pickle

import nacl.utils
from nacl.public import PrivateKey, Box

# init colors
init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
SERVER_PORT_KEY = 5003
separator_token = "<SEP>"
client_key = PrivateKey.generate()
client_public_key = client_key.public_key
foreign_public_key = None
user_list = ["Teste"]

# initialize TCP socket
s = socket.socket()
sk = socket.socket()
print(f"[*] Conectando em {SERVER_HOST}:{SERVER_PORT}...")
print(f"[*] Conectando em {SERVER_HOST}:{SERVER_PORT_KEY}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
sk.connect((SERVER_HOST, SERVER_PORT_KEY))
print("[+] Conectado.")
# prompt the client for a name
name = input("Insira seu nome: ")


def fetch_foreign_key():
    global foreign_public_key
    try:
        sk.send()
        foreign_public_key = pickle.loads(sk.recv(1024))
        print("Received Foreign key")
    except Exception as e:
        print(f"[!] Error: {e}")

def listen_for_messages():
    while True:
        try:
            message = pickle.loads(s.recv(1024))
            receive_box = Box(client_key, foreign_public_key)
            decripted_message = receive_box.decrypt(message).decode()
            decripted_message = decripted_message.replace(separator_token, ": ")

            print("\n" + decripted_message)

        except Exception as e:
            print(f"[!] Error: {e}")

# make a thread that listens for messages to this client & print them
t1 = Thread(target=listen_for_messages)
t1.daemon = True
t1.start()

# t2 = Thread(target=listen_for_foreign_keys)
# t2.daemon = True
# t2.start()

while True:

    sk.sendall(pickle.dumps(client_public_key))
    
    while True:
        to_send =  input()

        if to_send.lower() == 'q':
            break

        else:
            fetch_foreign_key()
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
            res = bytes(message, 'utf-8')
            send_box = Box(client_key, foreign_public_key)
            encrypted_msg = send_box.encrypt(res)
            s.send(pickle.dumps(encrypted_msg))

# close the socket
s.close()
sk.close()