import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
SERVER_PORT_KEY = 5003

# initialize TCP socket
s = socket.socket()
sk = socket.socket()
print(f"[*] Conectando em {SERVER_HOST}:{SERVER_PORT}...")
print(f"[*] Conectando em {SERVER_HOST}:{SERVER_PORT_KEY}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
sk.connect((SERVER_HOST, SERVER_PORT_KEY))

s.connect((SERVER_HOST, SERVER_PORT))
sk.connect((SERVER_HOST, SERVER_PORT_KEY))
print("[+] Conectado.")
# prompt the client for a name
name = input("Insira seu nome: ")
