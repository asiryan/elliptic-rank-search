"""Rebuild every family input on its published model using GP only for minimization."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))
from research.alpoege_family.family import specialize
from research.common.catalogue import cases, read, case_folder


class FamilySpecializationTests(unittest.TestCase):
    def test_every_parameter_recreates_its_model_and_certifies_its_actual_seed_bound(self):
        for row in cases('alpoege_family', controls=True):
            with self.subTest(id=row['id']):
                folder = case_folder(row)
                source = read(folder / 'reproduction.json')['input']
                seed, metadata = specialize(source['u'], source['v'])
                self.assertEqual(seed['ainvs'], read(folder / 'equation.json')['ainvs'])
                self.assertEqual(metadata['section_count'], 17)
                self.assertEqual(metadata['seed_lower_bound'], 16 if row['icarm_id'] == 737 else 17)


if __name__ == '__main__':
    unittest.main()
