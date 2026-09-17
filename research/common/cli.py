"""Research commands with explicit case selection and fresh output directories."""
import argparse
import json
from pathlib import Path
from .catalogue import cases, verify_case


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('list', 'verify', 'reproduce', 'deepen', 'metrics'):
        cmd = sub.add_parser(name)
        cmd.add_argument('--study', default='all', choices=['all', 'known_curve_improvements', 'alpoege_family'])
        cmd.add_argument('--case')
        cmd.add_argument('--controls', action='store_true')
        if name in ('reproduce', 'deepen'):
            cmd.add_argument('--output', required=True, type=Path)
            cmd.add_argument('--parallel', type=int, default=1)
            cmd.add_argument('--seconds', type=float)
    sub.add_parser('sections')
    campaign = sub.add_parser('campaign')
    campaign.add_argument('--config', required=True, type=Path)
    campaign.add_argument('--sieve', required=True, type=Path)
    campaign.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command == 'campaign':
        from .campaign import run_campaign
        print(json.dumps(run_campaign(args.config, args.sieve, args.output), indent=2))
        return
    if args.command == 'sections':
        from research.alpoege_family.family import verify_sections
        print(json.dumps(verify_sections(), indent=2))
        return
    selected = cases(args.study, args.case, args.controls)
    if not selected:
        parser.error('No matching cases')
    if args.command == 'list':
        print(json.dumps(selected, indent=2))
    elif args.command == 'verify':
        result = [verify_case(row) for row in selected]
        print(json.dumps({'verified': len(result), 'results': result}, indent=2))
    elif args.command == 'metrics':
        from .metrics import verify_metrics
        print(json.dumps([verify_metrics(row) for row in selected], indent=2))
    else:
        if not 1 <= args.parallel <= 3 or args.seconds is not None and not 0 < args.seconds <= 7200:
            parser.error('Use 1..3 concurrent curves and a positive budget <=7200 seconds')
        from .runner import reproduce
        reproduce(selected, args.output, args.parallel, args.seconds, args.command == 'deepen')
