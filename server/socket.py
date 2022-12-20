import json
import logging
import os
import socket
import sys

from utils.util import SOCKET_INFO


def socket_server(main_stdin, socket_info: SOCKET_INFO):
    server_logger = logging.getLogger("socket_server")
    server_logger.info(f"Pid:{os.getpid()}")
    sys.stdin = main_stdin
    s = socket.socket(socket_info.family, socket_info.type)

    with (s,):
        s.bind(socket_info.address)
        s.listen(1)
        connection, _ = s.accept()
        with connection:
            server_logger.info("Ready")
            while True:
                try:
                    number_seq_raw: str = input("Server input integers:")
                    serd_num_seq = None

                    if number_seq_raw != "q":
                        number_seq = [int(s) for s in number_seq_raw.split()]
                        serd_num_seq = json.dumps(number_seq)
                        server_logger.info(f"Send :{serd_num_seq}")

                        # write to socket
                        connection.sendall(f"{serd_num_seq}\n".encode())
                    else:
                        serd_num_seq = json.dumps("quit")
                        server_logger.info(f"Send :{serd_num_seq}")

                        # write to socket
                        connection.sendall(f"{serd_num_seq}\n".encode())
                        break

                except ValueError:
                    server_logger.warn("Error input", exc_info=True)
