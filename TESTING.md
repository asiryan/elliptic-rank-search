# Testing

## Offline verification

This suite requires Python alone:

```sh
python -m unittest discover -s tests -p test_certificates.py -v
python verify.py --examples
```

It replays all three included proofs, checks the expected lower bounds, rejects changed points, altered character bits, and inflated rank claims, and asserts that proof replay does not launch external programs.

## Search and arithmetic regression suite

Configure GP as described in [RUNNING.md](RUNNING.md), then run:

```sh
python doctor.py
python -m unittest discover -s tests -v
python first_cover.py --self-test
python first_jet.py --self-test
```

The unittest suite contains 54 tests. It covers:

- curve/input validation and the declared-input data boundary;
- exact projection inverses, companion-point group relations, and finite images of quartic points at infinity;
- complete and interrupted model records, inverse-map composition, isogenies, and local model changes;
- bounded anchor generation, torsion translations, conservative independence tests, and exact division witnesses;
- new points hidden by even character relations;
- checkpoint/resume behaviour, completed denominator intervals, partial model preparation, advancing search bounds, and isolation of slow models;
- an end-to-end equation-only trial on a large-coordinate model.

Some scheduling tests use controlled discoveries to exercise rare timeout and resume paths. Other tests execute real GP arithmetic and searches. Several budgets are deliberately short; a heavily loaded machine may need investigation of timeout-sensitive failures.

The standalone GP demonstration can also be run directly:

```sh
gp -fq gp/pointed_quartic.gp
```

In PowerShell, use `& $env:PARI_GP -fq gp/pointed_quartic.gp`. Expected marker: `PROJECTION_CHECK_OK`. Check stderr for GP errors as well as the process exit code: GP can report an arithmetic error without returning a nonzero exit status.

## Reproduction from a single point

```sh
python reproduce.py --output runs/reproduction --seconds 30 --workers 2 --anchors 16
```

Each child search receives the equation and one declared point. The coordinator verifies the resulting certificates and writes `runs/reproduction/verification.json`. It exits unsuccessfully if any target is missed. A retry can increase the time budget while retaining compatible checkpoints. A new experiment should use a fresh directory so that its timings include discovery from the original seed.

Successful reproduction means that each stated bound has a freshly checked independent set. It does not require the coordinates or order of the new basis to match the stored examples.

## Independence of the extracted folder

Copy the publishable files to another directory, configure GP explicitly, and repeat the suite and reproduction there. All imports, examples, defaults, and code hashes resolve within the copied project. The original workspace is not an input or dependency. `runs/` and `artifacts/` are disposable generated outputs and should be excluded from an export.

The completed extraction checks are recorded in [VALIDATION.md](VALIDATION.md).
