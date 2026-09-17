"""Independent finite-field point counts and reproducibility of the native sieve."""
from fractions import Fraction
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))
from research.alpoege_family.family.specialize import family, invariants

DLL = ROOT / 'tools/parameter_sieve/bin/Release/net8.0/ParameterSieve.dll'


@unittest.skipUnless(DLL.exists() and shutil.which('dotnet'), 'Build tools/parameter_sieve with .NET 8 first')
class ParameterSieveTests(unittest.TestCase):
    def invoke(self, *args):
        subprocess.run(['dotnet', str(DLL), *map(str, args)], check=True, capture_output=True, text=True, timeout=120)

    def test_rescore_matches_independent_point_enumeration(self):
        parameters = [(0, 1), (1, 4), (-43, 75), (-265, 221), (164518, 924945)]
        primes = [p for p in range(5, 98) if all(p % d for d in range(2, math.isqrt(p)+1))]
        expected = []
        for u, v in parameters:
            a = list(map(int, family(u, v)))
            disc = int(invariants(a)[2])
            score = 0.0
            for p in primes:
                if disc % p == 0:
                    continue
                count = 1  # the point at infinity
                for x in range(p):
                    for y in range(p):
                        count += (y*y+a[0]*x*y+a[2]*y-x*x*x-a[1]*x*x-a[3]*x-a[4]) % p == 0
                score += math.log(count/p)
            expected.append(score)
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw)
            source = path / 'input.json'
            source.write_text(json.dumps([{'u': u, 'v': v} for u, v in parameters]))
            results = []
            for workers in (1, 4):
                output = path / f'result-{workers}.json'
                self.invoke('rescore', '--input', source, '--output', output, '--start', 0, '--prime-bound', 97, '--workers', workers)
                results.append(json.loads(output.read_text()))
            self.assertEqual(results[0], results[1])
            for row, score in zip(results[0], expected):
                self.assertAlmostEqual(row['score'], score, places=12)

    def test_grid_covers_primitive_parameters_and_thread_count_preserves_selection(self):
        with tempfile.TemporaryDirectory() as raw:
            results = []
            for workers in (1, 4):
                output = Path(raw) / str(workers)
                self.invoke('grid', '--height', 8, '--keep', 8, '--refine-keep', 4, '--final-keep', 2,
                            '--prime-bound', 16382, '--workers', workers, '--output', output)
                self.assertEqual(json.loads((output / 'run.json').read_text())['PrimitiveCount'],
                                 sum(math.gcd(u, v) == 1 for u in range(-8, 9) for v in range(1, 9)))
                results.append(json.loads((output / 'candidates.json').read_text()))
            self.assertEqual(results[0], results[1])
            self.assertEqual(sum(row['Control'] for row in results[0]), 1)

    def test_seeded_sampling_and_exact_j_invariants(self):
        with tempfile.TemporaryDirectory() as raw:
            results = []
            for workers in (1, 4):
                output = Path(raw) / str(workers)
                self.invoke('sample', '--height', 100, '--samples', 100, '--keep', 8, '--refine-keep', 4,
                            '--final-keep', 2, '--prime-bound', 16382, '--seed', 20260917,
                            '--selection', 'cumulative', '--workers', workers, '--output', output)
                results.append(json.loads((output / 'candidates.json').read_text()))
            self.assertEqual(results[0], results[1])
            for row in results[0]:
                c4, c6, disc = invariants(family(row['u'], row['v']))
                self.assertEqual(Fraction(row['j_invariant']), c4**3/disc)


if __name__ == '__main__':
    unittest.main()
