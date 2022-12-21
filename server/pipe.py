#!/usr/bin/env python3
import logging
import os
import sys

from server.message.pipe import write_to_pipe
from utils.util import covert_number_raw

# Setup simple logging
logging.basicConfig(level=logging.INFO)


def pipe_server(main_stdin, w):
    pipe_server_logger = logging.getLogger("pipe_server")
    pipe_server_logger.info(f"Pid:{os.getpid()}")
    sys.stdin = main_stdin
    fd = os.fdopen(w.fileno(), "w")

    with fd:
        while True:
            number_seq_raw = input("Server input integers:")

            try:
                serd_num_seq: str = covert_number_raw(number_seq_raw=number_seq_raw)
            except ValueError:
                pipe_server_logger.warn("The input is invalid, please check the value.")
            else:
                ret: int = write_to_pipe(fd=fd, serd_num_seq=serd_num_seq)

                if ret:
                    break

    # Log completion
    pipe_server_logger.info("Close pipe server")
