from omibio.utils import check_if_exsit


class TestCheckIfExsit:
    def test_with_string(self):
        result = check_if_exsit("hello")
        assert result == "hello"

    def test_with_empty_string(self):
        result = check_if_exsit("")
        assert result == "N/A"

    def test_with_none(self):
        result = check_if_exsit(None)
        assert result == "N/A"

    def test_with_custom_default(self):
        result = check_if_exsit(None, default="default_value")
        assert result == "default_value"
