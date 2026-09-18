"""Installed code resources and the caller's explicitly scoped workspace."""
import hashlib
import json
import os
from pathlib import Path
import shutil

PACKAGE_ROOT = Path(__file__).resolve().parent
ROOT = Path(os.environ.get('ERS_WORKSPACE', Path.cwd())).resolve()
DATA_ROOTS = (ROOT, *(Path(p).resolve() for p in json.loads(os.environ.get('ERS_DATA_ROOTS', '[]'))))
GP = os.environ.get('PARI_GP') or shutil.which('gp') or 'gp'


def code_hashes():
    return {p.relative_to(PACKAGE_ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(PACKAGE_ROOT.rglob('*.py'))}
