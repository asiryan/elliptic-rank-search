# Elliptic Rank Search

**A Python and PARI/GP implementation of adaptive rational-point search with exact, replayable rank lower-bound certificates.**

Given an integral Weierstrass equation over the rationals and, optionally, known rational points, the program searches for further points and selects a provably independent set. Its main mechanism is to build many quartic models by projecting from known points, search those models in bounded regions, and feed useful discoveries back into the search.

Python uses only its standard library. PARI/GP performs model reduction, bounded point searches, and arithmetic used to propose new models. The proof verifier uses Python alone. No other elliptic-curve library or runtime is required.

## Results

The table compares rank lower bounds from our saved ICARM snapshot (**Source**) with those certified by the included exact witnesses (**Proved**).

| Curve | Source | Proved | Gain | Evidence |
|---|:---:|:---:|:---:|---|
| [ICARM&nbsp;#199](https://elliptic-rank.icarm.cloud/curve/199) | 13 | **15** | +2 | [Points](examples/icarm-199/points.json), [certificate](examples/icarm-199/certificate.json) |
| [ICARM&nbsp;#206](https://elliptic-rank.icarm.cloud/curve/206) | 12 | **14** | +2 | [Points](examples/icarm-206/points.json), [certificate](examples/icarm-206/certificate.json) |
| [ICARM&nbsp;#212](https://elliptic-rank.icarm.cloud/curve/212) | 11 | **13** | +2 | [Points](examples/icarm-212/points.json), [certificate](examples/icarm-212/certificate.json) |

These are lower bounds for existing curves, not claims of their exact ranks or new world records. The comparison is with the recorded snapshot; the live leaderboard can change. Priority relative to all other publications has not been established.

The reproduction experiment starts each curve from **one known point**, supplied explicitly in `seed.json`. The remaining stored witness points are used only for proof replay. Each `equation.json` contains coefficients alone and can be used for a separate equation-only search; this table does not claim equation-only reproduction. See [example provenance](examples/README.md) and [validation](VALIDATION.md).

## Quick start

Run all commands from this directory. First, verify the three stored results; this needs **Python only**:

```sh
python verify.py --examples
```

Expected lower bounds: `15`, `14`, `13`. The verifier checks the curve equations, the modular character rows, their binary matrix ranks, and the torsion correction. It does not trust rank numbers in JSON.

To search, install Python 3.10 or newer and a recent [PARI/GP](https://pari.math.u-bordeaux.fr/download.html). No `pip install` is needed. Put `gp` on `PATH`, or set `PARI_GP` to the executable's full path:

```sh
# Linux / macOS, if gp is not already on PATH:
export PARI_GP=/path/to/gp
python doctor.py
```

```powershell
# Windows PowerShell:
$env:PARI_GP = 'C:\PARI\gp.exe'
python doctor.py
```

`doctor.py` checks the GP functions actually required, including quartic minimization and model changes. The tested environment is Python 3.12.0 and PARI/GP 2.19.0 development build `31236-59c418aa0c` on Windows. Compatibility with other GP builds is checked by the capability probe and test suite, not inferred from their version number.

Find points starting only from a small equation:

```sh
python run.py --input examples/toy/equation.json --output runs/toy --bootstrap-seconds 10 --search-seconds 10 --seed-limit 1 --target 2 --workers 2 --anchors 16
python verify.py runs/toy/result.json
```

Reproduce all three improvements from one declared point per curve:

```sh
python reproduce.py --output runs/reproduction --seconds 30
```

Or run one example:

```sh
python seeded.py --input examples/icarm-199/seed.json --output runs/icarm-199 --seconds 30 --workers 2 --anchors 16 --target 15
python verify.py runs/icarm-199/result.json
```

Search time depends on the machine, GP build, and scheduling. A time limit can be reached before the target. A missed target gives no upper bound on the curve's rank.

## The algorithm

### 1. Input and initial points

The curve is given by

$$
y^2+a_1xy+a_3y=x^3+a_2x^2+a_4x+a_6,
$$

with integral coefficients and nonzero discriminant. Rational numbers are serialized as exact strings, such as `"17/9"`, to preserve precision across tools.

The equation-only entry point accepts exactly one field:

```json
{"ainvs": ["0", "0", "0", "-25", "4"]}
```

It rejects points and extra metadata. The seeded entry point also takes `"points": [["0", "2"]]`; every point is checked on the input curve.

Write $b_2=a_1^2+4a_2$, $b_4=a_1a_3+2a_4$, and $b_6=a_3^2+4a_6$. For $x=n/d^2$ and $y=m/d^3$, an exact square test is

$$
z^2=4n^3+b_2n^2d^2+2b_4nd^4+b_6d^6,
\qquad z=2m+a_1nd+a_3d^3.
$$

Small-point enumeration uses modular square filters, then an integer square root and the parity condition for $m$. The bootstrap also minimizes the equation and explores coefficient-derived shifts, scales, and divisors of $b_6$. Every recovered point is mapped back and checked exactly. An optional tangent-lattice stage prioritizes additional candidates.

The current bootstrap selector is conservative: it requires a rootless good reduction to rule out rational 2-torsion. Curves with rational 2-torsion can instead be supplied a known non-torsion seed to the torsion-aware seeded engine. A bootstrap failure does not prove that there are no rational points.

### 2. Projection from one point

Set $V=2y+a_1x+a_3$, so

$$
V^2=f(x)=4x^3+b_2x^2+2b_4x+b_6.
$$

Let $P=(x_0,v_0)$ be a known point in these coordinates. Intersect the line $V=v_0+t(x-x_0)$ with the cubic. After removing the known root and writing $u=x-x_0$, the remaining quadratic is

$$
4u^2+(12x_0+b_2-t^2)u+f'(x_0)-2v_0t=0.
$$

Its discriminant produces the quartic

$$
z^2=D_P(t)=t^4-2(12x_0+b_2)t^2+32v_0t
             +b_2^2-8b_2x_0-48x_0^2-32b_4.
$$

The inverse map to the original Weierstrass equation is

$$
x=\frac{t^2-b_2-4x_0+z}{8},
\qquad y=\frac{v_0+t(x-x_0)-a_1x-a_3}{2}.
$$

For any rational point $Q$ with $x(Q)\ne x_0$, take

$$
t=\frac{V(Q)-v_0}{x(Q)-x_0},
\qquad z=8x(Q)-t^2+b_2+4x_0.
$$

Substitution recovers $Q$ exactly. Thus one finite rational anchor already provides a birational representation of the curve; many independent anchors are not needed for representability. The excluded points $P,-P,O$ are already known. Rational points at infinity of a reduced quartic are handled separately when they map to finite points on the original curve.

Changing the sign of $z$ gives the other intersection point $R$, with $P+Q+R=O$. Once $P$ is known, that pair contributes at most one new independent direction. [gp/pointed_quartic.gp](gp/pointed_quartic.gp) and the Python tests check the formulas and group identity.

### 3. Why use many models?

A point with enormous coordinates on the original cubic may have small coordinates on a suitable reduced quartic. The choice of anchor and change of variables affects which points fall into a practical search box.

The engine builds anchors from bounded integer combinations of a certified independent set. Approximate canonical heights and lattice reduction prioritize short combinations; a second selection policy includes combinations supported on more basis points. All resulting group operations and basis changes are checked exactly. Approximate heights determine search priority, never the proof of independence.

PARI/GP reduces or minimizes each quartic. The implementation retains its inverse coordinate map, checks polynomial identities, and uses `hyperellratpoints` in bounded numerator/denominator regions. After mapping a candidate back, Python verifies its original curve equation.

### 4. The shared search loop

The default `unified` engine keeps three related objects:

1. **Exact observations:** every distinct observed point, including points whose independence is inconclusive.
2. **A certified independent subset:** the points used for the current rank lower bound.
3. **Search models and completed regions:** reusable quartics with inverse maps and completed denominator intervals.

New observations can improve the independent subset or provide useful projection centres. Local character relations also suggest bounded exact division attempts. For example, a candidate hidden behind an even relation may become visible after an exactly verified halving. Division alone stays in the same rational span; only a subsequent certificate justifies a larger rank claim.

When rational 2-torsion is present, the engine can also propose classical 2-isogeny quartics and search neighbouring isogenous curves. All returned points are transported and checked exactly. Integral changes near small primes provide further quartic models. These are bounded proposals, with no assertion that all covering classes or all useful models have been enumerated.

Model changes preserve completed search intervals. Partial GP output is used only after a complete record has been parsed; a timed-out search box is not marked complete. Slow models are isolated so they do not repeatedly block later models in the same batch. Enrichment also tracks progress through larger boxes, avoiding a permanent restart at the smallest bounds.

### 5. Exact rank certificates

For verification, use $X=4x$ and $W=4(2y+a_1x+a_3)$:

$$
W^2=g(X)=X^3+b_2X^2+8b_4X+16b_6.
$$

At an odd good prime $p$ and a root $\alpha$ of $g$ modulo $p$, evaluate the quadratic character of $X-\alpha$; at the corresponding 2-torsion reduction, use $g'(\alpha)$. These characters give homomorphisms to $\mathbb F_2$ that vanish on doubles. Stacking their values produces a binary matrix. This is the classical local-character method described by [Cremona, §2](https://johncremona.github.io/papers/filter.pdf).

If its rank is $s$ and $t$ bounds $\dim_{\mathbb F_2}E(\mathbb Q)[2]$, then $\mathrm{rank}\,E(\mathbb Q)\ge s-t$. Root counts at good primes supply $t$; a rootless reduction gives $t=0$. With rational torsion, witnessed finite-order columns are removed before selecting independent free columns.

The saved certificate records primes, roots, bit rows, torsion evidence, and an input fingerprint. Python recomputes them using integers, fractions, and binary elimination. A singleton fallback checks the first twelve multiples, using Mazur's torsion theorem. Replay needs no GP process, numerical heights, analytic rank, or conditional hypothesis.

### 6. What is established

The concrete finding is that this implementation's combination of point-centred models, adaptive reuse of observations, and exact certification yields the three stronger bounds above from one declared seed each. The construction of the quartic and the local-character independence method are classical. We do not claim to have established mathematical priority for the overall search strategy or a general speed advantage over existing software.

The implemented search is bounded and heuristic. It does not compute a complete Mordell–Weil group, a full Selmer group, an upper rank bound, or a saturation certificate. An inconclusive character test does not prove dependence; independent points can be hidden by even index. No bound guarantees that a new independent point has small coordinates in one of the selected models.

## Commands, output, and resume

See [RUNNING.md](RUNNING.md) for options, output formats, resume behaviour, and troubleshooting. Use `python run.py --help`, `python seeded.py --help`, and `python reproduce.py --help` for the exact CLI.

`run.py` requires a fresh empty output directory inside this project. `seeded.py` resumes its own checkpoint when given the same input, code, and search settings. The time budget may be increased. Keep each independent run in its own directory under `runs/`.

## Tests

With GP configured:

```sh
python doctor.py
python -m unittest discover -s tests -v
python first_cover.py --self-test
python first_jet.py --self-test
python reproduce.py --output runs/reproduction --seconds 30
```

For offline proof tests without GP:

```sh
python -m unittest discover -s tests -p test_certificates.py -v
python verify.py --examples
```

The suite covers exact projection and isogeny maps, torsion handling, point division, tampered certificates, resumable coverage, timeouts, retained observations, and an equation-only end-to-end search. The two `first_*` scripts are additional experimental first-point methods; they are not invoked by the default search loop. See [TESTING.md](TESTING.md).

## Files

| Files | Purpose |
|---|---|
| `run.py`, `bootstrap.py`, `geometry.py`, `lattice.py` | Equation-only initial search |
| `seeded.py`, `unified.py`, `search_policy.py` | Seeded search, scheduling, reference policies |
| `models.py`, `quartic.py`, `local_models.py`, `point_models.py` | Quartics, inverse maps, neighbours, division and isogenies |
| `bounded_anchor_pool.py`, `anchor_diversity.py` | Bounded anchor selection |
| `point_arithmetic.py` | Exact rational group arithmetic |
| `certificate.py`, `torsion_certificate.py`, `verify.py` | Exact certificate construction and replay |
| `first_cover.py`, `first_jet.py` | Experimental first-point methods |
| `runtime.py`, `doctor.py`, `reproduce.py` | Portable configuration and reproduction |
| `examples/`, `gp/`, `tests/` | Inputs, proof witnesses, GP demonstration, regressions |

The directory is self-contained: copy its contents into a new repository and use this README as the repository front page. Generated files under `runs/` and `artifacts/` are ignored. No executables or downloaded datasets are bundled.

## References and attribution

- J. E. Cremona, [On the computation of Mordell–Weil and 2-Selmer Groups of Elliptic Curves](https://johncremona.github.io/papers/filter.pdf), §2: local-character independence tests.
- The PARI Group, [hyperelliptic-curve functions](https://pari.math.u-bordeaux.fr/dochtml/ref/Hyperelliptic_curves.html): model changes, reduction, minimization, and rational-point search.
- [ICARM Elliptic Curve Rank Leaderboard](https://elliptic-rank.icarm.cloud/curves): source curves and the initial public points. The three curve pages credit Seewoo Lee and describe their Mestre–Fermigier constructions.
- [ICARM's verifier](https://github.com/icarm/elliptic-rank/blob/main/src/verify.ts): related implementation of the local-character method. The included Python verifier is separately implemented.

We acknowledge the NSF Institute for Computer-Aided Reasoning in Mathematics (ICARM) and NSF Grant DMS 2425401 for the source data and leaderboard infrastructure. Original curve construction and seed-point credit remain with their authors; this project supplies the additional search and lower-bound evidence.

## License

MIT. Copyright © 2025–2026 Valery Asiryan. See [LICENSE](LICENSE). PARI/GP is installed separately and retains its own license.
