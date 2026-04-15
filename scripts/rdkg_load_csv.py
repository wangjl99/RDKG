import csv, os, time
from neo4j import GraphDatabase
from collections import defaultdict

URI, USER, PASS = "bolt://localhost:7687", "neo4j", "rdkg_secret"
NODES = "data/nodes_no_trials.csv"
EDGES = "data/edges_no_trials.csv"
BATCH = 500

driver = GraphDatabase.driver(URI, auth=(USER, PASS))
print("Connected to Neo4j")

with driver.session() as s:
    # Constraints
    for label in ["Disease","Phenotype","Gene","Drug","Variant"]:
        try: s.run(f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{label}) REQUIRE n.id IS UNIQUE")
        except: pass
    print("✓ Constraints ready")

    # Load nodes
    print(f"Loading nodes from {NODES}...")
    batch, total = [], 0
    with open(NODES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            nid   = row.get("id:ID","").strip()
            label = row.get(":LABEL","Entity").strip().replace(" ","_").replace(":","_")
            if not nid: continue
            batch.append({"id":nid,"name":row.get("name","").strip(),
                          "label":label,"category":row.get("category","").strip()})
            if len(batch)>=BATCH:
                by_lbl = defaultdict(list)
                for n in batch: by_lbl[n["label"]].append(n)
                for lbl,nodes in by_lbl.items():
                    s.run(f"UNWIND $r AS r MERGE (n:`{lbl}` {{id:r.id}}) SET n.name=r.name,n.category=r.category",r=nodes)
                total+=len(batch); batch=[]
                print(f"  {total:,}...",end="\r")
    if batch:
        by_lbl = defaultdict(list)
        for n in batch: by_lbl[n["label"]].append(n)
        for lbl,nodes in by_lbl.items():
            s.run(f"UNWIND $r AS r MERGE (n:`{lbl}` {{id:r.id}}) SET n.name=r.name,n.category=r.category",r=nodes)
        total+=len(batch)
    print(f"  ✓ {total:,} nodes loaded")

    # Load edges
    print(f"Loading edges from {EDGES}...")
    batch, total = [], 0
    with open(EDGES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            src = row.get(":START_ID","").strip()
            tgt = row.get(":END_ID","").strip()
            rt  = row.get(":TYPE","RELATED_TO").strip().replace(" ","_").replace("-","_")
            if not src or not tgt: continue
            batch.append({"src":src,"tgt":tgt,"rt":rt,"pred":row.get("predicate","").strip()})
            if len(batch)>=BATCH:
                by_type = defaultdict(list)
                for e in batch: by_type[e["rt"]].append(e)
                for rt,edges in by_type.items():
                    s.run(f"UNWIND $r AS r MATCH (a {{id:r.src}}) MATCH (b {{id:r.tgt}}) MERGE (a)-[rel:`{rt}`]->(b) SET rel.predicate=r.pred",r=edges)
                total+=len(batch); batch=[]
                print(f"  {total:,}...",end="\r")
    if batch:
        by_type = defaultdict(list)
        for e in batch: by_type[e["rt"]].append(e)
        for rt,edges in by_type.items():
            s.run(f"UNWIND $r AS r MATCH (a {{id:r.src}}) MATCH (b {{id:r.tgt}}) MERGE (a)-[rel:`{rt}`]->(b) SET rel.predicate=r.pred",r=edges)
        total+=len(batch)
    print(f"  ✓ {total:,} edges loaded")

    # Summary
    print("\n── Summary ─────────────────────────────────")
    for lbl in ["Disease","Phenotype","Gene","Drug","Variant"]:
        n = s.run(f"MATCH (n:{lbl}) RETURN count(n) AS n").single()["n"]
        if n: print(f"  {lbl:<15} {n:>8,}")
    for rt in ["HAS_PHENOTYPE","HAS_VARIANT","HAS_TREATMENT","RELATED_TO"]:
        try:
            n = s.run(f"MATCH ()-[r:{rt}]->() RETURN count(r) AS n").single()["n"]
            if n: print(f"  {rt:<20} {n:>8,}")
        except: pass
    sample = s.run("MATCH (d:Disease) RETURN d.id, d.name LIMIT 3")
    print("\n  Sample diseases:")
    for r in sample: print(f"    {r['d.id']}  {r['d.name']}")

driver.close()
print("\n✓ Done!")
