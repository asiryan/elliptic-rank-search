# Experiment index

| Definition | Purpose | Starting data |
|---|---|---|
| [grid-smoke.json](grid-smoke.json) | Small installation check at H=8 | Family equation, modular scores |
| [grid-2048.json](grid-2048.json) | Historical exhaustive parameter grid: 5,102,343 primitive pairs | Family equation; 16,384 retained, 1,024 refined, 384 finalists |
| [sample-two-million.json](sample-two-million.json) | Six million primitive parameter draws at H=2,000,000, fixed seed 202609162 | Independent scoring bands, random reservoir and CRT sampling |
| [final-300s.json](final-300s.json) | Eighteen final continuation searches | Published complete witness sets, 300 seconds each |
| Each case's `reproduction.json` | Fresh recovery of a published lower bound | Generic section formulas or one declared public seed |

Use `ers-research campaign` for grid/sample definitions, `ers-research reproduce` for fresh case recipes, and `ers-research deepen --study alpoege_family --seconds 300` for continuation. See [the guide](../../../docs/REPRODUCIBILITY.md) for complete commands.

The `history/` directory preserves selected original plans and summaries with a [source index](history/manifest.json). JSON formatting and line endings may be normalized by Git. These are historical observations, not portable executable recipes. Absolute paths and references to undistributed working checkpoints inside those files are retained only to identify their original context. Full temporary logs and huge search checkpoints remain outside version control.

The [reports](../reports/) explain the broader search, audits of small parameters, controls and final continuation. Exploratory auxiliary-family reports are archived context; the supported fresh reproduction commands target the 21 published contributions and the two declared controls. No claim is made that every exploratory pilot has been packaged as a runnable experiment.
