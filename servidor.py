import socket
import threading

# Constantes de conexão
HOST = '127.0.0.1'
PORT = 55555

# Servidor escutando
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

salas = {}

def broadcast(sala, mensagem):
    for i in salas[sala]:
        #se a mensagem for str transforma para binário
        if isinstance(mensagem, str):
            mensagem=mensagem.encode()

        i.send(mensagem)

def enviar_mensagem(nome, sala, client):
    while True:
        mensagem = client.recv(1024)
        mensagem = f"{nome}: {mensagem.decode()}\n"
        broadcast(sala, mensagem)

while True:
    client, addr = server.accept()
    client.send(b'SALA')
    sala = client.recv(1024).decode()
    nome = client.recv(1024).decode()
    if sala not in salas.keys():
        salas[sala] = []
    salas[sala].append(client)
    print(f"{nome} se conectou na sala {sala}!\nINFO: {addr}")
    broadcast(sala, f"{nome} entrou na sala!\n")
    thread = threading.Thread(target=enviar_mensagem, args = (nome, sala, client))
    thread.start()