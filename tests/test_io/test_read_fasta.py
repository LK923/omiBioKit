import pytest
from omibio.bio import SeqEntry, SeqCollections
from omibio.io.read_fasta import (
    read_fasta_iter,
    read_fasta,
    FastaFormatError,
)


class TestReadFasta:
    def write(self, tmp_path, name, text):
        p = tmp_path / name
        p.write_text(text)
        return p

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            list(read_fasta_iter("no_such_file.fa"))

    def test_invalid_suffix(self, tmp_path):
        p = self.write(tmp_path, "a.txt", ">a\nATGC\n")
        with pytest.raises(FastaFormatError):
            list(read_fasta_iter(str(p)))

    def test_read_single_record(self, tmp_path):
        p = self.write(tmp_path, "a.fa", ">a\nATGC\n")
        res = list(read_fasta_iter(str(p)))
        assert len(res) == 1
        assert isinstance(res[0], SeqEntry)
        assert res[0].seq_id == "a"
        assert str(res[0].seq) == "ATGC"

    def test_read_multiple_records(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fa",
            ">a\nATGC\n>b\nGG\n",
        )
        res = list(read_fasta_iter(str(p)))
        assert [e.seq_id for e in res] == ["a", "b"]

    def test_missing_seq_non_strict(self, tmp_path):
        p = self.write(tmp_path, "a.fa", ">a\n>b\nAT\n")
        res = list(read_fasta_iter(str(p), strict=False, warn=False))
        assert len(res) == 1
        assert res[0].seq_id == "b"

    def test_missing_seq_strict(self, tmp_path):
        p = self.write(tmp_path, "a.fa", ">a\n>b\nAT\n")
        with pytest.raises(FastaFormatError):
            list(read_fasta_iter(str(p), strict=True))

    def test_missing_name_non_strict(self, tmp_path):
        p = self.write(tmp_path, "a.fa", ">\nATGC\n>a\nAT\n")
        res = list(read_fasta_iter(str(p), strict=False, warn=False))
        assert len(res) == 1
        assert res[0].seq_id == "a"

    def test_missing_name_strict(self, tmp_path):
        p = self.write(tmp_path, "a.fa", ">\nATGC\n")
        with pytest.raises(FastaFormatError):
            list(read_fasta_iter(str(p), strict=True))

    def test_invalid_char_non_strict_keep(self, tmp_path):
        p = self.write(tmp_path, "a.fa", ">a\nATXG\n")
        res = list(
            read_fasta_iter(
                str(p),
                strict=False,
                warn=False,
                skip_invalid_seq=False,
            )
        )
        assert len(res) == 1
        assert "X" in str(res[0].seq)

    def test_invalid_char_skip_record(self, tmp_path):
        p = self.write(tmp_path, "a.fa", ">a\nATXG\n>b\nAT\n")
        res = list(
            read_fasta_iter(
                str(p),
                strict=False,
                warn=False,
                skip_invalid_seq=True,
            )
        )
        assert len(res) == 1
        assert res[0].seq_id == "b"

    def test_invalid_char_strict(self, tmp_path):
        p = self.write(tmp_path, "a.fa", ">a\nATXG\n")
        with pytest.raises(FastaFormatError):
            list(read_fasta_iter(str(p), strict=True))

    def test_faa_protein(self, tmp_path):
        p = self.write(tmp_path, "a.faa", ">p\nACDE\n")
        res = list(read_fasta_iter(str(p)))
        assert len(res) == 1
        assert res[0].seq_id == "p"
        assert str(res[0].seq) == "ACDE"

    def test_comment_and_blank_lines(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fa",
            "# comment\n>a\nAT\n#x\nGC\n",
        )
        res = list(read_fasta_iter(str(p)))
        assert str(res[0].seq) == "ATGC"

    def test_read_fasta_collection(self, tmp_path):
        p = self.write(tmp_path, "a.fa", ">a\nAT\n>b\nGC\n")
        col = read_fasta(str(p))
        assert isinstance(col, SeqCollections)
        assert len(col) == 2
        assert "a" in col
        assert "b" in col

    def test_read_fasta_empty(self, tmp_path):
        p = self.write(tmp_path, "a.fa", "")
        col = read_fasta(str(p))
        assert len(col) == 0

    def test_warn(self, tmp_path):
        p = self.write(tmp_path, "a.fa", ">a\n>b\nAT\n")

        with pytest.warns(UserWarning, match="Sequence missing"):
            res = list(
                read_fasta_iter(
                    str(p),
                    strict=False,
                    warn=True,
                )
            )

        assert len(res) == 1
        assert res[0].seq_id == "b"

        p = self.write(tmp_path, "a.fa", ">\nACTG")
        with pytest.warns(UserWarning, match="name missing"):
            res = list(
                read_fasta_iter(
                    str(p),
                    strict=False,
                    warn=True,
                )
            )
        p = self.write(tmp_path, "a.fa", ">a\nINVALID")
        with pytest.warns(UserWarning, match="Invalid"):
            res = list(
                read_fasta_iter(
                    str(p),
                    strict=False,
                    warn=True,
                )
            )
