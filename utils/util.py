import json
from collections import namedtuple


BUFF_SIZE = 1024

SOCKET_INFO = namedtuple("SocketInfo", ["address", "family", "type"])


def covert_number_raw(number_seq_raw: str) -> str:
    serd_num_seq = None

    if number_seq_raw != "q":
        number_seq = [int(s) for s in number_seq_raw.split()]
        serd_num_seq = json.dumps(number_seq)
    else:
        serd_num_seq = json.dumps("quit")

    return serd_num_seq
