import pytest
from omibio.sequence.sequence import Sequence
from omibio.sequence.seq_utils.complement import reverse_complement
from omibio.analysis import kmer


class TestKmer:
    def test_basic_string(self):
        seq = "ACTACTACT"
        result = kmer(seq, 3, canonical=False)
        expected = {"ACT": 3, "CTA": 2, "TAC": 2}
        assert result.counts == expected

    def test_basic_sequence_obj(self):
        seq = Sequence("ACTACTACT")
        result = kmer(seq, 3, canonical=False)
        expected = {"ACT": 3, "CTA": 2, "TAC": 2}
        assert result.counts == expected

    def test_min_count_filter(self):
        seq = "ACTACTACT"
        result = kmer(seq, 3, canonical=False, min_count=3)
        expected = {"ACT": 3}
        assert result.counts == expected

    def test_canonical(self):
        seq = "ACTGAC"
        result = kmer(seq, 3, canonical=True)
        for k in result.keys():
            rc = reverse_complement(k, as_str=True)
            assert k <= rc

    def test_k_larger_than_seq(self):
        seq = "ACG"
        result = kmer(seq, 5)
        assert result.counts == {}

    def test_invalid_type_seq(self):
        with pytest.raises(TypeError):
            kmer(123, 3)

    def test_invalid_type_k(self):
        with pytest.raises(TypeError):
            kmer("ACTG", "3")

    def test_invalid_type_min_count(self):
        with pytest.raises(TypeError):
            kmer("ACTG", 3, min_count="2")

    def test_invalid_k_value(self):
        with pytest.raises(ValueError):
            kmer("ACTG", 0)

    def test_invalid_min_count_value(self):
        with pytest.raises(ValueError):
            kmer("ACTG", 3, min_count=-1)

    def test_cache(self):
        seq = "ACGTAC"
        result = kmer(seq, 2, canonical=True)
        assert "AC" in result
