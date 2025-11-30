import pytest
from omibio.utils.shuffle_seq import shuffle_seq
from omibio.sequence.sequence import Sequence


class TestShuffleSeq:

    def test_shuffle_string_basic(self):
        seq = "ATCG"
        result = shuffle_seq(seq, seed=42, as_str=True)
        assert isinstance(result, str)
        assert len(result) == 4
        assert sorted(result) == sorted(seq)

    def test_shuffle_sequence_basic(self):
        seq = Sequence("ATCG")
        result = shuffle_seq(seq, seed=42, as_str=False)
        assert isinstance(result, Sequence)
        assert len(result) == 4
        assert sorted(str(result)) == sorted("ATCG")

    def test_shuffle_empty_string(self):
        result = shuffle_seq("", seed=1, as_str=True)
        assert result == ""

    def test_shuffle_single_char(self):
        result = shuffle_seq("A", seed=1, as_str=True)
        assert result == "A"

    def test_shuffle_with_seed_reproducibility(self):
        seq = "ACGTACGT"
        result1 = shuffle_seq(seq, seed=123, as_str=True)
        result2 = shuffle_seq(seq, seed=123, as_str=True)
        assert result1 == result2

    def test_shuffle_without_seed_variability(self):
        seq = "ACGT" * 10
        results = {shuffle_seq(seq, as_str=True) for _ in range(5)}
        assert len(results) > 1

    def test_as_str_true_returns_str(self):
        result = shuffle_seq("ATCG", as_str=True)
        assert isinstance(result, str)

    def test_as_str_false_returns_sequence(self):
        result = shuffle_seq("ATCG", as_str=False)
        assert isinstance(result, Sequence)

    def test_input_sequence_object_returns_correct_type(self):
        seq_obj = Sequence("GCTA")
        result = shuffle_seq(seq_obj, as_str=False)
        assert isinstance(result, Sequence)
        assert sorted(str(result)) == sorted("GCTA")

    def test_input_string_with_as_str_false_returns_sequence(self):
        result = shuffle_seq("TTAA", as_str=False)
        assert isinstance(result, Sequence)
        assert sorted(str(result)) == sorted("TTAA")

    def test_shuffle_preserves_character_counts(self):
        original = "AAATTTCCCGGG"
        shuffled = shuffle_seq(original, seed=999, as_str=True)
        assert sorted(original) == sorted(shuffled)

    def test_invalid_input_type_raises_typeerror_int(self):
        with pytest.raises(TypeError, match="must be Sequence or str"):
            shuffle_seq(123)

    def test_invalid_input_type_raises_typeerror_list(self):
        with pytest.raises(TypeError, match="must be Sequence or str"):
            shuffle_seq([])

    def test_invalid_input_type_raises_typeerror_none(self):
        with pytest.raises(TypeError, match="must be Sequence or str"):
            shuffle_seq(None)

    def test_large_sequence_shuffles_correctly(self):
        long_seq = "ACGT" * 1000
        shuffled = shuffle_seq(long_seq, seed=7, as_str=True)
        assert len(shuffled) == 4000
        assert sorted(shuffled) == sorted(long_seq)

    def test_unicode_or_non_dna_chars_handled(self):
        seq = "XYZ!@#"
        shuffled = shuffle_seq(seq, seed=5, as_str=True)
        assert sorted(shuffled) == sorted(seq)

    def test_zero_seed_is_valid(self):
        result = shuffle_seq("ATGC", seed=0, as_str=True)
        assert isinstance(result, str)
        assert len(result) == 4
        assert sorted(result) == sorted("ATGC")

    def test_byte_string_not_allowed(self):
        with pytest.raises(TypeError, match="must be Sequence or str"):
            shuffle_seq(b"ATCG")
