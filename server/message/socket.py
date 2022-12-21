from socket import socket


def write_to_socket(connection: socket, serd_num_seq: str) -> int or None:
    connection.sendall(f"{serd_num_seq}\n".encode())

    if serd_num_seq == '"quit"':
        return -1
