#!/usr/bin/env python3

import json
import logging
import os
import sys
import time

from multiprocessing.sharedctypes import Synchronized, SynchronizedString
from server.message.shared_memory import write_to_shared_memory
from utils.util import BUFF_SIZE, covert_number_raw


def shared_memory_server(
    main_stdin, data_shm: SynchronizedString, stat_shm: Synchronized
):
    server_logger = logging.getLogger("shared_memory_server")
    server_logger.info(f"Pid:{os.getpid()}")
    sys.stdin = main_stdin

    while True:

        number_seq_raw: str = input("Server input integers:")

        try:
            serd_num_seq: str = covert_number_raw(number_seq_raw=number_seq_raw)
        except ValueError:
            server_logger.warn("Error input", exc_info=True)

        server_logger.info(f"Send :{serd_num_seq}")

        ret = write_to_shared_memory(
            data_shm=data_shm,
            stat_shm=stat_shm,
            serd_num_seq=serd_num_seq,
        )

        if ret:
            break

    # Log completion
    server_logger.info("Close shared_memory_server")
