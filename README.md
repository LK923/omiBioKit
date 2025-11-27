# omiBio - A Lightweight Bioinformatics Toolkit for Python

[![Latest Version](https://img.shields.io/github/v/release/LK923/omiBioKit)](https://github.com/LK923/omiBioKit/releases)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)


## Introduction
**omiBio** is a lightweight, user-friendly Python toolkit for bioinformatics — ideal for education, research, and rapid prototyping.

 **Key features**:
-  **Robust data structures**: `Sequence`, `Polypeptide`, `Gene`, `Genome`, etc., with optional validation.
-  **Simple I/O**: Read/write bioinformatics files (e.g., FASTA) with one-liners.
-  **Analysis tools**: GC content, ORF detection, consensus sequences, sliding windows, and more.
-  **CLI included**: Run common tasks from the terminal .
-  **Basic visualization**: Built-in plotting (via matplotlib) for quick insights.
-  **Functional & OOP APIs**: Use classes or convenient wrapper functions.

## Modules Overview

- `omibio.sequence`: Sequence-type data structures, including Sequence, Polypeptide, etc.
- `omibio.bioObjects`: Biological objects and data containers that support structured bioinformatics workflows. e.g., SeqInterval, Gene and Genome.
- `omibio.io`: Functions for reading and writing common bioinformatics file formats (e.g., FASTA), designed to be simple and user-friendly.
- `omibio.analysis`: Analysis functions, e.g., GC content, consensus sequences and find ORF.
- `omibio.utils`: General-purpose utility functions and function encapsulation for class methods.
- `omibio.cli`: Command-line interfaces for common workflows, enabling users to run analyses directly from the terminal.

## Usage example
#### Creating a sliding window GC chart using **omiBio**:
```python
from omibio.analysis import sliding_gc, draw_sliding_gc
from omibio.sequence import Sequence
from omibio.io import read

# Load sequences from FASTA (returns dict[str, Sequence])
seq_dict = read("examples/example.fasta")
dna: Sequence = seq_dict["example"]

# Compute GC content in sliding windows (window=200 bp, step=20 bp)

gc_list = sliding_gc(dna, window=200, step=20)

# Visualize easily
draw_sliding_gc(gc_list, seq=dna, window_avg=True)

```
The above code will produce results like this:

<p align="center">
  <img src="examples/assets/sliding_gc_viz_demo.png" alt="Example" width="800"/>
</p>

---
#### Using **omiBio**'s Command-line interfaces:
```bash
$ omibio orf example.fasta --min-length 100
```
The above CLI will produce results like this:
```bash
example_2    70      289     -       -2      219
example_16   53      257     +       +3      204
example_13   118     301     +       +2      183
example_4    92      272     -       -1      180
example_2    157     322     +       +2      165
example_5    17      173     -       -1      156
example_16   176     332     -       -1      156
example_3    177     324     -       -3      147
example_19   172     319     -       -2      147
example_1    44      188     +       +3      144
example_16   120     264     +       +1      144
example_17   164     308     -       -1      144
example_19   180     309     -       -3      129
example_3    68      194     -       -1      126
example_13   188     299     -       -1      111
example_17   93      201     +       +1      108
example_5    80      185     +       +3      105
example_11   214     319     +       +2      105
example_9    35      137     -       -1      102
example_13   134     236     +       +3      102
example_15   226     328     +       +2      102
example_17   114     216     -       -3      102

```
## Installation

### From PyPI (stable release):
```bash
$ pip install omibio
```

## Requirements

- **Python**: >= 3.9
- **Core dependencies**:
  - `click` (for CLI)
- **Optional dependencies** (install for extra features):
  - `matplotlib` → enables visualization 

>  Optional deps won't be installed by default. To get them:
> ```bash
> pip install omibio[plot]   # if you configure extras in pyproject.toml
> ```

For complete project build and dependency configuration, please refer to [`pyproject.toml`](pyproject.toml)