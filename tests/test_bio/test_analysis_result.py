import pytest
from omibio.bio import AnalysisResult


def fake_plot(res, **kwargs):
    res.called = True
    return "ok"


class TestAnalysisResult:
    class DummyResult(AnalysisResult):
        def info(self):
            return "info"

    class PlotResult(AnalysisResult):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.called = False

        def info(self):
            ...

    class badResult(AnalysisResult):
        pass

    def test_init_valid(self):
        r = self.DummyResult(type="type1", seq_id="id1", metadata={"a": 1})
        assert r.type == "type1"
        assert r.seq_id == "id1"
        assert r.metadata == {"a": 1}
        assert r.plot_func is None

    def test_type_invalid(self):
        with pytest.raises(TypeError):
            self.DummyResult(type=123)

    def test_seq_id_invalid(self):
        with pytest.raises(TypeError):
            self.DummyResult(seq_id=123)

    def test_plot_func_invalid(self):
        with pytest.raises(TypeError):
            self.DummyResult(plot_func="not_callable")

    def test_metadata_invalid(self):
        with pytest.raises(TypeError):
            self.DummyResult(metadata="not_dict")

    def test_plot_not_implemented(self):
        r = self.DummyResult()
        with pytest.raises(NotImplementedError):
            r.plot()

    def test_plot_called(self):
        r = self.PlotResult()
        r.plot_func = fake_plot
        res = r.plot()
        assert res == "ok"
        assert r.called is True

    def test_info_abstract(self):
        with pytest.raises(TypeError):
            self.badResult()

    def test_info_method(self):
        r = self.DummyResult()
        assert r.info() == "info"
