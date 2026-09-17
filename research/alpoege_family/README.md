# Alpoege-family research

Eighteen specializations were published as ICARM #733-#750. The family is the one identified by wgxli in the commentary to [ICARM #302](https://elliptic-rank.icarm.cloud/curve/302). This repository retains the exact rational parameter convention used in that discussion and the recovered generic section formulas.

| ICARM | T | Certified bound | Evidence |
|---|---|---:|---|
| [#733](https://elliptic-rank.icarm.cloud/curve/733) | `-7/12` | >=20 | [case](cases/icarm-733/case.json), [points](cases/icarm-733/points.json) |
| [#734](https://elliptic-rank.icarm.cloud/curve/734) | `1/4` | >=18 | [case](cases/icarm-734/case.json), [points](cases/icarm-734/points.json) |
| [#735](https://elliptic-rank.icarm.cloud/curve/735) | `-12/31` | >=20 | [case](cases/icarm-735/case.json), [points](cases/icarm-735/points.json) |
| [#736](https://elliptic-rank.icarm.cloud/curve/736) | `4/3` | >=19 | [case](cases/icarm-736/case.json), [points](cases/icarm-736/points.json) |
| [#737](https://elliptic-rank.icarm.cloud/curve/737) | `4/17` | >=18 | [case](cases/icarm-737/case.json), [points](cases/icarm-737/points.json) |
| [#738](https://elliptic-rank.icarm.cloud/curve/738) | `-13/47` | >=21 | [case](cases/icarm-738/case.json), [points](cases/icarm-738/points.json) |
| [#739](https://elliptic-rank.icarm.cloud/curve/739) | `-27/47` | >=22 | [case](cases/icarm-739/case.json), [points](cases/icarm-739/points.json) |
| [#740](https://elliptic-rank.icarm.cloud/curve/740) | `-47/23` | >=23 | [case](cases/icarm-740/case.json), [points](cases/icarm-740/points.json) |
| [#741](https://elliptic-rank.icarm.cloud/curve/741) | `-61/126` | >=23 | [case](cases/icarm-741/case.json), [points](cases/icarm-741/points.json) |
| [#742](https://elliptic-rank.icarm.cloud/curve/742) | `17/106` | >=21 | [case](cases/icarm-742/case.json), [points](cases/icarm-742/points.json) |
| [#743](https://elliptic-rank.icarm.cloud/curve/743) | `-19/74` | >=21 | [case](cases/icarm-743/case.json), [points](cases/icarm-743/points.json) |
| [#744](https://elliptic-rank.icarm.cloud/curve/744) | `-41/94` | >=22 | [case](cases/icarm-744/case.json), [points](cases/icarm-744/points.json) |
| [#745](https://elliptic-rank.icarm.cloud/curve/745) | `57/85` | >=23 | [case](cases/icarm-745/case.json), [points](cases/icarm-745/points.json) |
| [#746](https://elliptic-rank.icarm.cloud/curve/746) | `-47/80` | >=23 | [case](cases/icarm-746/case.json), [points](cases/icarm-746/points.json) |
| [#747](https://elliptic-rank.icarm.cloud/curve/747) | `-43/75` | >=23 | [case](cases/icarm-747/case.json), [points](cases/icarm-747/points.json) |
| [#748](https://elliptic-rank.icarm.cloud/curve/748) | `-265/221` | >=25 | [case](cases/icarm-748/case.json), [points](cases/icarm-748/points.json) |
| [#749](https://elliptic-rank.icarm.cloud/curve/749) | `-332/267` | >=25 | [case](cases/icarm-749/case.json), [points](cases/icarm-749/points.json) |
| [#750](https://elliptic-rank.icarm.cloud/curve/750) | `-83/111` | >=24 | [case](cases/icarm-750/case.json), [points](cases/icarm-750/points.json) |

## Family inputs

[family/specialize.py](family/specialize.py) defines the integral homogeneous family at `T=u/v`. It evaluates the archived [17 section formulas](family/sections.json), verifies point membership, minimizes the equation with GP and checks the coordinate change exactly. [family/README.md](family/README.md) documents provenance and conventions.

The formulas are mathematical inputs to this study. `ers-research sections` verifies their polynomial identities independently of GP or any saved final points. Their original reconstruction process is historical provenance, not an undisclosed prerequisite for reproducing the 18 results. At #737 the specialized input certifies only 16 independent directions; the case recipe still reaches the published bound 18.

## Evidence and reproduction

Each `cases/icarm-N/` directory has separate equation, points, certificate, metric, recipe and provenance files. `case.json` records hashes; `reproduction.json` declares the input and bounded search settings. See [the reproduction guide](../../docs/REPRODUCIBILITY.md).

The [controls](controls/) contain #302 (`164518/924945`, bound 31) and #727 (`-311/519`, bound 26). They were known curves used to calibrate the search. They are not counted among the eighteen new publications and are excluded from default batches.

## Research history

The [experiment index](experiments/README.md) connects portable sieve configurations, fresh-search recipes and historical summaries. The [final report](reports/published-final-20260917.md) records a separate 300-second continuation on each of the 18 published witness sets; it found no further rank gain. Negative runs are retained as search-budget observations, not rank upper bounds.

[The frozen catalogue](../data/icarm-20260917.json) preserves comparisons with ICARM at the recorded time. Leaderboard positions and future bounds may change. No claim of a complete Mordell-Weil group, saturation or record priority follows from these certificates.

We acknowledge the original family and section contributors, ICARM and NSF Grant DMS 2425401.
