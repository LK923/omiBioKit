import pytest
from omibio.io.write_fasta import write_fasta


def test_write_fasta_basic(tmp_path):
    file_path = tmp_path / "out.fasta"
    seqs = {"seq1": "ATGC", "seq2": "AAAAATTTTT"}

    write_fasta(file_name=file_path, seqs=seqs)

    content = file_path.read_text().splitlines()
    assert content == [
        ">seq1",
        "ATGC",
        ">seq2",
        "AAAAATTTTT",
    ]


def test_write_fasta_line_length(tmp_path):
    file_path = tmp_path / "out.fasta"
    seqs = {"seq1": "A" * 15}

    write_fasta(file_name=file_path, seqs=seqs, line_len=5)

    content = file_path.read_text().splitlines()
    assert content == [
        ">seq1",
        "AAAAA",
        "AAAAA",
        "AAAAA",
    ]


def test_write_fasta_with_blank_lines(tmp_path):
    file_path = tmp_path / "out.fasta"
    seqs = {"s1": "ATGC", "s2": "GGGG"}

    write_fasta(file_name=file_path, seqs=seqs)

    content = file_path.read_text().splitlines()
    assert content == [
        ">s1",
        "ATGC",
        ">s2",
        "GGGG",
    ]


def test_write_fasta_accepts_sequence_objects(tmp_path):
    class FakeSeq:
        def __str__(self):
            return "ATGCATGC"

    file_path = tmp_path / "out.fasta"
    seqs = {"myseq": FakeSeq()}

    write_fasta(file_name=file_path, seqs=seqs)

    content = file_path.read_text().splitlines()
    assert content == [
        ">myseq",
        "ATGCATGC",
    ]


def test_write_fasta_non_dict_raises():
    with pytest.raises(TypeError):
        write_fasta("x.fasta", ["not", "a", "dict"])


def test_write_fasta_name_not_str(tmp_path):
    file_path = tmp_path / "out.fasta"
    seqs = {123: "ATGC"}

    with pytest.raises(TypeError):
        write_fasta(file_name=file_path, seqs=seqs)


def test_write_fasta_creates_parent_dir(tmp_path):
    file_path = tmp_path / "nested" / "out.fasta"
    seqs = {"seq": "ATGC"}

    write_fasta(file_name=file_path, seqs=seqs)

    assert file_path.exists()
    assert file_path.read_text().splitlines() == [
        ">seq",
        "ATGC",
    ]


def test_empty_dict(tmp_path):
    file_path = tmp_path / "out.fasta"
    seqs = {}

    write_fasta(file_name=file_path, seqs=seqs)

    assert not file_path.exists()
