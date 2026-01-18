from importlib.metadata import version
from .sequence import (
    Sequence, Polypeptide,
    clean, write_report,
    complement, reverse_complement,
    random_seq, random_fasta,
    shuffle_seq,
    transcribe, reverse_transcribe,
    translate_nt
)
from .io import (
    read, read_fasta, read_fasta_iter, read_fastq, read_fastq_iter
)
from .analysis import (
    at, gc, find_consensus, find_motifs, find_orfs, get_formula,
    kmer, find_palindrome, calc_mass, sliding_gc
)
from .bio import (
    AnalysisResult, IntervalResult, KmerResult, SeqCollections,
    SeqEntry, SeqInterval
)
from .viz import (
    plot_kmer, plot_motifs, plot_orfs, plot_sliding_gc
)


__all__ = [
    "Sequence", "Polypeptide",
    "clean", "write_report",
    "complement", "reverse_complement",
    "random_seq", "random_fasta",
    "shuffle_seq",
    "transcribe", "reverse_transcribe",
    "translate_nt",
    "read", "read_fasta", "read_fasta_iter", "read_fastq", "read_fastq_iter",
    "at", "gc", "find_consensus", "find_motifs", "find_orfs", "get_formula",
    "kmer", "find_palindrome", "calc_mass", "sliding_gc",
    "AnalysisResult", "IntervalResult", "KmerResult", "SeqCollections",
    "SeqEntry", "SeqInterval",
    "plot_kmer", "plot_motifs", "plot_orfs", "plot_sliding_gc"
]
__version__ = version("omibio")
