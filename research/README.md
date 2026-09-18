# Research catalogue

This directory contains the reproducible mathematical inputs, proof witnesses and experiment descriptions. The general search implementation is in [src/elliptic_rank_search](../src/elliptic_rank_search).

| Study | Contributions | Declared fresh-search input |
|---|---|---|
| [Alpoege family](alpoege_family/README.md) | 18 curves, #733-#750, certified bounds 18-25 | The exact parameter and 17 generic section formulas |
| [Known-curve improvements](known_curve_improvements/README.md) | #199: 13→15; #206: 12→14; #212: 11→13 | One declared public point per curve |
| Family controls | #302 ≥31 and #727 ≥26 | The same generic section formulas; kept outside the discovery list |

[catalogue.json](catalogue.json) is the machine-readable index. The counts and links correspond to the [user's ICARM profile](https://elliptic-rank.icarm.cloud/user/89) and the frozen September 17 catalogue. These are rank lower bounds, not complete rank computations or claims that the full rational-point group has been recovered.

Use the [reproducibility guide](../docs/REPRODUCIBILITY.md) for proof replay, fresh search, metric verification, parameter selection and the separate final continuation experiment.

`data/icarm-20260917.json` contains the frozen public catalogue metadata, source URL and download timestamp. Each case records its public curve URL and source credits. Old paths in `experiments/history/` identify historical local records; no executable recipe reads those paths. Machine-independent recipes live outside that history directory.

We acknowledge the Institute for Computer-Aided Reasoning in Mathematics (ICARM), NSF Grant DMS 2425401, and the original curve and section authors.
