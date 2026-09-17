"""Compatibility launcher; implementation lives in src/elliptic_rank_search."""
from pathlib import Path
import runpy
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
if __name__ == '__main__' and '--examples' in sys.argv:
    from research.common.cli import main
    main(['verify', '--study', 'known_curve_improvements'])
elif __name__ == '__main__':
    runpy.run_module('elliptic_rank_search.cli.verify', run_name='__main__')
else:
    from research.common.catalogue import verify_examples
