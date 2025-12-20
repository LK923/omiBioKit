from omibio.sequence import clean
from omibio.io import read

res = read("./examples/data/example_dirty.fasta", warn=False)
cleaned = clean(
    res, name_policy="id_only", gap_policy="collapse", remove_empty=True
)
for name, seq in cleaned.items():
    print(name)
    print(seq)
