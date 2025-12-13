import pytest
from omibio.sequence.seq_utils.clean import (
    clean, write_report, CleanReport, CleanReportItem
)
from omibio.sequence.sequence import Sequence
import tempfile
import os
from omibio.sequence import Polypeptide


class TestCleanFasta:

    def setup_method(self):
        self.seqs = {
            "seq1 good_sequence": "ATGCATGCATGC",
            "seq2   spaces_and_lowercase": "atgcATGC",
            "seq 3    invalid$name": "ATG$CAT^GC",
            "seq4--alignment   collapse_test": "ATG---CATGC",
            "seq5_remove_gaps   ": "---ATGC---",
            "seq6_only_N": "NNNNNN",
            "seq7_only_gaps": "-----",
            "seq8_short": "ATG",
            "seq9_long": "A" * 100001,
            "seq10_illegal_characters": "ATGC$%^ATGC",
            "seq11_mixed_rna_dna": "AUGCATGCUA",
            "seq12_whitespace_lines": "ATGC\nATGC\nATGC",
            "seq4--alignment   collapse_test_duplicate": "ATG---CATGC",
            "": "ATGCATGCATGC",
            "seq1 dup": "ATGCATGCATGC",
            "seq1 dup2": "ATGCATGCATGC"
        }

    def test_clean_basic(self):
        cleaned, report = clean(self.seqs, min_len=4, report=True)
        assert isinstance(cleaned, dict)
        assert isinstance(report, CleanReport)
        assert cleaned["seq1 good_sequence"] == "ATGCATGCATGC"
        assert cleaned["seq2 spaces_and_lowercase"] == "ATGCATGC"
        assert cleaned["seq 3 invalid_name"] == "ATGNCATNGC"
        assert cleaned["seq4--alignment collapse_test"] == "ATG---CATGC"
        assert "seq4--alignment collapse_test" in cleaned
        assert cleaned["seq5_remove_gaps"] == "---ATGC---"
        assert cleaned["seq10_illegal_characters"] == "ATGCNNNATGC"
        assert cleaned["seq11_mixed_rna_dna"] == "AUGCATGCUA"
        assert cleaned["seq12_whitespace_lines"] == "ATGCATGCATGC"

    def test_clean_checking(self):
        with pytest.raises(ValueError):
            seqs = {"seq": "ATGC"}
            clean(seqs, allowed_bases={"Ag", "TC"})
        with pytest.raises(TypeError):
            clean({1, 2, 3})
        with pytest.raises(ValueError):
            clean(seqs, name_policy="invalid")
        with pytest.raises(ValueError):
            clean(seqs, gap_policy="invalid")
        with pytest.raises(TypeError):
            clean(seqs, min_len="invalid")
        with pytest.raises(TypeError):
            clean(seqs, max_len="invalid")
        with pytest.raises(ValueError):
            clean(seqs, min_len=-1)
        with pytest.raises(ValueError):
            clean(seqs, max_len=-1)
        with pytest.raises(ValueError):
            clean(seqs, min_len=2, max_len=1)
        with pytest.raises(TypeError):
            clean({(1, 2): "ACTG"})
        with pytest.raises(TypeError):
            clean({"seq": (1, 2)})

    def test_write_report_checking(self):
        with pytest.raises(TypeError):
            write_report(out_path=1, report=CleanReport())
        with pytest.raises(TypeError):
            write_report("path", report=[])

    def test_clean_report(self):
        with pytest.raises(TypeError):
            CleanReport().add(1)
        report = CleanReport()
        item = CleanReportItem(orig_name="name")
        report.add(item)
        assert report.records[0] is item

    def test_name_policy_id_only(self):
        cleaned = clean(
            self.seqs, name_policy="id_only", min_len=4)
        names = list(cleaned.keys())
        assert "seq1" in names
        assert "seq2" in names
        assert "seq" in names
        assert "seq4--alignment" in names

    def test_name_policy_underscores(self):
        cleaned = clean(
            self.seqs, name_policy="underscores", min_len=4)
        for name in cleaned.keys():
            assert " " not in name

    def test_gap_policy_remove(self):
        cleaned = clean(
            self.seqs, gap_policy="remove", min_len=4, name_policy="id_only"
        )
        assert "-" not in cleaned["seq4--alignment"]
        assert "-" not in cleaned["seq4--alignment_1"]

    def test_gap_policy_collapse(self):
        cleaned = clean(
            self.seqs, gap_policy="collapse", min_len=4, name_policy="id_only"
        )
        assert "--" not in cleaned["seq4--alignment"]

    def test_strict_mode(self):
        with pytest.raises(ValueError):
            clean({"seq_invalid": "ATGC$"}, strict=True, min_len=4)

    def test_remove_illegal(self):
        cleaned = clean(
            {"seq_invalid": "ATGC$%^"}, min_len=4, remove_illegal=True
        )
        assert cleaned["seq_invalid"] == "ATGC"

    def test_remove_empty_and_length_filter(self):
        _, report = clean(
            self.seqs, min_len=4, max_len=100000,
            remove_empty=True, report=True
        )
        removed_names = [r.orig_name for r in report.removed]
        for name in [
            "seq6_only_N", "seq7_only_gaps", "seq8_short", "seq9_long"
        ]:
            assert name in removed_names

    def test_as_str_option(self):
        cleaned = clean(self.seqs, min_len=4, as_str=False)
        for seq in cleaned.values():
            assert isinstance(seq, Sequence)

    def test_write_report_creates_file(self):
        _, report = clean(self.seqs, min_len=4, report=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.txt")
            write_report(path, report)
            assert os.path.exists(path)
            content = open(path).read()
            assert "Clean Report Summary" in content
            assert "=== Cleaned Sequences ===" in content
            assert "=== Removed Sequences ===" in content

    def test_no_name(self):
        cleaned = clean(self.seqs, min_len=4)
        assert "unnamed" in cleaned

    def test_duplicate_name(self):
        cleaned = clean(self.seqs, min_len=4, name_policy="id_only")
        assert "seq1" in cleaned
        assert "seq1_1" in cleaned
        assert "seq1_2" in cleaned

    def test_set_allowed_bases(self):
        seqs = {"seq": "AAAAAAAAAAA"}
        cleaned = clean(seqs, allowed_bases=["A"], name_policy="id_only")
        assert "seq" in cleaned
        assert cleaned["seq"] == "AAAAAAAAAAA"

    def test_as_polypeptide(self):
        seqs = {"seq": "AAAAAAAAAAA"}
        cleaned = clean(seqs, as_polypeptide=True)
        assert "seq" in cleaned
        assert isinstance(cleaned["seq"], Polypeptide)

    def test_as_str(self):
        seqs = {"seq": "AAAAAAAAAAA"}
        cleaned = clean(seqs, as_str=True)
        assert "seq" in cleaned
        assert isinstance(cleaned["seq"], str)
