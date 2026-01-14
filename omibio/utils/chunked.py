import typing


def chunked(
    to_chunk: typing.Sequence,
    chunk_size: int = 100
) -> typing.Iterator[typing.Sequence]:
    """Chunk an iterable into smaller iterables of a specified size."""

    for i in range(0, len(to_chunk), chunk_size):
        yield to_chunk[i: i+chunk_size]


def main():
    to_chunk = "ATCGATCGTATGCTGACGTATGCTGTAGCTGATGCTGATGCTGAC"
    result = chunked(to_chunk, 10)
    for chunk in result:
        print(chunk, type(chunk))


if __name__ == "__main__":
    main()
