import re
from pathlib import Path


class FastaFormatError(Exception):
    """Define error class: Fasta Format Error"""

    def __init__(self, message):
        super().__init__(message)


def read(
    file_name: str,
    as_str: bool = False,
    strict: bool = True,
    output_strict: bool = False
) -> dict:
    """Read fasta file and return sequence and name mapping.

    Read fasta file and return sequence, name mapping in a dictionary.
    Automatically ignore blank and comment lines. Can check file format errors.

    Args:
        file_name:
        The name of the fasta file to read, a str ends with
        ".fasta", ".fa", ".fna", ".faa".

    Returns:
        A dictionary that maps sequence names to the sequences below them.
        example:

    {
    "seq1": ATGATCGTAC,
    "seq2": AAAAAAAAAA,
    "seq3": NNNNNNNNNN
    }

    Raises:
        FastaFormatError: Errors in the file content format.
    """
    from omibio.sequence.sequence import Sequence
    # Check for file format
    file_path = Path(file_name)
    if not file_path.exists():
        raise FastaFormatError(f"File '{file_name}' not found.")

    # Check for file format
    ext = file_path.suffix.lower()
    valid_exts = {".fasta", ".fa", ".fna", ".faa"}
    if ext not in valid_exts:
        raise FastaFormatError("Needs a fasta file. ")

    sequences = {}
    current_name = None
    current_seq: list[str] = []

    def store_sequence(name, seq):
        if not name:
            return
        if name in sequences:
            raise FastaFormatError(f"Sequence Name '{name}' Already Exists")
        if not seq:
            raise FastaFormatError(f"Sequence Missing for {name}")
        sequences[name] = (
            "".join(seq) if as_str
            else Sequence("".join(seq), strict=output_strict)
        )

    if strict:
        match ext:
            case ".fasta" | ".fa" | ".fna":
                pattern = re.compile(r"[ATUCGRYKMBVDHSWN]+", flags=re.I)
            case ".faa":
                pattern = re.compile(r"[ACDEFGHIKLMNPQRSTVWYX*]+", flags=re.I)
    else:
        pattern = re.compile(r".*", flags=re.DOTALL)

    try:
        with open(file_name, "r") as file:
            for line in file:
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue  # Skip blank line.
                if line.startswith(">"):
                    # Store the previous sequence when
                    # encountering new sequence name.
                    store_sequence(current_name, current_seq)
                    # Store sequence name when encounter new sequence name.
                    current_name = line[1:].strip()

                    # Check for missing sequence name or
                    # duplicate sequence name.
                    if not current_name:
                        raise FastaFormatError("Sequence Name Missing")
                    current_seq = []  # Initialize sequence list

                elif current_name is None:
                    # Check if the first valid line starts with '>'.
                    raise FastaFormatError("Fasta file must begin with '>'")
                else:
                    # Store sequence.
                    if pattern.fullmatch(line):
                        current_seq.append(line.upper())
                    # Raise error if encountering invalid sequence.
                    else:
                        raise FastaFormatError(f"Invalid Sequence: {line}")

            # Store the last sequence when the file ends
            store_sequence(current_name, current_seq)

    except IOError as e:
        raise IOError(f"Error reading file '{file_name}': {e}")

    return sequences


def main():
    input_path = r"./examples/data/example_short_seqs.fasta"
    seq_dict = read(input_path, as_str=False)
    for seq in seq_dict.values():
        print(repr(seq))


if __name__ == "__main__":
    main()
