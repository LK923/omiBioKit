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
        r = KmerResult(counts=counts, k=2)
        assert list(r.items()) == list(counts.items())
        assert list(r.keys()) == list(counts.keys())
        assert list(r.values()) == list(counts.values())

    def test_iter_and_getitem(self):
        counts = {"AA": 2, "AT": 3}
        r = KmerResult(counts=counts, k=2)
        collected = list(iter(r))
        assert collected == list(counts.keys())
        assert r["AA"] == 2
        assert r["AT"] == 3

    def test_repr_and_str(self):
        counts = {"AA": 2}
        r = KmerResult(counts=counts, seq_id="id1", type="k", k=2)
        rep = repr(r)
        st = str(r)
        assert "KmerResult" in rep
        assert "id1" in rep
        assert "k" in rep
        assert st == str(counts)

    def test_kmer_does_not_match_k(self):
        counts = {"AA": 2, "ATA": 3}
        with pytest.raises(TypeError):
            KmerResult(counts=counts, k=2)

    def test_to_csv(self, tmp_path):
        counts = {"AA": 2, "AT": 3}
        r = KmerResult(counts=counts, k=2, seq_id="s1")
        csv_path = tmp_path / "kmer_counts.csv"
        r.to_csv(csv_path)

        with open(csv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert lines[0].strip() == "seq_id\tk\tkmer\tcount"
        expected_lines = {"s1\t2\tAA\t2", "s1\t2\tAT\t3"}
        actual_lines = {line.strip() for line in lines[1:]}
        assert actual_lines == expected_lines

    def test_info_prints_expected(self, capsys):
        obj = KmerResult(
            counts={"AA": 5, "AC": 3, "AG": 2},
            k=2,
            seq_id="test",
            type="kmer",
            metadata={"example_key": "example_value"}
        )

        obj.info()

        captured = capsys.readouterr()
        out = captured.out

        assert "kmers" in out
        assert f"k={obj.k}" in out
        assert "Available metadata" in out
