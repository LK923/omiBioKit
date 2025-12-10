# omiBio Change Log

## [v0.1.3] 12/08/2025
  - Add `read_fastq()`, `write_fastq()`
  - The `read_fasta()` function has been optimized into a generator function. Still uses the `SeqCollections` wrapper externally, but the generator version can be accessed by calling `read_fasta_iter()`.
  - Added `warn: bool` and `skip_invalid_seq: bool` kwargs to `read_fasta()`, relax the format checking.
  - TODO: Write test files for the new code.
