"""Offline research catalogue, symbolic identities, and durable checkpoint tests."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))
from research.common import catalogue
from research.alpoege_family.family import specialize as specialize_function
from importlib import import_module
family = import_module('research.alpoege_family.family.specialize')
from elliptic_rank_search.search.bootstrap import save


class ResearchTests(unittest.TestCase):
    def test_all_publications_and_controls_replay_offline(self):
        with patch('subprocess.run', side_effect=AssertionError('Offline proof replay launched a process')):
            public = [catalogue.verify_case(r) for r in catalogue.cases()]
            all_rows = [catalogue.verify_case(r) for r in catalogue.cases(controls=True)]
        self.assertEqual(len(public), 21)
        self.assertEqual(len(all_rows), 23)
        self.assertEqual({r['icarm_id'] for r in public}, {199, 206, 212, *range(733, 751)})

    def test_generic_sections_are_exact_polynomial_identities(self):
        with patch('subprocess.run', side_effect=AssertionError('Symbolic check needs no GP')):
            self.assertEqual(family.verify_sections()['sections_checked'], 17)
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / 'sections.json'
            data = json.loads(family.DATA.read_text())
            data['sections'][0]['x_coeffs'][0] = '1'
            path.write_text(json.dumps(data))
            with patch.object(family, 'DATA', path), self.assertRaises(ValueError):
                family.verify_sections()

    def test_altered_case_resource_is_rejected_before_proof(self):
        row = catalogue.cases(case='icarm-733')[0]
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            original = catalogue.case_folder(row)
            info = catalogue.read(original / 'case.json')
            for name in [*info['files_sha256'], 'case.json']:
                (directory / name).write_bytes((original / name).read_bytes())
            (directory / 'reproduction.json').write_text('{}')
            with patch.object(catalogue, 'case_folder', return_value=directory), self.assertRaisesRegex(ValueError, 'hash mismatch'):
                catalogue.verify_case(row)

    def test_core_does_not_import_studies(self):
        for path in (ROOT / 'src/elliptic_rank_search').rglob('*.py'):
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.Import):
                    self.assertFalse(any(n.name.startswith('research') for n in node.names), path)
                elif isinstance(node, ast.ImportFrom):
                    self.assertFalse((node.module or '').startswith('research'), path)

    def test_transient_checkpoint_lock_is_retried(self):
        original = Path.replace
        calls = []
        def locked_once(source, target):
            calls.append(target)
            if len(calls) == 1:
                raise PermissionError('Transient reader')
            return original(source, target)
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / 'checkpoint.json'
            save(path, {'complete': 1})
            with patch.object(Path, 'replace', locked_once), patch('time.sleep'):
                save(path, {'complete': 2})
            self.assertEqual(json.loads(path.read_text()), {'complete': 2})
            self.assertEqual(len(calls), 2)

    def test_persistent_checkpoint_lock_preserves_previous_record(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / 'checkpoint.json'
            save(path, {'complete': 1})
            with patch.object(Path, 'replace', side_effect=PermissionError('Locked')), patch('time.sleep'), self.assertRaises(PermissionError):
                save(path, {'complete': 2})
            self.assertEqual(json.loads(path.read_text()), {'complete': 1})

    def test_fresh_recipes_use_declared_seeds_not_results(self):
        for row in catalogue.cases(controls=True):
            folder = catalogue.case_folder(row)
            source = catalogue.read(folder / 'reproduction.json')['input']
            if row['study'] == 'alpoege_family':
                self.assertEqual(source['kind'], 'family_sections')
                self.assertNotIn('file', source)
            else:
                self.assertEqual(source, {'kind': 'declared_seed', 'file': 'seed.json'})
                self.assertEqual(len(catalogue.read(folder / source['file'])['points']), 1)


if __name__ == '__main__':
    unittest.main()
