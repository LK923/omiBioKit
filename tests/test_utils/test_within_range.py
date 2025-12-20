from omibio.utils import within_range


class TestWithinRange:
    def test_basic(self):
        assert within_range(15, 10, 20) is True
        assert within_range(20, 10, 20) is True
        assert within_range(10, 10, 20) is True
        assert within_range(5, 10, 20) is False
        assert within_range(25, 10, 20) is False
        assert within_range(15, min=10) is True
        assert within_range(15, max=20) is True

    def test_none_input(self):
        assert within_range(None, 0, 10) is False
