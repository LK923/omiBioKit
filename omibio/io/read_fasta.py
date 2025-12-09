from pathlib import Path
from typing import TYPE_CHECKING, Generator
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
    output_strict: bool = False,
    upper: bool = True,
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
            raise FastaFormatError(
                f"Sequence missing for {current_name}"
            )
        seq_str = "".join(current_seq)
        current_seq.clear()
        if faa:
            seq_obj = Polypeptide(seq_str, strict=output_strict)
        else:
            seq_obj = Sequence(seq_str, strict=output_strict)

        return SeqEntry(seq=seq_obj, seq_id=current_name, source=file_name)

    with open(file_name, "r") as file:
        for i, line in enumerate(file):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue  # Skip blank line.

            if line.startswith(">"):
                # Store the previous sequence when
                # encountering new sequence name.
                entry = push_entry()
                if entry:
                    yield entry

                # Store sequence name when encounter new sequence name.
                current_name = line[1:].strip()

                # Check for missing sequence name or
                # duplicate sequence name.
                if not current_name:
                    raise FastaFormatError(
                        f"Sequence Name Missing, last line: {i}"
                    )

            else:
                if current_name is None:
                    raise FastaFormatError(
                        "Fasta file must begin with '>'"
                    )
                # Store sequence.
                if strict:
                    line_up = line.upper()
                    for char in line_up:
                        if char not in allowed_set:
                            raise FastaFormatError(
                                f"Invalid Sequence in line {i}: {line}"
                            )
                    current_seq.append(line_up if upper else line)
                else:
                    current_seq.append(line.upper() if upper else line)

        # Store the last sequence when the file ends
        entry = push_entry()
        if entry:
            yield entry


def read_fasta(
    file_name: str,
    strict: bool = False,
    output_strict: bool = False,
    upper: bool = True,
) -> "SeqCollections":
    from omibio.bio import SeqCollections

    entries = []
    for entry in read_fasta_iter(
        file_name,
        strict=strict,
        output_strict=output_strict,
        upper=upper,
    ):
        entries.append(entry)

    return SeqCollections(entries=entries, source=file_name)


def main():
    input_path = r"./examples/data/example_lots_of_seqs.fasta"
    for entry in read_fasta_iter(input_path):
        print(repr(entry))


if __name__ == "__main__":
    main()
