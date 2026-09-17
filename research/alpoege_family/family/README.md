# Family and section provenance

The family is identified in the [commentary to ICARM #302](https://elliptic-rank.icarm.cloud/curve/302), credited there to wgxli. Our parameter is exactly `T=u/v`, with coprime integers and positive v; the code also represents infinity as `[1:0]`.

`sections.json` is the unchanged export formerly stored at `artifacts/obsolete/tools/RankHunt/Data/icarm302-sections.json`. Its SHA256 is `2c6a51b978ff22e8d0a31ce30e5e9f7f571f83804edab8d6ff2e45d4e8b96b90`. Its internal provenance names `elliptic_rank_structure_20260914.zip`, the historical RankStructureAudit check, and source-section digest `2af3a624875d00c57b76e124341cd25337e8c344855eab22609a086f34800619`. Those names identify the derivation; the archive and old tools are not runtime requirements.

Coefficients are ordered by increasing power of T. For specialization, x and y are homogenized to degrees four and six. The family model is `[a1,a2,a3,a4,a6] = [-l,d+e,-b,de,0]`, with l,p,q,d,e,b defined in `specialize.py`. The exact verifier checks every polynomial identity on this model. Additional base-change fields are retained historical data, unused by the 21-result reproduction commands.

A valid section identity alone does not establish independence of its specializations. The coordinator checks the specialized seed bound separately and checks all five identities for the minimal-model coordinate transformation. The formulas and source attribution remain fixed when the general search algorithm changes.
