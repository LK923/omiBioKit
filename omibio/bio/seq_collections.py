from omibio.bio.seq_entry import SeqEntry
from omibio.sequence import Sequence, Polypeptide
from typing import Iterable, ItemsView, Iterator, Literal, overload


class SeqCollections:
    """Class to hold a collection of SeqEntry objects."""

    def __init__(
        self,
        entries: Iterable[SeqEntry] | None = None,
        source: str | None = None
    ):
        """Initialization for SeqCollection.

        Args:
            entries (Iterable[SeqEntry] | None, optional):
                Iterable of SeqEntry objects to initialize the collection.
                Defaults to None.
            source (str | None, optional):
                Source information for the collection. Defaults to None.

        Raises:
            TypeError:
                If the input types are incorrect.
        """
        self._entries: dict[str, SeqEntry] = {}
        self._source = source
        if entries is not None and not isinstance(entries, Iterable):
            raise TypeError(
                "SeqCollections argument 'entries' must be Iterable "
                f"contains SeqEntry, got {type(entries).__name__}"
            )
        if entries:
            for entry in entries:
                self.add_entry(entry)

    @property
    def entries(self):
        """Return the dictionary of SeqEntry objects."""
        return self._entries

    @property
    def source(self):
        """Return the source information."""
        return self._source

    def add_entry(self, entry: SeqEntry):
        """Add a SeqEntry to the collection."""
        if not isinstance(entry, SeqEntry):
            raise TypeError(
                "SeqCollections argument 'entries' must be Iterable "
                f"contains SeqEntry, got {type(entry).__name__}"
            )
        seq_id = entry.seq_id
        if seq_id in self._entries:
            raise ValueError(
                f"Duplicate seq_id '{seq_id}'"
            )
        self._entries[seq_id] = entry

    def get_entry(self, seq_id: str) -> SeqEntry:
        """Return the SeqEntry for the given seq_id."""
        return self._entries[seq_id]

    def get_seq(self, seq_id: str) -> Sequence | Polypeptide:
        """Return the Sequence or Polypeptide for the given seq_id."""
        return self[seq_id]

    def seq_ids(self) -> list[str]:
        """Return a list of sequence IDs in the collection."""
        return list(self._entries.keys())

    def seqs(self) -> list[Sequence | Polypeptide]:
        """Return a list of sequences in the collection."""
        return [e.seq for e in self._entries.values()]

    def entry_list(self) -> list[SeqEntry]:
        """Return a list of SeqEntry objects in the collection."""
        return list(self._entries.values())

    def seq_dict(self) -> dict[str, Sequence | Polypeptide]:
        """Return a dictionary of seq_id to Sequence or Polypeptide."""
        return {e.seq_id: e.seq for e in self._entries.values()}

    def items(self) -> ItemsView[str, SeqEntry]:
        """Return an items view of the collection."""
        return self._entries.items()

    def keys(self) -> Iterable[str]:
        """Return the keys of the entries dictionary."""
        return self._entries.keys()

    def values(self) -> Iterable[SeqEntry]:
        """Return the values of the entries dictionary."""
        return self._entries.values()

    @overload
    def clean(
        self,
        name_policy: Literal["keep", "id_only", "underscores"] = ...,
        gap_policy: Literal["keep", "remove", "collapse"] = ...,
        strict: bool = ...,
        min_length: int = ...,
        max_length: int = ...,
        normalize_case: bool = ...,
        remove_illegal: bool = ...,
        allowed_bases: Iterable[str] | None = ...,
        remove_empty: bool = ...,
        as_polypeptide: bool = ...,
        inplace: Literal[False] = ...
    ) -> "SeqCollections": ...

    @overload
    def clean(
        self,
        name_policy: Literal["keep", "id_only", "underscores"] = ...,
        gap_policy: Literal["keep", "remove", "collapse"] = ...,
        strict: bool = ...,
        min_length: int = ...,
        max_length: int = ...,
        normalize_case: bool = ...,
        remove_illegal: bool = ...,
        allowed_bases: Iterable[str] | None = ...,
        remove_empty: bool = ...,
        as_polypeptide: bool = ...,
        inplace: Literal[True] = ...
    ) -> None: ...

    def clean(
        self,
        name_policy: Literal["keep", "id_only", "underscores"] = "keep",
        gap_policy: Literal["keep", "remove", "collapse"] = "keep",
        strict: bool = False,
        min_length: int = 10,
        max_length: int = 100_000,
        normalize_case: bool = True,
        remove_illegal: bool = False,
        allowed_bases: Iterable[str] | None = None,
        remove_empty: bool = True,
        as_polypeptide: bool = False,
        inplace: bool = False
    ):
        """Clean sequences according to specified policies.

        Args:
            name_policy (Literal["keep", "id_only", "underscores"], optional):
                Policy for cleaning sequence names. Defaults to "keep".
            gap_policy (Literal["keep", "remove", "collapse"], optional):
                Policy for handling gaps in sequences. Defaults to "keep".
            strict (bool, optional):
                If True, raises an error on illegal characters.
                Defaults to False.
            min_length (int, optional):
                Minimum length for sequences to keep. Defaults to 10.
            max_length (int, optional):
                Maximum length for sequences to keep. Defaults to 100,000.
            normalize_case (bool, optional):
                If True, converts sequences to uppercase. Defaults to True.
            remove_illegal (bool, optional):
                If True, removes illegal characters instead of replacing
                them with 'N'. Defaults to False.
            allowed_bases (set[str] | None, optional):
                Set of allowed bases. Defaults to VALID_BASES.
            remove_empty (bool, optional):
                If True, removes sequences that are empty or contain only 'N's.
                Defaults to True.
            inplace (bool, optional):
                If True, modifies the current SeqCollections object.
                Defaults to False.

        Raises:
            ValueError:
                If input values are invalid.
            TypeError:
                If input types are incorrect.

        Returns:
            SeqCollections | None:
                Cleaned SeqCollections object or None if inplace is True.
        """
        from omibio.sequence import clean

        cleaned: SeqCollections = clean(
            seqs=self,
            name_policy=name_policy,
            gap_policy=gap_policy,
            strict=strict,
            min_length=min_length,
            max_length=max_length,
            normalize_case=normalize_case,
            remove_illegal=remove_illegal,
            allowed_bases=allowed_bases,
            remove_empty=remove_empty,
            as_polypeptide=as_polypeptide,
        )
        if inplace:
            self._entries = cleaned._entries
            return None
        return cleaned

    def __iter__(self) -> Iterator[SeqEntry]:
        return iter(self._entries.values())

    def __getitem__(self, seq_id: str) -> Sequence | Polypeptide:
        return self._entries[seq_id].seq

    def __contains__(self, seq_id: str) -> bool:
        return seq_id in self._entries

    def __len__(self) -> int:
        return len(self._entries)

    def __repr__(self) -> str:
        return f"SeqCollections({list(self._entries.values())!r})"

    def __str__(self) -> str:
        return str(list(self._entries.values()))


def main():
    seqs = SeqCollections(
        [
            SeqEntry(Sequence("A--acACP"), seq_id="1"),
            SeqEntry(Sequence("A--acACP"), seq_id="2"),
        ]
    )
    print(seqs.clean())


if __name__ == "__main__":
    main()
