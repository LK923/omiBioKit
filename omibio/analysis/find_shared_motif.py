from omibio.io.read_fasta import read


def main() -> None:
    input_file = "./data/sequences.fasta"
    seq_dict = read(input_file)
    print(find_shared_motif(seq_dict))


def find_shared_motif(seq_dict: dict) -> str:
    sequences = list(seq_dict.values())
    longest_seq = max(sequences)
    max_length = len(longest_seq)
    for motif_length in range(max_length, 1, -1):

        for i in range(max_length - motif_length + 1):
            candidate = longest_seq[i: i + motif_length]
            if all(candidate in sequence for sequence in sequences[1:]):
                return candidate


if __name__ == "__main__":
    main()
