#!/usr/bin/env python3
"""Запуск проекта на Timeweb Cloud."""
import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    python = sys.executable
    port = os.environ.get('PORT', '8000')
    workers = os.environ.get('GUNICORN_WORKERS', '2')

    subprocess.check_call([python, 'manage.py', 'migrate', '--noinput'], cwd=root)
    subprocess.check_call([python, 'manage.py', 'collectstatic', '--noinput'], cwd=root)
    subprocess.check_call([python, 'manage.py', 'init_site'], cwd=root)

    os.execvp(
        'gunicorn',
        [
            'gunicorn',
            'retro_cameras.wsgi:application',
            '--bind', f'0.0.0.0:{port}',
            '--workers', workers,
            '--timeout', '120',
        ],
    )


if __name__ == '__main__':
    main()
