"""Run a declared parameter sieve, then generate seeds from generic sections."""
import hashlib
from pathlib import Path
import subprocess
import time

from elliptic_rank_search.runtime import ROOT
from elliptic_rank_search.search.bootstrap import save
from research.alpoege_family.family import specialize
from .catalogue import read


def run_campaign(config, sieve, output):
    config, sieve, output = Path(config).resolve(), Path(sieve).resolve(), Path(output).resolve()
    if output == ROOT or not output.is_relative_to(ROOT):
        raise ValueError('Use a dedicated output directory inside the current workspace')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use an empty campaign output directory')
    options = read(config)
    kind = options['kind']
    if kind not in ('grid', 'sample'):
        raise ValueError('Campaign kind must be grid or sample')
    if not sieve.is_file():
        raise ValueError('Build src/parameter_sieve first and supply its DLL or executable')
    output.mkdir(parents=True, exist_ok=True)
    native = output / 'parameters'
    command = ['dotnet', str(sieve)] if sieve.suffix.lower() == '.dll' else [str(sieve)]
    command += [kind, '--output', str(native)]
    keys = ['height', 'keep', 'refine_keep', 'final_keep', 'prime_bound', 'workers']
    if kind == 'sample':
        keys += ['samples', 'seed', 'selection']
    for key in keys:
        command += ['--' + key.replace('_', '-'), str(options[key])]
    started = time.perf_counter()
    save(output / 'config.json', {'options': options,
         'config_sha256': hashlib.sha256(config.read_bytes()).hexdigest(),
         'sieve_sha256': hashlib.sha256(sieve.read_bytes()).hexdigest()})
    with (output / 'sieve.stdout.txt').open('w', encoding='utf-8') as stdout, \
            (output / 'sieve.stderr.txt').open('w', encoding='utf-8') as stderr:
        subprocess.run(command, check=True, stdout=stdout, stderr=stderr)
    candidates = read(native / 'candidates.json')
    generated = []
    for candidate in candidates:
        normalized = {k.lower(): v for k, v in candidate.items()}
        u, v = normalized['u'], normalized['v']
        seed, metadata = specialize(u, v)
        name = f'{u}_{v}'
        save(output / 'seeds' / (name + '.json'), seed)
        generated.append({'id': name, 'parameter': metadata['parameter'],
                          'control': bool(normalized.get('control', False)),
                          'score': normalized['score'], 'seed': f'seeds/{name}.json', **metadata})
        save(output / 'summary.json', {'candidates': generated, 'complete': False})
    summary = {'candidates': generated, 'complete': True, 'seconds': time.perf_counter()-started,
               'score_is_not_a_rank_bound': True, 'seed_points_from_generic_sections_only': True}
    save(output / 'summary.json', summary)
    return summary
