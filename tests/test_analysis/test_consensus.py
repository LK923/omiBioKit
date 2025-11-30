import pytest
from omibio.analysis.consensus import find_consensus
from omibio.sequence import Sequence

# pytest --cov=omibio.analysis.consensus tests/ --cov-report=term-missing


class TestConsensus:

    def test_empty_list(self):
        assert find_consensus([]) == ""

    def test_non_list_input(self):
        with pytest.raises(TypeError):
            find_consensus("ACGT")

    def test_unequal_length(self):
        with pytest.raises(ValueError):
            find_consensus(["ACG", "ACGT"])

    def test_basic_consensus_str(self):
        r = find_consensus(["ACGT", "ACGT"], as_str=True)
        assert r == "ACGT"

    def test_basic_consensus_sequence(self):
        r = find_consensus(["ACGT", "ACGT"], as_str=False)
        assert isinstance(r, Sequence)
        assert str(r) == "ACGT"

    def test_consensus_with_rna_input(self):
        r = find_consensus(["ACGU", "ACGU"], as_str=True)
        assert r == "ACGT"

    def test_consensus_as_rna(self):
        r = find_consensus(["ACGT", "ACGT"], as_rna=True)
        assert str(r) == "ACGU"

    def test_gap_handling(self):
        r = find_consensus(["A-GT", "A?GT"], as_str=True)
        assert r == "ANGT"

    def test_all_gap_column(self):
        r = find_consensus(["-.-", "?.."], as_str=True)
        assert r == "NNN"

    def test_iupac_ambiguity(self):
        r = find_consensus(["A", "G"], as_str=True)
        assert r == "R"

    def test_iupac_three_way(self):
        r = find_consensus(["A", "C", "T"], as_str=True)
        assert r == "H"

    def test_iupac_unknown_combo(self):
        r = find_consensus(["A", "C", "G", "T"], as_str=True)
        assert r == "N"

    def test_mixed_types_sequence_objects(self):
        r = find_consensus([Sequence("ACGT"), "ACGT"], as_str=True)
        assert r == "ACGT"

    def test_ignore_gaps_correctly(self):
        r = find_consensus(["A---", "A..A"], as_str=True)
        assert r == "ANNA"

    def test_multiple_max_scores(self):
        r = find_consensus(["A", "G", "A", "G"], as_str=True)
        assert r == "R"
