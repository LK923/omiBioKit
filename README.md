# omiBioKit

A lightweight and easy-to-use Python bioinformatics toolkit for sequence analysis, ORF finding, GC content calculation, and random sequence generation.

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![License: MIT](https://img.shields.io/github/license/LK923/omiBioKit.svg)](https://github.com/LK923/omiBioKit)

---

## 🚀 Features

- 🔍 **Find Open Reading Frames (ORFs)** in FASTA sequences with customizable parameters:
  - Support for both strands
  - Overlapping ORF detection
  - Optional translation to amino acid sequences
  - Custom start codons (e.g., ATG, GTG)
- 📊 **Calculate GC Content** of nucleotide sequences
- 🧪 **Generate Random Sequences** of specified length and count
- 🔄 **Convert between sequence formats** (FASTA → FASTQ, etc.)
- 📈 **Extract subsets** by ID or genomic region
- 🧩 **Extensible CLI** with clear help messages and optional dependencies

---

## 🛠️ Installation

Install from PyPI:

```bash
pip install omibio
