# Searching the ICARM302 family at large parameter heights

New bounds ≥26: **0**. New curves confirmed to qualify for the leaderboard: **0**.

## Search performed

- New selection: 6,000,000 draws of primitive T with replacement, max(|numerator|, denominator) ≤ 2,000,000.
- Selection used several prime intervals, a random reservoir and favorable congruences; 2048 candidates were rescored at all primes up to 65521, and 128 were retained.
- Together with 96 candidates from the previous selection, 224 parameters were checked on the additional interval 65521 < p ≤ 262139. The lists were fixed before this check. Subsequent selection based on its results remains heuristic.
- For the 128 new parameters, the 17 sections were specialized afresh and checked exactly, along with the change to the minimal model. Saved verified inputs were used for the previous 96; every search checks its input again when it starts. Initial-point height diagnostics are used only to set the search order.
- 10 searches were completed, each with 2048 anchors, 8 workers, adaptive mode and a 300-second budget. The search engine was unchanged.
- Up to three searches ran concurrently; candidate selection was also running during part of that time. An equal worker count therefore does not imply the same speed as the control run.

| T | Previous bound ≥ | Resulting bound ≥ | Search time, s | Score up to 262139 |
|---|---:|---:|---:|---:|
| 1159069/1681844 | 17 | 17 | 300.02 | 25.8677 |
| 1962574/688659 | 17 | 17 | 300.04 | 25.7299 |
| -499517/723273 | 17 | 17 | 300.03 | 25.0115 |
| -145973/661007 | 17 | 17 | 300.03 | 25.1617 |
| 564787/938759 | 17 | 17 | 300.03 | 21.6096 |
| 48417/188047 | 17 | 17 | 300.21 | 23.5836 |
| -556632/920393 | 17 | 17 | 300.04 | 26.3358 |
| 327291/708941 | 17 | 17 | 300.03 | 25.7764 |
| 139941/325751 | 17 | 17 | 300.07 | 25.9258 |
| 95083/512532 | 17 | 18 | 300.05 | 20.1525 |

Equations and independent points for improved curves were saved locally:

- T=95083/512532, ≥18: data (historical local artifact).

## Comparison with ICARM

Snapshot: 750 curves, 2026-09-16T21:02:35.557423+00:00. Minimal equations were matched by c4 and c6. Positions under the available metrics were recomputed by two implementations.
Conductors for this batch were not fully computed. Failure to qualify under the three known metrics does not rule out qualification by conductor.
All results were saved locally. Nothing was submitted to the website.

## Control and limitations

Control #302: T=164518/924945, parameter height 924945, published lower bound 31. In a separate fresh run, the same algorithm recovered 31 independent directions from 17 in 147.94 seconds (2048 anchors, 8 workers). The control was excluded from new candidates.
All 73 published curves with bounds ≥26 were checked separately: the exact equation for equality of j-invariants was solved, the factorization was verified by multiplication including the constant factor, and T=∞ was considered. Rational parameters were found only for #302 (164518/924945) and #727 (-311/519); in both cases the minimal models over the rationals matched. Other authors' points were not downloaded for this check.
A larger parameter height broadens the search range but does not guarantee a higher rank. Prime scores and numerical point heights are not rank proofs.
Each result was checked again using an exact certificate; curve membership, provenance of discovered points and input hashes were verified. An unsuccessful search with a finite time budget does not give an upper rank bound.

Machine-readable results (historical local artifact) · All candidates (historical local artifact)
[ICARM #302](https://elliptic-rank.icarm.cloud/curve/302) · [ICARM catalogue](https://elliptic-rank.icarm.cloud/database.json)
Public catalogue maintained by ICARM with support from NSF Grant DMS 2425401.
