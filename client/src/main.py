import enum
import json
import os
import socket
import threading
import time
from datetime import datetime


class Colors(enum.StrEnum):
    RESET = "\033[0m"
    RED = "\033[31m"
    GRAY = "\033[90m"
    DARK_GREY = "\033[30m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


def handle_incoming_messages(client_socket: socket.socket) -> None:
    while True:
        try:
            message = client_socket.recv(1024)

            if not message:
                break

            try:
                data = json.loads(message.decode())
                timestamp = data.get("timestamp", "")
                sender = data.get("username", "unknown")
                text = data.get("text", "")

                print(
                    f"\r{Colors.GRAY}[{timestamp}]{Colors.RESET} {Colors.CYAN}{sender}{Colors.RESET}: {Colors.WHITE}{text}{Colors.RESET}\n> ",
                    end="",
                )

            except json.JSONDecodeError:
                print(
                    f"\r{Colors.DARK_GREY}[!] Server: {message.decode()}{Colors.RESET}\n> ",
                    end="",
                )

        except Exception as e:
            print(
                f"\r{Colors.RED}[!] Error receiving message:{Colors.RESET} {e}\n> ",
                end="",
            )
            break

    client_socket.close()


def get_connection_parameters() -> tuple[str, int]:
    os.system("clear")

    try:
        server_host = input("Enter server host: ").strip()
        server_port = int(input("Enter server port: ").strip())

    except ValueError:
        print(f"{Colors.RED}[!] Wrong connection parameters{Colors.RESET}")
        time.sleep(2)
        return get_connection_parameters()

    return server_host, server_port


def client() -> None:
    os.system("clear")

    username = input("Enter your username: ").strip()
    server_host, server_port = get_connection_parameters()

    os.system("clear")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_host, server_port))

        threading.Thread(
            target=handle_incoming_messages, args=(client_socket,), daemon=True
        ).start()

        while True:
            message = input("> ").strip()

            if not message:
                continue

            if message.lower() in ("/q", "/quit", "/e", "/exit"):
                break

            data = {
                "username": username,
                "timestamp": datetime.now().strftime("%Y-%M-%d %H:%M:%S"),
                "text": message,
            }

            try:
                client_socket.send(json.dumps(data).encode())
            except Exception as e:
                print(f"{Colors.RED}[!] Failed to send message:{Colors.RED} {e}")
                break

    except KeyboardInterrupt:
        print("\nBye")

    except Exception:
        print(
            f"{Colors.RED}[!] Failed to connect to {server_host}:{server_port}{Colors.RESET}"
        )

    finally:
        client_socket.close()


def main() -> None:
    client()


if __name__ == "__main__":
    client()
