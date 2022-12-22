#!/usr/bin/env python3
import json
import logging
import os
import statistics


# Setup simple logging
logging.basicConfig(level=logging.INFO)


def pipe_client(read_pipe):

    client_logger = logging.getLogger("pipe_client")
    client_logger.info(f"Pid:{os.getpid()}")

    with os.fdopen(read_pipe.fileno(), "r") as fd:
        client_logger.info("Ready")
        while True:
            try:
                line = fd.readline()
                number_seq = json.loads(line)

                if number_seq != "quit":
                    client_logger.info(f"Received: {number_seq}")
                    med = statistics.median(number_seq)
                    client_logger.info(f"Median: {med}")
                else:
                    break
            except Exception:
                client_logger.warning("Error", exc_info=True)
    client_logger.info("Close pipe client")
