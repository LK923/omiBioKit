from omibio.utils.truncate_repr import truncate_repr


class TestTruncateRepr:
    def test_none_input(self):
        assert truncate_repr(None) is None

    def test_empty_string(self):
        assert truncate_repr("") is None

    def test_short_string(self):
        s = "ACGT"
        assert truncate_repr(s) == repr(s)

    def test_exact_max_length(self):
        s = "A" * 30
        assert truncate_repr(s) == repr(s)

    def test_long_string_default_max(self):
        s = "A" * 40
        result = truncate_repr(s)
        assert result.startswith("'AAAAAAAAAAAA")
        assert result.endswith("AAAAAAAAAAAA'")

    def test_long_string_custom_max(self):
        s = "ACGT" * 20
        result = truncate_repr(s, max_length=20)
        assert result.startswith("'ACGTACG")
        assert result.endswith("ACGTACGT'")

    def test_unicode_string(self):
        s = "😊" * 50
        result = truncate_repr(s, max_length=10)
        assert result.startswith("'😊😊")
        assert result.endswith("😊😊'")

    def test_max_length_less_than_three(self):
        s = "ABCDEFG"
        result = truncate_repr(s, max_length=2)
        assert result == repr("ABCDEFG")
