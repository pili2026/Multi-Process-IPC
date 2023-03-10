#!/usr/bin/env python3

import json
import logging
import os
import time
import statistics


# Process2 logic
def shared_memory_client(data_shm, stat_shm):

    client_logger = logging.getLogger("Shared memory client")
    client_logger.info(f"Pid:{os.getpid()}")
    client_logger.info("Ready")

    while True:
        try:
            line = b""

            while True:
                match stat_shm.value:
                    case 0:
                        time.sleep(0.01)
                    case 1:
                        line += data_shm.value
                        stat_shm.value = 2
                    case -1:
                        stat_shm.value = 0
                        break
                    case _:
                        time.sleep(0.01)
            number_seq = json.loads(line)
            client_logger.info(f"Received: {number_seq}")

            if type(number_seq) is list:
                mode = statistics.mode(number_seq)
                client_logger.info(f"Mode is: {mode}")
            else:
                break
        except Exception:
            client_logger.warning("Error", exc_info=True)

    client_logger.info("Close shared memory client")
