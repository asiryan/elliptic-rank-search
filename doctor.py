"""Compatibility launcher; implementation lives in src/elliptic_rank_search."""
from pathlib import Path
import runpy
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
if __name__ == '__main__':
    runpy.run_module('elliptic_rank_search.cli.doctor', run_name='__main__')
else:
    from importlib import import_module
    sys.modules[__name__] = import_module('elliptic_rank_search.cli.doctor')
