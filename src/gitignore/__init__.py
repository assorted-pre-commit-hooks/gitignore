# SPDX-FileCopyrightText: 2026 Karl Wette
#
# SPDX-License-Identifier: MIT

"""pre-commit hook to sanitise Git ignore files."""

import argparse
from pathlib import Path
from typing import Sequence

__author__ = "Karl Wette"


class InvalidGitignoreEntry(Exception):
    """Raise on an invalid Git ignore file entry."""


def read_gitignore(filepath: Path):
    """Git ignore file entries."""
    with filepath.open("r", encoding="UTF-8") as f:
        return [line.strip() for line in f]


def main(argv: Sequence[str] | None = None) -> int:
    """Main function."""

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    entries = {}

    # Read in .gitignore files
    for filename in args.filenames:
        filepath = Path(filename)
        key = filepath.absolute()
        entries[key] = read_gitignore(filepath)

    # Iterate over .gitignore files
    for filename in args.filenames:
        filepath = Path(filename)
        key = filepath.absolute()

        # Iterate over entries in .gitignore files
        new_entries = []
        for entry in entries[key]:
            p = Path(entry)
            if entry.endswith("/"):
                s = "/"
            else:
                s = ""

            # Entries referring to parent directories are forbidden
            if p.parts[0] == "..":
                msg = f"{filename}: Git ignore entry cannot refer to parent directory ({p})"
                raise InvalidGitignoreEntry(msg)

            # If entry is a path, check if there's a .gitignore in a subdirectory it should go into
            if len(p.parts) > 1:
                full_p = filepath.parent / p
                for n in range(1, len(p.parts)):
                    move_to_filepath = (
                        filepath.parent / Path(*p.parts[0:n]) / ".gitignore"
                    )
                    if move_to_filepath.is_file():
                        entry_p = full_p.relative_to(move_to_filepath.parent)
                        if p.is_absolute():
                            entry_p = Path("/") / entry_p
                        move_to_key = move_to_filepath.absolute()
                        if move_to_key not in entries:
                            entries[move_to_key] = read_gitignore(move_to_filepath)
                        entries[move_to_key].append(str(entry_p) + s)
                        break
                if move_to_filepath.is_file():
                    continue

            # Write entry to the current .gitignore
            new_entries.append(entry)

        entries[key] = new_entries

    # Write out .gitignore files
    for filepath in entries:
        with filepath.open("w", encoding="UTF-8") as f:
            for entry in sorted(entries[filepath]):
                print(entry, file=f)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
