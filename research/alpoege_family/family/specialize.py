"""Exact specialization of the archived generic formulas; no result witnesses."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from elliptic_rank_search.search.bootstrap import gp, prefix
from elliptic_rank_search.search.search_policy import clean
from elliptic_rank_search.certificates.certificate import validate_curve_and_points
from elliptic_rank_search.certificates.torsion_certificate import select_basis, verify_certificate

DATA = Path(__file__).with_name('sections.json')


def family(u, v):
    l = 446667*u*u + 471466*u*v + 239031*v*v
    p = 318552*u*u + 368554*u*v - 72570*v*v
    q = 733413*u*u - 45082*u*v - 14960*v*v
    d = 5*(7174492962*u**4 - 7114589515*u**3*v - 22069002960*u*u*v*v + 3909144679*u*v**3 - 205134150*v**4)
    e = 882769396002*u**4 + 811447034567*u**3*v - 1174040743*u*u*v*v - 32493137198*u*v**3 - 2386325360*v**4
    b = p*q*(l+p+q) - p*e - q*d
    return list(map(F, [-l, d+e, -b, d*e, 0]))


def invariants(a):
    a1, a2, a3, a4, a6 = map(F, a)
    b2 = a1*a1+4*a2
    b4 = a1*a3+2*a4
    b6 = a3*a3+4*a6
    c4 = b2*b2-24*b4
    c6 = -b2**3+36*b2*b4-216*b6
    return c4, c6, (c4**3-c6**2)/1728


def check_change(original, minimal, change):
    A = list(map(F, original))
    a = list(map(F, minimal))
    scale, r, s, t = map(F, change)
    expected = [(A[0]+2*s)/scale,
                (A[1]-s*A[0]+3*r-s*s)/scale**2,
                (A[2]+r*A[0]+2*t)/scale**3,
                (A[3]-s*A[2]+2*r*A[1]-(t+r*s)*A[0]+3*r*r-2*s*t)/scale**4,
                (A[4]+r*A[3]+r*r*A[1]+r**3-t*A[2]-r*t*A[0]-t*t)/scale**6]
    if a != expected:
        raise ValueError('Minimal-model change does not satisfy its exact identities')


def specialize(u, v, seconds=10):
    if v == 0:
        u, v = 1, 0
    else:
        parameter = F(u, v)
        u, v = parameter.numerator, parameter.denominator
    original = family(u, v)
    if not invariants(original)[2]:
        raise ValueError('Singular specialization')
    sections = json.loads(DATA.read_text(encoding='utf-8'))['sections']
    points = [[sum(F(c)*u**i*v**(degree-i) for i, c in enumerate(section[key]))
               for key, degree in [('x_coeffs', 4), ('y_coeffs', 6)]] for section in sections]
    validate_curve_and_points({'ainvs': list(map(str, original)), 'points': points})
    script = prefix(original) + ('M=ellminimalmodel(E,&change);'
              'print("MINIMAL ",vector(5,i,Str(M[i])));'
              'print("CHANGE ",vector(4,i,Str(change[i])));print("FINISHED");quit;\n')
    out, _ = gp(script, seconds)
    if 'FINISHED' not in out:
        raise RuntimeError('Minimal-model preparation exceeded its budget')
    records = {line.split(' ', 1)[0]: line.split(' ', 1)[1] for line in out.splitlines() if ' ' in line}
    minimal = json.loads(records['MINIMAL'])
    change = json.loads(records['CHANGE'])
    check_change(original, minimal, change)
    scale, r, s, t = map(F, change)
    mapped = [[str((x-r)/scale**2), str((y-s*(x-r)-t)/scale**3)] for x, y in points]
    seed = clean({'ainvs': minimal, 'points': mapped})
    proof = select_basis(seed, max_prime=2000)
    verified = verify_certificate(proof, proof['certificate'])
    metadata = {'parameter': str(F(u, v)) if v else 'infinity', 'u': u, 'v': v,
                'section_count': len(sections), 'specialized_points': len(seed['points']),
                'seed_lower_bound': verified['rank_lower_bound'], 'change': change,
                'exact_model_change_verified': True,
                'sections_sha256': hashlib.sha256(DATA.read_bytes()).hexdigest()}
    return seed, metadata


def verify_sections():
    """Polynomial identities over Q[T], checked using exact rational coefficients."""
    def add(*polys):
        out = [F(0)] * max(map(len, polys))
        for poly in polys:
            for i, value in enumerate(poly):
                out[i] += value
        return out
    def mul(a, b):
        out = [F(0)] * (len(a)+len(b)-1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i+j] += x*y
        return out
    def scale(a, n):
        return [n*x for x in a]
    l = list(map(F, [239031, 471466, 446667]))
    p = list(map(F, [-72570, 368554, 318552]))
    q = list(map(F, [-14960, -45082, 733413]))
    d = scale(list(map(F, [-205134150, 3909144679, -22069002960, -7114589515, 7174492962])), 5)
    e = list(map(F, [-2386325360, -32493137198, -1174040743, 811447034567, 882769396002]))
    b = add(mul(mul(p, q), add(l, p, q)), scale(mul(p, e), -1), scale(mul(q, d), -1))
    sections = json.loads(DATA.read_text(encoding='utf-8'))['sections']
    for section in sections:
        x = list(map(F, section['x_coeffs']))
        y = list(map(F, section['y_coeffs']))
        residual = add(mul(y, y), scale(mul(l, mul(x, y)), -1), scale(mul(b, y), -1),
                       scale(mul(mul(x, x), x), -1), scale(mul(add(d, e), mul(x, x)), -1),
                       scale(mul(mul(d, e), x), -1))
        if any(residual):
            raise ValueError('A supplied generic section is not on the family')
    return {'sections_checked': len(sections), 'exact_polynomial_identities': True,
            'sha256': hashlib.sha256(DATA.read_bytes()).hexdigest()}
