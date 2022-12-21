#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import socket
import multiprocessing

from multiprocessing import Array, Process, Value
from enum import Enum

from client.pipe import pipe_client
from client.shared_memory import shared_memory_client
from client.socket import socket_client
from server.pipe import pipe_server
from server.shared_memory import shared_memory_server
from server.socket import socket_server
from server.server import server
from utils.util import SOCKET_INFO, BUFF_SIZE


# Setup simple logging
logging.basicConfig(level=logging.INFO)


class TaskStatus(Enum):
    CLIENT1 = "Client1"
    CLIENT2 = "Client2"
    CLIENT3 = "Client3"

    def __str__(self):
        return str(self.name.capitalize())


def execute_server():
    launcher_logger = logging.getLogger("launcher")
    launcher_logger.info(f"Pid:{os.getpid()}")

    main_stdin = os.fdopen(os.dup(sys.stdin.fileno()))
    read_pipe, write_pipe = multiprocessing.Pipe(False)
    socket_info = SOCKET_INFO(
        address=("127.0.0.1", 12345),
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
    )
    data_shm = Array("c", BUFF_SIZE)
    # 0 = both waiting for new round, 1 = segment ready, 2 = segment received, -1 = server wait for new round
    stat_shm = Value("i", 0)
    with (
        main_stdin,
        read_pipe,
        write_pipe,
    ):
        # Setup child processes
        procs = [
            Process(
                target=server,
                args=(
                    main_stdin,
                    socket_info,
                    write_pipe,
                    data_shm,
                    stat_shm,
                ),
            ),
            Process(target=socket_client, args=(socket_info,)),
            Process(target=pipe_client, args=(read_pipe,)),
            Process(
                target=shared_memory_client,
                args=(
                    data_shm,
                    stat_shm,
                ),
            ),
        ]

        # Start child processes
        for proc in procs:
            proc.start()

        # Wait for child processes to finish
        for proc in procs:
            proc.join()


def execute_socket():
    # Setup parent logger and log pid
    parent_logger = logging.getLogger("parent")
    parent_logger.info(f"Pid:{os.getpid()}")

    main_stdin = os.fdopen(os.dup(sys.stdin.fileno()))
    socket_info = SOCKET_INFO(
        address=("127.0.0.1", 12345),
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
    )

    with main_stdin:

        procs = [
            Process(target=socket_server, args=(main_stdin, socket_info)),
            Process(target=socket_client, args=(socket_info,)),
        ]

        # Start processes
        for proc in procs:
            proc.start()

        # Run to completion
        for proc in procs:
            proc.join()


def execute_pipe():
    # Setup parent logger and log pid
    parent_logger = logging.getLogger("parent")
    parent_logger.info(f"Pid:{os.getpid()}")
    main_stdin = os.fdopen(os.dup(sys.stdin.fileno()))

    # Setup pipe
    r, w = multiprocessing.Pipe(False)

    with (r, w, main_stdin):
        # Setup processes
        procs = [
            Process(
                target=pipe_server,
                args=(
                    main_stdin,
                    w,
                ),
            ),
            Process(target=pipe_client, args=(r,)),
        ]

        # Start processes
        for proc in procs:
            proc.start()

        # Run to completion
        for proc in procs:
            proc.join()


def shared_memory():
    # Setup parent logger and log pid
    parent_logger = logging.getLogger("parent")
    parent_logger.info(f"Pid:{os.getpid()}")
    main_stdin = os.fdopen(os.dup(sys.stdin.fileno()))

    data_shm = Array("c", 1024)
    # 0 = both waiting for new round, 1 = segment ready, 2 = segment received, -1 = server wait for new round
    stat_shm = Value("i", 0)

    # Setup processes
    procs = [
        Process(
            target=shared_memory_server,
            args=(
                main_stdin,
                data_shm,
                stat_shm,
            ),
        ),
        Process(
            target=shared_memory_client,
            args=(
                data_shm,
                stat_shm,
            ),
        ),
    ]

    # Start processes
    for proc in procs:
        proc.start()

    # Run to completion
    for proc in procs:
        proc.join()


# Main
def main(clients: list[str] = None):

    if clients:
        clients = [client.capitalize() for client in clients]

        if TaskStatus.CLIENT1.value in clients:
            execute_socket()
        if TaskStatus.CLIENT2.value in clients:
            execute_pipe()
        if TaskStatus.CLIENT3.value in clients:
            shared_memory()
    else:
        execute_server()


# Execute main
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--client", type=str, nargs="*", help="Client")
    args = parser.parse_args()
    clients: list[str] = args.client
    main(clients)
