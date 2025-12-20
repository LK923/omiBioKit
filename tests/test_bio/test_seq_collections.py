import pytest
from omibio.bio.seq_entry import SeqEntry
from omibio.bio import SeqCollections
from omibio.sequence import Sequence, Polypeptide


class TestSeqCollections:
    def make_entry(
        self,
        seq_id="s1",
        seq="ATGC",
        source="test",
        is_pep=False,
    ):
        if is_pep:
            seq_obj = Polypeptide(seq)
        else:
            seq_obj = Sequence(seq)
        return SeqEntry(
            seq_id=seq_id,
            seq=seq_obj,
            source=source,
        )

    def test_init_empty(self):
        sc = SeqCollections()
        assert len(sc) == 0
        assert sc.entries == {}

    def test_init_with_entries(self):
        e1 = self.make_entry("a")
        e2 = self.make_entry("b")
        sc = SeqCollections(entries=[e1, e2], source="test")
        assert len(sc) == 2
        assert "a" in sc
        assert "b" in sc
        assert sc.source == "test"

    def test_init_entries_not_iterable(self):
        with pytest.raises(TypeError):
            SeqCollections(entries=123)

    def test_add_entry_success(self):
        sc = SeqCollections(source="test")
        e = self.make_entry("x")
        sc.add_entry(e)
        assert len(sc) == 1
        assert sc.get_entry("x") is e

    def test_add_entry_not_seqentry(self):
        sc = SeqCollections(source="test")
        with pytest.raises(TypeError):
            sc.add_entry("not_entry")

    def test_add_entry_duplicate_seq_id(self):
        e = self.make_entry("dup")
        sc = SeqCollections(entries=[e], source="test")
        with pytest.raises(ValueError):
            sc.add_entry(self.make_entry("dup"))

    def test_get_entry(self):
        e = self.make_entry("g")
        sc = SeqCollections(entries=[e], source="test")
        assert sc.get_entry("g") is e

    def test_get_seq(self):
        e = self.make_entry("s")
        sc = SeqCollections(entries=[e], source="test")
        assert sc.get_seq("s") is e.seq

    def test_getitem(self):
        e = self.make_entry("i")
        sc = SeqCollections(entries=[e], source="test")
        assert sc["i"] is e.seq

    def test_contains(self):
        e = self.make_entry("c")
        sc = SeqCollections(entries=[e], source="test")
        assert "c" in sc
        assert "x" not in sc

    def test_seq_ids(self):
        e1 = self.make_entry("a")
        e2 = self.make_entry("b")
        sc = SeqCollections(entries=[e1, e2], source="test")
        assert set(sc.seq_ids()) == {"a", "b"}

    def test_seqs(self):
        e1 = self.make_entry("a", "AA")
        e2 = self.make_entry("b", "BB", is_pep=True)
        sc = SeqCollections(entries=[e1, e2], source="test")
        seqs = sc.seqs()
        assert e1.seq in seqs
        assert e2.seq in seqs

    def test_entry_list(self):
        e1 = self.make_entry("a")
        e2 = self.make_entry("b")
        sc = SeqCollections(entries=[e1, e2], source="test")
        lst = sc.entry_list()
        assert e1 in lst
        assert e2 in lst

    def test_seq_dict(self):
        e1 = self.make_entry("a", "AA")
        e2 = self.make_entry("b", "BB")
        sc = SeqCollections(entries=[e1, e2], source="test")
        d = sc.seq_dict()
        assert d == {"a": e1.seq, "b": e2.seq}

    def test_dict_methods(self):
        e = self.make_entry(seq_id="test", seq="ATGC")
        sc = SeqCollections(entries=[e], source="test")
        items = dict(sc.items())
        assert items["test"] is e

        assert list(sc.keys())[0] == "test"
        assert list(sc.values())[0] is e

    def test_iter(self):
        e1 = self.make_entry("a")
        e2 = self.make_entry("b")
        sc = SeqCollections(entries=[e1, e2], source="test")
        it = list(iter(sc))
        assert e1 in it
        assert e2 in it

    def test_len(self):
        sc = SeqCollections(source="test")
        assert len(sc) == 0
        sc.add_entry(self.make_entry("x"))
        assert len(sc) == 1

    def test_repr(self):
        e = self.make_entry("r")
        sc = SeqCollections(entries=[e], source="test")
        r = repr(sc)
        assert "SeqCollections" in r
        assert "r" in r

    def test_str(self):
        e = self.make_entry("s")
        sc = SeqCollections(entries=[e], source="test")
        assert str(sc) == str([e])
