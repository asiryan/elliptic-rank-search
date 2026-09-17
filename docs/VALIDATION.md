# Repository validation - 2026-09-17

The reorganized repository was validated locally on Windows with Python 3.12.0, PARI/GP 2.19.0 development build `31261-9397d772d8`, and .NET SDK 10.0.401 targeting .NET 8. GP was an explicitly configured external executable.

The general package was built as a wheel and installed without dependencies into a fresh virtual environment. All reproduction commands ran from an initially empty workspace; the imported engine and research modules came from that installation. The original working research files, sibling projects and stored final points were not fresh-search inputs.

## Completed checks

- All 21 published contributions and both controls were independently rediscovered from declared inputs and their final exact certificates replayed.
- All 23 stored certificates replayed offline; the 17 generic polynomial section identities passed.
- All 23 minimal models, exact invariants, height comparisons and conductors were checked, including primality and completeness of the supplied bad-prime factors.
- All 65 unit/regression tests passed, with real GP arithmetic. Both experimental first-point self-tests passed.
- The standalone .NET sieve built without a sibling project or external package. Modular scores matched independent finite-field point enumeration; one and four workers selected the same parameters. The small grid campaign generated valid section inputs end to end.
- All 119 archived plan/summary files matched the retained historical manifest.
- The independent v1 verifier remains byte-identical to the original: SHA256 `9e0d0d2562fc53705e92a2eaa9a3f6e7c923f1cd3fd82b14df68b60268f4ad54`.

The mathematical search formulas were relocated with package imports. Runtime paths and code hashing were made installation-independent. Checkpoint replacement now retries a short, bounded sequence of transient Windows sharing failures, retaining the prior file if replacement remains impossible. No search formula was changed by that I/O fix.

## Fresh installed-package results

Every run stopped as soon as the requested target was certified. The family recipes allowed up to 300 seconds (60 for #727), but this was not a repeat of the final 300-second continuation campaign. The three older cases began with one declared public point; family cases began with 17 formula evaluations. At #737 those evaluations initially certify only 16 independent directions.

| ICARM | Declared points | Target | Reproduced bound | Process time, s |
|---|---:|---:|---:|---:|
| #199 | 1 | 15 | >=15 | 0.86 |
| #206 | 1 | 14 | >=14 | 0.93 |
| #212 | 1 | 13 | >=13 | 0.81 |
| #302 | 17 | 31 | >=31 | 149.70 |
| #727 | 17 | 26 | >=26 | 14.78 |
| #733 | 17 | 20 | >=20 | 1.97 |
| #734 | 17 | 18 | >=18 | 2.01 |
| #735 | 17 | 20 | >=20 | 1.90 |
| #736 | 17 | 19 | >=19 | 1.98 |
| #737 | 17 | 18 | >=18 | 1.88 |
| #738 | 17 | 21 | >=21 | 1.94 |
| #739 | 17 | 22 | >=22 | 3.45 |
| #740 | 17 | 23 | >=23 | 9.89 |
| #741 | 17 | 23 | >=23 | 9.87 |
| #742 | 17 | 21 | >=21 | 2.02 |
| #743 | 17 | 21 | >=21 | 1.89 |
| #744 | 17 | 22 | >=22 | 7.19 |
| #745 | 17 | 23 | >=23 | 9.37 |
| #746 | 17 | 23 | >=23 | 10.48 |
| #747 | 17 | 23 | >=23 | 5.45 |
| #748 | 17 | 25 | >=25 | 15.78 |
| #749 | 17 | 25 | >=25 | 17.09 |
| #750 | 17 | 24 | >=24 | 8.08 |

The two controls are #302 and #727; the other 21 rows are the published contributions. Timings include process startup and final verification, with up to three curves processed concurrently. They are observations from one machine, not a benchmark or a guarantee. New bases can differ from the retained published bases.

Each child had its own declared input and output directory. The coordinator replayed the proof, audited scoped Python file reads, and checked that final points came from the declared seeds or exact discovery logs. These checks are reproducibility guards, not an operating-system security sandbox.

## Retained history and scope

The historical 18-curve, 300-second-per-curve continuation and the full million-parameter campaigns were **not repeated** during reorganization. Their configurations and original summaries are retained separately. Only the local Windows checks are reported as executed here.

[validation-20260917.json](../research/provenance/validation-20260917.json) contains per-case results, settings, audit outcomes, code hashes and metric values. [migration.json](../research/provenance/migration.json) records the original commit and source hashes. The earlier [three-curve extraction report](../research/known_curve_improvements/experiments/extraction-20260915.md) remains historical documentation.

These results establish the stated lower bounds and the portability of the packaged workflow. They do not establish exact ranks, saturation, completeness of rational-point groups or priority over every prior publication.
