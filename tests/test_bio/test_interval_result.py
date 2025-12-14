import pytest
from omibio.bio import IntervalResult, AnalysisResult
from omibio.bio.seq_interval import SeqInterval


class TestIntervalResult:
    def make_interval(self, start=0, end=2, nt_seq="AT"):
        return SeqInterval(start=start, end=end, nt_seq=nt_seq)

    def test_init_empty(self):
        r = IntervalResult()
        assert isinstance(r, AnalysisResult)
        assert r.intervals == []
        assert len(r) == 0

    def test_init_with_intervals(self):
        intervals = [self.make_interval(), self.make_interval(3, 5, "GC")]
        r = IntervalResult(intervals=intervals, seq_id="s1", type="test")
        assert r.intervals == intervals
        assert r.seq_id == "s1"
        assert r.type == "test"
        assert len(r) == 2

    def test_invalid_intervals(self):
        with pytest.raises(TypeError):
            IntervalResult(intervals="not a list")

    def test_iter_and_getitem(self):
        intervals = [self.make_interval(), self.make_interval(3, 5, "GC")]
        r = IntervalResult(intervals=intervals)
        collected = list(r)
        assert collected == intervals
        assert r[0] == intervals[0]
        assert r[0:2] == intervals

    def test_repr_and_str(self):
        intervals = [self.make_interval()]
        r = IntervalResult(intervals=intervals, seq_id="id1", type="type1")
        rep = repr(r)
        st = str(r)
        assert "IntervalResult" in rep
        assert "id1" in rep
        assert "type1" in rep
        assert st == str(intervals)
