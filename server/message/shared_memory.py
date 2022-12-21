from multiprocessing.sharedctypes import SynchronizedString, Synchronized
import time

from utils.util import BUFF_SIZE


def write_to_shared_memory(
    data_shm: SynchronizedString, stat_shm: Synchronized, serd_num_seq: str
) -> int or None:

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

    if serd_num_seq == '"quit"':
        return -1
