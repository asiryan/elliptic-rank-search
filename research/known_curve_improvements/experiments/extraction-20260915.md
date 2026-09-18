# Extraction validation - 2026-09-15

## Environment

- Windows x64.
- Python 3.12.0, standard library only.
- PARI/GP 2.19.0 development build `31236-59c418aa0c`, GMP kernel.
- Two GP workers and sixteen anchors for the reproduction runs.

GP is an external installation selected through `PARI_GP`; it is not bundled.
Other operating systems and GP builds have not been tested in this extraction.

## Checks performed

1. Replayed all stored proof witnesses: 15 independent points for #199, 14 for #206, and 13 for #212.
2. Ran the full 54-test Python suite using real GP for arithmetic/search regressions.
3. Ran both experimental first-point self-tests.
4. Ran the standalone GP projection demonstration and checked its success marker and stderr.
5. Ran the equation-only toy example: no supplied points, one discovered seed, then a certified lower bound of 2.
6. Repeated seeded searches for #199, #206, and #212 from exactly one declared point each and verified all final certificates.
7. Copied only publishable files into another directory and ran the tests and reproductions there. No old source directory, result archive, compiled assembly, or original point-search helper was required.
8. Inspected the three copied searches' recorded Python data reads. They contained only code, the declared seed, and each run's own outputs within the project.
9. Checked offline certificate replay with the GP executable deliberately unavailable.

The Python-only selector also has a regression for an even multiple used as a singleton seed. Its local-character image can be zero, so the final verifier replays the exact infinite-order singleton proof in that case.

## Reproduction interpretation

The targets were reached from fresh single-seed inputs with a 30-second search allowance per curve. The corrected #199 target of 15 was also reproduced from one seed, taking approximately 0.8 seconds inside the search engine. The initial isolated runs for #206 and #212 took approximately 0.9 and 0.8 seconds respectively, including Python process startup and final verification. These are illustrative measurements on one machine, not a general benchmark or runtime guarantee.

The input seed is public; the additional stored witness points are not search inputs. A new run may select a different independent set with the same proved bound. The stored proof replay is deterministic and independent of search timing.

## Scope

The extraction preserves the search formulas and the existing regression fixes, replaces the external rank checker with exact Python selection and replay, resolves GP through `PARI_GP` or `PATH`, and makes paths local to the new directory. Previous workspace checkpoints are not portable to this code version; start a fresh run.

These checks validate the included claims and the extraction. They do not establish a complete rank computation, a general runtime bound, or priority over existing mathematical methods.
