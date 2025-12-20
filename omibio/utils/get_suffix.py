from pathlib import Path


def get_suffix(path: str, with_dot: bool = True) -> str:
    """Get the suffix of a file path string.

    Args:
        path (str):
            The file path string.
        with_dot (bool, optional)
            Whether to include the leading dot in the suffix. Defaults to True.

    Returns:
        str:
            The suffix of the file path string.
    """
    suffix = Path(path).suffix.lower()
    return suffix if with_dot else suffix.lstrip(".")


def main():
    path = "test.suffix"
    print(get_suffix(path))
    print(get_suffix(path, with_dot=False))


if __name__ == "__main__":
    main()
