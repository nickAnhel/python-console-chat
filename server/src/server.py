import socket
import threading

from src.config import SERVER_HOST, SERVER_PORT


CONNECTIONS: list[socket.socket] = []


def handle_new_connection(connection: socket.socket, address: str) -> None:
    while True:
        try:
            message = connection.recv(1024)
            if message:
                decoded = message.decode()
                print(f"{address}: {decoded}")
                try:
                    broadcast(f"{address}: {decoded}", connection)
                    connection.send("Message delivered successfully.".encode())

                except Exception as e:
                    connection.send(f"Failed to deliver message: {e}".encode())
            else:
                disconnect(connection)
                break

        except ConnectionResetError:
            disconnect(connection)
            break

        except Exception as e:
            print(f"Error handling client {address}: {e}")
            disconnect(connection)
            break


def broadcast(message: str, sender_socket: socket.socket) -> None:
    for conn in CONNECTIONS:
        if conn != sender_socket:
            try:
                conn.send(message.encode())

            except Exception as e:
                print(f"Broadcast error: {e}")
                disconnect(conn)


def disconnect(connection: socket.socket) -> None:
    try:
        connection.close()
    except Exception:
        pass

    if connection in CONNECTIONS:
        CONNECTIONS.remove(connection)


def server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen()

        print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            connection, address = server_socket.accept()
            CONNECTIONS.append(connection)
            threading.Thread(
                target=handle_new_connection, args=(connection, address), daemon=True
            ).start()

    except Exception as e:
        print(f"Server error: {e}")

    finally:
        for conn in CONNECTIONS:
            disconnect(conn)

        server_socket.close()
