from typing import Iterable, Iterator


def chunked(to_chunk: Iterable, chunk_size: int = 100) -> Iterator[Iterable]:
    for i in range(0, len(to_chunk), chunk_size):
        yield to_chunk[i: i+chunk_size]


def main():
    from omibio.sequence import Sequence
    to_chunk = Sequence("ATCGATCGTATGCTGACGTATGCTGTAGCTGATGCTGATGCTGAC")
    result = chunked(to_chunk, 10)
    for chunk in result:
        print(chunk, type(chunk))


if __name__ == "__main__":
    main()
