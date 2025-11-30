from omibio.sequence.sequence import Sequence
from typing import Literal
import re
from dataclasses import dataclass


@dataclass
class CleanReportItem:
    orig_name: str
    clean_name: str | None = None
    orig_len: int = 0
    clean_len: int = 0
    removed: bool = False
    gap_policy: str | None = None
    illegal_removed: int = 0
    illegal_replaced: int = 0
    name_changed: bool = False
    reason: str = ""


class CleanReport:
    def __init__(self):
        self.records: list[CleanReportItem] = []

    def add(self, item: CleanReportItem):
        self.records.append(item)

    @property
    def kept(self):
        return [r for r in self.records if not r.removed]

    @property
    def removed(self):
        return [r for r in self.records if r.removed]

    def summary(self):
        return {
            "total": len(self.records),
            "kept": len(self.kept),
            "removed": len(self.removed)
        }


VALID_BASES = {
    "A", "T", "C", "G", "U",
    "N", "R", "Y", "K", "M", "B", "V", "D", "H", "S", "W"
}
WHITESPACE_RE = re.compile(r"\s+")
INVALID_NAME_CHAR_RE = re.compile(r"[^ A-Za-z0-9_.-]")
ALIG_SYMBOL_RE = re.compile(r"-+")


def clean(
    seqs: dict[str, str | Sequence],
    name_policy: Literal["keep", "id_only", "underscores"] = "keep",
    gap_policy: Literal["keep", "remove", "collapse"] = "keep",
    strict: bool = False,
    min_len: int = 10,
    max_len: int = 100000,
    normalize_case: bool = True,
    remove_illegal: bool = False,
    allowed_bases: set[str] | None = None,
    remove_empty: bool = True,
    as_str: bool = True,
    report: bool = False
) -> dict[str, str | Sequence] | tuple[dict[str, str | Sequence], CleanReport]:

    if allowed_bases is None:
        allowed_bases = VALID_BASES
    else:
        allowed_bases = set(allowed_bases)

    cleaned_seqs = {}
    if report:
        clean_report = CleanReport()

    # ---------------- name processing ----------------
    def process_name(name) -> str:
        name = WHITESPACE_RE.sub(" ", name.strip())

        if name_policy == "id_only":
            name = name.split(" ", 1)[0]

        name = INVALID_NAME_CHAR_RE.sub("_", name)

        if name_policy == "underscores":
            name = name.replace(" ", "_")

        if not name:
            name = "unnamed"

        return name

    # ---------------- sequence cleaning ----------------
    def process_seq(seq: str, item: CleanReportItem) -> str:

        pure_seq = WHITESPACE_RE.sub("", seq)
        item.orig_len = len(pure_seq)

        cleaned = pure_seq
        if normalize_case:
            cleaned = cleaned.upper()

        match gap_policy:
            case "remove":
                item.gap_policy = "remove"
                cleaned = cleaned.replace("-", "")
            case "collapse":
                item.gap_policy = "collapse"
                cleaned = ALIG_SYMBOL_RE.sub("-", cleaned)
            case _:
                item.gap_policy = "keep"

        if strict:
            for i, base in enumerate(cleaned):
                if base not in allowed_bases and base != "-":
                    raise ValueError(
                        f"Illegal character {base} in sequence at position {i}"
                    )
        else:
            illegal_removed = 0
            illegal_replaced = 0
            new_seq = []

            for base in cleaned:
                if base in allowed_bases or base == "-":
                    new_seq.append(base)
                else:
                    if remove_illegal:
                        illegal_removed += 1
                    else:
                        new_seq.append("N")
                        illegal_replaced += 1

            cleaned = "".join(new_seq)
            item.illegal_removed = illegal_removed
            item.illegal_replaced = illegal_replaced

        if remove_empty and set(cleaned) <= {"N", "-"}:
            item.reason = "empty_or_N_only"
            return ""

        if not cleaned or not (min_len <= len(cleaned) <= max_len):
            item.reason = "length_filter"
            return ""

        return cleaned

    # ---------------- main loop ----------------
    for raw_name, raw_seq in seqs.items():

        item = CleanReportItem(orig_name=raw_name)

        cleaned_name = process_name(raw_name)

        cleaned = process_seq(str(raw_seq), item)

        if not cleaned:
            item.removed = True
            item.clean_len = 0
            if report:
                clean_report.add(item)
            continue

        if cleaned_name in cleaned_seqs:
            count = 1
            new_name = f"{cleaned_name}_{count}"
            while new_name in cleaned_seqs:
                count += 1
                new_name = f"{cleaned_name}_{count}"
            cleaned_name = new_name

        item.clean_name = cleaned_name
        item.clean_len = len(cleaned)

        if cleaned_name != raw_name:
            item.name_changed = True

        cleaned_seq = Sequence(cleaned) if not as_str else cleaned

        cleaned_seqs[cleaned_name] = cleaned_seq

        if report:
            clean_report.add(item)

    return cleaned_seqs if not report else (cleaned_seqs, clean_report)


def write_report(out_path: str, report: CleanReport):
    """
    Write a clean report to a file in aligned text format.
    Works with the CleanReport / CleanReportItem classes defined.
    """
    lines = []

    # --- Summary ---
    lines.append("=== Clean Report Summary ===")
    summary = report.summary()
    lines.append(f"Total sequences: {summary['total']}")
    lines.append(f"Kept: {summary['kept']}")
    lines.append(f"Removed: {summary['removed']}")
    lines.append("")

    # --- Kept sequences table ---
    lines.append("=== Cleaned Sequences ===")
    headers = [
        "orig_name", "clean_name",
        "orig_len", "clean_len",
        "name_changed", "gap_policy",
        "illegal_removed", "illegal_replaced"
    ]

    # Prepare rows
    rows = []
    for r in report.kept:
        rows.append([
            r.orig_name,
            r.clean_name,
            str(r.orig_len),
            str(r.clean_len),
            "yes" if r.name_changed else "no",
            r.gap_policy if r.gap_policy else "",
            str(r.illegal_removed),
            str(r.illegal_replaced)
        ])

    # Column widths
    col_widths = [
        max(
            len(headers[i]), max((len(row[i]) for row in rows), default=0)
        ) for i in range(len(headers))
    ]

    # Header row
    header_line = "  ".join(
        headers[i].ljust(col_widths[i]) for i in range(len(headers))
    )
    lines.append(header_line)
    lines.append("-" * len(header_line))

    # Data rows
    for row in rows:
        lines.append(
            "  ".join(row[i].ljust(col_widths[i]) for i in range(len(headers)))
        )
    lines.append("")

    # --- Removed sequences ---
    lines.append("=== Removed Sequences ===")
    lines.append("orig_name          reason")
    lines.append("-" * 50)
    for r in report.removed:
        reason = getattr(r, "reason", "removed")
        lines.append(f"{r.orig_name.ljust(18)} {reason}")

    # Write to file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    from omibio.io import write_fasta, read
    input_path = r"./examples/data/example_dirty.fasta"
    output_path = r"./examples/output/clean_fasta_output.fasta"

    seqs = read(input_path, as_str=True, strict=False)

    cleaned_seqs, report = clean(
        seqs, name_policy="id_only", gap_policy="collapse",
        report=True, remove_illegal=True
    )

    write_fasta(output_path, cleaned_seqs, space_between=True)
    print(output_path)

    write_report(r"./examples/output/clean_report.txt", report)
    print(r"./examples/output/clean_report.txt")
    print(report.records)


if __name__ == "__main__":
    main()
