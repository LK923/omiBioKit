from pathlib import Path
from typing import TYPE_CHECKING, Generator
import warnings
if TYPE_CHECKING:
    from omibio.bio import SeqCollections, SeqEntry

VALID_NT = set("ATUCGRYKMBVDHSWN")


class FastqFormatError(Exception):

    def __init__(self, message):
        super().__init__(message)


def read_fastq_iter(
    file_name: str,
    strict: bool = False,
    warn: bool = True,
    skip_invalid_seq: bool = False
) -> Generator["SeqEntry"]:
    from omibio.bio import SeqEntry
    from omibio.sequence import Sequence

    file_path = Path(file_name)
    if not file_path.exists():
        raise FileNotFoundError(f"File '{file_name}' not found.")

    suffix = file_path.suffix.lower()
    if suffix not in {".fastq", ".fq"}:
        raise FastqFormatError(
            f"Invalid format to read: {suffix}"
        )

    with open(file_name, "r") as file:
        line_num = 0

        while True:
            header = file.readline()
            line_num += 1
            if not header:
                break

            header = header.rstrip()
            if not header:
                continue

            if not header.startswith("@"):
                raise FastqFormatError(
                    f"Line {line_num}: FASTQ header must start with '@', "
                    f"got: {header}"
                )
            seq = file.readline()
            plus = file.readline()
            qual = file.readline()
            line_num += 3

            seq, plus, qual = seq.rstrip(), plus.rstrip(), qual.rstrip()

            if (not seq) or (not plus) or (not qual):
                raise FastqFormatError(
                    f"File ends prematurely at line {line_num}"
                )

            if not plus.startswith("+"):
                if strict:
                    raise FastqFormatError(
                        f"Line {line_num}: invalid '+' line: {plus}"
                    )
                elif warn:
                    warnings.warn(
                        f"Line {line_num}: invalid '+' line: {plus}, "
                        "skip record"
                    )
                continue

            if len(seq) != len(qual):
                if strict:
                    raise FastqFormatError(
                        f"Line {line_num-2} & {line_num}: Sequence / quality "
                        f"length mismatch: ({len(seq)} vs {len(qual)})"
                    )
                elif warn:
                    warnings.warn(
                        f"Line {line_num-2} & {line_num}: Sequence / quality, "
                        f"length mismatch: ({len(seq)} vs {len(qual)})"
                        "skip record"
                    )
                continue

            skip_record = False
            for char in seq.upper():
                if char not in VALID_NT:
                    if strict:
                        raise FastqFormatError(
                            f"Invalid Sequence in line {line_num-2}: {seq}"
                        )
                    elif warn:
                        warnings.warn(
                            f"Invalid Sequence in line {line_num-2}: {seq}, "
                            f"{"skip" if skip_invalid_seq else "invalid"} "
                            "record"
                        )
                    if skip_invalid_seq:
                        skip_record = True
                    break
            if skip_record:
                continue

            yield SeqEntry(
                    seq=Sequence(seq), seq_id=header[1:],
                    qual=qual, source=file_name
                )


def read_fastq(
    file_name: str,
    strict: bool = False,
    warn: bool = True,
    skip_invalid_seq: bool = False
) -> "SeqCollections":
    from omibio.bio import SeqCollections

    entries = []
    for entry in read_fastq_iter(
        file_name,
        strict=strict,
        warn=warn,
        skip_invalid_seq=skip_invalid_seq
    ):
        entries.append(entry)

    return SeqCollections(entries=entries, source=file_name)


def main():
    input_path = r"./examples/data/read_fastq_test.fastq"
    result = read_fastq_iter(input_path, warn=True)
    for entry in result:
        print(repr(entry))


if __name__ == "__main__":
    main()
