#!/usr/bin/env python3

import json
import logging
import os
import sys
import time

from multiprocessing.sharedctypes import Synchronized, SynchronizedString
from utils.util import BUFF_SIZE


def shared_memory_server(
    main_stdin, data_shm: SynchronizedString, stat_shm: Synchronized
):
    server_logger = logging.getLogger("shared_memory_server")
    server_logger.info(f"Pid:{os.getpid()}")
    sys.stdin = main_stdin

    while True:

        number_seq_raw: str = input("Server input integers:")

        if number_seq_raw != "q":
            number_seq = [int(s) for s in number_seq_raw.split()]
            serd_num_seq = json.dumps(number_seq)
            server_logger.info(f"Send :{serd_num_seq}")

            # write to shared memory
            while stat_shm.value != 0:
                time.sleep(0.01)
            serd_num_seq_bytes = serd_num_seq.encode()
            l = len(serd_num_seq_bytes)
            c = 0

            while c < l:
                h = min(l, c + BUFF_SIZE)
                while stat_shm.value not in (0, 2):
                    time.sleep(0.01)
                data_shm.value = serd_num_seq_bytes[c:h]
                stat_shm.value = 1
                c = h
            while stat_shm.value != 2:
                time.sleep(0.01)
            stat_shm.value = -1

        else:
            serd_num_seq = json.dumps("quit")
            server_logger.info(f"Send :{serd_num_seq}")

            # write to shared memory
            while stat_shm.value != 0:
                time.sleep(0.01)
            serd_num_seq_bytes = serd_num_seq.encode()
            l = len(serd_num_seq_bytes)
            c = 0

            while c < l:
                h = min(l, c + BUFF_SIZE)
                while stat_shm.value not in (0, 2):
                    time.sleep(0.01)
                data_shm.value = serd_num_seq_bytes[c:h]
                stat_shm.value = 1
                c = h
            while stat_shm.value != 2:
                time.sleep(0.01)
            stat_shm.value = -1
            break

    # Log completion
    server_logger.info("Close shared_memory_server")
