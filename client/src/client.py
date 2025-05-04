import socket
import threading

from src.config import SERVER_HOST, SERVER_PORT


def handle_incoming_messages(client_socket: socket.socket) -> None:
    while True:
        try:
            message = client_socket.recv(1024)

            if message:
                print(message.decode())

            else:
                break

        except Exception as e:
            print(f"Receive error: {e}")
            break

    client_socket.close()


def client() -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        threading.Thread(
            target=handle_incoming_messages, args=(client_socket,), daemon=True
        ).start()

        while True:
            try:
                message = input("")

                if message.lower() in ("quit", "exit"):
                    break

                client_socket.send(message.encode())

            except Exception as e:
                print(f"Send error: {e}")
                break

    finally:
        client_socket.close()
