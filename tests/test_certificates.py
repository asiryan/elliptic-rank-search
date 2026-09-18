"""Offline proof replay and rejection of altered evidence; GP is not needed."""
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from elliptic_rank_search.certificates.torsion_certificate import verify_certificate
from research.common.catalogue import verify_examples

ROOT = Path(__file__).resolve().parents[1]


class PublishedCertificateTests(unittest.TestCase):
    def setUp(self):
        folder = ROOT / 'research/known_curve_improvements/cases/icarm-199'
        self.data = json.loads((folder / 'points.json').read_text())
        self.cert = json.loads((folder / 'certificate.json').read_text())

    def test_all_improvements_replay_without_external_programs(self):
        from unittest.mock import patch
        with patch('subprocess.run', side_effect=AssertionError('External process in proof replay')):
            claims = verify_examples()
        self.assertEqual([(r['icarm_id'], r['rank_lower_bound']) for r in claims],
                         [(199, 15), (206, 14), (212, 13)])

    def test_altered_point_or_rank_claim_is_rejected(self):
        data = copy.deepcopy(self.data)
        data['points'][0][0] = '0'
        with self.assertRaises(ValueError):
            verify_certificate(data, self.cert)
        cert = copy.deepcopy(self.cert)
        cert['rank_lower_bound'] += 1
        with self.assertRaises(ValueError):
            verify_certificate(self.data, cert)

    def test_altered_character_bit_is_rejected(self):
        cert = copy.deepcopy(self.cert)
        row = cert['independent_rows'][0]
        row['bits'] = str(1 - int(row['bits'][0])) + row['bits'][1:]
        with self.assertRaisesRegex(ValueError, 'Incorrect character row'):
            verify_certificate(self.data, cert)

    def test_even_multiple_seed_retains_its_singleton_proof(self):
        from fractions import Fraction as Q
        import tempfile
        from unittest.mock import patch
        from elliptic_rank_search.arithmetic.point_arithmetic import multiply
        from elliptic_rank_search.certificates.torsion_certificate import certify
        from elliptic_rank_search.search.seeded import independent_result
        a = [0, 0, 0, -25, 4]
        twice = multiply(a, (Q(0), Q(2)), 2)
        data = {'ainvs': list(map(str, a)), 'points': [list(map(str, twice))]}
        with tempfile.TemporaryDirectory() as raw:
            source = Path(raw) / 'input.json'
            source.write_text(json.dumps(data))
            with patch('subprocess.run', side_effect=AssertionError('External process in singleton proof')):
                selected = certify(source)
                result = independent_result({**data, 'points': selected['points']}, selected['LowerBound'])
                claim = verify_certificate(result, result['certificate'])
        self.assertEqual(claim['rank_lower_bound'], 1)
        self.assertTrue(claim['all_points_independent_modulo_torsion'])


if __name__ == '__main__':
    unittest.main()
