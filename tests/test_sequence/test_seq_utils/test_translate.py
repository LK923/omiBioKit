import pytest
from omibio.sequence.polypeptide import Polypeptide
from omibio.bio.seq_interval import SeqInterval
from omibio.sequence.seq_utils.translate import translate_nt


class TestTranslateNT:
    def test_invalid_type(self):
        with pytest.raises(TypeError):
            translate_nt(123)

    def test_none_or_short(self):
        assert translate_nt("") == ""
        assert translate_nt("AT") == ""

    def test_invalid_frame(self):
        with pytest.raises(ValueError):
            translate_nt("ATG", frame=3)

    def test_basic_translation(self):
        assert translate_nt("ATGAAA") == Polypeptide("MK")

    def test_as_str(self):
        assert translate_nt("ATGAAA", as_str=True) == "MK"

    def test_stop_symbol(self):
        assert translate_nt("ATGTAA", stop_symbol=True, as_str=True) == "M*"

    def test_no_stop_symbol(self):
        assert translate_nt("ATGTAA", stop_symbol=False, as_str=True) == "M"

    def test_to_stop(self):
        assert translate_nt("ATGAAATAA", to_stop=True, as_str=True) == "MK"

    def test_frame_shift(self):
        assert translate_nt("AATGAAA", frame=1, as_str=True) == "MK"

    def test_require_start_success(self):
        assert translate_nt(
            "CCCATGAAA", require_start=True, as_str=True
        ) == "MK"

    def test_require_start_fail(self):
        assert translate_nt("CCCAAA", require_start=True, as_str=True) == ""

    def test_seqinterval_input(self):
        s = SeqInterval(start=0, end=6, nt_seq="ATGAAA")
        assert translate_nt(s, as_str=True) == "MK"

    def test_ambiguous_codon(self):
        assert translate_nt("ATGNNN", as_str=True) == "MX"

    def test_rna_input(self):
        assert translate_nt("AUGAAA", as_str=True) == "MK"
