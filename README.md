# 🗪 Python Console Chat

A multi-user console-based TCP chat written in Python. Supports concurrent client connections, message exchange, delivery confirmation, and error handling.

## 🔗 Architecture

```
+-------------+       +-------------+       +-------------+
|  Client 1   | <-->  |             | <-->  |  Client 2   |
| (nickname)  |       |   Server    |       | (nickname)  |
+-------------+       |    (TCP)    |       +-------------+
                      |             |
                      +-------------+
                             ^
                             |
                      +-------------+
                      |  Client N   |
                      +-------------+
```

- Each client connects to the server via TCP
- The server receives messages and broadcasts them to other connected clients
- Uses `threading` to handle clients concurrently

## 🛠 Technologies Used

- `python3.14`
- `socket` — for TCP communication
- `threading` — for handling multiple clients in parallel

## 🚀 Running the Project

Navigate to the `server` or `client` directory (depending on what you want to run) and execute the following sequence of commands using `uv`:

```bash
uv run -m src.main
```

or `python3`:

```bash
python3 -m src.main
```