
"""Small, readable texter script.

Prints two integers (each on its own line):
  1) total number of words
  2) number of words whose first character is an uppercase letter

Usage:
  python texter.py [path]

If `path` is '-' the script reads from stdin. If omitted the script
will try to use `test.txt` in the same directory as the script.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Tuple, TextIO


def process_text(text: str) -> Tuple[int, int]:
    """Return (total_words, capitalized_words) for given text.

    A word is any sequence separated by whitespace. A word is counted
    as capitalized if its first character is an uppercase letter.
    """
    words = text.split()
    total = len(words)
    capital = sum(1 for w in words if w and w[0].isupper())
    return total, capital


class Texter:
    """Tiny wrapper around process_text to operate on file-like objects."""

    def run(self, fh: TextIO) -> Tuple[int, int]:
        return process_text(fh.read())


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Count words and capitalized words")
    p.add_argument("path", nargs="?", help="Path to text file or '-' for stdin")
    args = p.parse_args(argv)

    path = args.path
    if not path:
        default = Path(__file__).resolve().parent / "test.txt"
        if default.exists():
            path = str(default)
        else:
            p.print_usage()
            return 1

    if path == "-":
        fh = sys.stdin
    else:
        try:
            fh = open(path, "r", encoding="utf-8")
        except FileNotFoundError:
            print(f"Error: file not found: {path}", file=sys.stderr)
            return 2
        except OSError as exc:
            print(f"Error: could not read file: {exc}", file=sys.stderr)
            return 2

    try:
        total, capital = Texter().run(fh)
    finally:
        if fh is not sys.stdin:
            fh.close()

    print(total)
    print(capital)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

