"""
rdkg_diagnose.py
================
Run this first to understand the current state of your Neo4j instance
and diagnose why queries return 0 results.

Usage:
    # Check local Neo4j (your existing RDKG data)
    python rdkg_diagnose.py --uri bolt://localhost:7687 --user neo4j --password YOUR_PASSWORD

    # Check Docker Neo4j (fresh container)
    python rdkg_diagnose.py --uri bolt://localhost:7687 --user neo4j --password rdkg_secret
"""

import argparse
from neo4j import GraphDatabase


def diagnose(uri, user, password):
    print(f"\n{'='*60}")
    print(f"RDKG Neo4j Diagnostic")
    print(f"URI: {uri}")
    print(f"{'='*60}\n")

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("✓ Connection successful\n")
    except Exception as e:
        print(f"✗ Connection FAILED: {e}")
        print("\nFix: check URI, user, password and that Neo4j is running")
        return

    with driver.session() as s:

        # 1. Node label counts
        print("── Node labels ─────────────────────────────────")
        result = s.run("CALL db.labels() YIELD label RETURN label ORDER BY label")
        labels = [r["label"] for r in result]
        if not labels:
            print("  ✗ NO NODES FOUND — database is empty")
            print("  → Run: python rdkg_load.py  to load your data\n")
        else:
            for label in labels:
                count = s.run(f"MATCH (n:`{label}`) RETURN count(n) AS n").single()["n"]
                print(f"  {label:<20} {count:>8,} nodes")

        # 2. Relationship type counts
        print("\n── Relationship types ──────────────────────────")
        result = s.run("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType")
        rel_types = [r["relationshipType"] for r in result]
        if not rel_types:
            print("  ✗ NO RELATIONSHIPS FOUND")
        else:
            for rt in rel_types:
                count = s.run(f"MATCH ()-[r:`{rt}`]->() RETURN count(r) AS n").single()["n"]
                print(f"  {rt:<30} {count:>8,} edges")

        # 3. Check for expected RDKG node properties
        print("\n── Property checks ─────────────────────────────")
        checks = [
            ("Disease with mondo_id",    "MATCH (d:Disease) WHERE d.mondo_id IS NOT NULL RETURN count(d) AS n"),
            ("Disease with orphanet_id", "MATCH (d:Disease) WHERE d.orphanet_id IS NOT NULL RETURN count(d) AS n"),
            ("Phenotype with hpo_id",    "MATCH (p:Phenotype) WHERE p.hpo_id IS NOT NULL RETURN count(p) AS n"),
            ("Variant with clinvar_id",  "MATCH (v:Variant) WHERE v.clinvar_id IS NOT NULL RETURN count(v) AS n"),
            ("Treatment with maxo_id",   "MATCH (t:Treatment) WHERE t.maxo_id IS NOT NULL RETURN count(t) AS n"),
        ]
        for label, query in checks:
            try:
                n = s.run(query).single()["n"]
                status = "✓" if n > 0 else "✗"
                print(f"  {status} {label:<35} {n:>8,}")
            except Exception:
                print(f"  ? {label:<35} (query failed — node/property may not exist yet)")

        # 4. Sample disease node to show what properties exist
        print("\n── Sample disease node ─────────────────────────")
        sample = s.run("MATCH (d:Disease) RETURN d LIMIT 1").single()
        if sample:
            node = dict(sample["d"])
            print(f"  Properties found: {list(node.keys())}")
            for k, v in list(node.items())[:8]:
                print(f"    {k}: {str(v)[:60]}")
        else:
            print("  No Disease nodes to sample.")

        # 5. Connectivity check (are relationships wired correctly?)
        print("\n── Cross-source connectivity ────────────────────")
        connectivity = [
            ("Disease → Phenotype (HPOA)",  "MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p) RETURN count(p) AS n LIMIT 1"),
            ("Disease → Variant (ClinVar)", "MATCH (d:Disease)-[:HAS_VARIANT]->(v) RETURN count(v) AS n LIMIT 1"),
            ("Disease → Treatment (MAxO)",  "MATCH (d:Disease)-[:HAS_TREATMENT]->(t) RETURN count(t) AS n LIMIT 1"),
            ("Disease → Xref (Orphanet)",   "MATCH (d:Disease)-[:HAS_XREF]->(x) RETURN count(x) AS n LIMIT 1"),
        ]
        for label, query in connectivity:
            try:
                n = s.run(query).single()["n"]
                status = "✓" if n > 0 else "✗ relationship missing"
                print(f"  {status} {label}")
            except Exception as e:
                print(f"  ? {label} — {e}")

    driver.close()
    print(f"\n{'='*60}")
    print("If database is empty → run:  python rdkg_load.py")
    print("If properties differ  → edit rdkg_load.py label/property names")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri",      default="bolt://localhost:7687")
    parser.add_argument("--user",     default="neo4j")
    parser.add_argument("--password", default="rdkg_secret")
    args = parser.parse_args()
    diagnose(args.uri, args.user, args.password)
