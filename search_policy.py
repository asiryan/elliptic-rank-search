"""Bounded, curve-independent anchor ordering and search boxes."""
from fractions import Fraction as Q
import random
from runtime import ROOT, GP
from point_arithmetic import on_curve, negate
from anchor_diversity import diverse_vectors

POLICY={'version':3,'area_exponents':[20,24,28,32,36,40],
        'denominator_exponents':[0,4,8,12,16,20],
        'model_order':'interleave coefficient size, anchor height, fixed shuffle',
        'random_seed':20260914,'batch_size':32,
        'rebuild_on_certified_growth':True,'reference_access':False,
        'anchor_enumeration':'half bounded best-first, half fixed support strata 2..8; at most 16*anchors vectors',
        'certificate_update':'previous independent basis plus newly observed points'}

def clean(data):
    a=list(map(Q,data['ainvs']))
    if len(a)!=5 or any(v.denominator!=1 for v in a):
        raise ValueError('This seeded search requires five integral Weierstrass coefficients')
    points=[]
    for p in data.get('points',[]):
        p=tuple(map(Q,p))
        if len(p)!=2 or not on_curve(a,p):raise ValueError('Invalid seed point')
        points.append(list(map(str,min(p,negate(a,p)))))
    points=sorted(set(map(tuple,points)),key=lambda p:(Q(p[0]),Q(p[1])))
    return {'ainvs':list(map(str,a)),'points':[list(p) for p in points]}

def order_models(models):
    rng=random.Random(POLICY['random_seed'])
    shuffled=list(models);rng.shuffle(shuffled)
    lists=[sorted(models,key=lambda m:(m['coefficient_bits'],m['anchor_height'],m['key'])),
           sorted(models,key=lambda m:(m['anchor_height'],m['coefficient_bits'],m['key'])),shuffled]
    result=[];seen=set()
    for group in zip(*lists):
        for m in group:
            if m['key'] not in seen:seen.add(m['key']);result.append(m)
    return result

def boxes():
    for area in POLICY['area_exponents']:
        for den in POLICY['denominator_exponents']:
            if 2*den<=area:yield 2**(area-den),2**den
