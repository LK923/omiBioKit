import pytest
from omibio.sequence.seq_utils.complement import complement, reverse_complement
from omibio.sequence.sequence import Sequence


class TestComplementOps:

    def test_complement_str(self):
        seq = "ATGC"
        comp = complement(seq, as_str=True)
        assert comp == "TACG"

    def test_complement_sequence_obj(self):
        seq = Sequence("ATGC")
        comp = complement(seq)
        assert isinstance(comp, Sequence)
        assert str(comp) == "TACG"

    def test_reverse_complement_str(self):
        seq = "ATGC"
        rc = reverse_complement(seq, as_str=True)
        assert rc == "GCAT"

    def test_reverse_complement_sequence_obj(self):
        seq = Sequence("ATGC")
        rc = reverse_complement(seq)
        assert isinstance(rc, Sequence)
        assert str(rc) == "GCAT"

    def test_empty_sequence(self):
        seq = ""
        comp = complement(seq, as_str=True)
        rc = reverse_complement(seq, as_str=True)
        assert comp == ""
        assert rc == ""

    def test_invalid_type_complement(self):
        with pytest.raises(TypeError):
            complement(123)

    def test_invalid_type_reverse_complement(self):
        with pytest.raises(TypeError):
            reverse_complement(123)

    def test_lowercase_input(self):
        seq = "atgc"
        comp = complement(seq, as_str=True)
        rc = reverse_complement(seq, as_str=True)
        assert comp == "TACG"
        assert rc == "GCAT"

    def test_mixed_case_input(self):
        seq = "aTgC"
        comp = complement(seq, as_str=True)
        rc = reverse_complement(seq, as_str=True)
        assert comp == "TACG"
        assert rc == "GCAT"
