def within_range(
    n: int, min: int | None = None, max: int | None = None
) -> bool:
    """Check if a number is within a range."""
    if not n:
        return False
    return not ((min and n < min)
                or (max and n > max))


def main():
    n = 5
    max_length = 20
    min_length = 5
    print(within_range(n, min=min_length, max=max_length))


if __name__ == "__main__":
    main()
