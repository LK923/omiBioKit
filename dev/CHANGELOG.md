# omiBio Change Log

## [v0.1.3] 12/08/2025
  - Add `read_fastq()`, `write_fastq()`
  - The `read_fasta()` function has been optimized into a generator function. Still uses the `SeqCollections` wrapper externally, but the generator version can be accessed by calling `read_fasta_iter()`.
  - Added `warn: bool` and `skip_invalid_seq: bool` kwargs to `read_fasta()`, relax the format checking.

## [v0.1.3] 12/09/2025
  - Improve structure of CLI
  - Enhence `omibio gc compute` (previous `omibio gc`), `omibio gc compute`, etc.
  - Add `omibio gc window-gc` for sliding window GC CLI.

## [v0.1.3] 12/10/2025
  - Add `fasta_view_cli.py`
  - Remove the `__setitem__` method from the `Sequence` class and `Polypeptide`.
  - Add `slots=True` to `SeqInterval` class and `SeqEntry` class
  - Change requirement to python >= 3.11 (former 3.9)

## [v0.1.3] 12/11/2025
  - Deleted Gene & Genome since they're outdated and their positioning overlaps with SeqEntry & SeqCollections.
  - Add new CLI: `omibio fastq to-fasta`, `omibio fastq view`, `omibio fasta info`.
  - Add at_content() method to Sequence class.
  - Motify `write_fasta()` & `write_fastq()`: now support only return list of lines without writing to a specific file.

## [v0.1.3] 12/12/2025
  - Add tests, coverage >= 95%

## [v0.1.3] 12/13/2025
  - Enhence CLI: support sdtin & stdout
  - Add `omibio plot <COMMANDS>` for CLI plotting
  - Add `omibio plot kmer`, `omibio plot window`, `omibio kmer count`, `omibio kmer total`
  - Enhence `plot_kmer()`, now support muiltiple sequences

## [v0.1.4] 12/14/2025
  - Modify `AnalysisResult` to abstract class, add `KmerResult` & `IntervalRsult` for different types for analysis functions.
  - Modify analysis functions to adapt new `AnalysisResult`
  - Enhence CLI: `omibio fasta info` & `omibio fastq info`: avoid muiltiple traversal
  - Enhence ploting functions to adapt new `AnalysisResult`
  - Enhence all CLIs
  - update README.md, MOUDULES.md

## [v0.1.4] 12/19/2025
  - `Add read()` as a unified interface for file parsing functions.
  - Add `get_suffix` to utils.
  - Implement utils.

## [v0.1.4] 01/18/2026
  -Update analysis functions: no longer add original sequence to `AnalysisResult.metadata`. Add more detailed metadata.
  - Update `omibio.__init__`
  - Remove `slots=True` from dataclass
  - Add `info()` abstract method  to `AnalysisResult`, and add corresponding method to `IntervalResult` & `KmerResult`
  - Add `to_csv()` to` IntervalResult` & `KmerResult`
  - Fix bugs of `plot_orfs()` where '+' '-' strand did not show correctly
  - Add utils: `check_if_exist.py`
  - And some small-scalar modifications
