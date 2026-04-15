"""
rdkg_load.py
============
Loads RDKG data into the Docker Neo4j container.

Strategy A (recommended): Export from your LOCAL Neo4j → load into Docker Neo4j
Strategy B: Load directly from source CSV/TSV files (MONDO, HPOA, ClinVar, MAxO)

Run diagnosis first:
    python scripts/rdkg_diagnose.py --uri bolt://localhost:7687 --password YOUR_LOCAL_PW
    python scripts/rdkg_diagnose.py --uri bolt://localhost:7687 --password rdkg_secret

Usage:
    # Strategy A: mirror local → docker
    python rdkg_load.py --strategy mirror \
        --src-uri bolt://localhost:7687 --src-password YOUR_LOCAL_PASSWORD \
        --dst-uri bolt://localhost:7687 --dst-password rdkg_secret

    # Strategy B: load from source files (edit DATA_DIR below)
    python rdkg_load.py --strategy files
"""

import argparse
import os
from neo4j import GraphDatabase

# ── Edit these paths to point to your source data files ──────────────────────
DATA_DIR = "./data"

SOURCE_FILES = {
    # MONDO TSV with columns: mondo_id, name, synonyms, orphanet_id, omim_id
    "mondo":   os.path.join(DATA_DIR, "mondo_diseases_simple.tsv"),
    # HPOA TSV with columns: database_id, disease_name, hpo_id, frequency, onset
    "hpoa":    os.path.join(DATA_DIR, "phenotype.hpoa"),
    # ClinVar TSV: mondo_id / omim_id, gene, hgvs, clinical_significance
    "clinvar": os.path.join(DATA_DIR, "clinvar_rare_disease.tsv"),
    # MAxO TSV: disease_id, disease_name, action_id, action_name, relation
    "maxo":    os.path.join(DATA_DIR, "maxo_disease_citation_relationships.csv"),
}
# ─────────────────────────────────────────────────────────────────────────────


# ── Strategy A: Mirror local Neo4j → Docker Neo4j ────────────────────────────

def mirror_neo4j(src_uri, src_user, src_pw, dst_uri, dst_user, dst_pw, batch=500):
    """
    Reads Disease, Phenotype, Variant, Treatment nodes and their
    relationships from a source Neo4j and writes them to a destination.
    """
    src = GraphDatabase.driver(src_uri, auth=(src_user, src_pw))
    dst = GraphDatabase.driver(dst_uri, auth=(dst_user, dst_pw))

    print("Mirroring Neo4j: source → docker\n")

    with src.session() as sr, dst.session() as dr:

        # ── Diseases ──────────────────────────────────────────────────────
        print("Loading Disease nodes...")
        result = sr.run("MATCH (d:Disease) RETURN properties(d) AS props")
        batch_data = []
        for i, record in enumerate(result):
            batch_data.append(record["props"])
            if len(batch_data) >= batch:
                dr.run("UNWIND $rows AS r MERGE (d:Disease {mondo_id: r.mondo_id}) SET d += r",
                       rows=batch_data)
                print(f"  {i+1} diseases...", end="\r")
                batch_data = []
        if batch_data:
            dr.run("UNWIND $rows AS r MERGE (d:Disease {mondo_id: r.mondo_id}) SET d += r",
                   rows=batch_data)
        count = dr.run("MATCH (d:Disease) RETURN count(d) AS n").single()["n"]
        print(f"  ✓ {count:,} Disease nodes loaded")

        # ── Phenotypes ────────────────────────────────────────────────────
        print("Loading Phenotype nodes...")
        result = sr.run("MATCH (p:Phenotype) RETURN properties(p) AS props")
        batch_data = [r["props"] for r in result]
        for i in range(0, len(batch_data), batch):
            dr.run("UNWIND $rows AS r MERGE (p:Phenotype {hpo_id: r.hpo_id}) SET p += r",
                   rows=batch_data[i:i+batch])
        count = dr.run("MATCH (p:Phenotype) RETURN count(p) AS n").single()["n"]
        print(f"  ✓ {count:,} Phenotype nodes loaded")

        # ── Variants ──────────────────────────────────────────────────────
        print("Loading Variant nodes...")
        result = sr.run("MATCH (v:Variant) RETURN properties(v) AS props")
        batch_data = [r["props"] for r in result]
        for i in range(0, len(batch_data), batch):
            dr.run("UNWIND $rows AS r MERGE (v:Variant {clinvar_id: r.clinvar_id}) SET v += r",
                   rows=batch_data[i:i+batch])
        count = dr.run("MATCH (v:Variant) RETURN count(v) AS n").single()["n"]
        print(f"  ✓ {count:,} Variant nodes loaded")

        # ── Treatments ────────────────────────────────────────────────────
        print("Loading Treatment nodes...")
        result = sr.run("MATCH (t:Treatment) RETURN properties(t) AS props")
        batch_data = [r["props"] for r in result]
        for i in range(0, len(batch_data), batch):
            dr.run("UNWIND $rows AS r MERGE (t:Treatment {maxo_id: r.maxo_id}) SET t += r",
                   rows=batch_data[i:i+batch])
        count = dr.run("MATCH (t:Treatment) RETURN count(t) AS n").single()["n"]
        print(f"  ✓ {count:,} Treatment nodes loaded")

        # ── Relationships ─────────────────────────────────────────────────
        rel_queries = {
            "HAS_PHENOTYPE": """
                MATCH (d:Disease)-[r:HAS_PHENOTYPE]->(p:Phenotype)
                RETURN d.mondo_id AS src, p.hpo_id AS tgt,
                       properties(r) AS props
            """,
            "HAS_VARIANT": """
                MATCH (d:Disease)-[r:HAS_VARIANT]->(v:Variant)
                RETURN d.mondo_id AS src, v.clinvar_id AS tgt,
                       properties(r) AS props
            """,
            "HAS_TREATMENT": """
                MATCH (d:Disease)-[r:HAS_TREATMENT]->(t:Treatment)
                RETURN d.mondo_id AS src, t.maxo_id AS tgt,
                       properties(r) AS props
            """,
        }

        dst_rel_queries = {
            "HAS_PHENOTYPE": """
                UNWIND $rows AS r
                MATCH (d:Disease {mondo_id: r.src})
                MATCH (p:Phenotype {hpo_id: r.tgt})
                MERGE (d)-[rel:HAS_PHENOTYPE]->(p) SET rel += r.props
            """,
            "HAS_VARIANT": """
                UNWIND $rows AS r
                MATCH (d:Disease {mondo_id: r.src})
                MATCH (v:Variant {clinvar_id: r.tgt})
                MERGE (d)-[rel:HAS_VARIANT]->(v) SET rel += r.props
            """,
            "HAS_TREATMENT": """
                UNWIND $rows AS r
                MATCH (d:Disease {mondo_id: r.src})
                MATCH (t:Treatment {maxo_id: r.tgt})
                MERGE (d)-[rel:HAS_TREATMENT]->(t) SET rel += r.props
            """,
        }

        for rel_type, src_q in rel_queries.items():
            print(f"Loading {rel_type} relationships...")
            result = sr.run(src_q)
            batch_data = [{"src": r["src"], "tgt": r["tgt"], "props": r["props"]}
                          for r in result]
            for i in range(0, len(batch_data), batch):
                dr.run(dst_rel_queries[rel_type], rows=batch_data[i:i+batch])
            print(f"  ✓ {len(batch_data):,} {rel_type} edges loaded")

    src.close()
    dst.close()
    print("\n✓ Mirror complete. Run diagnose.py to verify.")


