import pytest
from unittest.mock import MagicMock
from matplotlib.axes import Axes
from omibio.bio import AnalysisResult, SeqInterval


class TestAnalysisResult:
    def make_interval(self, nt_seq="ATGC"):
        return SeqInterval(start=1, end=4, nt_seq=nt_seq)

    def test_init_valid(self):
        itv = self.make_interval()
        ar = AnalysisResult(intervals=[itv], seq_id="s1", type="test")
        assert ar.intervals == [itv]
        assert ar.seq_id == "s1"
        assert ar.type == "test"
        assert isinstance(ar.metadata, dict)

    def test_init_intervals_not_list(self):
        itv = self.make_interval()
        with pytest.raises(TypeError):
            AnalysisResult(intervals=itv)

    def test_init_plot_func_not_callable(self):
        itv = self.make_interval()
        with pytest.raises(TypeError):
            AnalysisResult(intervals=[itv], plot_func=123)

    def test_init_metadata_not_dict(self):
        itv = self.make_interval()
        with pytest.raises(TypeError):
            AnalysisResult(intervals=[itv], metadata=[])

    def test_len(self):
        ar = AnalysisResult(
            intervals=[self.make_interval(), self.make_interval()]
        )
        assert len(ar) == 2

    def test_iter(self):
        itvs = [self.make_interval(), self.make_interval()]
        ar = AnalysisResult(intervals=itvs)
        assert list(iter(ar)) == itvs

    def test_getitem_int(self):
        itvs = [self.make_interval(), self.make_interval("GG")]
        ar = AnalysisResult(intervals=itvs)
        assert ar[1].nt_seq == "GG"

    def test_getitem_slice(self):
        itvs = [
            self.make_interval("A"),
            self.make_interval("B"),
            self.make_interval("C"),
        ]
        ar = AnalysisResult(intervals=itvs)
        res = ar[1:]
        assert isinstance(res, list)
        assert [i.nt_seq for i in res] == ["B", "C"]

    def test_plot_not_supported(self):
        ar = AnalysisResult(intervals=[self.make_interval()])
        with pytest.raises(NotImplementedError):
            ar.plot()

    def test_plot_supported(self):
        called = {}
        fake_ax = MagicMock(spec=Axes)

        def fake_plot(res, **kwargs) -> Axes:
            called["ok"] = True
            return fake_ax

        ar = AnalysisResult(
            intervals=[self.make_interval()],
            plot_func=fake_plot,
        )
        ax = ar.plot()
        assert ax is fake_ax
        assert called["ok"] is True

    def test_to_dict_basic(self):
        itvs = [
            self.make_interval("AAA"),
            self.make_interval("TTT"),
        ]
        ar = AnalysisResult(intervals=itvs)
        d = ar.to_dict(key_name="X")
        assert d == {"X_1": "AAA", "X_2": "TTT"}

    def test_to_dict_skip_empty_nt_seq(self):
        itvs = [
            self.make_interval(None),
            self.make_interval("GG"),
        ]
        ar = AnalysisResult(intervals=itvs)
        d = ar.to_dict()
        assert list(d.values()) == ["GG"]

    def test_to_dict_prefix_not_str(self):
        ar = AnalysisResult(intervals=[self.make_interval()])
        with pytest.raises(TypeError):
            ar.to_dict(prefix=1)

    def test_repr(self):
        ar = AnalysisResult(
            intervals=[self.make_interval("AA")],
            seq_id="id1",
            type="t",
        )
        r = repr(ar)
        assert "AnalysisResult" in r
        assert "id1" in r
        assert "t" in r

    def test_str(self):
        itvs = [self.make_interval("AA")]
        ar = AnalysisResult(intervals=itvs)
        assert str(ar) == str(itvs)
