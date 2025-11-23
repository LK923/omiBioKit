import re


def main():
    sequence = input("Enter sequence: ")
    pattern = input("Enter pattern: ")
    print(find_motif(sequence, pattern))


def find_motif(seq, pat):
    results = []
    pattern = re.compile(rf"(?=({pat}))")
    for match in re.finditer(pattern, seq):
        start_pos = match.start()
        end_pos = match.end()
        results.append(f"[{start_pos + 1}:{end_pos}]")

    return ", ".join(results)


if __name__ == "__main__":
    main()
