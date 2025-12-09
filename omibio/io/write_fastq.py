from pathlib import Path
from omibio.bio import SeqCollections


def write_fastq(
    file_name: str,
    seqs:  SeqCollections
) -> list[str]:
    if not seqs:
        return []
    if not isinstance(seqs, SeqCollections):
        raise TypeError(
            "write_fastq() argument 'seqs' must be SeqCollections, "
            f"got {type(seqs).__name__}"
        )
    file_path = Path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    try:
        with file_path.open("w", encoding="utf-8") as f:
            for entry in seqs.entry_list():
                f.write(f"@{entry.seq_id}\n")
                lines.append(f"@{entry.seq_id}\n")

                f.write(str(entry.seq) + "\n")
                lines.append(str(entry.seq) + "\n")

                f.write("+\n")
                lines.append("+\n")

                f.write(entry.qual + "\n")
                lines.append(entry.qual + "\n")

    except OSError as e:
        raise OSError(f"Could not write fastq to '{file_name}': {e}") from e

    return lines


def main():
    from omibio.io.read_fastq import read_fastq

    input_path = r"./examples/data/example_fastq.fastq"
    output_path = r"./examples/output/write_fastq_output.fastq"

    seqs = read_fastq(input_path)
    lines = write_fastq(output_path, seqs)
    print(output_path)
    print("".join(lines))


if __name__ == "__main__":
    main()
