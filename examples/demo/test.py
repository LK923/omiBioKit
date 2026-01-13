from omibio.io import read_fasta
from omibio.utils import chunked
from omibio.sequence import Sequence
from omibio.analysis import find_orfs
from concurrent.futures import ProcessPoolExecutor


def analysis(sequences: list[Sequence]):
    results = []
    for seq in sequences:
        orfs = find_orfs(seq)
        for orf in orfs:
            results.append(orf)
    return results


def main():
    seqs = read_fasta("./huge_data/huge.fasta").seqs()
    chunks = chunked(seqs, chunk_size=10)
    results = []

    with ProcessPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(analysis, chunk) for chunk in chunks]
        for f in futures:
            orfs = f.result()
            for orf in orfs:
                results.append(orf)
    print(len(results))


if __name__ == "__main__":
    main()
