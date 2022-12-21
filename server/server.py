#!/usr/bin/env python3
import logging
import os
import socket
import sys

from multiprocessing.sharedctypes import SynchronizedString, Synchronized
from server.message.pipe import write_to_pipe
from server.message.shared_memory import write_to_shared_memory
from server.message.socket import write_to_socket

from utils.util import SOCKET_INFO, covert_number_raw


def server(
    main_stdin,
    socket_info: SOCKET_INFO,
    write_pipe,
    data_shm: SynchronizedString,
    stat_shm: Synchronized,
):
    server_logger = logging.getLogger("server")
    server_logger.info(f"Pid:{os.getpid()}")
    sys.stdin = main_stdin
    s = socket.socket(socket_info.family, socket_info.type)
    fd = os.fdopen(write_pipe.fileno(), "w")
    with (
        fd,
        s,
    ):
        s.bind(socket_info.address)
        s.listen(1)
        connection, _ = s.accept()
        with connection:
            server_logger.info("Ready")
            while True:
                number_seq_raw: str = input("Server input integers:\n")

                try:
                    serd_num_seq: str = covert_number_raw(number_seq_raw=number_seq_raw)
                except ValueError:
                    server_logger.warn("Error input", exc_info=True)

                server_logger.info(f"Send :{serd_num_seq}")

                socket_ret = write_to_socket(
                    connection=connection, serd_num_seq=serd_num_seq
                )

                pipe_ret = write_to_pipe(fd=fd, serd_num_seq=serd_num_seq)

                shared_memory_ret = write_to_shared_memory(
                    data_shm=data_shm,
                    stat_shm=stat_shm,
                    serd_num_seq=serd_num_seq,
                )

                if socket_ret and pipe_ret and shared_memory_ret:
                    break
