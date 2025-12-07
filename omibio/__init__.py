from importlib.metadata import version
from .sequence import Sequence, Polypeptide
from .bioObjects import SeqInterval, Gene, Genome, AnalysisResult
from .utils.clean import CleanReport, CleanReportItem
from .io.read_fasta import FastaFormatError

__version__ = version("omibio")

__all__ = [
    "Sequence", "Polypeptide",
    "SeqInterval", "Gene", "Genome", "AnalysisResult",
    "CleanReport", "CleanReportItem",
    "FastaFormatError"
]
