import pytest
from omibio.bio import SeqEntry, SeqCollections
from omibio.io.read_fastq import (
    read_fastq_iter,
    read_fastq,
    FastqFormatError,
)
import io


class TestReadFastq:
    def write(self, tmp_path, name, text):
        p = tmp_path / name
        p.write_text(text)
        return p

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            list(read_fastq_iter("no_such.fastq"))

    def test_invalid_suffix(self, tmp_path):
        p = self.write(tmp_path, "a.fa", "@a\nAT\n+\n!!\n")
        with pytest.raises(FastqFormatError):
            list(read_fastq_iter(str(p)))

    def test_single_record(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nATGC\n+\n!!!!\n",
        )
        res = list(read_fastq_iter(str(p)))
        assert len(res) == 1
        assert isinstance(res[0], SeqEntry)
        assert res[0].seq_id == "a"
        assert str(res[0].seq) == "ATGC"
        assert res[0].qual == "!!!!"

    def test_multiple_records(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nAT\n+\n!!\n@b\nGC\n+\n##\n",
        )
        res = list(read_fastq_iter(str(p)))
        assert [e.seq_id for e in res] == ["a", "b"]

    def test_empty_line_non_strict(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "\n@a\nAT\n+\n!!\n",
        )
        res = list(read_fastq_iter(str(p), warn=False))
        assert len(res) == 1
        assert res[0].seq_id == "a"

    def test_header_not_at(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "a\nAT\n+\n!!\n",
        )
        with pytest.raises(FastqFormatError):
            list(read_fastq_iter(str(p)))

    def test_file_ends_prematurely(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nAT\n+\n",
        )
        with pytest.raises(FastqFormatError):
            list(read_fastq_iter(str(p)))

    def test_invalid_plus_non_strict(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nAT\nx\n!!\n",
        )
        res = list(read_fastq_iter(str(p), strict=False, warn=False))
        assert res == []

    def test_invalid_plus_strict(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nAT\nx\n!!\n",
        )
        with pytest.raises(FastqFormatError):
            list(read_fastq_iter(str(p), strict=True))

    def test_length_mismatch_non_strict(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nATG\n+\n!!\n",
        )
        res = list(read_fastq_iter(str(p), strict=False, warn=False))
        assert res == []

    def test_length_mismatch_strict(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nATG\n+\n!!\n",
        )
        with pytest.raises(FastqFormatError):
            list(read_fastq_iter(str(p), strict=True))

    def test_invalid_nt_keep_record(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nATXG\n+\n!!!!\n",
        )
        res = list(
            read_fastq_iter(
                str(p),
                strict=False,
                warn=False,
                skip_invalid_seq=False,
            )
        )
        assert len(res) == 1
        assert "X" in str(res[0].seq)

    def test_invalid_nt_skip_record(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nATXG\n+\n!!!!\n@b\nAT\n+\n!!\n",
        )
        res = list(
            read_fastq_iter(
                str(p),
                strict=False,
                warn=False,
                skip_invalid_seq=True,
            )
        )
        assert len(res) == 1
        assert res[0].seq_id == "b"

    def test_invalid_nt_strict(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nATXG\n+\n!!!!\n",
        )
        with pytest.raises(FastqFormatError):
            list(read_fastq_iter(str(p), strict=True))

    def test_read_fastq_collection(self, tmp_path):
        p = self.write(
            tmp_path,
            "a.fastq",
            "@a\nAT\n+\n!!\n@b\nGC\n+\n##\n",
        )
        col = read_fastq(str(p))
        assert isinstance(col, SeqCollections)
        assert len(col) == 2
        assert "a" in col
        assert "b" in col

    def test_read_fastq_empty(self, tmp_path):
        p = self.write(tmp_path, "a.fastq", "")
        col = read_fastq(str(p))
        assert len(col) == 0

    def test_warn(self, tmp_path):
        p = self.write(tmp_path, "a.fastq", "@a\nAT\nINVALID\n!!\n")

        with pytest.warns(UserWarning, match="invalid"):
            res = list(read_fastq_iter(str(p), warn=True))

        p = self.write(tmp_path, "a.fastq", "@a\nAAT\n+\n!!\n")

        with pytest.warns(UserWarning, match="mismatch"):
            res = list(read_fastq_iter(str(p), warn=True))

        p = self.write(tmp_path, "a.fastq", "@a\nAO\n+\n!!\n")

        with pytest.warns(UserWarning, match="Invalid"):
            res = list(
                read_fastq_iter(str(p), warn=True, skip_invalid_seq=True)
            )

        assert len(res) == 0

    def test_readfrom_stringio(self):
        fasta_content = "@seq\nACTG\n+\nIIII"
        fh = io.StringIO(fasta_content)
        entries = list(read_fastq_iter(fh))
        assert len(entries) == 1
        assert isinstance(entries[0], SeqEntry)
        assert entries[0].seq_id == "seq"
        assert entries[0].seq == "ACTG"
        assert entries[0].qual == "IIII"

        seqcollections = read_fastq(fh)
        assert seqcollections.source == "<stdin>"
