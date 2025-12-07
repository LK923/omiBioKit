import pytest
from omibio.bio import SeqInterval
from omibio.sequence import Sequence, Polypeptide

# pytest --cov=omibio.bioObjects.seq_interval tests/ --cov-report=term-missing


class TestSeqInterval:
    def test_init(self):
        s = SeqInterval(
            start=0, end=9, nt_seq="ATGAAATAA", type="ORF", seq_id="test",
            strand="-", gc=0.22, aa_seq="MK", frame=-1
        )
        assert s.start == 0
        assert s.end == 9
        assert s.nt_seq == "ATGAAATAA"
        assert s.type == "ORF"
        assert s.seq_id == "test"
        assert s.strand == "-"
        assert s.gc == 0.22
        assert s.aa_seq == "MK"
        assert s.frame == -1

        s = SeqInterval(start=0, end=9)
        assert not s.nt_seq == "ACAC"
        assert not s.type
        assert not s.seq_id
        assert s.strand == "+"
        assert not s.gc
        assert not s.aa_seq
        assert not s.frame

    def test_post_init(self):
        s = SeqInterval(
            start=0, end=9, nt_seq=Sequence("ATG"), aa_seq=Polypeptide("M")
        )
        assert s.nt_seq == "ATG"
        assert s.aa_seq == "M"

        with pytest.raises(TypeError):
            SeqInterval()
        with pytest.raises(TypeError):
            SeqInterval(0, 9, nt_seq=[])
        with pytest.raises(TypeError):
            SeqInterval(0, 9, aa_seq=[])
        with pytest.raises(ValueError):
            SeqInterval(0, 9, strand="test")
        with pytest.raises(ValueError):
            SeqInterval(-1, 9)
        with pytest.raises(ValueError):
            SeqInterval(-11, -9)
        with pytest.raises(ValueError):
            SeqInterval(9, 0)
        with pytest.raises(TypeError):
            SeqInterval(0, 9, gc='test')

    def test_length(self):
        s = SeqInterval(123, 9123)
        assert s.length == 9000
        assert len(s) == 9000

    def test_to_sequence(self):
        s = SeqInterval(0, 9, nt_seq="AAAAAAA")
        assert s.to_sequence(strict=True).strict is True
        assert s.to_sequence(rna=True).is_rna is True
        assert s.to_sequence() == Sequence("AAAAAAA")
        with pytest.raises(ValueError):
            SeqInterval(0, 9).to_sequence()

    def test_to_polypeptide(self):
        s = SeqInterval(0, 9, aa_seq="AK")
        assert s.to_polypeptide(strict=True).strict is True
        assert s.to_polypeptide() == Polypeptide("AK")
        with pytest.raises(ValueError):
            SeqInterval(0, 9).to_polypeptide()

    def test_repr(self):
        s = SeqInterval(
            start=0, end=9, nt_seq="ATGAAATAA", type="ORF", seq_id="test",
            strand="-", gc=0.22, aa_seq="MK", frame=-1
        )
        assert repr(s) == (
            "SeqInterval('ATGAAATAA', 0-9(-), length=9, type='ORF', "
            "seq_id='test', aa_seq='MK', frame=-1)"
        )
        s = SeqInterval(
            0, 67,
            nt_seq=(
                "AGCTATGCTGATGCTAGTCTGATGCTGTAGTGCT"
                "AGTCTGTAGCACGATGCGAGTCACGATCTGATG")
        )
        assert repr(s) == (
            "SeqInterval('AGCTATGCTGATG...TCACGATCTGATG', 0-67(+), length=67)"
        )

    def test_str(self):
        s = SeqInterval(0, 9, nt_seq="AAAAAAAAA")
        assert str(s) == "AAAAAAAAA"
        s = SeqInterval(0, 9)
        assert str(s) == ""
