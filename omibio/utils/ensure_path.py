from os import PathLike
from pathlib import Path


def ensure_path(path: str | PathLike) -> Path:
    """Ensure a path exists.

    Args:
        path (str | Path):
            The path to check.
    Raises:
        FileNotFoundError:
            If the path does not exist.
    Returns:
        Path:
            The path as a Path object if it exists.
    """
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
