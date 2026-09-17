# Elliptic Rank Search

Adaptive rational-point search with exact, replayable rank lower-bound certificates, together with reproducible research on high-rank elliptic curves.

The general engine accepts a Weierstrass equation and optionally known rational points. It builds and searches quartic models, feeds discoveries back into the search, and certifies independence exactly. Python uses its standard library; search additionally needs PARI/GP. Certificate replay needs Python alone.

## Published results

All **21 contributions** recorded on [Valery Asiryan's ICARM profile](https://elliptic-rank.icarm.cloud/user/89) are included with equations, rational points, exact certificates, provenance and fresh-search recipes.

| Study | Results | Fresh input |
|---|---|---|
| [Alpoege family](research/alpoege_family/README.md) | 18 curves, #733–#750, bounds 18–25 | Parameter T and 17 generic section formulas |
| [Known-curve improvements](research/known_curve_improvements/README.md) | #199: 13→15; #206: 12→14; #212: 11→13 | One declared public point per curve |

The known curves #302 ≥31 and #727 ≥26 are separate controls. All rank claims are lower bounds. A finite unsuccessful search does not prove that further independent points do not exist.

## Quick start

Run these commands from a checkout with Python 3.10 or newer:

```sh
python -m pip install -e .
ers-research verify
ers-research sections
```

The first verification command replays all 21 published certificates offline; `--controls` includes both controls. The section check verifies all 17 polynomial identities exactly.

To search, install [PARI/GP](https://pari.math.u-bordeaux.fr/download.html) separately, put `gp` on `PATH` or set `PARI_GP` to its executable, then run:

```sh
ers doctor
ers-research reproduce --output runs/all-published
```

For Windows PowerShell, configure a non-PATH installation with `$env:PARI_GP = 'C:\PARI\gp.exe'`. The capability probe checks required arithmetic functions, including quartic minimization. The validated local build is recorded in [docs/VALIDATION.md](docs/VALIDATION.md).

Fresh family runs generate seeds from formulas; published final witnesses are not search inputs. Searches stop when the target is certified. A missed target causes a nonzero batch exit. Success requires a new exact certificate, not identical basis coordinates or execution times.

A small equation-only example:

```sh
ers search --input examples/toy/equation.json --output runs/toy --bootstrap-seconds 10 --search-seconds 10 --seed-limit 1 --target 2 --workers 2 --anchors 16
ers verify runs/toy/result.json
```

## Repository layout

```text
src/
  elliptic_rank_search/            General engine; no dependency on research
    arithmetic/                   Exact point arithmetic and model geometry
    search/                       Discovery, anchor policies and search loops
    certificates/                 Exact certificate construction and replay
    cli/                          General command-line entry points
  parameter_sieve/                 Optional standalone .NET parameter selection
research/
  common/                         Catalogue, reproduction and metric commands
  known_curve_improvements/       Three improved existing curves
  alpoege_family/
    family/                       Equation, 17 formulas and exact specialization
    cases/                        Eighteen published curves and proof witnesses
    controls/                     Known #302 and #727
    experiments/                  Configurations and historical summaries
    reports/                      Research narrative and final continuation
  data/                           Frozen ICARM catalogue metadata
  provenance/                     Migration and validation records
examples/toy/                      Small functional inputs
tests/                            Mathematical and search regressions
docs/                             Algorithm, usage and reproducibility
runs/                             Generated outputs, ignored by Git
```

The root Python launchers remain available. `python verify.py --examples` and `python reproduce.py` preserve the original three-curve scope; use `ers-research` for the full catalogue. Working checkpoints remain local. A clean installation needs no old research artifacts or sibling repository.

## Documentation and checks

- [Algorithm and mathematical references](docs/ALGORITHM.md)
- [Search commands and checkpoint behaviour](docs/RUNNING.md)
- [Reproduce results, metrics and parameter campaigns](docs/REPRODUCIBILITY.md)
- [Tests](docs/TESTING.md) and [completed validation](docs/VALIDATION.md)
- [Research catalogue](research/README.md) and [experiment index](research/alpoege_family/experiments/README.md)

```sh
python -m unittest discover -s tests -v
```

The full suite needs configured GP. Native-sieve tests run when its .NET tool has been built. Certificates and section identities can be checked without GP using the commands in the testing guide. Long discovery searches are explicit research commands.

## Attribution and license

Curve construction, family identification and original seed/section credit remain with their authors; each study documents its sources. We acknowledge ICARM and NSF Grant DMS 2425401 for the leaderboard data and infrastructure. The included Python certificate verifier is independently implemented using the local-character method described in [Cremona's paper](https://johncremona.github.io/papers/filter.pdf).

MIT, copyright © 2025–2026 Valery Asiryan. See [LICENSE](LICENSE). PARI/GP is installed separately under its own license.
