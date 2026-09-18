# Coverage audit for small T and lower ranks

**Parameters up to height 64 have been fully enumerated; additional-point searches have been run for only some curves. The absence of further candidates has not been established.**

For T=u/v in lowest terms, the parameter height is H(T)=max(|u|,v), with v>0.

## Status before this audit

| H(T) ≤ | Curves prepared | Point-search result available | Conductor known |
|---:|---:|---:|---:|
| 4 | 23 | 23 | 23 |
| 8 | 87 | 87 | 86 |
| 12 | 183 | 183 | 177 |
| 16 | 319 | 242 | 300 |
| 32 | 1295 | 447 | 1042 |
| 64 | 5039 | 634 | 2865 |

A saved search result does not establish completeness of the group found. For example, some earlier runs lasted only 2-4 seconds. For H≤64, 4405 parameters still had no saved result from a search for additional points.
Beyond H=64, selected parameters have been retained. The earlier sieve up to H=2048 scored all 5 102 343 primitive parameters using local scores; it was not a complete rational-point search on every curve.
Relative to the catalogue snapshot, there were initially 91 unlisted curves that needed one more independent direction to qualify under the known metrics. These are search targets, not claims that additional points exist.

## Additional checks

17 new searches were completed. All used the unchanged engine, adaptive mode, 2048 anchors and 8 workers; budgets and outcomes are listed below.

| T | Previous bound ≥ | Resulting bound ≥ | Budget, s |
|---|---:|---:|---:|
| -8/29 | 17 | 18 | 45 |
| 8/21 | 17 | 17 | 45 |
| -14/17 | 17 | 17 | 45 |
| -7/27 | 17 | 18 | 45 |
| infinity | 15 | 15 | 60 |
| 2/7 | 18 | 18 | 60 |
| 1/2 | 16 | 16 | 60 |
| 3 | 17 | 17 | 60 |
| 2/3 | 17 | 17 | 60 |
| -1/4 | 15 | 15 | 60 |
| -11/6 | 19 | 19 | 60 |
| -11/7 | 19 | 19 | 60 |
| 8/5 | 19 | 19 | 60 |
| -4/5 | 17 | 17 | 60 |
| -2/9 | 17 | 17 | 60 |
| 1/10 | 17 | 17 | 60 |
| 6 | 18 | 18 | 60 |

An additional 44 conductors were fully computed, with 65 bounded attempts including retries with larger budgets.
New curves confirmed to qualify for the leaderboard: **0**. There remained 91 unlisted curves one independent point short of qualification under the known metrics.
The projective parameter T=∞=[1:0], which is absent from the finite grid of fractions, was checked separately. The specialization is nonsingular; the initial sections give a bound ≥15. Its conductor was fully computed. A bound ≥17 would place it in the top 10 by conductor, and ≥18 would place it first by conductor in the corresponding table. These additional independent directions have not been established.

## Retained data

- T=-8/29, ≥18, qualification not yet confirmed: equation and points (historical local artifact).
- T=-7/27, ≥18, qualification not yet confirmed: equation and points (historical local artifact).
- T=infinity, ≥15, qualification not yet confirmed: equation and points (historical local artifact).

Candidates one independent direction short of qualification (historical local artifact) · Earlier search history (historical local artifact) · Full results (historical local artifact)

Each new result was checked again using an exact certificate; point provenance, input hashes and data-read boundaries were checked. The positions of all 5040 curves (5039 finite parameters and T=∞) were checked by an independent calculation. The minimal equation, discriminant and known primes of bad reduction were separately verified for each exported set.
A ranking by an unknown conductor remains unknown. An unsuccessful bounded search does not prove an upper rank bound. Nothing was submitted to ICARM.
[ICARM catalogue](https://elliptic-rank.icarm.cloud/database.json) snapshot: 750 curves, 2026-09-16T21:10:12.117547+00:00.
Public catalogue maintained by ICARM with support from NSF Grant DMS 2425401.
