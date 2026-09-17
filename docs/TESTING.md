# Testing

Install the package from a checkout: `python -m pip install -e .`.

## Python-only checks

```sh
ers-research verify --controls
ers-research sections
python -m unittest discover -s tests -p test_certificates.py -v
python -m unittest discover -s tests -p test_research.py -v
```

These replay all 23 certificates, verify the 17 exact polynomial identities, reject altered mathematical evidence and case resources, and check the engine/study boundary. Atomic-checkpoint tests exercise transient Windows-style sharing failure and persistent failure while preserving the prior checkpoint.

## Arithmetic and search regressions

Configure GP and check its capabilities, then run:

```sh
ers doctor
python -m unittest discover -s tests -v
python first_cover.py --self-test
python first_jet.py --self-test
```

The original 54 regressions are retained. New tests rebuild every family model from formulas and certify each actual initial seed bound. They also cover the research catalogue and standalone sieve. The current full suite has 65 tests; three native-sieve tests are skipped until that optional tool is built.

The suite exercises exact inverse maps, torsion corrections, divided points, interrupted reductions, search feedback, model scheduling, checkpoint/resume and declared-input data boundaries. Some tests deliberately simulate rare interruption paths; others execute real GP searches. Very short arithmetic budgets can be sensitive to machine load.

The standalone GP projection demonstration is `gp -fq gp/pointed_quartic.gp`. In PowerShell use `& $env:PARI_GP -fq gp/pointed_quartic.gp`. Check for `PROJECTION_CHECK_OK` and no GP errors on stderr.

## Native parameter selection

```sh
dotnet build src/parameter_sieve/ParameterSieve.csproj -c Release
python -m unittest discover -s tests -p test_parameter_sieve.py -v
```

Tests enumerate finite-field points independently to check modular scores, compare selected parameters across one and four workers, verify primitive grid coverage, and recompute exact j-invariants. No GP or sibling elliptic-curve library is needed for these tests.

## Research and installation validation

[REPRODUCIBILITY.md](REPRODUCIBILITY.md) explains fresh-search commands. They produce explicit stage inputs, discovery logs, exact certificates, point-origin audits and data-read audits. Fresh output directories prevent accidental continuation from a stored result. A missed target is saved and causes nonzero exit status.

The package is additionally tested by building a wheel, installing it into a fresh virtual environment, and running from an empty workspace with GP explicitly configured. Code and research inputs resolve from that installation without old runs or source helpers. Completed results are in [VALIDATION.md](VALIDATION.md).

Run the checks locally using the commands above. Long GP searches are separate, explicit research commands.
