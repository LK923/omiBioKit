from pathlib import Path


def ensure_path(path: str | Path) -> Path:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File '{p}' not found.")
    return p


def main():
    path = r"./examples/data/read_fasta_test.fasta"
    try:
        ensure_path(path)
    except FileNotFoundError:
        print("False")


if __name__ == "__main__":
    main()
