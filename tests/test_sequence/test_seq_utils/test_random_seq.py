import pytest
from omibio.sequence.sequence import Sequence
from omibio.sequence.seq_utils.random_seq import random_seq, random_fasta


class TestRandomSeq:

    def test_random_seq_returns_sequence_object(self):
        seq = random_seq(10)
        assert isinstance(seq, Sequence)
        assert len(seq) == 10

    def test_random_seq_returns_str(self):
        seq = random_seq(10, as_str=True)
        assert isinstance(seq, str)
        assert len(seq) == 10

    def test_random_seq_seed_reproducibility(self):
        seq1 = random_seq(12, seed=123, as_str=True)
        seq2 = random_seq(12, seed=123, as_str=True)
        assert seq1 == seq2

    def test_random_seq_invalid_length(self):
        with pytest.raises(ValueError):
            random_seq(-1)

    def test_random_seq_empty_alphabet(self):
        with pytest.raises(ValueError):
            random_seq(10, alphabet="")

    def test_random_seq_weight_length_mismatch(self):
        with pytest.raises(ValueError):
            random_seq(10, alphabet="ATCG", weights=[0.1, 0.2])

    def test_random_seq_with_weights(self):
        seq = random_seq(
            20, alphabet="AB", weights=[0.9, 0.1], seed=10, as_str=True
        )
        assert seq.count("A") > seq.count("B")


class TestRandomFasta:

    def test_random_fasta_creates_file(self, tmp_path):
        out = tmp_path / "test.fa"
        random_fasta(file_path=str(out), seq_num=3, length=5, seed=10)

        assert out.exists()

        content = out.read_text().strip().splitlines()
        assert content[0].startswith(">Sequence_")
        assert len(content) >= 6

    def test_random_fasta_seed_reproducibility(self, tmp_path):
        out1 = tmp_path / "a.fa"
        out2 = tmp_path / "b.fa"

        random_fasta(file_path=str(out1), seq_num=2, length=8, seed=99)
        random_fasta(file_path=str(out2), seq_num=2, length=8, seed=99)

        assert out1.read_text() == out2.read_text()

    def test_random_fasta_custom_alphabet(self, tmp_path):
        out = tmp_path / "test.fa"
        random_fasta(file_path=str(out), seq_num=1, length=10, alphabet="XYZ")

        seq = out.read_text().splitlines()[1]
        assert all(ch in "XYZ" for ch in seq)
