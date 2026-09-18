# Running the search

All commands below assume that the current directory is the project root. Install the package first with `python -m pip install -e .`. Python 3.10+ and GP are the only search dependencies. Python certificate replay requires no external program.

## Configuration

Set `PARI_GP` to an executable path, or make `gp` available on `PATH`. Do not include command-line arguments inside `PARI_GP`. Paths containing spaces are supported. On Windows, `gp` is also a PowerShell alias: use `python doctor.py` to test the executable selection, or `& $env:PARI_GP --version` to call it directly.

```sh
python doctor.py
```

The engine starts independent GP processes with a 64 MiB initial stack and normally a 512 MiB maximum stack. Parallel workers can therefore require substantial memory. Start with two workers and sixteen anchors. Increasing either value does not guarantee faster discovery.

## Equation-only search

```sh
python run.py --input examples/toy/equation.json --output runs/toy --bootstrap-seconds 10 --search-seconds 10 --seed-limit 1 --target 2 --workers 2 --anchors 16
```

The input must contain only five integral `ainvs`, in the order `[a1,a2,a3,a4,a6]`. It must be nonsingular. The program first discovers seed points from the equation, then expands the certified seed set.

| Option | Meaning |
|---|---|
| `--bootstrap-seconds` | Budget for initial discovery; positive, at most 3600 |
| `--search-seconds` | Budget for seeded expansion; 0 disables expansion, at most 7200 |
| `--seed-limit` | Maximum number of discovered independent points passed to expansion; omitted means no explicit limit |
| `--target` | Requested stopping lower bound, from 1 to 100 |
| `--workers` | Number of parallel GP jobs, from 1 to 24 |
| `--anchors` | Anchor budget, from 1 to 4096 |
| `--job-seconds` | Bootstrap GP job budget, from 0.05 to 60 |
| `--lattice-seconds` | Optional tangent-lattice budget inside the bootstrap budget; default 0 |
| `--anchor-mode` | Expansion policy; default `unified` |

`run.py` requires an empty output directory inside the current workspace. A nonempty directory is rejected so an equation-only trial cannot silently consume a previous search. The default CLI target is 31; specify a realistic target for the curve under investigation.

Budgets bound heuristic stages rather than every instruction of wall-clock execution. Process startup, preparation, exact verification, queued work, and checkpoint writes can add overhead. The bootstrap may also exhaust its finite list of proposals before the time limit.

## Seeded search and resume

The seeded input adds an explicit list of rational points:

```json
{
  "ainvs": ["0", "0", "0", "-25", "4"],
  "points": [["0", "2"]]
}
```

```sh
python seeded.py --input examples/toy/seed.json --output runs/seeded-toy --seconds 10 --target 2 --workers 2 --anchors 16
python verify.py runs/seeded-toy/result.json
```

Repeat the same `seeded.py` command to resume. The input bytes, code hashes, target, worker count, anchor policy, and other stored settings must match. The `--seconds` budget can change and applies to this invocation's search loop. If you change other settings, choose a new output directory. Checkpoints from historical versions are not compatible with this export.

To continue the expansion of an equation-only run, use its generated `seed.json` with `seeded.py` in a new output directory. That new search has its own checkpoint and may repeat work. Do not restart `run.py` in its existing nonempty directory.

Reference policies are available through `--anchor-mode fixed`, `frozen`, `adaptive`, `parity`, or `geometric`. They share arithmetic components with the default solver and exist for controlled comparisons. `frozen` preserves the initial anchor models through a resume; `unified` maintains the shared pool of observations and retained models described in the README.

## Output

| File | Contents |
|---|---|
| `result.json` | Final independent points, proved lower bound, certificate, and replay result |
| `checkpoint.json` | Seeded engine state, settings, code hashes, observed points, models, covered intervals, events, and status |
| `points.json` | Latest selected independent points and lower bound |
| `basis.json` | Working certification input; it can contain candidates beyond the final independent subset |
| `discoveries.jsonl` | Exact newly observed points and their search provenance |
| `data-reads.json` | Python file reads recorded by the CLI's data-boundary guard |
| `config.json`, `bootstrap.json`, `bootstrap-jobs.jsonl` | Equation-only configuration and initial-search progress |
| `seed.json`, `origins.json`, `models.json` | Bootstrap points, origins, and search models |

Only use `result.json` with a successful replay as final proof evidence. A count in a progress log is not a certificate. If the initial search fails, `result.json` records a zero lower bound and the failure status without a positive certificate.

`target_reached` means the requested lower bound was certified. `budget_completed`, `model_preparation_incomplete`, or `frontier_exhausted` describe the bounded search, not the true rank. `interrupted` means an orderly interruption saved a checkpoint; an abrupt process termination may leave only the previous checkpoint.

The command-line data guard permits the declared input, Python code, and output files within the current workspace and configured research data roots. Search workers are not given the published research witnesses. This is an audit mechanism, not an operating-system security sandbox; it does not monitor arbitrary reads performed by GP or reads outside the configured data roots. GP scripts are generated from validated arithmetic data and checked against a forbidden-call list for rank/database and external-data operations.

## Replay or build a certificate

```sh
# Embedded certificate from either supported search CLI:
python verify.py runs/seeded-toy/result.json

# Separate stored proof:
python verify.py research/known_curve_improvements/cases/icarm-199/points.json --certificate research/known_curve_improvements/cases/icarm-199/certificate.json

# Recompute a conservative local-character certificate from arbitrary points:
python -m elliptic_rank_search.certificates.certificate research/known_curve_improvements/cases/icarm-199/points.json --output runs/new-certificate.json --max-prime 2000
```

For the last command, create `runs/` first if it does not exist. `certificate.py` implements the conservative v1 certificate. `verify.py` additionally understands the torsion-augmented and singleton formats produced by the seeded engine. A valid certificate can be inconclusive about independence; inspect its lower bound and `all_points_independent_modulo_torsion` field.

## Experimental first-point methods

The export also retains two standalone coefficient-only probes:

```sh
python first_cover.py --input examples/toy/equation.json --output runs/first-cover.json --seconds 3
python first_jet.py --input examples/toy/equation.json --output runs/first-jet.json --seconds 3
```

`first_cover.py` explores a bounded collection of cubic-algebra relations and associated coverings. `first_jet.py` uses local expansions and small auxiliary polynomials. Neither is part of `run.py`'s default bootstrap. Each has its own `--self-test` and optional coefficient-only `--benchmark` fixtures. The jet probe has a separate first-point certificate structure and `verify_hit` replay function; its output is not accepted by the general `verify.py` CLI.

## Troubleshooting

- **GP is missing:** install it separately and set `PARI_GP` to its executable; run `doctor.py`.
- **Missing GP function:** use a build supporting the functions listed by `doctor.py`, then run the full tests.
- **No initial seed:** increase the bootstrap budget, try another first-point method, or supply a known non-torsion point. The default bootstrap is conservative with rational 2-torsion.
- **No independent seed basis:** the supplied points may be torsion or their local-character test may be inconclusive. This message is not a proof of dependence.
- **Resume mismatch:** restore the original input/code/settings or start a fresh directory.
- **GP memory errors:** reduce workers and anchors first. An unsuccessful arithmetic process cannot certify a new lower bound.

## Research commands

The general engine is independent of the studies. Use `ers-research` (or `python -m research`) to select studies, verify their published evidence, and reproduce searches. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

The root launchers remain compatible. `python verify.py --examples` and `python reproduce.py` still select only the original three improvements. The new `ers-research verify` and `ers-research reproduce` commands select all 21 contributions by default.
