#!/usr/bin/env python3
import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "src" / "dimans" / "__init__.py"
VERSION_RE = re.compile(r'^(__version__\s*=\s*["\'])(\d+)\.(\d+)\.(\d+)(["\'])$', re.M)


def read_version() -> tuple[int, int, int]:
    match = VERSION_RE.search(VERSION_FILE.read_text())
    if not match:
        raise SystemExit(f"could not find __version__ in {VERSION_FILE}")
    return tuple(int(part) for part in match.group(2, 3, 4))


def bump_version(part: str, major: int, minor: int, patch: int) -> tuple[int, int, int]:
    if part == "major":
        return major + 1, 0, 0
    if part == "minor":
        return major, minor + 1, 0
    return major, minor, patch + 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bump the dimans version in src/dimans/__init__.py"
    )
    parser.add_argument("part", choices=["patch", "minor", "major"])
    args = parser.parse_args()

    current = read_version()
    new_version = bump_version(args.part, *current)
    new_str = ".".join(str(part) for part in new_version)

    path = VERSION_FILE
    content = path.read_text()
    replaced = VERSION_RE.sub(rf"\g<1>{new_str}\g<5>", content, count=1)
    path.write_text(replaced)

    print(f"bumped {'.'.join(map(str, current))} -> {new_str}")


if __name__ == "__main__":
    main()
