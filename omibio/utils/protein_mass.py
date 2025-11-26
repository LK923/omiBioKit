from omibio.sequence.polypeptide import Polypeptide


def main():
    print(calc_mass("A"))


def calc_mass(aa_seq: Polypeptide | str, accuracy: int = 3) -> float:
    if not isinstance(aa_seq, (Polypeptide, str)):
        raise TypeError(
            "calc_mass() argument 'aa_seq' must be Polypeptide or str, got "
            + type(aa_seq).__name__
        )
    if isinstance(aa_seq, str):
        aa_seq = Polypeptide(aa_seq)

    return aa_seq.mass(accuracy)


if __name__ == "__main__":
    main()
