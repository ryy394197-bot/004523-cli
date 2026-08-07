#!/usr/bin/env python3
"""重複檔名偵測與報告 CLI"""
from __future__ import annotations
import argparse, hashlib
from collections import defaultdict
from pathlib import Path

def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> None:
    p = argparse.ArgumentParser(description='重複檔名偵測與報告 CLI')
    p.add_argument("dir", type=Path)
    args = p.parse_args()
    groups: dict[str, list[Path]] = defaultdict(list)
    for f in args.dir.rglob("*"):
        if f.is_file():
            groups[file_hash(f)].append(f)
    for digest, files in groups.items():
        if len(files) > 1:
            print(f"# duplicate {digest[:12]}")
            for f in files:
                print(f"  {f}")

if __name__ == "__main__":
    main()
