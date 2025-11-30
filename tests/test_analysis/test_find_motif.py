import pytest
from omibio.sequence.sequence import Sequence
from omibio.bioObjects.seq_interval import SeqInterval
from omibio.analysis.find_motif import find_motif
import re

# pytest --cov=omibio.analysis.find_motif tests/ --cov-report=term-missing


class TestFindMotif:

    def test_invalid_seq_type(self):
        with pytest.raises(TypeError):
            find_motif(123, "A")

    def test_invalid_pattern_type(self):
        with pytest.raises(TypeError):
            find_motif("ACGT", 123)

    def test_empty_pattern(self):
        with pytest.raises(ValueError):
            find_motif("ACGT", "")

    def test_simple_match(self):
        res = find_motif("ACGTACGT", "A")
        assert len(res) == 2
        assert isinstance(res[0], SeqInterval)
        assert str(res[0].nt_seq) == "A"

    def test_case_insensitive(self):
        res = find_motif("AaAa", "a", ignore_case=True)
        assert len(res) == 4

    def test_case_sensitive(self):
        res = find_motif("AaAa", "a", ignore_case=False)
        assert len(res) == 2

    def test_pattern_regex(self):
        pat = re.compile("A.C")
        res = find_motif("A1C A2C A3C", pat)
        assert len(res) == 3

    def test_pattern_regex_force_case(self):
        pat = re.compile("a")
        res = find_motif("AaAa", pat, ignore_case=False)
        assert len(res) == 2

    def test_seq_object(self):
        seq = Sequence("ACGTAC")
        res = find_motif(seq, "CG")
        assert len(res) == 1
        assert res[0].start == 1
        assert res[0].end == 3

    def test_with_seq_id(self):
        res = find_motif("ACGTAC", "AC", seq_id="seq1")
        assert all(r.seq_id == "seq1" for r in res)

    def test_multiple_char_pattern(self):
        res = find_motif("TTTGGGTTTGGG", "GGG")
        assert len(res) == 2

    def test_no_match(self):
        res = find_motif("ACGTACGT", "ZZZ")
        assert res == []

    def test_overlap_not_captured(self):
        res = find_motif("AAAAA", "AA")
        assert len(res) == 2  # regex default non-overlapping

    def test_nt_seq_correct_slice(self):
        res = find_motif("ACGTACGT", "CG")
        assert [str(r.nt_seq) for r in res] == ["CG", "CG"]

    def test_regex_ignore_case_added(self):
        pat = re.compile("a")
        res = find_motif("A", pat, ignore_case=True)
        assert len(res) == 1

    def test_regex_ignore_case_removed(self):
        pat = re.compile("a", re.IGNORECASE)
        res = find_motif("A", pat, ignore_case=False)
        assert len(res) == 0
