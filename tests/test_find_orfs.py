import pytest
from omibio.sequence import Sequence
from omibio.analysis.find_orfs import find_orfs, find_orfs_in_frame

# pytest --cov=omibio.analysis.find_orfs tests/ --cov-report=term-missing


class TestFindORFs:
    def test_basic_positive_strand(self):
        seq = "ATGAAATAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=12, start_codons={"ATG"}
        )
        assert len(orfs) == 1
        assert orfs[0].start == 0
        assert orfs[0].end == 9
        assert orfs[0].strand == '+'
        assert orfs[0].frame == 1

    def test_no_start_codon(self):
        seq = "AAATAA"
        orfs = find_orfs(
            seq, min_length=3, max_length=10, start_codons={"ATG"}
        )
        assert len(orfs) == 0

    def test_no_stop_codon(self):
        seq = "ATGAAA"
        orfs = find_orfs(
            seq, min_length=3, max_length=10, start_codons={"ATG"}
        )
        assert len(orfs) == 0

    def test_shorter_than_min_length(self):
        seq = "ATGTAA"
        orfs = find_orfs(
            seq, min_length=9, max_length=15, start_codons={"ATG"}
        )
        assert len(orfs) == 0

    def test_longer_than_max_length(self):
        seq = "ATG" + "A" * 30 + "TAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=20, start_codons={"ATG"})

        assert len(orfs) == 0

    def test_multiple_frames_positive(self):
        seq = "AATGAAATAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=15, start_codons={"ATG"}
        )
        assert len(orfs) == 1
        assert orfs[0].frame == 2

    def test_no_reverse_complement(self):
        seq = "TTTATTTTA"
        orfs = find_orfs(
            seq, min_length=6, max_length=15,
            include_reverse=False, start_codons={"ATG"}
        )
        assert len(orfs) == 0

    def test_overlapping_orfs_allowed(self):
        seq = "ATGAAAATGAAATAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=15,
            overlap=True, start_codons={"ATG"}
            )
        assert len(orfs) == 2

    def test_overlapping_orfs_not_allowed(self):
        seq = "ATGAAATGATAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=15,
            overlap=False, start_codons={"ATG"}
        )
        assert len(orfs) == 1

    def test_custom_start_codons(self):
        seq = "GTGAAATAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=12, start_codons={"GTG"}
        )
        assert len(orfs) == 1

    def test_rna_input(self):
        seq = "AUGAAAUAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=12, start_codons={"ATG"}
        )
        assert len(orfs) == 1

    def test_sequence_object_input(self):
        seq = Sequence("ATGAAATAA")
        orfs = find_orfs(
            seq, min_length=6, max_length=12, start_codons={"ATG"}
        )
        assert len(orfs) == 1

    def test_empty_sequence(self):
        orfs = find_orfs(
            "", min_length=0, max_length=10, start_codons={"ATG"}
        )
        assert len(orfs) == 0

    def test_min_length_zero(self):
        seq = "ATGTAA"
        orfs = find_orfs(
            seq, min_length=0, max_length=10, start_codons={"ATG"}
        )
        assert len(orfs) == 1

    def test_invalid_length_not_int(self):
        with pytest.raises(TypeError):
            find_orfs("ATGAAATAA", min_length=[])
        with pytest.raises(TypeError):
            find_orfs("ATGAAATAA", min_length=1, max_length=[])

    def test_invalid_length_negative(self):
        with pytest.raises(ValueError):
            find_orfs("ATGAAATAA", min_length=-1)
        with pytest.raises(ValueError):
            find_orfs("ATGAAATAA", min_length=1, max_length=-5)

    def test_invalid_max_length_less_than_min(self):
        with pytest.raises(ValueError):
            find_orfs("ATGAAATAA", min_length=10, max_length=5)

    def test_empty_start_codons(self):
        with pytest.raises(ValueError):
            find_orfs("ATGAAATAA", start_codons=[])

    def test_invalid_seq_type(self):
        with pytest.raises(TypeError):
            find_orfs(123)

    def test_invalid_start_codon_type(self):
        with pytest.raises(TypeError):
            find_orfs("ATGAAATAA", start_codons=[123])

    def test_start_codon_wrong_length(self):
        with pytest.raises(ValueError):
            find_orfs("ATGAAATAA", start_codons={"AT"})

    def test_invalid_seq_id(self):
        with pytest.raises(TypeError):
            find_orfs("ATGAAATAA", seq_id=1)

    def test_sort_by_length_descending(self):
        seq = "ATGAAAAATAAATGAAATAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=30,
            overlap=True, start_codons={"ATG"}
        )
        assert len(orfs) == 2
        assert orfs[0].length >= orfs[1].length

    def test_translate_true(self):
        seq = "ATGAAATAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=12,
            translate=True, start_codons={"ATG"}
        )
        assert orfs[0].aa_seq == "MK"

    def test_translate_false(self):
        seq = "ATGAAATAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=12,
            translate=False, start_codons={"ATG"}
        )
        assert orfs[0].aa_seq is None

    def test_frame_assignment_reverse(self):
        seq = "TTAGGGCAT"
        orfs = find_orfs(
            seq, min_length=6, max_length=15,
            include_reverse=True, start_codons={"ATG"}
        )
        assert orfs[0].frame in (-1, -2, -3)

    def test_find_orfs_in_frame_direct_call(self):
        seq = "ATGAAATAA"
        orfs = find_orfs_in_frame(
            seq, min_length=6, max_length=12, overlap=False,
            strand='+', frame=0, translate=False,
            start_codons={"ATG"}, seq_id="test"
        )
        assert len(orfs) == 1
        assert orfs[0].seq_id == "test"

    def test_stop_codon_tga(self):
        seq = "ATGAAATGA"
        orfs = find_orfs(
            seq, min_length=6, max_length=12, start_codons={"ATG"}
        )
        assert len(orfs) == 1

    def test_stop_codon_tag(self):
        seq = "ATGAAATAG"
        orfs = find_orfs(
            seq, min_length=6, max_length=12, start_codons={"ATG"}
        )
        assert len(orfs) == 1

    def test_multiple_stop_codons(self):
        seq = "ATGAAATAATAG"
        orfs = find_orfs(
            seq, min_length=6, max_length=15, start_codons={"ATG"}
        )
        assert len(orfs) == 1

    def test_seq_id_propagation(self):
        seq = "ATGAAATAA"
        orfs = find_orfs(
            seq, min_length=6, max_length=12,
            start_codons={"ATG"}, seq_id="seq1"
        )
        assert orfs[0].seq_id == "seq1"
