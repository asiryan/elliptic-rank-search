"""Replay exact rank certificates using only the Python standard library."""
import argparse
import json
from pathlib import Path

from elliptic_rank_search.certificates.torsion_certificate import verify_certificate


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', type=Path,
                        help='A result with an embedded certificate, or a points JSON')
    parser.add_argument('--certificate', type=Path, help='A separate certificate JSON')
    args = parser.parse_args()
    if args.input is None:
        parser.error('Supply a points/result file and, if needed, --certificate')
    data = read(args.input)
    cert = read(args.certificate) if args.certificate else data.get('certificate')
    if cert is None:
        parser.error('Input has no certificate; supply --certificate')
    result = verify_certificate(data, cert)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
