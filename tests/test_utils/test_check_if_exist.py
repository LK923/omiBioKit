from omibio.utils import check_if_exist


class TestCheckIfexist:
    def test_with_string(self):
        result = check_if_exist("hello")
        assert result == "hello"

    def test_with_empty_string(self):
        result = check_if_exist("")
        assert result == "N/A"

    def test_with_none(self):
        result = check_if_exist(None)
        assert result == "N/A"

    def test_with_custom_default(self):
        result = check_if_exist(None, default="default_value")
        assert result == "default_value"
