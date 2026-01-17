import csv
import psycopg
from typing import Any


def get_data(path: str) -> list[dict[str, Any]]:
    orfs = []

    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            orfs.append({
                "seq_id": row["seq_id"],
                "start_pos": int(row["start"]),
                "end_pos": int(row["end"]),
                "strand": row["strand"],
                "frame": int(row["frame"]),
                "length": int(row["length"]),
                "seq": row["nt_seq"]
            })

    return orfs


if __name__ == "__main__":
    orfs = get_data("./examples/data/orfs.tsv")
    conn = psycopg.connect(
        dbname="bioinfodb",
        user="oceanmist",
        password="bioinfodb",
        host="localhost",
        port=5432
    )
    cur = conn.cursor()

    for orf in orfs:
        cur.execute(
            """
            INSERT INTO orfs (
                seq_id, start_pos, end_pos, strand, frame, length, seq
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                orf["seq_id"], orf["start_pos"], orf["end_pos"],
                orf["strand"], orf["frame"], orf["length"], orf["seq"]
            )
        )
    conn.commit()
    cur.close()
    conn.close()
