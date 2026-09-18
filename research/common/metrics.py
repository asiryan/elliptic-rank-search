"""Recompute model invariants and leaderboard heights; certify supplied bad primes."""
from decimal import Decimal
from fractions import Fraction

from elliptic_rank_search.search.bootstrap import gp, prefix, vec
from research.alpoege_family.family.specialize import invariants, check_change
from .catalogue import read, case_folder


def verify_metrics(row):
    folder = case_folder(row)
    a = read(folder / 'equation.json')['ainvs']
    expected = read(folder / 'invariants.json')
    for name, value in zip(('c4', 'c6', 'discriminant'), invariants(a)):
        if value != Fraction(expected[name]):
            raise ValueError(f'{row["id"]}: incorrect {name}')
    primes = expected.get('bad_primes') or []
    script = prefix(a) + 'default(realprecision,80);M=ellminimalmodel(E,&change);\n'
    script += 'print("MINIMAL ",vector(5,i,Str(M[i])));print("CHANGE ",vector(4,i,Str(change[i])));\n'
    script += 'print("HEIGHT ",log(max(abs(M.c4)^3,M.c6^2)));\n'
    script += 'print("FALTINGS ",-log(abs(imag(conj(M.omega[1])*M.omega[2])))/2);\n'
    if primes:
        script += ('P=' + vec(primes) + ';N=1;D=abs(M.disc);'
                   'for(i=1,#P,p=P[i];if(!isprime(p),error("Composite bad prime"));'
                   'if(D%p,error("Extraneous bad prime"));'
                   'while(D%p==0,D=D/p);N=N*p^elllocalred(M,p)[1]);'
                   'if(D!=1,error("Incomplete bad prime list"));print("CONDUCTOR ",N);\n')
    script += 'print("FINISHED");quit;\n'
    output, stats = gp(script, 120)
    if 'FINISHED' not in output:
        raise RuntimeError('Metric computation exceeded its budget')
    import json
    values = dict(line.split(' ', 1) for line in output.splitlines() if ' ' in line)
    minimal = json.loads(values['MINIMAL'])
    check_change(a, minimal, json.loads(values['CHANGE']))
    if list(map(Fraction, minimal)) != list(map(Fraction, a)):
        raise ValueError('Stored equation is not the normalized minimal model')
    for key, label in [('naive_height', 'HEIGHT'), ('faltings_height', 'FALTINGS')]:
        if expected.get(key) is not None and abs(Decimal(values[label])-Decimal(str(expected[key]))) > Decimal('1e-10'):
            raise ValueError(f'{row["id"]}: {key} differs from the snapshot')
    if primes and str(expected['conductor']) != values['CONDUCTOR']:
        raise ValueError('Conductor differs from supplied local-reduction evidence')
    return {'id': row['id'], 'minimal_model_verified': True, 'exact_invariants_verified': True,
            'naive_height': values['HEIGHT'], 'faltings_height': values['FALTINGS'],
            'conductor': values.get('CONDUCTOR'),
            'conductor_status': 'verified_from_proven_prime_factors' if primes else 'no_factorization_supplied',
            'real_precision_digits': 80, 'seconds': stats['seconds']}
