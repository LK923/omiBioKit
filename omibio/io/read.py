from os import PathLike
from typing import TextIO, Literal
from omibio.bio import SeqCollections
from omibio.io.read_fasta import read_fasta
from omibio.io.read_fastq import read_fastq
from omibio.utils.get_suffix import get_suffix


FASTA_FORMATS = {"faa", "fa", "fasta", "fna"}
FASTQ_FORMATS = {"fastq", "fq"}


def read(
    source: str | PathLike | TextIO,
    format: Literal["faa", "fa", "fasta", "fna", "fastq", "fq"] | None = None,
    strict: bool = False,
    warn: bool = True,
    skip_invalid_seq: bool = False
) -> SeqCollections:
    """A unified interface for file parsing functions.

    Users can specify a file format to read, or the program can automatically
    determine the file format based on the file suffix in the path.

    Args:
        source (str | PathLike | TextIO):
            Path to the input file, or a TextIO object.
        format (Literal, optional):
            File format to read. If not specified, the program will try to
            determine the file format based on the file suffix.
        strict (bool, optional):
            Whether to raise an exception when encountering invalid sequences.
            Defaults to False.
        warn (bool, optional):
            Whether to issue a warning when encountering invalid sequences.
            Defaults to True.
        skip_invalid_seq (bool, optional):
            Whether to skip invalid sequences. Defaults to False.

    Raises:
        TypeError:
            If the format is not recognized.
        TypeError:
            If missing the format argument for a TextIO input.

    Returns:
        SeqCollections:
            A SeqCollections object containing the parsed sequences.
    """

    if hasattr(source, "read") and format is None:
        if format is None:
            raise TypeError(
                "read() Missing argument 'format' for a TextIO input"
            )
    else:
        if format is None:
            format_str = get_suffix(str(source), with_dot=False)
        else:
            format_str = format.lstrip(".")

    if format_str in FASTA_FORMATS:
        result = read_fasta(
            source=source,
            strict=strict,
            warn=warn,
            skip_invalid_seq=skip_invalid_seq
        )
    elif format_str in FASTQ_FORMATS:
        result = read_fastq(
            source=source,
            strict=strict,
            warn=warn,
            skip_invalid_seq=skip_invalid_seq
        )
    else:
        raise TypeError(
            f"Invalid format to read: {format!r}"
        )

    return result


def main():
    input_path = r"./examples/data/example_fastq.fastq"
    result = read(input_path)
    for res in result:
        print(repr(res))
    print(result.source)


if __name__ == "__main__":
    main()
