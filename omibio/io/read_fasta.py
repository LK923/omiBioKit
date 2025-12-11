from pathlib import Path
from typing import TYPE_CHECKING, Generator
import warnings
if TYPE_CHECKING:
    from omibio.bio import SeqCollections, SeqEntry

VALID_NT = set("ATUCGRYKMBVDHSWN")
VALID_AA = set("ACDEFGHIKLMNPQRSTVWYX*")


class FastaFormatError(Exception):

    def __init__(self, message):
        super().__init__(message)


def read_fasta_iter(
    file_name: str,
    strict: bool = False,
    warn: bool = True,
    output_strict: bool = False,
    skip_invalid_seq: bool = False,
) -> Generator["SeqEntry"]:
    from omibio.sequence import Sequence, Polypeptide
    from omibio.bio import SeqEntry

    file_path = Path(file_name)
    if not file_path.exists():
        raise FileNotFoundError(f"File '{file_name}' not found.")

    suffix = file_path.suffix.lower()
    if suffix not in {".faa", ".fa", ".fasta", ".fna"}:
        raise FastaFormatError(
            f"Invalid format to read: {suffix}"
        )
    faa = (suffix == ".faa")

    current_name = None
    current_seq: list[str] = []
    allowed_set = VALID_AA if faa else VALID_NT

    def push_entry():
        if current_name is None:
            return
        if not current_seq:
            msg = f"Sequence missing for {current_name}"
            if strict:
                raise FastaFormatError(msg)
            elif warn:
                warnings.warn(msg + ", skip record")
            return

        seq_str = "".join(current_seq)
        current_seq.clear()
        if faa:
            seq_obj = Polypeptide(seq_str, strict=output_strict)
        else:
            seq_obj = Sequence(seq_str, strict=output_strict)

        return SeqEntry(seq=seq_obj, seq_id=current_name, source=file_name)

    with open(file_name, "r") as file:

        for i, line in enumerate(file, start=1):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue

            if line.startswith(">"):
                entry = push_entry()
                if entry:
                    yield entry

                current_name = line[1:].strip()

                if not current_name:
                    if strict:
                        raise FastaFormatError(
                            f"Sequence Name Missing in line {i}"
                        )
                    elif warn:
                        warnings.warn(
                            f"Sequence Name Missing in line {i}, "
                            "skip record"
                        )
                    current_name = None
                    current_seq.clear()
                    continue

            else:
                if current_name is None:
                    continue
                # Store sequence.
                line = line.upper()
                skip_record = False
                for char in line:
                    if char not in allowed_set:
                        if strict:
                            raise FastaFormatError(
                                f"Invalid Sequence in line {i}: {line}"
                            )
                        elif warn:
                            warnings.warn(
                                f"Invalid Sequence in line {i}: {line}, "
                                f"{'skip' if skip_invalid_seq else 'invalid'} "
                                "record"
                            )
                        if skip_invalid_seq:
                            skip_record = True
                            break
                if skip_record:
                    current_name = None
                    current_seq.clear()
                    continue

                current_seq.append(line)

        # Store the last sequence when the file ends
        entry = push_entry()
        if entry:
            yield entry


def read_fasta(
    file_name: str,
    strict: bool = False,
    output_strict: bool = False,
    warn: bool = True,
    skip_invalid_seq: bool = False
) -> "SeqCollections":
    from omibio.bio import SeqCollections

    entries = []
    for entry in read_fasta_iter(
        file_name,
        strict=strict,
        output_strict=output_strict,
        warn=warn,
        skip_invalid_seq=skip_invalid_seq
    ):
        entries.append(entry)

    return SeqCollections(entries=entries, source=file_name)


def main():
    input_path = r"./examples/data/read_fasta_test.fasta"
    for entry in read_fasta(
        input_path, strict=False, skip_invalid_seq=True, warn=True
    ):
        print(repr(entry))


if __name__ == "__main__":
    main()
