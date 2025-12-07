import pytest
from unittest.mock import patch
from omibio.io.read_fasta import read, FastaFormatError
from omibio.sequence.sequence import Sequence


class TestReadFasta:
    def test_file_not_found(self):
        with pytest.raises(FastaFormatError):
            read("no_such_file.fasta")

    def test_invalid_extension(self, tmp_path):
        p = tmp_path / "abc.txt"
        p.write_text(">seq1\nATGC")
        with pytest.raises(FastaFormatError):
            read(str(p))

    def test_missing_header(self, tmp_path):
        p = tmp_path / "bad.fasta"
        p.write_text("ATGC")
        with pytest.raises(FastaFormatError):
            read(str(p))

    def test_missing_seq_name(self, tmp_path):
        p = tmp_path / "bad.fasta"
        p.write_text(">\nATGC")
        with pytest.raises(FastaFormatError):
            read(str(p))

    def test_duplicate_name(self, tmp_path):
        p = tmp_path / "dup.fasta"
        p.write_text(">a\nAT\n>a\nGC")
        with pytest.raises(FastaFormatError):
            read(str(p))

    def test_invalid_seq_strict_dna(self, tmp_path):
        p = tmp_path / "bad.fasta"
        p.write_text(">seq\nATL")
        with pytest.raises(FastaFormatError):
            read(str(p), strict=True)

    def test_basic_read_as_str(self, tmp_path):
        p = tmp_path / "ok.fasta"
        p.write_text(">seq\nATGC")
        r = read(str(p))
        assert r["seq"] == "ATGC"

    def test_basic_read_sequence_obj(self, tmp_path):
        p = tmp_path / "ok.fasta"
        p.write_text(">seq\nATGC")
        r = read(str(p))
        assert isinstance(r["seq"], Sequence)
        assert str(r["seq"]) == "ATGC"

    def test_multiline(self, tmp_path):
        p = tmp_path / "ok.fasta"
        p.write_text(">s\nAT\nGC")
        r = read(str(p))
        assert r["s"] == "ATGC"

    def test_comment_and_blank_lines(self, tmp_path):
        p = tmp_path / "ok.fasta"
        p.write_text(">s\nAT#x\n\nGC")
        r = read(str(p))
        assert r["s"] == "ATGC"

    def test_protein_faa_strict(self, tmp_path):
        p = tmp_path / "ok.faa"
        p.write_text(">p\nACDE")
        r = read(str(p))
        assert r["p"] == "ACDE"

    def test_protein_faa_invalid(self, tmp_path):
        p = tmp_path / "bad.faa"
        p.write_text(">p\nACDEZ")
        with pytest.raises(FastaFormatError):
            read(str(p), strict=True)

    def test_strict_false_accept_any(self, tmp_path):
        p = tmp_path / "any.fasta"
        p.write_text(">x\nA*.-xyz")
        r = read(str(p), strict=False)
        assert r["x"] == "A*.-XYZ"

    def test_output_strict_true(self, tmp_path):
        p = tmp_path / "ok.fasta"
        p.write_text(">x\nATGC")
        r = read(str(p), output_strict=True)
        assert isinstance(r["x"], Sequence)
        assert str(r["x"]) == "ATGC"

    def test_missing_Seq(self, tmp_path):
        p = tmp_path / "ms.fasta"
        p.write_text(">x\n>s\nACTG")
        with pytest.raises(FastaFormatError):
            read(str(p))

    def test_ioerror(self, tmp_path):
        test_file = tmp_path / "file.fasta"
        test_file.write_text(">seq1\nATG")  # 必须存在

        def mock_open(*args, **kwargs):
            raise IOError("mocked IOError")

        with patch("builtins.open", mock_open):
            with pytest.raises(IOError) as excinfo:
                read(str(test_file))
            assert "mocked IOError" in str(excinfo.value)
