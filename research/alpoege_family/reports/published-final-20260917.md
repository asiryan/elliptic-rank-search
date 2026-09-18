# Final pass over the 18 published curves

Each curve received an additional 300 seconds of search with 8 workers, 2048 anchors and adaptive mode. Searches ran sequentially, starting from the best points saved by our earlier runs. The engine matched the #302 control run; stopping at the first improvement was disabled.

| ICARM | T | Previous bound ≥ | Final bound ≥ | Search, s |
|---|---|---:|---:|---:|
| [#749](https://elliptic-rank.icarm.cloud/curve/749) | -332/267 | 25 | 25 | 300.00 |
| [#748](https://elliptic-rank.icarm.cloud/curve/748) | -265/221 | 25 | 25 | 300.06 |
| [#750](https://elliptic-rank.icarm.cloud/curve/750) | -83/111 | 24 | 24 | 300.03 |
| [#747](https://elliptic-rank.icarm.cloud/curve/747) | -43/75 | 23 | 23 | 300.05 |
| [#746](https://elliptic-rank.icarm.cloud/curve/746) | -47/80 | 23 | 23 | 300.22 |
| [#740](https://elliptic-rank.icarm.cloud/curve/740) | -47/23 | 23 | 23 | 300.02 |
| [#745](https://elliptic-rank.icarm.cloud/curve/745) | 57/85 | 23 | 23 | 300.06 |
| [#741](https://elliptic-rank.icarm.cloud/curve/741) | -61/126 | 23 | 23 | 300.06 |
| [#739](https://elliptic-rank.icarm.cloud/curve/739) | -27/47 | 22 | 22 | 300.36 |
| [#744](https://elliptic-rank.icarm.cloud/curve/744) | -41/94 | 22 | 22 | 300.04 |
| [#738](https://elliptic-rank.icarm.cloud/curve/738) | -13/47 | 21 | 21 | 300.07 |
| [#743](https://elliptic-rank.icarm.cloud/curve/743) | -19/74 | 21 | 21 | 300.04 |
| [#742](https://elliptic-rank.icarm.cloud/curve/742) | 17/106 | 21 | 21 | 300.04 |
| [#733](https://elliptic-rank.icarm.cloud/curve/733) | -7/12 | 20 | 20 | 300.05 |
| [#735](https://elliptic-rank.icarm.cloud/curve/735) | -12/31 | 20 | 20 | 300.07 |
| [#736](https://elliptic-rank.icarm.cloud/curve/736) | 4/3 | 19 | 19 | 300.06 |
| [#734](https://elliptic-rank.icarm.cloud/curve/734) | 1/4 | 18 | 18 | 300.11 |
| [#737](https://elliptic-rank.icarm.cloud/curve/737) | 4/17 | 18 | 18 | 300.09 |

Completed: 18/18. Improved: 0. Runs left incomplete by errors: 0. Recovered failures: 1.

All reported ranks are lower bounds with exact independence checks. Results, inputs, provenance logs and certificates were saved locally. No new data were submitted to the website.

## Improvements for ICARM

This pass produced no further increases in the rank lower bounds.

For #734, a transient Windows error occurred after 64 seconds while replacing the checkpoint file. The progress reader was fixed to allow that replacement. The search resumed from the saved state with the same settings until the total reached 300 seconds. The search engine was unchanged. The original error log was retained.

Pass completeness and settings verification (see experiment history).
