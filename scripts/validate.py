#!/usr/bin/env python3
"""Validate the blocklist files before they reach Pi-hole.

Checks every lists/*.txt file:
  - header lines start with '#', the "# Entries: N" header matches the count
  - each entry is a lowercase FQDN (no IPs, wildcards, URLs, ports, spaces)
  - no duplicates, entries sorted
Exits 1 on the first file with errors; all errors are printed.
"""
import ipaddress
import re
import sys
from pathlib import Path

LABEL = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)$")
TLD = re.compile(r"^(?:[a-z]{2,63}|xn--[a-z0-9-]{1,59})$")
ENTRIES = re.compile(r"^# Entries: (\d+)$")


def is_fqdn(name: str) -> bool:
    if len(name) > 253 or "." not in name:
        return False
    try:
        ipaddress.ip_address(name)
        return False
    except ValueError:
        pass
    labels = name.split(".")
    return all(LABEL.match(l) for l in labels) and bool(TLD.match(labels[-1]))


def check(path: Path) -> list[str]:
    errors, entries, declared = [], [], None
    for no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            m = ENTRIES.match(line)
            if m:
                declared = int(m.group(1))
            continue
        if raw != line:
            errors.append(f"{path}:{no}: leading/trailing whitespace")
        if not is_fqdn(line):
            errors.append(f"{path}:{no}: not a lowercase FQDN: {line!r}")
        entries.append(line)

    seen = set()
    for e in entries:
        if e in seen:
            errors.append(f"{path}: duplicate entry {e}")
        seen.add(e)
    if entries != sorted(entries):
        errors.append(f"{path}: entries are not sorted")
    if declared is None:
        errors.append(f"{path}: missing '# Entries: N' header")
    elif declared != len(entries):
        errors.append(f"{path}: header says {declared} entries, file has {len(entries)}")
    return errors


def main() -> int:
    files = sorted(Path("lists").glob("*.txt"))
    if not files:
        print("no lists/*.txt files found")
        return 1
    errors = [e for f in files for e in check(f)]
    for e in errors:
        print(e)
    for f in files:
        print(f"{f}: ok" if not any(e.startswith(str(f)) for e in errors) else f"{f}: FAILED")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
