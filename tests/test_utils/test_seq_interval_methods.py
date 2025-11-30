import pytest
from omibio.bioObjects.seq_interval import SeqInterval
from omibio.utils.seq_interval_methods import (
    same_seq_as, overlaps, contains, distance_to
)


class TestIntervalUtils:
    def test_same_seq_as_invalid(self):
        assert same_seq_as(1, 2) is False
        a = SeqInterval(start=0, end=1, nt_seq="A", seq_id="A")
        assert same_seq_as(a, 1) is False

    def test_same_seq_as_valid(self):
        a = SeqInterval(start=0, end=5, nt_seq="AAAAA", seq_id="X")
        b = SeqInterval(start=10, end=20, nt_seq="CCCCCCCCCC", seq_id="X")
        c = SeqInterval(start=0, end=5, nt_seq="GGGGG", seq_id="Y")
        assert same_seq_as(a, b) is True
        assert same_seq_as(a, c) is False

    def test_overlaps_diff_seq(self):
        a = SeqInterval(start=0, end=5, nt_seq="AAAAA", seq_id="A")
        b = SeqInterval(start=0, end=5, nt_seq="CCCCC", seq_id="B")
        assert overlaps(a, b) is False

    def test_overlaps_cases(self):
        a = SeqInterval(start=0, end=10, nt_seq="A"*10, seq_id="A")
        b = SeqInterval(start=5, end=15, nt_seq="C"*10, seq_id="A")
        c = SeqInterval(start=10, end=20, nt_seq="G"*10, seq_id="A")
        assert overlaps(a, b) is True
        assert overlaps(a, c) is False

    def test_contains_position(self):
        a = SeqInterval(start=5, end=10, nt_seq="A"*5, seq_id="A")
        assert contains(a, 5) is True
        assert contains(a, 9) is True
        assert contains(a, 10) is False
        assert contains(a, 4) is False

    def test_contains_interval(self):
        a = SeqInterval(start=5, end=15, nt_seq="A"*10, seq_id="A")
        b = SeqInterval(start=6, end=10, nt_seq="C"*4, seq_id="A")
        c = SeqInterval(start=4, end=10, nt_seq="G"*6, seq_id="A")
        d = SeqInterval(start=6, end=10, nt_seq="T"*4, seq_id="B")
        assert contains(a, b) is True
        assert contains(a, c) is False
        assert contains(a, d) is False

    def test_contains_invalid(self):
        a = SeqInterval(start=0, end=1, nt_seq="A", seq_id="A")
        assert contains(a, "x") is False

    def test_distance_invalid_type(self):
        a = SeqInterval(start=0, end=10, nt_seq="A"*10, seq_id="A")
        with pytest.raises(TypeError):
            distance_to(a, 123)

    def test_distance_diff_seq(self):
        a = SeqInterval(start=0, end=10, nt_seq="A"*10, seq_id="A")
        b = SeqInterval(start=20, end=30, nt_seq="C"*10, seq_id="B")
        with pytest.raises(ValueError):
            distance_to(a, b)

    def test_distance_overlapping(self):
        a = SeqInterval(start=0, end=10, nt_seq="A"*10, seq_id="A")
        b = SeqInterval(start=5, end=20, nt_seq="C"*15, seq_id="A")
        assert distance_to(a, b) == 0

    def test_distance_a_before_b(self):
        a = SeqInterval(start=0, end=5, nt_seq="A"*5, seq_id="A")
        b = SeqInterval(start=10, end=20, nt_seq="C"*10, seq_id="A")
        assert distance_to(a, b) == 5

    def test_distance_b_before_a(self):
        a = SeqInterval(start=10, end=20, nt_seq="A"*10, seq_id="A")
        b = SeqInterval(start=0, end=5, nt_seq="C"*5, seq_id="A")
        assert distance_to(a, b) == 5
