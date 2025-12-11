# omiBio Change Log

## [v0.1.3] 12/08/2025
  - Add `read_fastq()`, `write_fastq()`
  - The `read_fasta()` function has been optimized into a generator function. Still uses the `SeqCollections` wrapper externally, but the generator version can be accessed by calling `read_fasta_iter()`.
  - Added `warn: bool` and `skip_invalid_seq: bool` kwargs to `read_fasta()`, relax the format checking.

## [v0.1.3] 12/09/2025
  - Improve structure of CLI
  - Enhence `omibio gc compute` (previous `omibio gc`), `omibio gc compute`, etc.
  - Add `omibio gc sliding-window` for sliding window GC CLI.

## [v0.1.3] 12/10/2025
  - Add `fasta_view_cli.py`
  - Remove the `__setitem__` method from the `Sequence` class and `Polypeptide`.
  - Add `slots=True` to SeqInterval class and SeqEntry class
  - Change requirement to python >= 3.12 (former 3.9)

## [v0.1.3] 12/11/2025
  - Deleted Gene & Genome since they're outdated and their positioning overlaps with SeqEntry & SeqCollections.
  - Add new CLI: `omibio fastq to-fasta`, `omibio fastq view`, `omibio fasta info`.
  - Add at_content() method to Sequence class.
  - Motify write_fasta() & write_fastq(): now support only return list of lines without writing to a specific file.