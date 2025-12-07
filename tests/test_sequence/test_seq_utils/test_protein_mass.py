import pytest
from omibio.sequence.polypeptide import Polypeptide
from omibio.analysis.protein_mass import calc_mass


class TestCalcMass:

    def test_calc_mass_with_string(self):
        expected = (
            Polypeptide.AA_MASS["A"]
            + Polypeptide.AA_MASS["C"]
            + Polypeptide.AA_MASS["D"]
            + 18.01528
        )
        assert calc_mass("ACD", accuracy=3) == round(expected, 3)

    def test_calc_mass_with_polypeptide_object(self):
        seq = Polypeptide("WY")
        expected = (
            Polypeptide.AA_MASS["W"]
            + Polypeptide.AA_MASS["Y"]
            + 18.01528
        )
        assert calc_mass(seq, accuracy=2) == round(expected, 2)

    def test_empty_sequence(self):
        assert calc_mass("", accuracy=3) == 0.0

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError):
            calc_mass(123)

    def test_accuracy_parameter(self):
        seq = "AC"
        low_prec = calc_mass(seq, accuracy=1)
        high_prec = calc_mass(seq, accuracy=5)
        assert round(low_prec, 1) == low_prec
        assert round(high_prec, 5) == high_prec
        assert low_prec != high_prec
