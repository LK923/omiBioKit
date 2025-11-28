import pytest
from omibio.sequence import Polypeptide

# pytest --cov=omibio.sequence.polypeptide tests/ --cov-report=term-missing


class TestPolypeptide:

    def test_init_and_strict_flag(self):
        p = Polypeptide("ACD", strict=True)
        assert p.strict is True
        assert str(p) == "ACD"
        with pytest.raises(TypeError):
            Polypeptide("ACX", strict="yes")

    def test_invalid_strict_raises(self):
        with pytest.raises(ValueError):
            Polypeptide("ACX", strict=True)

    def test_init_none_seq(self):
        p = Polypeptide(None)
        assert p.aa_seq == ""

    def test_setter_invalid_type(self):
        p = Polypeptide()
        with pytest.raises(TypeError):
            p.aa_seq = 123

    def test_copy_modes(self):
        p = Polypeptide("ACD", strict=False)
        q = p.copy(strict=True)
        assert q.strict is True
        assert q.aa_seq == "ACD"

    def test_to_strict(self):
        p = Polypeptide("ACD")
        q = p.to_strict()
        assert q.strict is True
        assert q.aa_seq == "ACD"

    def test_mass_empty(self):
        assert Polypeptide("").mass() == 0.0

    def test_mass_non_empty(self):
        p = Polypeptide("ACD")
        assert p.mass() > 0

    def test_composition(self):
        p = Polypeptide("AACC")
        assert p.composition() == {"A": 2, "C": 2}

    def test_count(self):
        p = Polypeptide("AACC")
        assert p.count("A") == 2

    def test_subseq_normal(self):
        p = Polypeptide("ACDEFG")
        q = p.subseq(1, 4)
        assert str(q) == "CDE"

    def test_formula_empty(self):
        assert Polypeptide("").formula() == ""

    def test_formula_valid(self):
        p = Polypeptide("ACD")
        f = p.formula()
        assert isinstance(f, str)
        assert "C" in f

    def test_formula_invalid_aa(self):
        p = Polypeptide("ACX")
        with pytest.raises(ValueError):
            p.formula()

    def test_is_valid(self):
        assert Polypeptide("ACD").is_valid() is True
        assert Polypeptide("ACX").is_valid() is False

    def test_len(self):
        assert len(Polypeptide("ACD")) == 3

    def test_repr(self):
        r = repr(Polypeptide("ACD"))
        assert "Polypeptide(" in r

    def test_getitem(self):
        p = Polypeptide("ACD")
        assert p[1] == "C"

    def test_setitem_valid(self):
        p = Polypeptide("ACD")
        p[1] = "F"
        assert p.aa_seq == "AFD"

    def test_setitem_invalid_strict(self):
        p = Polypeptide("ACD", strict=True)
        with pytest.raises(ValueError):
            p[1] = "X"

    def test_contains(self):
        p = Polypeptide("ACD")
        assert "A" in p
        assert "Z" not in p

    def test_eq_polypeptide(self):
        assert Polypeptide("ACD") == Polypeptide("ACD")

    def test_eq_string(self):
        assert Polypeptide("ACD") == "ACD"
        assert Polypeptide("ACD") != "XYZ"

    def test_eq_other_types(self):
        assert not Polypeptide("A") == ["A"]

    def test_add_polypeptide(self):
        p = Polypeptide("AC")
        q = Polypeptide("DE")
        r = p + q
        assert r.aa_seq == "ACDE"

    def test_add_string(self):
        p = Polypeptide("AC")
        r = p + "DE"
        assert r.aa_seq == "ACDE"

    def test_add_invalid(self):
        p = Polypeptide("AC")
        with pytest.raises(TypeError):
            p + 123

    def test_mul_positive(self):
        p = Polypeptide("AC")
        r = p * 3
        assert r.aa_seq == "ACACAC"

    def test_mul_invalid_type(self):
        p = Polypeptide("AC")
        with pytest.raises(TypeError):
            p * 2.5

    def test_mul_negative(self):
        p = Polypeptide("AC")
        with pytest.raises(ValueError):
            p * -1
