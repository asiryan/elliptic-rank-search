"""Run the three single-seed ICARM examples and verify every resulting proof."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

from bootstrap import save
from runtime import ROOT
from torsion_certificate import verify_certificate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'runs/reproduction')
    parser.add_argument('--seconds', type=float, default=30, help='Search budget per curve')
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--anchors', type=int, default=16)
    args = parser.parse_args()
    if not (0 < args.seconds <= 7200 and 1 <= args.workers <= 24 and 1 <= args.anchors <= 4096):
        parser.error('Invalid bounded search settings')
    output = args.output.resolve()
    if output == ROOT or not output.is_relative_to(ROOT):
        parser.error('Use a dedicated output directory inside this project')
    rows = json.loads((ROOT / 'examples/summary.json').read_text())['curves']
    results = []
    for row in rows:
        name = f"icarm-{row['icarm_id']}"
        folder = output / name
        started = time.perf_counter()
        # Only a curve and one declared seed are passed to the search process.
        # Stored proof witnesses are never inputs to this command.
        subprocess.run([sys.executable, str(ROOT / 'seeded.py'),
                        '--input', str(ROOT / 'examples' / name / 'seed.json'),
                        '--output', str(folder), '--seconds', str(args.seconds),
                        '--workers', str(args.workers), '--anchors', str(args.anchors),
                        '--target', str(row['rank_lower_bound'])], check=True)
        data = json.loads((folder / 'result.json').read_text())
        claim = verify_certificate(data, data['certificate'])
        reached = (claim['rank_lower_bound'] >= row['rank_lower_bound'] and
                   claim['all_points_independent_modulo_torsion'])
        result = {'icarm_id': row['icarm_id'], 'target': row['rank_lower_bound'],
                  **claim, 'target_reached': reached,
                  'process_seconds': time.perf_counter() - started}
        results.append(result)
        save(output / 'verification.json', results)
    print(json.dumps(results, indent=2))
    if not all(row['target_reached'] for row in results):
        raise SystemExit('A target was not reached within the budget; increase --seconds and resume.')


if __name__ == '__main__':
    main()
