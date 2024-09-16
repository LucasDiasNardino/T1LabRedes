import socket

def tcp_client(host='127.0.0.1', port=65433, nickname='user1'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(nickname.encode('utf-8'))  # Envia o nickname para o servidor

        while True:
            # Enviar mensagem para outro usuário
            dest = input("Enviar mensagem para (nickname): ")
            msg = input("Digite a mensagem: ")
            s.sendall(f"/MSG {dest} {msg}".encode('utf-8'))

            # Recebe mensagens do servidor
            response = s.recv(1024)
            print("Resposta: ", response.decode('utf-8'))

tcp_client()
