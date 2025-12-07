import pytest
from omibio.bio import AnalysisResult, SeqInterval


class TestAnalysisResult:
    def test_init_valid(self):
        ivs = [SeqInterval(0, 10, "ATGC")]
        ar = AnalysisResult(intervals=ivs, seq_id="seq1", type="test")
        assert ar.intervals == ivs
        assert ar.seq_id == "seq1"
        assert ar.type == "test"
        assert ar.metadata == {}
        assert len(ar) == 1
        for i, iv in enumerate(ar):
            assert iv == ivs[i]
        assert ar[0] == ivs[0]
        assert ar[0:1] == ivs[0:1]

    def test_init_invalid_intervals(self):
        with pytest.raises(TypeError):
            AnalysisResult(intervals="not a list")

    def test_init_invalid_plot_func(self):
        ivs = [SeqInterval(0, 5, "A")]
        with pytest.raises(TypeError):
            AnalysisResult(intervals=ivs, plot_func="not callable")

    def test_init_invalid_metadata(self):
        ivs = [SeqInterval(0, 5, "A")]
        with pytest.raises(TypeError):
            AnalysisResult(intervals=ivs, metadata="not a dict")

    def test_plot_not_implemented(self):
        ivs = [SeqInterval(0, 5, "A")]
        ar = AnalysisResult(intervals=ivs)
        with pytest.raises(NotImplementedError):
            ar.plot()

    def test_plot_callable_called(self):
        ivs = [SeqInterval(0, 5, "A")]

        def fake_plot(ar_instance, **kwargs):
            return "called"

        ar = AnalysisResult(intervals=ivs, plot_func=fake_plot)
        result = ar.plot(option=True)
        assert result == "called"

    def test_repr_and_str(self):
        ivs = [SeqInterval(0, 5, "A")]
        ar = AnalysisResult(intervals=ivs, seq_id="s", type="t")
        r = repr(ar)
        s = str(ar)
        assert "AnalysisResult" in r
        assert s == str(ivs)

    def test_empty_intervals(self):
        ar = AnalysisResult(intervals=[])
        assert len(ar) == 0
        assert list(ar) == []
        assert ar.intervals == []
