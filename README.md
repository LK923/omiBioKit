# omiBio - A lightweight and easy-to-use Python bioinformatics toolkit.

[![Latest Version](https://img.shields.io/github/v/release/LK923/omiBioKit)](https://github.com/LK923/omiBioKit/releases)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

## Introduction
omiBio (omiBioKit) is an open-source Python 3 package that is lightweight, easy to use, and publicly available, suitable for education, general bioinformatics, and scientific research.

- Provides various commonly used bioinformatics data structures, such as Sequence and Polypeptide, as well as a variety of corresponding methods, and offers optional validity checks.
- For users accustomed to using functional interfaces, we have also encapsulated most of the class methods into functions.
- rovides tools for reading and writing general bioinformatics files (such as FASTA), taht is easy to use, and produces clear results.
- Provides a variety of commonly used analysis tool functions, with a rich set of optional parameters, making it easy to use and flexible.
- Provide command-line interfaces for commonly used tools.
- Provides simple visualization tools (based on matplotlib).

## Usage example
```python
from omibio.analysis import sliding_gc, draw_sliding_gc
from omibio.io import read

seq_dict = read("./example.fasta")
dna: Sequence = seq_dict["example"]

gc_list = sliding_gc(dna, window=200, step=20)
draw_sliding_gc(gc_list, seq=dna, window_avg=True)

```
The above code will produce the following result:
![Example](examples/assets/sliding_gc_viz_demo.png)

## Installation

Install from PyPI:

```bash
pip install omibio
