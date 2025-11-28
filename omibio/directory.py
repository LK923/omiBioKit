from pathlib import Path
from collections import defaultdict

root_dir = Path("omibio")
output_file = Path("MODULES.md")

packages = defaultdict(list)

for py_file in root_dir.rglob("*.py"):
    if py_file.name == "__init__.py":
        continue
    package = py_file.parent.relative_to(root_dir)
    packages[str(package)].append(py_file.name)

sorted_packages = sorted(packages.items())

with open(output_file, "w", encoding="utf-8") as f:
    f.write("# omibio Library Modules\n\n")
    f.write(
        "[![Latest Version](https://img.shields.io/github/v/release/LK923/omiBioKit?color=blue)]"  # noqa
        "(https://github.com/LK923/omiBioKit/releases)\n"
        )
    for pkg, files in sorted_packages:
        pkg_display = pkg if pkg != "." else "omibio root"
        f.write(f"## {pkg_display}\n\n")
        for file in sorted(files):
            f.write(f"- {file}\n")
        f.write("\n---\n\n")
