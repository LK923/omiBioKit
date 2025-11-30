import pytest
from omibio.sequence.sequence import Sequence
from omibio.utils.transcribe import transcribe, reverse_transcribe


class TestTranscribe:
    def test_transcribe_str_plus(self):
        assert transcribe("ATGC") == Sequence("AUGC")

    def test_transcribe_str_minus(self):
        assert transcribe("ATGC", strand="-") == Sequence("GCAU")

    def test_transcribe_sequence_input(self):
        seq = Sequence("ATGC")
        assert transcribe(seq) == Sequence("AUGC")

    def test_transcribe_as_str(self):
        assert transcribe("ATGC", as_str=True) == "AUGC"

    def test_transcribe_invalid_type(self):
        with pytest.raises(TypeError):
            transcribe(123)

    def test_reverse_transcribe_str(self):
        assert reverse_transcribe("AUGC") == Sequence("ATGC")

    def test_reverse_transcribe_sequence(self):
        seq = Sequence("AUGC")
        assert reverse_transcribe(seq) == Sequence("ATGC")

    def test_reverse_transcribe_as_str(self):
        assert reverse_transcribe("AUGC", as_str=True) == "ATGC"

    def test_reverse_transcribe_invalid_type(self):
        with pytest.raises(TypeError):
            reverse_transcribe(3.14)

    def test_transcribe_empty(self):
        assert transcribe("") == Sequence("")

    def test_reverse_transcribe_empty(self):
        assert reverse_transcribe("") == Sequence("")
