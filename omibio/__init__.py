from importlib.metadata import version
from omibio.sequence import Sequence, Polypeptide
from omibio.bio import SeqInterval, Gene, Genome
from omibio.sequence.seq_utils.clean import CleanReport, CleanReportItem
from omibio.io.read_fasta import FastaFormatError, read

__version__ = version("omibio")

__all__ = [
    "Sequence", "Polypeptide",
    "SeqInterval", "Gene", "Genome",
    "CleanReport", "CleanReportItem",
    "FastaFormatError", "read"
]
