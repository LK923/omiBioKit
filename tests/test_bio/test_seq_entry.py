import pytest
from omibio.bio.seq_entry import SeqEntry
from omibio.sequence import Sequence, Polypeptide


class TestSeqEntry:
    def make_seq(self, seq="ATGC", is_pep=False):
        if is_pep:
            return Polypeptide(seq)
        return Sequence(seq)

    def test_init_valid_dna(self):
        s = self.make_seq("ATGC")
        e = SeqEntry(seq=s, seq_id="id1")
        assert e.seq is s
        assert e.seq_id == "id1"
        assert e.source is None
        assert e.qual is None
        assert e.metadata == {}

    def test_init_valid_peptide(self):
        s = self.make_seq("ACD", is_pep=True)
        e = SeqEntry(seq=s, seq_id="pep1")
        assert e.seq is s
        assert e.seq_id == "pep1"

    def test_init_seq_not_valid_type(self):
        with pytest.raises(TypeError):
            SeqEntry(seq="ATGC", seq_id="x")

    def test_init_seq_id_not_str(self):
        s = self.make_seq()
        with pytest.raises(TypeError):
            SeqEntry(seq=s, seq_id=123)

    def test_str(self):
        s = self.make_seq("ATGC")
        e = SeqEntry(seq=s, seq_id="s1")
        assert str(e) == str(s)

    def test_repr_basic(self):
        s = self.make_seq("ATGC")
        e = SeqEntry(seq=s, seq_id="s1")
        r = repr(e)
        assert "SeqEntry" in r
        assert "seq_id='s1'" in r
        assert "ATGC" in r

    def test_repr_with_qual(self):
        s = self.make_seq("ATGC")
        e = SeqEntry(seq=s, seq_id="s1", qual="!!!!")
        r = repr(e)
        assert "qual=" in r
        assert "!!!!" in r

    def test_metadata_default(self):
        s = self.make_seq("ATGC")
        e = SeqEntry(seq=s, seq_id="s1")
        assert isinstance(e.metadata, dict)

    def test_metadata_custom(self):
        s = self.make_seq("ATGC")
        meta = {"a": 1}
        e = SeqEntry(seq=s, seq_id="s1", metadata=meta)
        assert e.metadata is meta
