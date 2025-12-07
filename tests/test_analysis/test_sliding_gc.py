import pytest
from omibio.analysis.sliding_gc import sliding_gc
from omibio.bio import SeqInterval
from omibio.sequence.sequence import Sequence

# pytest --cov=omibio.analysis.sliding_gc tests/ --cov-report=term-missing


class TestSlidingGC:
    def test_empty_seq(self):
        assert sliding_gc("").intervals == []

    def test_invalid_seq_type(self):
        with pytest.raises(TypeError):
            sliding_gc(123)

    def test_invalid_window_step(self):
        with pytest.raises(ValueError):
            sliding_gc("ATGC", window=0)
        with pytest.raises(ValueError):
            sliding_gc("ATGC", step=0)

    def test_window_larger_than_seq(self):
        r = sliding_gc("ATGC", window=10)
        assert len(r) == 1
        assert isinstance(r[0], SeqInterval)
        assert r[0].start == 0
        assert r[0].end == 4
        assert r[0].gc == 50.0

    def test_string_input_basic(self):
        r = sliding_gc("ATGCATGC", window=4, step=2)
        assert len(r) == 3
        assert [x.gc for x in r] == [50.0, 50.0, 50.0]

    def test_sequence_object_input(self):
        obj = Sequence("GGCCAA")
        r = sliding_gc(obj, window=3, step=3)
        assert len(r) == 2
        assert r[0].gc == 100.0
        assert r[1].gc == pytest.approx(33.33, rel=1e-2)

    def test_step_larger_than_window(self):
        r = sliding_gc("GGCCAATT", window=3, step=5)
        assert len(r) == 2
        assert r[0].gc == 100.0
        assert r[1].gc == 0.0

    def test_exact_window_match(self):
        r = sliding_gc("GCGC", window=4, step=1)
        assert len(r) == 1
        assert r[0].gc == 100.0

    def test_non_overlapping_windows(self):
        r = sliding_gc("GCGCGAAA", window=2, step=2)
        assert len(r) == 4
        assert r[0].gc == 100.0
        assert r[1].gc == 100.0
        assert r[2].gc == 50.0
        assert r[3].gc == 0.0

    def test_with_seq_id(self):
        r = sliding_gc("ATGCATGC", window=4, step=4, seq_id="chr1")
        assert all(x.seq_id == "chr1" for x in r)
