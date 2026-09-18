"""Reproduce claimed bounds from declared inputs in fresh, audited search processes."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from elliptic_rank_search.runtime import ROOT, code_hashes
from elliptic_rank_search.search.bootstrap import save
from elliptic_rank_search.certificates.torsion_certificate import verify_certificate
from elliptic_rank_search.search.search_policy import clean
from .catalogue import RESEARCH, read, case_folder


def prepare(row, folder):
    resources = case_folder(row)
    recipe = read(resources / 'reproduction.json')
    source = recipe['input']
    if source['kind'] == 'family_sections':
        from research.alpoege_family.family import specialize
        seed, details = specialize(source['u'], source['v'])
    elif source['kind'] == 'declared_seed':
        declared = (resources / source['file']).resolve()
        if not declared.is_relative_to(resources):
            raise ValueError('Declared seed path escapes the case')
        seed = read(declared)
        details = {'kind': 'declared_seed', 'initial_point_count': len(seed['points']),
                   'source_sha256': hashlib.sha256(declared.read_bytes()).hexdigest()}
    else:
        raise ValueError('Unrecognized reproduction input')
    if seed['ainvs'] != read(resources / 'equation.json')['ainvs']:
        raise ValueError('Regenerated model differs from the claimed curve')
    save(folder / 'initial.json', seed)
    save(folder / 'preparation.json', details)
    return recipe, seed


def run_case(row, output, seconds=None, continuation=False, overrides=None):
    folder = Path(output) / row['id']
    if folder.exists() and any(folder.iterdir()):
        raise ValueError(f'{folder}: fresh reproduction requires an empty directory')
    folder.mkdir(parents=True, exist_ok=True)
    recipe, seed = prepare(row, folder)
    stages = recipe['stages']
    if not stages:
        raise ValueError('A reproduction recipe needs at least one search stage')
    if overrides:
        stages = [dict(stage, **overrides) for stage in stages]
    if seconds is not None:
        stages = [dict(stages[0], seconds=seconds)]
    if continuation:
        # Explicit continuation experiment only, never labelled rediscovery.
        witness = read(case_folder(row) / 'points.json')
        verify_certificate(witness, read(case_folder(row) / 'certificate.json'))
        seed = {'ainvs': witness['ainvs'], 'points': witness['points']}
    initial_count = len(seed['points'])
    target = 100 if continuation else recipe['target']
    env = dict(os.environ, ERS_DATA_ROOTS=json.dumps([str(RESEARCH)]))
    started = time.perf_counter()
    records = []
    for index, options in enumerate(stages, 1):
        source = folder / f'stage-{index:02d}-input.json'
        stage = folder / f'stage-{index:02d}'
        save(source, {'ainvs': seed['ainvs'], 'points': seed['points']})
        command = [sys.executable, '-m', 'elliptic_rank_search.search.seeded', '--input', str(source),
                   '--output', str(stage), '--seconds', str(options['seconds']), '--workers', str(options['workers']),
                   '--anchors', str(options['anchors']), '--anchor-mode', options['mode'], '--target', str(target)]
        with (folder / f'stage-{index:02d}.stdout.txt').open('w', encoding='utf-8') as stdout, \
                (folder / f'stage-{index:02d}.stderr.txt').open('w', encoding='utf-8') as stderr:
            process = subprocess.run(command, env=env, stdout=stdout, stderr=stderr,
                                     timeout=options['seconds'] + 90)
        if process.returncode:
            raise RuntimeError(f'{row["id"]}: search exited {process.returncode}; inspect its stderr')
        result = read(stage / 'result.json')
        claim = verify_certificate(result, result['certificate'])
        reads = read(stage / 'data-reads.json')
        unexpected = [name for name in reads if Path(name).suffix not in ('.py', '.pyc') and
                      Path(name).resolve() != source.resolve() and not Path(name).resolve().is_relative_to(stage.resolve())]
        if unexpected:
            raise ValueError(f'Undeclared search data reads: {unexpected}')
        discoveries = [json.loads(line)['point'] for line in (stage / 'discoveries.jsonl').read_text(encoding='utf-8').splitlines()] \
                      if (stage / 'discoveries.jsonl').exists() else []
        allowed = set(map(tuple, clean({'ainvs': seed['ainvs'], 'points': seed['points'] + discoveries})['points']))
        if not set(map(tuple, clean(result)['points'])).issubset(allowed):
            raise ValueError('A result point is neither a declared seed nor a logged discovery')
        state = read(stage / 'checkpoint.json')
        records.append({'stage': index, 'settings': options, 'rank_lower_bound': claim['rank_lower_bound'],
                        'search_seconds': state['wall_seconds'], 'status': state['status'],
                        'data_boundary_checked': True, 'point_origins_checked': True,
                        'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
        seed = {'ainvs': result['ainvs'], 'points': result['points']}
        if not continuation and claim['rank_lower_bound'] >= recipe['target']:
            break
    save(folder / 'result.json', result)
    summary = {'id': row['id'], 'icarm_id': row['icarm_id'], 'target': recipe['target'],
               'rank_lower_bound': claim['rank_lower_bound'], 'target_reached': claim['rank_lower_bound'] >= recipe['target'],
               'experiment': 'continuation' if continuation else 'fresh_reproduction',
               'published_witnesses_used_as_input': continuation, 'initial_points': initial_count,
               'seconds': time.perf_counter()-started, 'stages': records, 'verification': claim,
               'code_sha256': code_hashes(), 'completed_at': datetime.now(timezone.utc).isoformat()}
    save(folder / 'verification.json', summary)
    print(json.dumps({k: summary[k] for k in ('id', 'target', 'rank_lower_bound', 'target_reached', 'seconds')}), flush=True)
    return summary


def reproduce(rows, output, parallel=1, seconds=None, continuation=False, overrides=None):
    output = Path(output).resolve()
    if output == ROOT or not output.is_relative_to(ROOT):
        raise ValueError('Use a dedicated output directory inside the current workspace')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use an empty output directory for the reproduction batch')
    output.mkdir(parents=True, exist_ok=True)
    save(output / 'plan.json', {'cases': [r['id'] for r in rows], 'parallel_curves': parallel,
                               'seconds_override': seconds, 'continuation': continuation,
                               'code_sha256': code_hashes()})
    results, errors = [], []
    with ThreadPoolExecutor(parallel) as pool:
        pending = {pool.submit(run_case, row, output, seconds, continuation, overrides): row for row in rows}
        for future in as_completed(pending):
            try:
                results.append(future.result())
            except Exception as error:
                failure = {'id': pending[future]['id'], 'error': str(error)}
                errors.append(failure)
                print(json.dumps(failure), flush=True)
            save(output / 'summary.json', {'results': results, 'errors': errors, 'expected': len(rows),
                                           'completed': len(results),
                                           'reached': sum(r['target_reached'] for r in results)})
    if errors or not all(r['target_reached'] for r in results):
        raise RuntimeError('Some reproduction targets were not reached; see the saved summary')
    return results
