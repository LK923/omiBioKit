from omibio.utils import ensure_iterable
from pathlib import Path
from omibio.bio import KmerResult, IntervalResult, SeqInterval


class TestEnsureIterable:
    def test_basic(self):
        assert ensure_iterable("test") == ["test"]
        assert ensure_iterable(b"test") == [b"test"]
        assert ensure_iterable(Path("test")) == [Path("test")]
        assert ensure_iterable({"test": 0}) == [{"test": 0}]

    def test_none_input(self):
        assert ensure_iterable(None) == []

    def test_iterable(self):
        assert ensure_iterable({"A", "B"}) == {"A", "B"}
        assert ensure_iterable(["A", "B"]) == ["A", "B"]
        assert ensure_iterable(("A", "B")) == ("A", "B")

    def test_omibio_objects(self):
        assert ensure_iterable(KmerResult(k=1, counts={"A": 1})) == [KmerResult(k=1, counts={"A": 1})]  # noqa
        assert ensure_iterable(IntervalResult(SeqInterval(1, 2))) == [IntervalResult(SeqInterval(1, 2))]  # noqa