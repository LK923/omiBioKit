import pytest
from omibio.bio import SeqEntry, SeqCollections
from omibio.io.write_fastq import write_fastq
from omibio.sequence import Sequence


class TestWriteFastq:
    def make_entry(self, seq_str="ATGC", seq_id="s1", qual="!!!!"):
        return SeqEntry(seq=Sequence(seq_str), seq_id=seq_id, qual=qual)

    def test_empty_collection(self):
        col = SeqCollections()
        lines = write_fastq(col)
        assert lines == []

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            write_fastq(["not a SeqCollections"])

    def test_basic_lines(self):
        e1 = self.make_entry("AT", "a", "!!")
        e2 = self.make_entry("GC", "b", "##")
        col = SeqCollections([e1, e2])
        lines = write_fastq(col)
        assert lines == [
            "@a", "AT", "+", "!!",
            "@b", "GC", "+", "##",
        ]

    def test_write_to_file(self, tmp_path):
        e1 = self.make_entry("AT", "a", "!!")
        col = SeqCollections([e1])
        file_path = tmp_path / "test.fastq"
        lines = write_fastq(col, str(file_path))
        assert file_path.exists()
        content = file_path.read_text().splitlines()
        assert content == lines

    def test_nested_dir_creation(self, tmp_path):
        e1 = self.make_entry("AT", "a", "!!")
        col = SeqCollections([e1])
        file_path = tmp_path / "nested" / "dir" / "test.fastq"
        lines = write_fastq(col, str(file_path))
        assert file_path.exists()
        content = file_path.read_text().splitlines()
        assert content == lines
