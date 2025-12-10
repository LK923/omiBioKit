# omiBio Change Log

## [v0.1.3] 12/08/2025
  - Add `read_fastq()`, `write_fastq()`
  - The `read_fasta()` function has been optimized into a generator function. Still uses the `SeqCollections` wrapper externally, but the generator version can be accessed by calling `read_fasta_iter()`.
  - Added `warn: bool` and `skip_invalid_seq: bool` kwargs to `read_fasta()`, relax the format checking.
  - TODO: Write test files for the new code.

## [v0.1.3] 12/09/2025
  - Improve structure of CLI
  - Enhence `omibio gc compute` (previous `omibio gc`), `omibio gc compute`, etc.
  - Add `omibio gc sliding-window` for sliding window GC CLI.
