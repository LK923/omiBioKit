from pathlib import Path
from omibio.sequence import Sequence, Polypeptide
from omibio.bio import SeqCollections
from typing import Mapping


def write_fasta(
    file_name: str,
    seqs: Mapping[str, Sequence | Polypeptide | str] | SeqCollections,
    line_len: int = 60
) -> list[str]:
    """Writes sequences to a FASTA file.

    Args:
        file_name (_type_):
            Path to output FASTA file.
        seqs (_type_):
            Dictionary of sequence name (str) to sequence (str or Sequence).
        line_len (int, optional):
            Number of characters per line in the FASTA file. Defaults to 60.

    Raises:
        TypeError:
            if seqs is not a dict or if sequence names are not str.
        OSError:
            if unable to write to file.
    """
    if not seqs:
        return []

    if isinstance(seqs, SeqCollections):
        seq_dict = seqs.seq_dict()
    elif isinstance(seqs, dict):
        seq_dict = seqs
    else:
        raise TypeError(
            "write_fasta() argument 'seqs' must be dict or SeqCollections, "
            f"got {type(seqs).__name__}"
        )
    file_path = Path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    try:
        with file_path.open("w", encoding="utf-8") as f:
            for name, seq in seq_dict.items():
                if not isinstance(name, str):
                    raise TypeError(
                        "write_fasta() Sequence name must be str, got "
                        + type(name).__name__
                    )

                seq_str = str(seq).replace("\n", "")
                f.write(f">{name}\n")
                lines.append(f">{name}")

                for i in range(0, len(seq_str), line_len):
                    f.write(seq_str[i:i+line_len] + "\n")
                    lines.append(seq_str[i:i+line_len])

    except OSError as e:
        raise OSError(f"Could not write fasta to '{file_name}': {e}") from e

    return lines


def main():
    from omibio.io.read_fasta import read_fasta

    input_path = r"./examples/data/example_short_seqs.fasta"
    output_path = r"./examples/output/write_fasta_output.fasta"

    seqs = read_fasta(input_path)
    write_fasta(output_path, seqs)
    print(output_path)


if __name__ == "__main__":
    main()
