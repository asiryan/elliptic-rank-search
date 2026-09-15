# Example provenance

The three ICARM curves were originally submitted by Seewoo Lee. Their pages describe Mestre–Fermigier constructions and contain the original independent-point witnesses:

- [Curve #199](https://elliptic-rank.icarm.cloud/curve/199): snapshot lower bound 13; included certificate proves 15.
- [Curve #206](https://elliptic-rank.icarm.cloud/curve/206): snapshot lower bound 12; included certificate proves 14.
- [Curve #212](https://elliptic-rank.icarm.cloud/curve/212): snapshot lower bound 11; included certificate proves 13.

Each folder contains:

| File | Use |
|---|---|
| `equation.json` | Five integral coefficients, with no supplied points |
| `seed.json` | The equation and one declared point for seeded reproduction |
| `points.json` | The complete independently certified witness set |
| `certificate.json` | A replayable exact certificate for that witness set |

The seed is the first public witness point, possibly replaced by its group inverse. On a general Weierstrass equation, the inverse of `(x,y)` is `(x,-y-a1*x-a3)`. This normalization preserves the generated subgroup and does not supply a new direction.

The witness sets and certificates were retained from the local improvement report dated 2026-09-15, with #199 updated from the subsequent saved search that certified 15 independent points. The standalone engine also reproduced the bound 15 from its single declared seed. [summary.json](summary.json) records the snapshot's old bounds, the proved new bounds, source URLs, and the original source-snapshot SHA256. That hash is historical provenance: the complete downloaded snapshot is not distributed here, and checking the mathematical proofs does not require it.

The examples are selected successes, not a random benchmark. The old lower bounds are comparison data only. They are not evidence for our new claims: the included exact certificates provide that evidence.

The `toy/` folder uses `y^2 = x^3 - 25x + 4`. Its seeded input supplies `(0,2)`; it is a small functional example for both entry points.

Credit for the curves and original public points remains with their authors. We acknowledge ICARM and NSF Grant DMS 2425401 for the source data and infrastructure.
