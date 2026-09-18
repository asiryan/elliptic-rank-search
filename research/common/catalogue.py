"""Read research cases and replay their mathematical proof witnesses offline."""
import json
from pathlib import Path

from elliptic_rank_search.certificates.torsion_certificate import verify_certificate

RESEARCH = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def cases(study='all', case=None, controls=False):
    rows = read(RESEARCH / 'catalogue.json')['cases']
    return [r for r in rows if (case is not None and r['id'] == case or
            case is None and (study == 'all' or r['study'] == study) and
            (controls or r['kind'] != 'control'))]


def case_folder(row):
    path = (RESEARCH / row['path']).resolve()
    if not path.is_relative_to(RESEARCH.resolve()):
        raise ValueError('Catalogue case path escapes the study resources')
    return path


def verify_case(row):
    folder = case_folder(row)
    points = read(folder / 'points.json')
    if points['ainvs'] != read(folder / 'equation.json')['ainvs']:
        raise ValueError('Witnesses use a different curve model')
    proof = verify_certificate(points, read(folder / 'certificate.json'))
    if not proof['all_points_independent_modulo_torsion'] or proof['rank_lower_bound'] != row['rank_lower_bound']:
        raise ValueError(f'{row["id"]}: claimed bound was not verified')
    return {'id': row['id'], 'icarm_id': row['icarm_id'], **proof}


def verify_examples():
    return [verify_case(row) for row in cases('known_curve_improvements')]
