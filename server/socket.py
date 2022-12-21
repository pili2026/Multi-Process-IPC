import logging
import os
import socket
import sys

from server.message.socket import write_to_socket
from utils.util import SOCKET_INFO, covert_number_raw


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
                number_seq_raw: str = input("Server input integers:")

                try:
                    serd_num_seq: str = covert_number_raw(number_seq_raw=number_seq_raw)
                except ValueError:
                    server_logger.warn("The input is invalid, please check the value.")
                else:
                    ret = write_to_socket(
                        connection=connection, serd_num_seq=serd_num_seq
                    )

                    if ret:
                        break

    server_logger.info("Close socket server")
