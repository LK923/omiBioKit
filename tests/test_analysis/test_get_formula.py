import pytest
from omibio.analysis import get_formula
from omibio.sequence import Polypeptide


class TestGetFormula:
    def test_polypeptide_input(self):
        pep = Polypeptide("ACD")
        formula = get_formula(pep)
        assert isinstance(formula, str)
        assert len(formula) > 0

    def test_string_input(self):
        formula = get_formula("ACD")
        assert isinstance(formula, str)
        assert len(formula) > 0

    def test_empty_string(self):
        formula = get_formula("")
        assert isinstance(formula, str)
        assert "H" in formula or formula == ""

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError):
            get_formula(123)
        with pytest.raises(TypeError):
            get_formula(None)
        with pytest.raises(TypeError):
            get_formula([])
