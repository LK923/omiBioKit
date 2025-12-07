from pathlib import Path
from collections import defaultdict


def main():
    root_dir = Path("omibio")
    output_file = Path("MODULES.md")

    packages = defaultdict(list)

    for file in root_dir.rglob("*"):
        if file.suffix in {".py", ".toml"} and file.name != "__init__.py":
            package = file.parent.relative_to(root_dir)
            packages[str(package)].append(file.name)

    sorted_packages = sorted(packages.items())

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# omibio Library Modules\n\n")
        f.write(
            "[![Latest Version]"
            "(https://img.shields.io/github/v/release/LK923/omiBioKit?color=blue)]"  # noqa
            "(https://github.com/LK923/omiBioKit/releases)\n"
            )
        for pkg, files in sorted_packages:
            pkg_display = pkg if pkg != "." else "omibio root"
            f.write(f"## {pkg_display}\n")
            for file in sorted(files):
                f.write(f"- {file}\n")
            f.write("\n")
    print(output_file)


if __name__ == "__main__":
    main()
