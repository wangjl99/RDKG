"""
RDKG Use Case 3: AI agent querying RDKG via MCP tools
=====================================================================
This script simulates how Claude (or any MCP-compatible AI agent)
would use the RDKG MCP server to answer a clinical question.

It calls the same tool functions exposed by rdkg_mcp_server.py
directly, so you can run it standalone to verify all tools work
before connecting Claude Desktop.

Clinical question: "A patient presents with retrognathia, short stature,
and macrocephaly. What rare diseases should be considered, and what
treatments are available?"
"""

import httpx
import json

API = "http://localhost:8000"


# ── Simulate MCP tool calls ──────────────────────────────────────────────────

def tool_search_disease(name: str) -> list:
    r = httpx.get(f"{API}/disease/search", params={"name": name})
    return r.json() if r.status_code == 200 else []

def tool_get_phenotypes(mondo_id: str) -> list:
    r = httpx.get(f"{API}/disease/{mondo_id}/phenotypes")
    return r.json() if r.status_code == 200 else []

def tool_get_variants(mondo_id: str) -> list:
    r = httpx.get(f"{API}/disease/{mondo_id}/related")
    return r.json() if r.status_code == 200 else []

def tool_get_treatments(mondo_id: str) -> list:
    r = httpx.get(f"{API}/disease/{mondo_id}/related")
    return r.json() if r.status_code == 200 else []

def tool_diseases_by_phenotype(hpo_id: str) -> list:
    r = httpx.get(f"{API}/phenotype/{hpo_id}/diseases")
    return r.json() if r.status_code == 200 else []

def tool_run_sparql(query: str) -> list:
    r = httpx.post(f"{API}/sparql", params={"query": query})
    return r.json() if r.status_code == 200 else []


# ── AI agent reasoning trace ─────────────────────────────────────────────────

def rdkg_agent_demo():
    """
    Simulates an AI agent working through a clinical question step by step,
    using RDKG MCP tools. Each tool call is logged to show the reasoning trace.
    """
    print("=" * 65)
    print("RDKG AI AGENT DEMO — MCP tool calls")
    print("=" * 65)
    print()
    print("Clinical question:")
    print("  Patient has retrognathia (HP:0000278), short stature (HP:0004322),")
    print("  and macrocephaly (HP:0000256). Autosomal dominant inheritance.")
    print("  What rare diseases should be considered? What treatments exist?")
    print()

    # ── Tool call 1: phenotype → disease ──────────────────────────────────
    print("─" * 65)
    print("Tool call 1: diseases_by_phenotype(hpo_id='HP:0000278')")
    diseases_retrognathia = tool_diseases_by_phenotype("HP:0000278")
    print(f"  → {len(diseases_retrognathia)} diseases with retrognathia")

    print("Tool call 2: diseases_by_phenotype(hpo_id='HP:0004322')")
    diseases_short = tool_diseases_by_phenotype("HP:0004322")
    print(f"  → {len(diseases_short)} diseases with short stature")

    print("Tool call 3: diseases_by_phenotype(hpo_id='HP:0000256')")
    diseases_macro = tool_diseases_by_phenotype("HP:0000256")
    print(f"  → {len(diseases_macro)} diseases with macrocephaly")

    # Find intersection — diseases matching all 3 phenotypes
    ids_retro = {d.get("disease_id") for d in diseases_retrognathia if d.get("disease_id")}
    ids_short = {d.get("disease_id") for d in diseases_short if d.get("disease_id")}
    ids_macro = {d.get("disease_id") for d in diseases_macro if d.get("disease_id")}

    candidates_all3 = ids_retro & ids_short & ids_macro
    candidates_any2 = (ids_retro & ids_short) | (ids_retro & ids_macro) | (ids_short & ids_macro)
    candidates_any2 -= candidates_all3

    print(f"\n  Diseases matching all 3 phenotypes: {len(candidates_all3)}")
    print(f"  Diseases matching 2 of 3 phenotypes: {len(candidates_any2)}")

    # ── Tool call 4: expand top candidate ─────────────────────────────────
    print()
    print("─" * 65)
    top_candidates = list(candidates_all3)[:3] or list(candidates_any2)[:3]

    for mondo_id in top_candidates:
        print(f"\nTool call: get_disease(mondo_id='{mondo_id}')")
        disease_info = tool_search_disease(mondo_id)
        name = disease_info[0].get("name", mondo_id) if disease_info else mondo_id
        print(f"  → Disease: {name}")

        print(f"Tool call: get_phenotypes(mondo_id='{mondo_id}')")
        phenotypes = tool_get_phenotypes(mondo_id)
        print(f"  → {len(phenotypes)} total phenotypes in RDKG (HPOA source)")
        for p in phenotypes[:4]:
            print(f"     {p.get('hpo_id', '')}  {p.get('name', '')}  "
                  f"[{p.get('frequency', p.get('predicate', ''))}]")

        print(f"Tool call: get_variants(mondo_id='{mondo_id}')")
        variants = tool_get_variants(mondo_id)
        print(f"  → {len(variants)} related entities")
        for v in variants[:3]:
            print(f"     {v.get('id', '')}  {v.get('name', '')}  "
                  f"[{v.get('predicate', '')}]")

        print(f"Tool call: get_treatments(mondo_id='{mondo_id}')")
        treatments = tool_get_treatments(mondo_id)
        print(f"  → {len(treatments)} related entities (drugs, genes, variants)")
        for t in treatments[:3]:
            print(f"     {t.get('t.name', '')}  [{t.get('t.maxo_id', '')}]")

    # ── Tool call 5: SPARQL for cross-phenotype query ──────────────────────
    print()
    print("─" * 65)
    print("Tool call: run_sparql — diseases sharing all 3 phenotypes (federated query)")
    sparql_q = """
    PREFIX rdkg: <http://rdkg.org/ontology/>
    SELECT ?disease ?label (COUNT(?pheno) AS ?matches)
    WHERE {
      VALUES ?phenotype { <http://purl.obolibrary.org/obo/HP_0000278>
                          <http://purl.obolibrary.org/obo/HP_0004322>
                          <http://purl.obolibrary.org/obo/HP_0000256> }
      ?disease rdkg:hasPhenotype ?phenotype ;
               <http://www.w3.org/2000/01/rdf-schema#label> ?label .
      BIND(?phenotype AS ?pheno)
    }
    GROUP BY ?disease ?label
    HAVING (?matches >= 2)
    ORDER BY DESC(?matches)
    LIMIT 10
    """
    sparql_results = tool_run_sparql(sparql_q)
    print(f"  → {len(sparql_results)} diseases from SPARQL cross-phenotype query")

    print()
    print("=" * 65)
    print("Agent reasoning summary:")
    print(f"  Top candidates (all 3 phenotypes): {list(candidates_all3)[:5]}")
    print(f"  Recommended next step: review variants + consult genetic specialist")
    print("=" * 65)


if __name__ == "__main__":
    rdkg_agent_demo()
