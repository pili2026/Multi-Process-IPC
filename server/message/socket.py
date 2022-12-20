from socket import socket


def write_to_socket(connection: socket, serd_num_seq: str) -> None:
    connection.sendall(f"{serd_num_seq}\n".encode())


def write_to_socket_with_close(connection: socket, serd_num_seq: str) -> None:
    connection.sendall(f"{serd_num_seq}\n".encode())
    connection.close()
