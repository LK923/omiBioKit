from re import sub

# TODO: Convert this to a more universal and more easy-to-use tool.


def main():
    print(transcribe("ATCGATGCAGCTACTACTAC"))


def transcribe(seq):
    rna_seq = sub("T", "U", seq)
    return rna_seq


if __name__ == "__main__":
    main()
