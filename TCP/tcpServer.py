import socket
import threading

clients = {}

def handle_client(conn, addr):
    print(f"Cliente conectado: {addr}")
    while True:
        try:
            # Recebe dados do cliente
            data = conn.recv(1024)
            if not data:
                break
            
            # Extrai o destinatário e a mensagem
            message = data.decode('utf-8')
            parts = message.split(' ', 2)
            if len(parts) == 3 and parts[0] == '/MSG':
                dest_nickname = parts[1]
                msg_to_send = parts[2]

                # Envia a mensagem ao destinatário
                if dest_nickname in clients:
                    clients[dest_nickname].sendall(f"{addr}: {msg_to_send}".encode('utf-8'))
                else:
                    conn.sendall(f"Usuário {dest_nickname} não encontrado.".encode('utf-8'))

        except Exception as e:
            print(f"Erro: {e}")
            break

    conn.close()

def tcp_server(host='0.0.0.0', port=65433):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Servidor TCP ouvindo em {host}:{port}...")

    while True:
        conn, addr = server.accept()
        nickname = conn.recv(1024).decode('utf-8')  # Supondo que o cliente envie seu nickname primeiro
        clients[nickname] = conn  # Registra o cliente no dicionário

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

tcp_server()
