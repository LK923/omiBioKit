import pytest
from omibio.bio import KmerResult, AnalysisResult


class TestKmerResult:
    def test_init_empty(self):
        r = KmerResult()
        assert isinstance(r, AnalysisResult)
        assert r.counts == {}
        assert r.k == 0
        assert len(r) == 0

    def test_init_with_counts(self):
        counts = {"AA": 2, "AT": 3}
        r = KmerResult(counts=counts, k=2, seq_id="s1", type="kmer")
        assert r.counts == counts
        assert r.k == 2
        assert r.seq_id == "s1"
        assert r.type == "kmer"
        assert len(r) == 2

    def test_invalid_counts(self):
        with pytest.raises(TypeError):
            KmerResult(counts="not a dict")

    def test_items_keys_values(self):
        counts = {"AA": 2, "AT": 3}
        r = KmerResult(counts=counts)
        assert list(r.items()) == list(counts.items())
        assert list(r.keys()) == list(counts.keys())
        assert list(r.values()) == list(counts.values())

    def test_iter_and_getitem(self):
        counts = {"AA": 2, "AT": 3}
        r = KmerResult(counts=counts)
        collected = list(iter(r))
        assert collected == list(counts.keys())
        assert r["AA"] == 2
        assert r["AT"] == 3

    def test_repr_and_str(self):
        counts = {"AA": 2}
        r = KmerResult(counts=counts, seq_id="id1", type="k")
        rep = repr(r)
        st = str(r)
        assert "KmerResult" in rep
        assert "id1" in rep
        assert "k" in rep
        assert st == str(counts)
