"""Find and remove all repositories that don't have any local changes.
"""
from __future__ import annotations
from pathlib import Path
import shutil
import subprocess


def run(path: Path, args: str) -> list[str]:
    res = subprocess.run(
        ['git'] + args.split(),
        check=True,
        cwd=str(path),
        stdout=subprocess.PIPE,
    )
    return res.stdout.decode().splitlines()


def is_dirty(path: Path) -> bool:
    return bool(run(path, 'status --short'))


def one_remote(path: Path) -> bool:
    return len(run(path, 'remote')) == 1


def one_branch(path: Path) -> bool:
    return len(run(path, 'branch')) == 1


def all_pushed(path: Path) -> bool:
    return not run(path, 'log --branches --not --remotes')


def main() -> None:
    for path in (Path.home() / 'Documents').iterdir():
        if not (path / '.git').exists():
            continue
        if is_dirty(path):
            continue
        if not one_remote(path):
            continue
        if not one_branch(path):
            continue
        if not all_pushed(path):
            continue
        print(path)
        shutil.rmtree(path)


main()
