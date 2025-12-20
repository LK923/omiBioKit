import io
import pytest
from omibio.io import read
from omibio.bio import SeqCollections


class TestRead:
    def test_textio_missing_format(self):
        fh = io.StringIO(">seq1\nATGC\n")
        with pytest.raises(TypeError, match="Missing argument 'format'"):
            read(fh)

    def test_textio_with_fasta_format(self):
        fh = io.StringIO(">seq1\nATGC\n")
        result = read(fh, format="fasta")
        assert isinstance(result, SeqCollections)
        assert len(result) == 1
        assert "seq1" in result

    def test_textio_with_fastq_format(self):
        fh = io.StringIO("@seq1\nATGC\n+\n!!!!\n")
        result = read(fh, format="fastq")
        assert isinstance(result, SeqCollections)
        assert len(result) == 1
        assert "seq1" in result

    def test_path_auto_detect_fasta(self, tmp_path):
        fasta = tmp_path / "file.fa"
        fasta.write_text(">seq1\nATGC\n")
        result = read(fasta)
        assert isinstance(result, SeqCollections)
        assert len(result) == 1
        assert "seq1" in result

    def test_path_auto_detect_fastq(self, tmp_path):
        fastq = tmp_path / "file.fq"
        fastq.write_text("@seq1\nATGC\n+\n!!!!\n")
        result = read(fastq)
        assert isinstance(result, SeqCollections)
        assert len(result) == 1
        assert "seq1" in result

    def test_invalid_format_raises(self):
        path = "file.txt"
        with pytest.raises(TypeError, match="Invalid format to read"):
            read(path, format="txt")

    def test_skip_invalid_seq_warning(self):
        fh = io.StringIO(">seq1\nATXX\n")
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = read(fh, format="fasta", skip_invalid_seq=True)
            assert isinstance(result, SeqCollections)
            assert len(result) == 0
            assert any("skip" in str(wi.message) for wi in w)
