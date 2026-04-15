"""
RDKG Use Case 2: Knowledge gap analysis — diseases with phenotypic
annotation but no treatment in MAxO
=====================================================================
This demonstrates RDKG's value as an analytical resource: by traversing
cross-source edges, we can identify diseases that have rich phenotypic
characterisation (HPOA) but zero MAxO treatment annotations.

These represent high-priority targets for biocuration or drug repurposing
research — a finding that requires integrating HPOA and MAxO in one graph,
which no single source database enables.

This use case satisfies the Database journal requirement for a
"biological discovery or testable hypothesis."
"""

import httpx
import json

API = "http://localhost:8000"

SPARQL_QUERY_GAP = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdkg: <http://rdkg.org/ontology/>
PREFIX mondo: <http://purl.obolibrary.org/obo/MONDO_>

SELECT ?disease ?label ?phenotype_count
WHERE {
  ?disease a rdkg:Disease ;
           rdfs:label ?label ;
           rdkg:hasOrphanetID ?orphanet .

  {
    SELECT ?disease (COUNT(DISTINCT ?phenotype) AS ?phenotype_count)
    WHERE {
      ?disease rdkg:hasPhenotype ?phenotype .
    }
    GROUP BY ?disease
    HAVING (?phenotype_count >= 5)
  }

  FILTER NOT EXISTS {
    ?disease rdkg:hasTreatment ?treatment .
  }
}
ORDER BY DESC(?phenotype_count)
LIMIT 50
"""

CYPHER_QUERY_GAP = """
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
WHERE NOT EXISTS { (d)-[:HAS_TREATMENT]->() }
WITH d, count(p) AS phenotype_count
WHERE phenotype_count >= 5
RETURN d.mondo_id        AS mondo_id,
       d.name            AS disease_name,
       d.orphanet_id     AS orphanet_id,
       phenotype_count
ORDER BY phenotype_count DESC
LIMIT 50
"""


def find_treatment_gaps(use_sparql: bool = False) -> list[dict]:
    """
    Identify diseases with >= 5 HPO phenotype annotations
    but no MAxO treatment, representing curation gaps.
    """
    print("\n[RDKG Use Case 2] Identifying treatment annotation gaps...")
    print(f"Method: {'SPARQL' if use_sparql else 'Cypher'}\n")

    if use_sparql:
        r = httpx.post(f"{API}/sparql", params={"query": SPARQL_QUERY_GAP})
    else:
        r = httpx.post(f"{API}/cypher", params={"query": CYPHER_QUERY_GAP})

    if r.status_code != 200:
        print(f"Query error: {r.text}")
        return []

    results = r.json()
    print(f"Found {len(results)} diseases with phenotypes but no treatment annotation:\n")

    for i, row in enumerate(results[:10], 1):
        if use_sparql:
            name = row.get("label", {}).get("value", "N/A")
            mondo = row.get("disease", {}).get("value", "N/A").split("/")[-1]
            n_pheno = row.get("phenotype_count", {}).get("value", "?")
        else:
            name = row.get("disease_name", "N/A")
            mondo = row.get("mondo_id", "N/A")
            n_pheno = row.get("phenotype_count", "?")
        print(f"  {i:2}. {name}")
        print(f"       {mondo} | {n_pheno} phenotypes annotated | 0 treatments in MAxO")

    return results


def cross_source_completeness_summary() -> dict:
    """
    Summarise annotation completeness across all 5 RDKG sources.
    Shows the proportion of diseases with data in each source — 
    this becomes the data for Figure 4 (coverage statistics).
    """
    print("\n[Coverage summary] Running cross-source completeness audit...\n")

    queries = {
        "total_diseases": "MATCH (d:Disease) RETURN count(d) AS n",
        "with_orphanet":  "MATCH (d:Disease) WHERE d.orphanet_id IS NOT NULL RETURN count(d) AS n",
        "with_hpoa":      "MATCH (d:Disease)-[:HAS_PHENOTYPE]->() WITH d RETURN count(DISTINCT d) AS n",
        "with_clinvar":   "MATCH (d:Disease)-[:HAS_VARIANT]->() WITH d RETURN count(DISTINCT d) AS n",
        "with_maxo":      "MATCH (d:Disease)-[:HAS_TREATMENT]->() WITH d RETURN count(DISTINCT d) AS n",
        "fully_annotated": """
            MATCH (d:Disease)-[:HAS_PHENOTYPE]->()
            MATCH (d)-[:HAS_VARIANT]->()
            MATCH (d)-[:HAS_TREATMENT]->()
            WHERE d.orphanet_id IS NOT NULL
            WITH d RETURN count(DISTINCT d) AS n
        """,
    }

    summary = {}
    for label, query in queries.items():
        r = httpx.post(f"{API}/cypher", params={"query": query})
        if r.status_code == 200:
            n = r.json()[0].get("n", 0)
            summary[label] = n
            print(f"  {label:<22}: {n:,}")

    total = summary.get("total_diseases", 1)
    print("\n  Coverage rates (% of total MONDO diseases):")
    for k, v in summary.items():
        if k != "total_diseases":
            pct = v / total * 100
            print(f"  {k:<22}: {pct:.1f}%")

    return summary


if __name__ == "__main__":
    gaps = find_treatment_gaps(use_sparql=False)
    stats = cross_source_completeness_summary()
    print("\n" + "="*60)
    print("Coverage stats (use for Figure 4 in paper):")
    print(json.dumps(stats, indent=2))