# ── Strategy B: Load from source files ───────────────────────────────────────

def load_from_files(dst_uri, dst_user, dst_pw):
    """
    Loads RDKG directly from your source TSV/CSV files.
    Edit SOURCE_FILES paths at the top of this script.
    """
    import csv
    driver = GraphDatabase.driver(dst_uri, auth=(dst_user, dst_pw))

    with driver.session() as s:

        # Indexes for performance
        print("Creating indexes...")
        for idx in [
            "CREATE INDEX IF NOT EXISTS FOR (d:Disease) ON (d.mondo_id)",
            "CREATE INDEX IF NOT EXISTS FOR (p:Phenotype) ON (p.hpo_id)",
            "CREATE INDEX IF NOT EXISTS FOR (v:Variant) ON (v.clinvar_id)",
            "CREATE INDEX IF NOT EXISTS FOR (t:Treatment) ON (t.maxo_id)",
        ]:
            s.run(idx)

        # ── MONDO diseases ────────────────────────────────────────────────
        path = SOURCE_FILES["mondo"]
        if os.path.exists(path):
            print(f"Loading MONDO from {path}...")
            batch, total = [], 0
            with open(path) as f:
                reader = csv.DictReader(f, delimiter="\t")
                for row in reader:
                    # Adjust column names to match your actual file headers
                    batch.append({
                        "mondo_id":    row.get("MONDO_ID", row.get("mondo_id", "")),
                        "name":        row.get("Primary_Label", row.get("name", "")),
                        "orphanet_id": row.get("Orphanet_IDs", row.get("orphanet_id", "")),
                        "omim_id":     row.get("OMIM_IDs", row.get("omim_id", "")),
                    })
                    if len(batch) >= 500:
                        s.run("UNWIND $rows AS r MERGE (d:Disease {mondo_id: r.mondo_id}) SET d += r",
                              rows=batch)
                        total += len(batch); batch = []
            if batch:
                s.run("UNWIND $rows AS r MERGE (d:Disease {mondo_id: r.mondo_id}) SET d += r",
                      rows=batch)
                total += len(batch)
            print(f"  ✓ {total:,} Disease nodes")
        else:
            print(f"  ✗ MONDO file not found: {path}")

        # ── HPOA phenotype annotations ────────────────────────────────────
        path = SOURCE_FILES["hpoa"]
        if os.path.exists(path):
            print(f"Loading HPOA from {path}...")
            phenotype_nodes, edges, total = {}, [], 0
            with open(path) as f:
                for line in f:
                    if line.startswith("#") or line.startswith("database_id"):
                        continue
                    parts = line.strip().split("\t")
                    if len(parts) < 4:
                        continue
                    db_id    = parts[0]   # OMIM:xxxxxx or ORPHA:xxx
                    hpo_id   = parts[3]   # HP:xxxxxxx
                    freq     = parts[7] if len(parts) > 7 else ""
                    onset    = parts[8] if len(parts) > 8 else ""
                    phenotype_nodes[hpo_id] = hpo_id
                    edges.append({"db_id": db_id, "hpo_id": hpo_id,
                                  "frequency": freq, "onset": onset})

            # Phenotype nodes
            pheno_list = [{"hpo_id": hid} for hid in phenotype_nodes]
            for i in range(0, len(pheno_list), 500):
                s.run("UNWIND $rows AS r MERGE (p:Phenotype {hpo_id: r.hpo_id})",
                      rows=pheno_list[i:i+500])
            print(f"  ✓ {len(pheno_list):,} Phenotype nodes")

            # Disease-phenotype edges (match on OMIM or ORPHA xref on Disease)
            for i in range(0, len(edges), 500):
                s.run("""
                    UNWIND $rows AS r
                    MATCH (d:Disease)
                    WHERE d.omim_id CONTAINS r.db_id
                       OR d.orphanet_id CONTAINS r.db_id
                       OR d.mondo_id = r.db_id
                    MATCH (p:Phenotype {hpo_id: r.hpo_id})
                    MERGE (d)-[rel:HAS_PHENOTYPE]->(p)
                    SET rel.frequency = r.frequency, rel.onset = r.onset
                """, rows=edges[i:i+500])
            print(f"  ✓ {len(edges):,} HAS_PHENOTYPE edges")
        else:
            print(f"  ✗ HPOA file not found: {path}")

        # ── MAxO treatments ───────────────────────────────────────────────
        path = SOURCE_FILES["maxo"]
        if os.path.exists(path):
            print(f"Loading MAxO from {path}...")
            import csv as csv_mod
            treatments, edges, total = {}, [], 0
            with open(path) as f:
                reader = csv_mod.DictReader(f)
                for row in reader:
                    disease_id = row.get("disease_id", "")
                    # MAxO file may have PMID citations, not maxo action IDs
                    # Adjust based on your actual column structure
                    action = row.get("action_id", row.get("citation", ""))
                    name   = row.get("action_name", row.get("relationship_type", ""))
                    if not action:
                        continue
                    treatments[action] = name
                    edges.append({"disease_id": disease_id,
                                  "maxo_id": action, "name": name})

            t_list = [{"maxo_id": k, "name": v} for k, v in treatments.items()]
            for i in range(0, len(t_list), 500):
                s.run("UNWIND $rows AS r MERGE (t:Treatment {maxo_id: r.maxo_id}) SET t.name = r.name",
                      rows=t_list[i:i+500])
            print(f"  ✓ {len(t_list):,} Treatment nodes")

            for i in range(0, len(edges), 500):
                s.run("""
                    UNWIND $rows AS r
                    MATCH (d:Disease)
                    WHERE d.mondo_id = r.disease_id OR d.omim_id CONTAINS r.disease_id
                    MATCH (t:Treatment {maxo_id: r.maxo_id})
                    MERGE (d)-[:HAS_TREATMENT]->(t)
                """, rows=edges[i:i+500])
            print(f"  ✓ {len(edges):,} HAS_TREATMENT edges")
        else:
            print(f"  ✗ MAxO file not found: {path}")

    driver.close()
    print("\n✓ Load complete. Run: python scripts/rdkg_diagnose.py")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", choices=["mirror", "files"], default="mirror",
                        help="mirror = copy from local Neo4j; files = load from source TSV/CSV")
    parser.add_argument("--src-uri",      default="bolt://localhost:7687")
    parser.add_argument("--src-user",     default="neo4j")
    parser.add_argument("--src-password", default="",
                        help="Password for your LOCAL existing Neo4j")
    parser.add_argument("--dst-uri",      default="bolt://localhost:7687")
    parser.add_argument("--dst-user",     default="neo4j")
    parser.add_argument("--dst-password", default="rdkg_secret",
                        help="Password for Docker Neo4j (rdkg_secret by default)")
    args = parser.parse_args()

    if args.strategy == "mirror":
        if not args.src_password:
            print("Error: --src-password required for mirror strategy")
            print("Usage: python rdkg_load.py --strategy mirror --src-password YOUR_PW")
        else:
            mirror_neo4j(
                args.src_uri,  args.src_user, args.src_password,
                args.dst_uri,  args.dst_user, args.dst_password
            )
    else:
        load_from_files(args.dst_uri, args.dst_user, args.dst_password)
