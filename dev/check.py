import subprocess

COMMANDS = [
    "pytest --cov=omibio --cov-report=term-missing tests/",
    "mypy omibio",
    "flake8 omibio tests",
    "python ./dev/generate_directory.py",
]


def run(cmd):
    print(f"\n>>> Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"\033[31mCommand failed: \033[0m{cmd}")
    else:
        print(f"\033[1;32mCommand succeeded: \033[0m{cmd}")


def main():
    for cmd in COMMANDS:
        run(cmd)
    print("\033[1;32mChecking completed\033[0m")


if __name__ == "__main__":
    main()
