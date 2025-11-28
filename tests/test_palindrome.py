import pytest
from omibio.sequence.sequence import Sequence
from omibio.analysis.palindrome import find_palindrome

# pytest --cov=omibio.analysis.palindrome tests/ --cov-report=term-missing


class TestFindPalindrome:
    def test_basic_palindrome_even_length(self):
        seq = "AGCT"
        palindromes = find_palindrome(seq, min_len=4, max_len=6)
        assert len(palindromes) == 1
        assert palindromes[0].start == 0
        assert palindromes[0].end == 4
        assert palindromes[0].nt_seq == "AGCT"

    def test_basic_palindrome_odd_length_ignored(self):
        seq = "ATGCC"
        palindromes = find_palindrome(seq, min_len=4, max_len=5)
        assert len(palindromes) == 0

    def test_no_palindrome(self):
        seq = "ATGCTA"
        palindromes = find_palindrome(seq, min_len=4, max_len=6)
        assert len(palindromes) == 0

    def test_multiple_palindromes(self):
        seq = "ATGCATNNNATGCAT"
        palindromes = find_palindrome(seq, min_len=4, max_len=6)
        assert len(palindromes) == 4

    def test_min_len_greater_than_seq_len(self):
        with pytest.raises(ValueError):
            find_palindrome("ATGC", min_len=6, max_len=8)

    def test_max_len_less_than_min_len(self):
        with pytest.raises(ValueError):
            find_palindrome("ATGCAT", min_len=6, max_len=4)

    def test_invalid_seq_type(self):
        with pytest.raises(TypeError):
            find_palindrome(123, min_len=4, max_len=6)

    def test_invalid_min_len_type(self):
        with pytest.raises(TypeError):
            find_palindrome("ATGCAT", min_len="4", max_len=6)

    def test_invalid_max_len_type(self):
        with pytest.raises(TypeError):
            find_palindrome("ATGCAT", min_len=4, max_len="6")

    def test_empty_string_input(self):
        palindromes = find_palindrome("", min_len=4, max_len=6)
        assert len(palindromes) == 0

    def test_short_sequence_below_min_len(self):
        with pytest.raises(ValueError):
            find_palindrome("ATG", min_len=4, max_len=6)

    def test_exact_min_len_match(self):
        seq = "ATAT"
        palindromes = find_palindrome(seq, min_len=4, max_len=4)
        assert len(palindromes) == 1

    def test_palindrome_at_end_of_sequence(self):
        seq = "NNNAGCT"
        palindromes = find_palindrome(seq, min_len=4, max_len=6)
        assert len(palindromes) == 1
        assert palindromes[0].start == 3

    def test_palindrome_at_start_of_sequence(self):
        seq = "AGCTNNN"
        palindromes = find_palindrome(seq, min_len=4, max_len=6)
        assert len(palindromes) == 1
        assert palindromes[0].start == 0

    def test_overlapping_palindromes_different_lengths(self):
        seq = "ATGCATGCAT"
        palindromes = find_palindrome(seq, min_len=4, max_len=10)
        lengths = {p.end - p.start for p in palindromes}
        assert 6 in lengths
        assert 10 in lengths

    def test_max_len_odd_adjusted_to_even(self):
        seq = "ATGCATGC"
        palindromes = find_palindrome(seq, min_len=4, max_len=7)
        assert all((p.end - p.start) % 2 == 0 for p in palindromes)

    def test_sequence_with_nucleotide_case_mixed(self):
        seq = "aGcT"
        palindromes = find_palindrome(seq, min_len=4, max_len=6)
        assert len(palindromes) == 1

    def test_sequence_object_input(self):
        seq = Sequence("ATGCAT")
        palindromes = find_palindrome(seq, min_len=4, max_len=6)
        assert len(palindromes) == 2

    def test_max_len_larger_than_seq_len(self):
        seq = "ATGCAT"
        palindromes = find_palindrome(seq, min_len=4, max_len=20)
        assert len(palindromes) >= 1
