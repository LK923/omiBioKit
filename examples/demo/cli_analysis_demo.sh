#!/bin/bash
omibio fasta view ./examples/data/example_long_seqs.fasta -h 5 |\
    omibio kmer count -k 3 --no-sort |\
    omibio plot kmer -o ./examples/output --cmap Purples --no-show
echo "./examples/output/kmer_heatmap.png"