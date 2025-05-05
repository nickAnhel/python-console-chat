import json
import logging
import socket
import threading

from src.config import settings

logger = logging.getLogger("server." + __name__)

CONNECTIONS: list[socket.socket] = []


def handle_new_connection(connection: socket.socket, address: tuple[str, int]) -> None:
    while True:
        try:
            message = connection.recv(1024)

            if not message:
                disconnect(connection)
                break

            try:
                data = json.loads(message.decode())
                logger.info("New message from %r (%s:%s): %r", data["username"], address[0], address[1], data["text"])

                broadcast(json.dumps(data), connection)

                connection.send("Message delivered successfully.".encode())

            except json.JSONDecodeError:
                connection.send("Invalid message format.".encode())

        except Exception as e:
            logger.error("Error handling client %s:%s %s", address[0], address[1], e)
            disconnect(connection)
            break


def broadcast(message: str, sender_socket: socket.socket) -> None:
    for connection in CONNECTIONS:
        if connection != sender_socket:
            try:
                connection.send(message.encode())
            except Exception:
                disconnect(connection)


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
        server_socket.bind((settings.server.host, settings.server.port))
        server_socket.listen()
        logger.info(
            "Server listening on %s:%s", settings.server.host, settings.server.port
        )

        while True:
            connection, address = server_socket.accept()
            CONNECTIONS.append(connection)

            logger.info("New connection from %s:%s", address[0], address[1])

            threading.Thread(
                target=handle_new_connection, args=(connection, address), daemon=True
            ).start()

    except KeyboardInterrupt:
        logger.info("Exited with code 0")

    except Exception as e:
        logger.error("Server error: %s", e)

    finally:
        for connection in CONNECTIONS:
            disconnect(connection)
        server_socket.close()
