def to_percentage(num: int | float, decimals: int = 2) -> str:
    """Convert a number to a percentage string."""
    return f"{float(num) * 100:.{decimals}f}%"


def main():
    num = 0.898989
    print(to_percentage(num))


if __name__ == "__main__":
    main()
