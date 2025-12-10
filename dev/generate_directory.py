from pathlib import Path
from itertools import chain


def main():
    root_dir = Path("omibio")
    output_file = Path("MODULES.md")

    files = list(
        chain(
            (f.relative_to(root_dir) for f in root_dir.rglob("*.py") if f.name != "__init__.py"),  # noqa
            (f.relative_to(root_dir) for f in root_dir.rglob("*.toml"))
        )
    )

    tree = {}
    for file in files:
        parts = file.parts
        current = tree
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current.setdefault("_files", []).append(parts[-1])

    def write_tree(f, subtree, indent=0):
        for name, content in sorted(subtree.items()):
            if name == "_files":
                for file_name in sorted(content):
                    f.write("  " * indent + f"- {file_name}\n")
            else:
                f.write("  " * indent + f"### {name}/\n")
                write_tree(f, content, indent + 1)
            f.write("\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# omibio Modules\n\n")
        f.write(
            "[![Latest Version]"
            "(https://img.shields.io/github/v/release/LK923/omiBioKit?color=blue)]"  # noqa
            "(https://github.com/LK923/omiBioKit/releases)\n\n"
        )
        write_tree(f, tree)

    print(f"Written to {output_file}")


if __name__ == "__main__":
    main()
