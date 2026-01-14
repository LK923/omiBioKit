import pytest
from omibio.analysis import at
from omibio.sequence import Sequence


class TestGC:
    def test_sequence_input(self):
        s = Sequence("ATCG")
        assert at(s) == 0.5
        assert at(s, percent=True) == "50.00%"

    def test_str_input(self):
        s = "ATCG"
        assert at(s) == 0.5
        assert at(s, percent=True) == "50.00%"

    def test_empyt_input(self):
        s = Sequence()
        assert at(s) == 0.0
        assert at(s, percent=True) == "0.00%"
        s = ""
        assert at(s) == 0.0
        assert at(s, percent=True) == "0.00%"

    def test_type_error(self):
        with pytest.raises(TypeError):
            at([1, 2])
        with pytest.raises(TypeError):
            at(111)
