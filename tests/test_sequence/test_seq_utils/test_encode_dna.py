import pytest
from omibio.sequence import Sequence, encode_dna, decode_dna
from omibio.bio import SeqEntry, SeqInterval


class TestEncodeDNA:
    def test_general_encoding(self):
        seq_str = "ACGTNRYSWKMBDHV-"
        seq = Sequence(seq_str)
        entry = SeqEntry(seq=seq, seq_id='test')
        itv = SeqInterval(0, 16, nt_seq=seq_str)
        expect_result = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        assert list(encode_dna(seq_str)) == expect_result
        assert list(encode_dna(seq)) == expect_result
        assert list(encode_dna(entry)) == expect_result
        assert list(encode_dna(itv)) == expect_result

    def test_general_decoding(self):
        seq_str = "ACGTNRYSWKMBDHV-"
        encoded = encode_dna(seq_str)
        assert decode_dna(encoded) == "ACGTNRYSWKMBDHV-"

    def test_type_checking(self):
        with pytest.raises(TypeError):
            encode_dna(123)
        with pytest.raises(TypeError):
            decode_dna(123)
