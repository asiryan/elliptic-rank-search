"""Compatibility command for the original three single-seed experiments."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
from research.common.catalogue import cases
from research.common.runner import reproduce


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('runs/reproduction'))
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--anchors', type=int, default=16)
    args = parser.parse_args()
    if not (0 < args.seconds <= 7200 and 1 <= args.workers <= 24 and 1 <= args.anchors <= 4096):
        parser.error('Invalid bounded search settings')
    reproduce(cases('known_curve_improvements'), args.output, seconds=args.seconds,
              overrides={'workers': args.workers, 'anchors': args.anchors})


if __name__ == '__main__':
    main()
