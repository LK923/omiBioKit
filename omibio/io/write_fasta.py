from pathlib import Path


def write_fasta(
    file_path,
    seq_dict,
    line_len: int = 60,
    space_between: bool = False
) -> None:
    """Writes sequences to a FASTA file.

    Args:
        file_path (_type_):
            Path to output FASTA file.
        seq_dict (_type_):
            Dictionary of sequence name (str) to sequence (str or Sequence).
        line_len (int, optional):
            Number of characters per line in the FASTA file. Defaults to 60.
        space_between (bool, optional):
            Whether to add a blank line between sequences. Defaults to False.

    Raises:
        TypeError:
            if seq_dict is not a dict or if sequence names are not str.
        OSError:
            if unable to write to file.
    """

    if not isinstance(seq_dict, dict):
        raise TypeError(
            "write_fasta() argument 'seq_dict' must be dict, got "
            + type(seq_dict).__name__
        )
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with file_path.open("w", encoding="utf-8") as f:
            for name, seq in seq_dict.items():
                if not isinstance(name, str):
                    raise TypeError(
                        "write_fasta() Sequence name must be str, got "
                        + type(name).__name__
                    )

                seq = str(seq).replace("\n", "")
                f.write(f">{name}\n")

                for i in range(0, len(seq), line_len):
                    f.write(seq[i:i+line_len] + "\n")

                if space_between:
                    f.write("\n")

    except OSError as e:
        raise OSError(f"Could not write FASTA to '{file_path}': {e}") from e


def main():
    from omibio.io.read_fasta import read

    input_path = r"./examples/data/example_short_seqs.fasta"
    output_path = r"./examples/output/write_fasta_output.fasta"

    seq_dict = read(input_path)
    write_fasta(output_path, seq_dict, space_between=True)
    print(output_path)


if __name__ == "__main__":
    main()
