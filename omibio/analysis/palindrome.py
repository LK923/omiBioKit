from omibio.io.read_fasta import read
from omibio.utils.complement import reverse_complement

# TODO: Needs modifications.


def main() -> None:
    input_file = r"./examples/data/sim.fa"  # Input file path
    sequences = list(read(input_file).values())
    results = []
    for sequence in sequences:
        results.extend(find_palindrome(sequence))
    print("\n".join(map(str, results)))


def find_palindrome(
    sequence: str,
    min_len: int = 4,
    max_len: int = 12
) -> list[str]:
    """Finds all palindromic sequences in the given DNA sequence."""
    seq_length = len(sequence)
    results = []

    # Check for palindromic sequences of lengths from 12 down to 4
    for palindrome_length in range(max_len, min_len - 1, -1):
        # Iterate through the sequence to find palindromic substrings
        for i in range(seq_length - palindrome_length + 1):
            # Extract the candidate substring
            candidate = sequence[i: i + palindrome_length]

            # Check if the candidate is a palindrome
            if candidate == reverse_complement(candidate):
                results.append((i + 1, len(candidate)))

    return results


if __name__ == "__main__":
    main()
