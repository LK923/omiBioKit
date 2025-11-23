from omibio.io.read_fasta import read


def main() -> None:
    input_file = r"./examples/data/sim.fa"  # Path of input fasta file
    sequence = read(input_file)  # Read fasta file
    consensus, profile = find_profile_matrix(sequence)
    write(consensus, profile)
    print(f"Consesnsus: {consensus}")  # Print consensus sequence


def find_profile_matrix(seq_dict: dict) -> tuple[str, dict]:
    """ Build a profile matrix and find a consensus sequence.

    Build a profile matrix and find a consensus sequence
    From a dictionary of sequences with the same length.

    Args: seq_dict:
        A dictionary where keys are the names of sequence
        and the values are the sequences.

    Returns:
    A tuple with two elements:
        consensus: the consensus sequence.
        profile: a dictionary of profile matrix.
        profile example:

            {
            "A" : [4,2,3,1,1,0,2,3],
            "C" : [1,2,0,0,1,4,5,6]
            ...
            }
    """
    sequences = list(seq_dict.values())  # Get all sequences
    lengths = [len(seq) for seq in sequences]  # Get length list of sequences

    # Check if the sequence lengths are consistent
    if len(set(lengths)) != 1:
        raise ValueError("The lengths of sequences are different.")
    seq_length = lengths[0]  # Get sequence length

    # Create profile dict for each nitrogen base and its list
    # Extend the length list of each base to the sequence length
    profile = {base: [0] * seq_length for base in "ACGT"}

    # Count the frequency of base occurrence
    for sequence in sequences:
        for i, base in enumerate(sequence):
            base_frequency = profile[base]
            base_frequency[i] += 1

    # Get the consensus according to the profile matrix
    # Compare the frequency of occurrence each base appears at each position
    # The base with the highest frequency of occurrence
    # Will be used as the consensus base.
    # If the frequencies of occurrence are the same,
    # The base is selected according to the A-C-G-T priority
    consensus = "".join(
        max("ACGT", key=lambda b: profile[b][i]) for i in range(seq_length)
    )

    return consensus, profile


def write(consensus: str, profile: dict) -> None:
    """ Write consensus and profile matrix to output file.

    Write the results of consensus and profile matrix
    In a text file called "consensus_output.txt"

    Args:
    consensus: the consensus sequence
    profile: the dictionary of profile matrix
    profile example:

        {
        "A" : [4,2,3,1,1,0,2,3],
        "C" : [1,2,0,0,1,4,5,6]
        ...
        }

    Write:
    write the consensus on the top and the profile matrix under it.
    Example:

        "
        ACATGTC
        A: 4 1 3 1 0 3 1
        C: 2 3 3 2 2 1 3
        G: 2 3 3 3 4 1 3
        T: 2 3 1 4 4 5 3
        "
    """
    # The path of output file
    output_file_name = r"./examples/output/consensus.txt"

    with open(output_file_name, "w") as f:
        f.write(f"{consensus}\n")
        for base in "ACGT":
            f.write(f"{base}: {' '.join(map(str, profile[base]))}\n")
    print(f"Output file: {output_file_name}")  # Print the path of output file


if __name__ == "__main__":
    main()
