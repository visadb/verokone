#!/usr/bin/env python3
from pathlib import Path


def read_names(file_path: Path) -> list[str]:
    """Read names from file, ignoring empty lines and stripping whitespace."""
    if not file_path.exists():
        raise FileNotFoundError(f"Names file not found: {file_path}")
    return [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    names_file = Path("names.txt")
    for name in read_names(names_file):
        print(f"{name}: totalIncome 666 EUR")


if __name__ == "__main__":
    main()
