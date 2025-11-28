import pytest
from omibio.analysis import gc
from omibio.sequence import Sequence

# pytest --cov=omibio.analysis.gc_content tests/ --cov-report=term-missing


class TestGC:
    def test_sequence_input(self):
        s = Sequence("AACAA")
        assert gc(s) == 0.2
        assert gc(s, percent=True) == "20.00%"

    def test_str_input(self):
        s = "AACAA"
        assert gc(s) == 0.2
        assert gc(s, percent=True) == "20.00%"

    def test_empyt_input(self):
        s = Sequence()
        assert gc(s) == 0.0
        assert gc(s, percent=True) == "0.00%"
        s = ""
        assert gc(s) == 0.0
        assert gc(s, percent=True) == "0.00%"

    def test_type_error(self):
        with pytest.raises(TypeError):
            gc([1, 2])
        with pytest.raises(TypeError):
            gc(111)
