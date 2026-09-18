# Family and section provenance

The family is identified in the [commentary to ICARM #302](https://elliptic-rank.icarm.cloud/curve/302), credited there to wgxli. Our parameter is exactly `T=u/v`, with coprime integers and positive v; the code also represents infinity as `[1:0]`.

`sections.json` contains the original exported section formulas. Its source note identifies the historical reconstruction archive and independent RankStructureAudit check. The formulas can be verified directly with `ers-research sections`; the archive and old tools are not runtime requirements.

Coefficients are ordered by increasing power of T. For specialization, x and y are homogenized to degrees four and six. The family model is `[a1,a2,a3,a4,a6] = [-l,d+e,-b,de,0]`, with l,p,q,d,e,b defined in `specialize.py`. The exact verifier checks every polynomial identity on this model. Additional base-change fields are retained historical data, unused by the 21-result reproduction commands.

A valid section identity alone does not establish independence of its specializations. The coordinator checks the specialized seed bound separately and checks all five identities for the minimal-model coordinate transformation. The formulas and source attribution remain fixed when the general search algorithm changes.
