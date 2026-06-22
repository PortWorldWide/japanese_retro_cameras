#!/usr/bin/env python3
"""Сборка проекта для Timeweb Cloud (не зависит от CRLF в shell-скриптах)."""
import subprocess
import sys
from pathlib import Path


def normalize_line_endings(path: Path) -> None:
    if not path.exists():
        return
    data = path.read_bytes().replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    path.write_bytes(data)


def main() -> None:
    root = Path(__file__).resolve().parent
    normalize_line_endings(root / 'requirements.txt')

    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt'],
        cwd=root,
    )
    subprocess.check_call(
        [sys.executable, 'manage.py', 'collectstatic', '--noinput'],
        cwd=root,
    )


if __name__ == '__main__':
    main()
