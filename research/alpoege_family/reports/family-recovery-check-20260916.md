# Brief recovery check from 17 sections

| ICARM | T | Input points | Certified result | Search time |
|---|---|---:|---:|---:|
| [#302](https://elliptic-rank.icarm.cloud/curve/302) | 164518/924945 | 17 | ≥31 | 147.94 s |
| [#727](https://elliptic-rank.icarm.cloud/curve/727) | -311/519 | 17 | ≥26 | 13.33 s |

Both curves are specializations of the same ICARM302 family. The initial 17 points were recomputed from the generic formulas; the model transformation and agreement with the ICARM equations were checked exactly. The sets match the archived inputs up to sign and order.
Searches using the then-current seeded.py ran in fresh directories without resuming earlier results. Settings were adaptive mode, 2048 anchors and 8 workers per curve. Inputs contained only the equation and 17 generic points; published additional points were not supplied to the search.
Independence, curve membership, input hashes, provenance of points from the initial set or search logs, and data-read boundaries were checked again for the results. An extension retaining the original 17 points was also saved separately.
Archived certificates for 26 and 31 were checked again. For the archived blind-record-v3, hashes of every file in the manifest were verified. Its audit records that neither reference points nor the recipe were read during the run itself; the known curve had previously been used in developing the method. The earlier guided recovery of 31 published points is a separate experiment using known answers.
**This recovers independent sets establishing rank lower bounds. It does not prove completeness of the rational-point group, saturation of the subgroup found, or the exact rank. The common family supplies 17 sections but does not guarantee that every additional independent direction can be found quickly at each T.**

Results (historical local artifact) · Archive verification (historical local artifact)
