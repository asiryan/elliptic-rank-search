# Parameter sieve

An optional standalone .NET 8 tool for the Alpoege/ICARM #302 family. It selects rational parameters and computes finite-field scores. Python generates the section inputs and certifies ranks separately.

```sh
dotnet build tools/parameter_sieve/ParameterSieve.csproj -c Release
dotnet tools/parameter_sieve/bin/Release/net8.0/ParameterSieve.dll grid --height 8 --keep 8 --refine-keep 4 --final-keep 2 --prime-bound 16382 --workers 2 --output runs/grid
```

`grid` enumerates primitive pairs. `sample` accepts `--samples`, `--height`, `--seed`, and `--selection cumulative|bands|crt|dense`; the archived configurations supply all settings. `rescore --input parameters.json --start 0 --prime-bound 97 --workers 2 --output runs/rescored.json` expects an array of `{ "u": 1, "v": 4 }` objects, with positive denominators.

All scores are heuristic, using good reductions of the supplied generic model and primes at least 5. Singular model reductions contribute zero. The grid includes #302 as a labelled control without consuming a finalist slot. Sampling excludes the known control and deduplicates finalists by exact j-invariant. Equal j-invariant is a conservative exclusion criterion, not an isomorphism proof or a complete novelty test.

Checkpointed native runs can resume with the same options. The higher-level `ers-research campaign` coordinator deliberately uses an empty directory to keep new runs distinct. Grid summation and sampler RNG are deterministic across worker counts; elapsed times are not.

[provenance.json](provenance.json) records the historical source hashes. Scoring and selection were extracted from the local RankHunt tools; dependencies on the sibling `EllipticCurves` project and its point-export code were removed. Exact j-invariant arithmetic is included here. The tests compare scores with independent finite-field point enumeration and compare selected parameters with one and four workers.
