from src.fastaReader import read
import re

# TODO: Convert this to a more universal and more easy-to-use tool.


def calculate_pct(file_name: str) -> dict[str, float]:
    """Calculate the percentage of G and C in each sequence in the file"""
    seq = read(file_name)  # Get the sequences and their names through read().
    percentages = {}

    output_path = r".\output\gc_counter_output.txt"
    with open(output_path, "w") as f:
        for key in seq:
            gc = re.findall(r"[CG]", seq[key])  # Get the list of G and C.
            # Assign value of percentages to the key.
            percentages[key] = 100 * (len(gc) / len(seq[key]))
            f.write(f"{key}: {percentages[key]:.2f}%\n")

    print(f"GC percentages written to {output_path}")
    return percentages


def main():
    print(calculate_pct(r".\data\example_fa.fasta"))


if __name__ == "__main__":
    main()
