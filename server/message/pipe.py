from io import TextIOWrapper


def write_to_pipe(fd: TextIOWrapper, serd_num_seq: str) -> int or None:

    fd.write(f"{serd_num_seq}\n")
    fd.flush()

    if serd_num_seq == '"quit"':
        return -1
