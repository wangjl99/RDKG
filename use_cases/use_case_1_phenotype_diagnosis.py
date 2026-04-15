"""
RDKG Use Case 1: Phenotype-driven rare disease differential diagnosis
=====================================================================
Given a set of HPO phenotype terms (as a clinician would provide),
traverse RDKG to retrieve candidate diseases ranked by phenotype match,
then expand each candidate to its variants and available treatments.

This demonstrates the core clinical utility of RDKG's multi-source integration:
a single traversal query crosses HPOA (phenotypes), ClinVar (variants),
and MAxO (treatments) — data that lives in three separate databases
but is unified in RDKG under MONDO disease identifiers.
"""

import httpx
import json
from collections import defaultdict

API = "http://localhost:8000"


def phenotype_driven_diagnosis(hpo_terms: list[str], top_n: int = 10) -> dict:
    """
    Core use case: given HPO terms, find candidate diseases and their
    associated variants and treatments from RDKG.

    Parameters
    ----------
    hpo_terms : list of HPO IDs, e.g. ["HP:0000278", "HP:0001250", "HP:0000007"]
    top_n     : number of candidate diseases to return

    Returns
    -------
    dict with candidates, each containing disease info, phenotype overlap,
    known variants, and available treatments
    """
    disease_scores = defaultdict(lambda: {"count": 0, "phenotypes": [], "disease": {}})

    # Step 1: for each HPO term, retrieve associated diseases
    print(f"\n[Step 1] Querying {len(hpo_terms)} HPO terms against RDKG HPOA edges...")
    for hpo_id in hpo_terms:
        r = httpx.get(f"{API}/phenotype/{hpo_id}/diseases")
        if r.status_code != 200:
            print(f"  Warning: {hpo_id} not found in RDKG")
            continue
        diseases = r.json()
        for d in diseases:
            mondo_id = d.get("d.mondo_id")
            if not mondo_id:
                continue
            disease_scores[mondo_id]["count"] += 1
            disease_scores[mondo_id]["disease"] = d
            disease_scores[mondo_id]["phenotypes"].append(hpo_id)
        print(f"  {hpo_id}: {len(diseases)} associated diseases")

    # Step 2: rank by phenotype overlap score
    ranked = sorted(
        disease_scores.items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )[:top_n]

    print(f"\n[Step 2] Top {top_n} candidate diseases by phenotype overlap:")
    results = []
    for mondo_id, info in ranked:
        print(f"\n  {mondo_id} | {info['disease'].get('d.name', 'N/A')}")
        print(f"    Phenotype match: {info['count']}/{len(hpo_terms)} terms")

        # Step 3: expand to variants
        vr = httpx.get(f"{API}/disease/{mondo_id}/variants")
        variants = vr.json() if vr.status_code == 200 else []
        print(f"    Pathogenic variants: {len(variants)}")
        for v in variants[:3]:
            print(f"      {v.get('v.gene', '')} {v.get('v.hgvs', '')} "
                  f"[{v.get('v.clinical_significance', '')}]")

        # Step 4: expand to treatments
        tr = httpx.get(f"{API}/disease/{mondo_id}/treatments")
        treatments = tr.json() if tr.status_code == 200 else []
        print(f"    Available treatments: {len(treatments)}")
        for t in treatments[:3]:
            print(f"      {t.get('t.name', '')} [{t.get('t.maxo_id', '')}]")

        results.append({
            "mondo_id": mondo_id,
            "name": info["disease"].get("d.name"),
            "orphanet_id": info["disease"].get("d.orphanet_id"),
            "phenotype_match_score": f"{info['count']}/{len(hpo_terms)}",
            "matched_phenotypes": info["phenotypes"],
            "variants": variants[:5],
            "treatments": treatments[:5],
        })

    return {"input_hpo_terms": hpo_terms, "candidates": results}


if __name__ == "__main__":
    # Clinical scenario: patient presents with
    # retrognathia (HP:0000278) + short stature (HP:0004322) +
    # autosomal dominant inheritance (HP:0000006)
    # Expected top hit: Achondroplasia (MONDO:0007765)
    demo_hpo = ["HP:0000278", "HP:0004322", "HP:0000006"]
    results = phenotype_driven_diagnosis(demo_hpo, top_n=5)

    print("\n" + "="*60)
    print("RESULTS JSON (for paper Figure / SPARQL comparison):")
    print(json.dumps(results, indent=2))
