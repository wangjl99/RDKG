from fastapi import FastAPI, HTTPException, Query
from neo4j import GraphDatabase
import os

app = FastAPI(title="RDKG API", version="2.0")

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=(os.getenv("NEO4J_USER", "neo4j"),
          os.getenv("NEO4J_PASSWORD", "rdkg_secret"))
)

@app.get("/health")
def health():
    try:
        with driver.session() as s:
            s.run("RETURN 1")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/stats")
def stats():
    with driver.session() as s:
        nodes = {}
        for label in ["Disease","Phenotype","Gene","Drug","Variant"]:
            n = s.run(f"MATCH (n:{label}) RETURN count(n) AS n").single()["n"]
            if n: nodes[label] = n
        rels = {}
        r = s.run("CALL db.relationshipTypes() YIELD relationshipType AS rt RETURN rt")
        for row in r:
            rt = row["rt"]
            n = s.run(f"MATCH ()-[r:`{rt}`]->() RETURN count(r) AS n").single()["n"]
            if n: rels[rt] = n
        return {"nodes": nodes, "relationships": rels}

@app.get("/disease/search")
def search_disease(name: str = Query(...)):
    with driver.session() as s:
        result = s.run(
            "MATCH (d:Disease) WHERE toLower(d.name) CONTAINS toLower($name) "
            "RETURN d.id AS id, d.name AS name, d.category AS category LIMIT 20",
            name=name)
        rows = [dict(r) for r in result]
        if not rows:
            raise HTTPException(status_code=404, detail="Disease not found")
        return rows

@app.get("/disease/{disease_id:path}/phenotypes")
def get_phenotypes(disease_id: str):
    with driver.session() as s:
        result = s.run(
            "MATCH (d:Disease {id: $id})-[r:HAS_PHENOTYPE]->(p:Phenotype) "
            "RETURN p.id AS hpo_id, p.name AS name, r.predicate AS predicate "
            "ORDER BY p.name",
            id=disease_id)
        return [dict(r) for r in result]

@app.get("/disease/{disease_id:path}/related")
def get_related(disease_id: str):
    with driver.session() as s:
        result = s.run(
            "MATCH (d:Disease {id: $id})-[r]->(n) "
            "RETURN n.id AS id, n.name AS name, labels(n)[0] AS label, "
            "type(r) AS rel_type, r.predicate AS predicate "
            "ORDER BY labels(n)[0], n.name",
            id=disease_id)
        return [dict(r) for r in result]

@app.get("/disease/{disease_id:path}")
def get_disease(disease_id: str):
    with driver.session() as s:
        result = s.run(
            "MATCH (d:Disease {id: $id}) "
            "RETURN d.id AS id, d.name AS name, d.category AS category",
            id=disease_id)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail=f"Disease '{disease_id}' not found")
        return dict(record)

@app.get("/phenotype/search")
def search_phenotype(name: str = Query(...)):
    with driver.session() as s:
        result = s.run(
            "MATCH (p:Phenotype) WHERE toLower(p.name) CONTAINS toLower($name) "
            "RETURN p.id AS hpo_id, p.name AS name LIMIT 20",
            name=name)
        return [dict(r) for r in result]

@app.get("/phenotype/{hpo_id:path}/diseases")
def diseases_by_phenotype(hpo_id: str):
    with driver.session() as s:
        result = s.run(
            "MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype {id: $id}) "
            "RETURN d.id AS disease_id, d.name AS disease_name, d.category AS category "
            "ORDER BY d.name LIMIT 500",
            id=hpo_id)
        return [dict(r) for r in result]

@app.get("/drug/search")
def search_drug(name: str = Query(...)):
    with driver.session() as s:
        result = s.run(
            "MATCH (dr:Drug) WHERE toLower(dr.name) CONTAINS toLower($name) "
            "RETURN dr.id AS drug_id, dr.name AS name LIMIT 20",
            name=name)
        return [dict(r) for r in result]

@app.post("/cypher")
def cypher_query(query: str):
    blocked = ["CREATE","DELETE","MERGE","SET","DROP","DETACH"]
    if any(kw in query.upper() for kw in blocked):
        raise HTTPException(status_code=403, detail="Write operations not permitted")
    with driver.session() as s:
        result = s.run(query)
        return [dict(r) for r in result]
