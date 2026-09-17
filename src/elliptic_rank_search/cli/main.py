"""Command dispatcher for the study-independent library."""
import argparse
import runpy
import sys

COMMANDS = {
    'search': 'elliptic_rank_search.cli.run',
    'seeded': 'elliptic_rank_search.search.seeded',
    'verify': 'elliptic_rank_search.cli.verify',
    'doctor': 'elliptic_rank_search.cli.doctor',
    'first-cover': 'elliptic_rank_search.search.first_cover',
    'first-jet': 'elliptic_rank_search.search.first_jet',
}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description='General rational-point search and exact certificate replay.')
    parser.add_argument('command', choices=COMMANDS)
    if not argv or argv[0] in ('-h', '--help'):
        parser.print_help()
        return
    command = parser.parse_args(argv[:1]).command
    previous = sys.argv
    try:
        sys.argv = ['ers ' + command] + argv[1:]
        runpy.run_module(COMMANDS[command], run_name='__main__')
    finally:
        sys.argv = previous
