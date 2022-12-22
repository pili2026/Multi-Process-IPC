import os
import logging
import socket
import json

from utils.util import SOCKET_INFO, BUFF_SIZE

logging.basicConfig(level=logging.INFO)


def socket_client(socket_info: SOCKET_INFO):
    import statistics

    client_logger = logging.getLogger("socket_client")
    client_logger.info(f"Pid:{os.getpid()}")

    with socket.socket(socket_info.family, socket_info.type) as s:
        s.connect(socket_info.address)
        client_logger.info("Ready")
        while True:
            try:
                line = b""
                while True:
                    p = s.recv(BUFF_SIZE)
                    line += p
                    if len(p) < BUFF_SIZE:
                        break

                number_seq = json.loads(line)
                client_logger.info(f"Received: {number_seq}")

                if type(number_seq) is list:
                    mean = statistics.mean(number_seq)
                    client_logger.info(f"Mean: {mean}")
                else:
                    s.close()
                    break

            except Exception:
                client_logger.warning("Error received")
                s.close()
                break
    client_logger.info("Client socket close")
