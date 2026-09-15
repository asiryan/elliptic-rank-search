"""Portable project paths and PARI/GP executable selection."""
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
# An explicit path is useful on Windows, where `gp` is a PowerShell alias.
# subprocess executes the binary directly and never invokes a shell.
GP = os.environ.get('PARI_GP') or shutil.which('gp') or 'gp'
