# Reproducing the research

Run from a checkout after `python -m pip install -e .`. The `ers-research` executable and `python -m research` have the same interface. No internet connection or leaderboard account is used by these commands.

## 1. Replay the published mathematical evidence

```sh
ers-research verify
ers-research verify --controls
ers-research sections
```

The first command verifies all **21 published contributions**: 18 family curves and three improved existing curves. `--controls` also includes #302 and #727. The third command checks the 17 section identities over the rational polynomial ring. These commands need Python only. Rank fields in JSON are not accepted as proofs; the verifier recomputes curve membership, modular character rows, matrix rank and the torsion correction.

`research/catalogue.json` is the canonical index. Each case separates the equation, witness points, certificate, invariants, reproduction recipe and case metadata. All rationals in mathematical data are exact strings. Proof replay checks the mathematical contents directly, so JSON formatting and line endings do not affect verification. Recipes and metric records are checked by their respective reproduction and metric commands.

## 2. Rediscover the lower bounds from declared inputs

Install PARI/GP separately; set `PARI_GP` to its executable if it is not on `PATH`, then run `ers doctor`. The required function probe is more informative than the version number. See [RUNNING.md](RUNNING.md).

```sh
ers-research reproduce --output runs/all-published
ers-research reproduce --study alpoege_family --output runs/family
ers-research reproduce --case icarm-748 --output runs/one-curve
ers-research reproduce --controls --output runs/with-controls
```

Choose an empty output directory for each experiment. The family inputs are generated afresh from `family/sections.json` at the exact rational parameter. The coordinator checks each model change and seed point and matches the resulting minimal equation. It does not pass the stored final witnesses to the search. For the three older improvements, the declared input is one public seed point per curve.

The generic formulas supply 17 sections, but their specialized independence must be checked: at #737 the initial certified bound is **16**. The research layer records this rather than assuming 17 independent points for every parameter.

Recipes specify target, time, workers, anchor count and policy. Current family recipes allow 300 seconds, eight GP workers and 2048 adaptive anchors; control #727 allows 60 seconds. The older improvements use 30 seconds, two workers, 16 anchors and the unified policy. `--seconds N` replaces the recipe's stages with one stage at that budget. `--parallel 2` or `3` runs that many curves concurrently, multiplying the per-curve worker allocation; the default is one curve at a time.

Each child writes its initial input, exact discoveries, result certificate, checkpoint and Python data-read audit. The coordinator verifies that final points came from the declared seeds or logged discoveries and that scoped data reads contain only code, the declared input and that stage's output. Installed research resources are included in this guard. It is an audit mechanism, not an operating-system sandbox.

Success means a newly certified bound at least as strong as the published target. The new basis need not match the saved coordinates. Wall-clock limits, GP versions and scheduling can change search paths; this is not a claim of identical logs or guaranteed runtime. A missed target does not prove an upper bound. The batch records failures and exits nonzero if a target is missed.

## 3. Check leaderboard metrics

```sh
ers-research metrics
```

This recomputes exact `c4`, `c6` and discriminant, checks the minimal model, and computes naive and Faltings heights at 80-digit precision. It proves the supplied factors prime, checks they cover exactly the minimal discriminant's prime support, and computes conductor exponents by local reduction. It does not factor large discriminants from scratch. Floating heights are compared to the frozen site's rounded values with absolute tolerance `1e-10`.

The frozen catalogue supports historical comparisons; present leaderboard positions can change. No submission is sent to ICARM.

## 4. Repeat parameter selection

The optional .NET 8 tool is separate from the Python search engine and has no external package or sibling-project dependencies:

```sh
dotnet build src/parameter_sieve/ParameterSieve.csproj -c Release
ers-research campaign --config research/alpoege_family/experiments/grid-smoke.json --sieve src/parameter_sieve/bin/Release/net8.0/ParameterSieve.dll --output runs/sieve-check
```

Replace the configuration with `grid-2048.json` or `sample-two-million.json` for the archived broad campaigns. The latter requests six million primitive parameter draws with replacement up to parameter height two million; it does not enumerate every parameter. The grid config enumerates primitive pairs `|u| <= 2048`, `1 <= v <= 2048` and separately scores the known record control. See the [experiment index](../research/alpoege_family/experiments/README.md).

Outputs contain scored parameters and freshly generated section inputs. Feed a generated seed to `ers seeded` for a chosen target and budget. A sieve score is not a rank certificate, and j-invariant deduplication is not a complete novelty check. The generic model can have bad reduction at a prime even if its minimal model does not; the historical scorer assigns zero at those singular model reductions. The port retains this convention.

## 5. Repeat the final continuation experiment

```sh
ers-research deepen --study alpoege_family --seconds 300 --output runs/final-continuation
```

This mode explicitly starts from the **published full witnesses** and continues searching. It records `published_witnesses_used_as_input: true`. It is a separate experiment from fresh rediscovery. The archived September 17 continuation used 300 seconds per curve on all 18 family curves and found no further rank gain; its reports and interruption recovery are preserved.

## A clean installation

Build a wheel with `python -m pip wheel . --no-deps`, install it into a fresh virtual environment, change to an empty writable directory, and run `ers-research verify`, `ers-research sections`, `ers doctor`, and `ers-research reproduce --controls --output runs/reproduction`. Only a separately configured GP executable is required for search. Historical `runs/`, ignored `artifacts/` and the original sibling repository are not required.

The native sieve is an optional source-checkout tool and is not installed into the Python wheel. Its source is included in the source distribution. The completed local validation and measured reproduction results are recorded in [VALIDATION.md](VALIDATION.md).
