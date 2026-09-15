"""Replay exact rank certificates using only the Python standard library."""
import argparse
import json
from pathlib import Path

from torsion_certificate import verify_certificate


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def verify_examples():
    folder = Path(__file__).resolve().parent / 'examples'
    results = []
    for row in read(folder / 'summary.json')['curves']:
        example = folder / f"icarm-{row['icarm_id']}"
        data = read(example / 'points.json')
        claim = verify_certificate(data, read(example / 'certificate.json'))
        if (claim['rank_lower_bound'] != row['rank_lower_bound'] or
                not claim['all_points_independent_modulo_torsion']):
            raise ValueError(f"Example {row['icarm_id']} did not verify")
        results.append({'icarm_id': row['icarm_id'], **claim})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', type=Path,
                        help='A result with an embedded certificate, or a points JSON')
    parser.add_argument('--certificate', type=Path, help='A separate certificate JSON')
    parser.add_argument('--examples', action='store_true', help='Verify all three ICARM examples')
    args = parser.parse_args()
    if args.examples:
        if args.input or args.certificate:
            parser.error('--examples cannot be combined with input or --certificate')
        result = verify_examples()
    else:
        if args.input is None:
            parser.error('Supply an input or --examples')
        data = read(args.input)
        cert = read(args.certificate) if args.certificate else data.get('certificate')
        if cert is None:
            parser.error('Input has no certificate; supply --certificate')
        result = verify_certificate(data, cert)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
