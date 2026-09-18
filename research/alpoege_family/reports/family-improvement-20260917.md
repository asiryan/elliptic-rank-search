# Can the ICARM302 family be improved for record searches?

September 17, 2026. A bounded study of the geometry and two computational pilot experiments.

**Faster discovery of new records has not been established.** Specific changes to the family were constructed and checked, going beyond broader enumeration of T. Imposing extra points gives inexpensive lower bounds of 18-19, but did not improve the final rank found in the paired pilot. A different elliptic fibration on the same surface does produce curves outside the original family, but the tested version has a lower generic rank and larger coefficients in the chosen coordinates.

Practical decision: neither of these two approaches currently warrants a large computational budget. The next search for an improved family should assess generic rank, arithmetic sizes of specializations and the actual yield of high ranks within equal time budgets together.

## What was already known

The retained audit confirms our earlier result **rank E(Q(T)) = 17**. It checks 17 sections, their height matrix with determinant 1092, and a squarefree discriminant of degree 24. It has not been established that the lattice they generate has index one in the full section lattice; this is not required for the rank proof.

Rank 17 is maximal for an elliptic K3 surface over Q(T). This restriction concerns the generic rank within that geometric class, not ranks of individual curves over Q or search efficiency. [Elkies, 2026, introduction and Theorem 1](https://arxiv.org/html/2608.25406v1).

Thus, one cannot simply adjust the coefficients of this K3 model, remain in the same class and obtain generic rank 18. One can change the base, choose another fibration or seek another surface. These are different operations with different costs.

The earlier searches were substantial:

| Retained experiment | What was actually checked |
|---|---|
| rank26-plus-20260916 | Sieved 5 102 343 rational parameters of height ≤2048 and another 2 million random parameters; 159 point searches on 150 parameters; no new bounds ≥26, best new result ≥25 |
| high-height-20260916 | 6 million random parameters of height ≤2 million; 224 sieve finalists; 10 searches of 300 seconds each: nine stayed at bound 17, one reached 18 |
| small-t-audit-20260917 | Enumerated all 5039 parameters of height ≤64, but point searches had been run for only 634 at the time of the audit |

This is evidence of the tested strategy's low yield. It does not prove that the family is exhausted: sieving does not determine rank, and a lower bound that stops improving is not an upper bound.

## Extra points from quadratic conditions

The 318 quadratic sections constructed earlier gave 126 distinct conditions z²=h(T). Satisfying a condition supplies an explicit rational point on the curve. Its independence from the specialized original sections was checked separately.

Exhaustive enumeration of 20 087 rational T=u/v with max(|u|,v)≤128 found 244 parameters on these covers. Square testing took 0.61 seconds once the conditions were prepared. Preparing the curves, adding points, producing certificates and computing diagnostic heights for these 244 parameters took about 19 seconds in total.

At 112 parameters, the added points improved the certified initial lower bound. This produced 106 initial bounds of 18 and two bounds of 19; the remaining improvements started from smaller certified bounds. Failure to improve the certificate does not by itself prove that a new point is dependent.

Two compact examples with initial bound 19:

| T | Two conditions | Logarithmic height of the minimal curve |
|---|---|---:|
| 22/87 | Covers 235 and 251 | 248.68 |
| 34/125 | Covers 126 and 146 | 271.40 |

For the first example, the conditions are

\[
z_1^2=2621951051076+8268590077188T+6460014767761T^2,
\]
\[
z_2^2=592140288609-1755202210890T+1763969844025T^2.
\]

Satisfying both defines a smooth genus-1 curve. Auxiliary elliptic models were constructed for both pairs, with unconditionally certified ranks ≥2 and ≥3 respectively. Nineteen points over their function fields are independent: exact certificates establish independence at the listed specializations. This gives families of generic rank ≥19 over an elliptic base and infinitely many rational parameters. It does not assert rank 19 over Q(T).

**The problem is the arithmetic size of the parameters.** In the available parametrizations of individual covers, even with input parameter height ≤16, the median output height of T was 7 763 655 297. Of 40 320 evaluations, 2915 distinct T had height ≤2 million. On the two auxiliary elliptic curves, the small point combinations tested produced no additional T with numerators and denominators of at most 12 digits: only the original examples qualified. This is a bounded search and an observation about the chosen coordinates, not a proof that such growth is unavoidable.

**A particularly significant limitation:** the record parameter T=164518/924945 satisfies none of these 126 conditions. The same is true of three other strong parameters checked: -311/519, -6486/7309 and 936/811. Replacing the entire search with these covers would therefore exclude known successful curves. Extra generic rank alone does not guarantee a more favorable distribution of rare rank jumps.

## Do 18-19 initial points help the search engine?

Eight curves were selected before searching: two intersections of pairs of covers and six individual covers with the lowest curve height, initial certified bound 17 and a confirmed extra point. Each curve had two runs: one with only the 17 original points, and one with the geometrically enlarged set.

Settings were identical: 12 seconds of search, 2 worker processes, 256 anchors and adaptive mode. Runs were sequential, alternating the order of the two variants. The search engine was unchanged.

| T | Starting from 17: final bound | Starting from 18-19: final bound |
|---|---:|---:|
| 22/87 | 20 | 20 |
| 34/125 | 20 | 20 |
| 4/3 | 19 | 19 |
| 3/31 | 19 | 19 |
| 6 | 18 | 18 |
| -35/33 | 18 | 18 |
| -17/35 | 20 | 20 |
| 2/35 | 19 | 19 |

All numbers are unconditional certified lower bounds, not computed exact ranks. Within this budget, the final bounds were identical in 8 of 8 pairs. This is not statistical proof of equal effectiveness, nor a comparison of record frequency between two parameter distributions. Extra-point preparation was excluded from the 12-second budget. The first time each intermediate rank bound was reached was not compared separately.

## Another elliptic fibration on the same surface

A more substantial change was tested: the old parameter T becomes a coordinate within the new curve, and a different rational function on the surface defines the new family.

The construction uses the section P=P₂−P₅ of height 8 and the divisor O+P. In the model obtained by completing the square,

\[
Y^2=x^3+A_2x^2+A_4x+A_6
\]

write P=(N/l²,M/l³), deg l=2. Choose

\[
a_0\equiv-M/N\pmod{l^2},\quad c_0=(M+a_0N)/l^2,
\]
\[
a=a_0+kl^2,\quad c=c_0+kN,
\]
\[
u=A_2+(N-a^2)/l^2,\quad v=A_4+(2ac+Nu)/l^2.
\]

The new family is the quartic

\[
z^2=F(T,k)=\frac{u^2-4v}{l^2}.
\]

Its relation to the old surface is given by x=(-u+lz)/2 and Y=(ax-c)/l; the inverse expression for the new parameter is (lY-a₀x+c₀)/(l²x−N). All 60 rational sections used for the new quartic were checked by exact symbolic identities. The coefficients of F and the change of the new parameter were saved in fibration.json.

This fibration has generic rank **15**. The computed degrees of c₄,c₆,Δ are 8,12,22; the finite discriminant has one linear factor of multiplicity 2 and a squarefree factor of degree 20. The polynomials c₄ and Δ are coprime. The singular fibers are therefore 20 fibers of type I₁ and two of type I₂, one at infinity. Rational component classes of the two I₂ fibers occupy two dimensions in the Neron-Severi group. For the original fibration, its rational rank is 17+2=19; the Shioda-Tate formula for the new one gives 19−2−2=15. 15 points were independently certified on specializations.

This goes beyond the old rational specializations: for the new parameter s=-1/7, the equation j_old(T)=j_new has an irreducible numerator of degree 24, and T=∞ does not work either. Thus, this curve is not isomorphic, even over an algebraic closure, to any old curve at rational T. Its novelty relative to all prior work was not checked.

However, the arithmetic sizes were worse. In the table, h(E)=log max(|c₄|³,c₆²), with invariants taken on the global minimal model. This is a size measure, not the conductor or the canonical height of points.

| Family, 319 parameters of height ≤16 | Minimum h(E) | Median h(E) |
|---|---:|---:|
| Original, generic rank 17 | 147.01 | 218.97 |
| New, option 0, generic rank 15 | 194.73 | 304.96 |
| Another constructed variant, option 2 | 356.51 | 543.75 |

Equal parameter height depends on the chosen coordinates. The table assesses these specific curve generators; it does not prove that no reparametrization can improve the new variants.

Four exploratory runs of 15 seconds each, on the two curves with the smallest h(E) and the two with the best sums of local scores at primes 5…4093, gave:

| New s | Initial bound | Final bound |
|---|---:|---:|
| -1/7 | 15 | 15 |
| -2/11 | 14 | 14 |
| -7/15 | 15 | 16 |
| 4/9 | 15 | 15 |

The bound of 14 in the second row does not prove that this specialization has exact rank 14. The initial summary log incorrectly recorded the starting bound as a constant 15; it was corrected using the original certificate. The points, search and final certificate were unchanged.

## How to choose the next improvement

The proposed criterion is **the number of distinct curves with certified bound ≥26 per unit of computing time**, together with curve heights and the distribution of bounds reached. The threshold of 26 is a measurable intermediate criterion for our search history; it does not guarantee success at 32.

The next geometric candidate should first be assessed as follows:

1. Retain generic rank 17, or justify that smaller arithmetic sizes compensate for the loss of rank. The constructed rank-15 variant has not yet passed this test.
2. Optimize the parametrization for the sizes of minimal curves. A fractional linear change of T does not create new isomorphism classes, but can substantially change which curves are accessible within a bounded parameter height.
3. Seek other fibrations or other K3 surfaces with 17 explicitly verified sections. Arbitrary changes to the coefficients of the original formula do not preserve these sections.
4. Compare families over comparable h(E) ranges, with the same total budget for preparation, sieving, search and certification. Fix parameter selection before obtaining results; do not restrict the entire sample to covers that exclude the record controls.
5. Check whether the local score predicts additional rank at the given curve sizes. A large sieve score without accounting for height should not be treated as proof of high rank. [Elkies-Klagsbrun](https://arxiv.org/html/2003.00077) discuss how practical sieving efficiency depends on size and conductor.

The existing family already reaches the limit for one criterion: generic rank among elliptic K3 surfaces over Q. Whether it is optimal in computing cost per new record is unknown. The checks rule out two specific simple improvement hypotheses within these small budgets; a more effective family has not yet been found.

## Verification and reproduction

The summary data are in summary.json. The audit.py script rechecks 488 initial-set certificates, 16 paired-pilot results, the auxiliary elliptic curves, 4 results from the new fibration and its initial certificates, lattice data, source-material hashes and the unchanged search engine. Search data access and the input-set hash were checked during each pilot run.

From the repository root:

```text
python runs/family-improvement-20260917/audit.py
python runs/family-improvement-20260917/research.py construct
python runs/family-improvement-20260917/research.py scan --height 128
python runs/family-improvement-20260917/research.py prepare --source scan --height 128 --count 244
python runs/family-improvement-20260917/auxiliary.py
python runs/family-improvement-20260917/neighbor.py --option 0 --height 16
```

The two pilot launchers deliberately refuse to overwrite an existing experiment plan. Use a separate experiment directory to repeat a pilot. Full GP inputs, outputs, curve models, points and certificates were saved alongside them. Prototype files are not standalone final results; the final variants of the new fibration are in neighbor/option-0 and neighbor/option-2.
