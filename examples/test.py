def gc(seq, percent=False):
    gc_content = (seq.count("C") + seq.count("G")) / len(seq)
    return (
        round(gc_content, 4) if not percent
        else f"{round(gc_content * 100, 2)}%"
    )


print(gc("ACAC"))
