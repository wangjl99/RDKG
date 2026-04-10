# Neo4j Cypher Query Examples

Comprehensive query examples for the RDAccelerate Rare Disease Knowledge Graph using Neo4j Cypher.

## 📋 Table of Contents

- [Basic Queries](#basic-queries)
- [Disease Queries](#disease-queries)
- [Phenotype Queries](#phenotype-queries)
- [Drug & Treatment Queries](#drug--treatment-queries)
- [Gene & Variant Queries](#gene--variant-queries)
- [Path Queries](#path-queries)
- [Aggregation Queries](#aggregation-queries)
- [Advanced Analytics](#advanced-analytics)

---

## 🔍 Basic Queries

### Count All Nodes

```cypher
MATCH (n)
RETURN count(n) AS total_nodes;
```

### Count All Relationships

```cypher
MATCH ()-[r]->()
RETURN count(r) AS total_relationships;
```

### Count by Entity Type

```cypher
MATCH (n)
RETURN labels(n)[0] AS entity_type, count(n) AS count
ORDER BY count DESC;
```

### Count by Relationship Type

```cypher
MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(r) AS count
ORDER BY count DESC;
```

---

## 🏥 Disease Queries

### Find Disease by Name

```cypher
MATCH (d:Disease)
WHERE d.name CONTAINS 'Marfan'
RETURN d.id, d.name, d.category;
```

### Find Disease by ID

```cypher
MATCH (d:Disease {id: 'MONDO:0007947'})
RETURN d;
```

### Diseases with Most Phenotypes

```cypher
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
RETURN d.id, d.name, count(p) AS phenotype_count
ORDER BY phenotype_count DESC
LIMIT 20;
```

### Diseases in Specific Category

```cypher
MATCH (d:Disease)
WHERE d.name CONTAINS 'dystrophy'
RETURN d.id, d.name
ORDER BY d.name
LIMIT 50;
```

### Disease Hierarchy (Parents)

```cypher
MATCH (d:Disease {id: 'MONDO:0007947'})-[:SUBCLASS_OF]->(parent:Disease)
RETURN d.name AS disease, parent.name AS parent_disease;
```

### Disease Hierarchy (All Ancestors)

```cypher
MATCH path = (d:Disease {id: 'MONDO:0007947'})-[:SUBCLASS_OF*]->(ancestor:Disease)
RETURN [node in nodes(path) | node.name] AS hierarchy;
```

### Disease Siblings (Same Parent)

```cypher
MATCH (d:Disease {id: 'MONDO:0007947'})-[:SUBCLASS_OF]->(parent:Disease)<-[:SUBCLASS_OF]-(sibling:Disease)
WHERE d <> sibling
RETURN sibling.id, sibling.name
LIMIT 20;
```

---

## 🩺 Phenotype Queries

### Find Phenotype by Name

```cypher
MATCH (p:Phenotype)
WHERE p.name CONTAINS 'arachnodactyly'
RETURN p.id, p.name;
```

### Most Common Phenotypes

```cypher
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
RETURN p.id, p.name, count(d) AS disease_count
ORDER BY disease_count DESC
LIMIT 20;
```

### Phenotypes for Specific Disease

```cypher
MATCH (d:Disease {id: 'MONDO:0007947'})-[:HAS_PHENOTYPE]->(p:Phenotype)
RETURN p.id, p.name
ORDER BY p.name;
```

### Phenotype Co-occurrence

```cypher
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p1:Phenotype),
      (d)-[:HAS_PHENOTYPE]->(p2:Phenotype)
WHERE id(p1) < id(p2)
WITH p1, p2, count(d) AS shared_diseases
WHERE shared_diseases > 10
RETURN p1.name, p2.name, shared_diseases
ORDER BY shared_diseases DESC
LIMIT 20;
```

---

## 💊 Drug & Treatment Queries

### Find Drug by Name

```cypher
MATCH (drug:Drug)
WHERE drug.name CONTAINS 'aspirin'
RETURN drug.id, drug.name;
```

### Drugs Treating Specific Disease

```cypher
MATCH (drug:Drug)-[:TREATS]->(d:Disease {id: 'MONDO:0007947'})
RETURN drug.id, drug.name
ORDER BY drug.name;
```

### Diseases Treated by Drug

```cypher
MATCH (drug:Drug {id: 'DrugBank:DB00945'})-[:TREATS]->(d:Disease)
RETURN d.id, d.name
ORDER BY d.name;
```

### Most Versatile Drugs (Treat Most Diseases)

```cypher
MATCH (drug:Drug)-[:TREATS]->(d:Disease)
RETURN drug.id, drug.name, count(d) AS disease_count
ORDER BY disease_count DESC
LIMIT 20;
```

### Medical Procedures (MAXO Treatments)

```cypher
MATCH (t:Treatment)-[:TREATS]->(d:Disease)
RETURN t.id, t.name, count(d) AS disease_count
ORDER BY disease_count DESC;
```

### Combined Drug + Procedure Treatments

```cypher
MATCH (drug:Drug)-[:TREATS]->(d:Disease {id: 'MONDO:0007947'})
OPTIONAL MATCH (treatment:Treatment)-[:TREATS]->(d)
RETURN 
  collect(DISTINCT drug.name) AS drugs,
  collect(DISTINCT treatment.name) AS procedures;
```

---

## 🧬 Gene & Variant Queries

### Find Gene by Symbol

```cypher
MATCH (g:Gene)
WHERE g.name CONTAINS 'FBN1'
RETURN g.id, g.name;
```

### Genes Associated with Disease

```cypher
MATCH (g:Gene)-[:RELATED_TO]->(d:Disease {id: 'MONDO:0007947'})
RETURN g.id, g.name
ORDER BY g.name;
```

### Diseases Associated with Gene

```cypher
MATCH (g:Gene {id: 'NCBIGene:2200'})-[:RELATED_TO]->(d:Disease)
RETURN d.id, d.name
ORDER BY d.name;
```

### Gene-Disease-Phenotype Pathway

```cypher
MATCH (g:Gene {id: 'NCBIGene:2200'})-[:RELATED_TO]->(d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
RETURN g.name AS gene, d.name AS disease, collect(p.name) AS phenotypes
LIMIT 10;
```

### Variants in Gene

```cypher
MATCH (v:Variant)-[:HAS_GENE]->(g:Gene {id: 'NCBIGene:2200'})
RETURN v.id, v.name
LIMIT 20;
```

### Pathogenic Variants Causing Disease

```cypher
MATCH (v:Variant)-[:CAUSES_CONDITION]->(d:Disease {id: 'MONDO:0007947'})
RETURN v.id, v.name
LIMIT 20;
```

---

## 🛤️ Path Queries

### Shortest Path Between Two Diseases

```cypher
MATCH path = shortestPath(
  (d1:Disease {id: 'MONDO:0007947'})-[*..5]-(d2:Disease {id: 'MONDO:0005089'})
)
RETURN path;
```

### All Paths Gene → Disease → Phenotype

```cypher
MATCH path = (g:Gene)-[:RELATED_TO]->(d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
WHERE g.id = 'NCBIGene:2200'
RETURN path
LIMIT 10;
```

### Drug → Disease → Gene Connections

```cypher
MATCH path = (drug:Drug)-[:TREATS]->(d:Disease)<-[:RELATED_TO]-(g:Gene)
WHERE drug.id = 'DrugBank:DB00945'
RETURN path
LIMIT 10;
```

### Complex Path: Variant → Gene → Disease → Phenotype

```cypher
MATCH path = (v:Variant)-[:HAS_GENE]->(g:Gene)-[:RELATED_TO]->(d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
WHERE v.id STARTS WITH 'ClinVar:'
RETURN path
LIMIT 5;
```

---

## 📊 Aggregation Queries

### Statistics by Entity Type

```cypher
MATCH (n)
WITH labels(n)[0] AS entity_type, count(n) AS count
RETURN entity_type, count
ORDER BY count DESC;
```

### Average Phenotypes per Disease

```cypher
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
WITH d, count(p) AS phenotype_count
RETURN 
  avg(phenotype_count) AS avg_phenotypes,
  min(phenotype_count) AS min_phenotypes,
  max(phenotype_count) AS max_phenotypes;
```

### Disease Coverage by Source

```cypher
MATCH (d:Disease)
WHERE d.id STARTS WITH 'MONDO:'
WITH count(d) AS mondo_count
MATCH (d:Disease)
WHERE d.id STARTS WITH 'Orphanet:'
WITH mondo_count, count(d) AS orphanet_count
RETURN mondo_count, orphanet_count;
```

### Relationship Density

```cypher
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
WITH count(d) AS diseases, count(p) AS phenotypes, count(*) AS edges
RETURN diseases, phenotypes, edges, 
       toFloat(edges) / (diseases * phenotypes) AS density;
```

---

## 🔬 Advanced Analytics

### Diseases with No Phenotypes

```cypher
MATCH (d:Disease)
WHERE NOT (d)-[:HAS_PHENOTYPE]->()
RETURN d.id, d.name
LIMIT 20;
```

### Orphan Diseases (No Treatments)

```cypher
MATCH (d:Disease)
WHERE NOT (d)<-[:TREATS]-()
RETURN d.id, d.name
LIMIT 50;
```

### Find Similar Diseases (Shared Phenotypes)

```cypher
MATCH (d1:Disease {id: 'MONDO:0007947'})-[:HAS_PHENOTYPE]->(p:Phenotype)<-[:HAS_PHENOTYPE]-(d2:Disease)
WHERE d1 <> d2
WITH d2, count(p) AS shared_phenotypes
RETURN d2.id, d2.name, shared_phenotypes
ORDER BY shared_phenotypes DESC
LIMIT 20;
```

### Jaccard Similarity Between Diseases

```cypher
MATCH (d1:Disease {id: 'MONDO:0007947'})-[:HAS_PHENOTYPE]->(p1:Phenotype)
WITH d1, collect(p1) AS phenotypes1
MATCH (d2:Disease)-[:HAS_PHENOTYPE]->(p2:Phenotype)
WHERE d1 <> d2
WITH d1, d2, phenotypes1, collect(p2) AS phenotypes2
WITH d1, d2,
     [p IN phenotypes1 WHERE p IN phenotypes2] AS intersection,
     phenotypes1 + [p IN phenotypes2 WHERE NOT p IN phenotypes1] AS union_set
WHERE size(intersection) > 0
RETURN d2.id, d2.name,
       toFloat(size(intersection)) / size(union_set) AS jaccard_similarity
ORDER BY jaccard_similarity DESC
LIMIT 20;
```

### Drug Repurposing Candidates

```cypher
// Find drugs treating diseases with similar phenotypes
MATCH (d1:Disease {id: 'MONDO:0007947'})-[:HAS_PHENOTYPE]->(p:Phenotype)<-[:HAS_PHENOTYPE]-(d2:Disease)
WHERE d1 <> d2
  AND NOT (d1)<-[:TREATS]-()
MATCH (drug:Drug)-[:TREATS]->(d2)
WITH d1, drug, count(p) AS shared_phenotypes
RETURN drug.id, drug.name, shared_phenotypes
ORDER BY shared_phenotypes DESC
LIMIT 10;
```

### Disease Clustering by Phenotype Similarity

```cypher
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
WITH d, collect(p.id) AS phenotype_set
MATCH (other:Disease)-[:HAS_PHENOTYPE]->(p2:Phenotype)
WHERE d <> other
WITH d, other, phenotype_set, collect(p2.id) AS other_phenotypes
WITH d, other,
     [x IN phenotype_set WHERE x IN other_phenotypes] AS intersection
WHERE size(intersection) >= 5
RETURN d.name, collect(other.name) AS similar_diseases
LIMIT 20;
```

### Hub Nodes (Highly Connected)

```cypher
MATCH (n)
WITH n, 
     size((n)-[]->()) AS outgoing,
     size((n)<-[]-()) AS incoming
WHERE outgoing + incoming > 100
RETURN labels(n)[0] AS type, n.name, outgoing, incoming, 
       outgoing + incoming AS total_connections
ORDER BY total_connections DESC
LIMIT 20;
```

### Phenotype Hierarchy Depth

```cypher
MATCH path = (p:Phenotype)-[:SUBCLASS_OF*]->(root)
WHERE NOT (root)-[:SUBCLASS_OF]->()
RETURN p.name, length(path) AS depth
ORDER BY depth DESC
LIMIT 20;
```

---

## 🎯 Use Case Queries

### Clinical Decision Support: Find Differential Diagnoses

```cypher
// Given phenotypes, find matching diseases
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
WHERE p.id IN ['HP:0001166', 'HP:0001634', 'HP:0000789']
WITH d, count(p) AS matching_phenotypes
RETURN d.id, d.name, matching_phenotypes
ORDER BY matching_phenotypes DESC
LIMIT 10;
```

### Variant Interpretation: Pathogenic Variants for Phenotype

```cypher
MATCH (v:Variant)-[:CAUSES_CONDITION]->(d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
WHERE p.id = 'HP:0001166'
RETURN DISTINCT v.id, v.name, d.name
LIMIT 20;
```

### Research: Gene-Disease-Drug Network

```cypher
MATCH (g:Gene)-[:RELATED_TO]->(d:Disease)<-[:TREATS]-(drug:Drug)
WHERE g.id = 'NCBIGene:2200'
RETURN g.name AS gene, 
       collect(DISTINCT d.name) AS diseases,
       collect(DISTINCT drug.name) AS drugs;
```

### Literature Mining: Understudied Diseases

```cypher
// Diseases with many phenotypes but no gene associations
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
WHERE NOT (d)<-[:RELATED_TO]-(:Gene)
WITH d, count(p) AS phenotype_count
WHERE phenotype_count > 10
RETURN d.id, d.name, phenotype_count
ORDER BY phenotype_count DESC
LIMIT 20;
```

---

## 📈 Performance Tips

### Use Indexes

```cypher
// Create indexes for better performance (already created in setup)
CREATE INDEX disease_name IF NOT EXISTS FOR (n:Disease) ON (n.name);
CREATE INDEX gene_name IF NOT EXISTS FOR (n:Gene) ON (n.name);
```

### Profile Queries

```cypher
// Check query performance
PROFILE
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
RETURN d.name, count(p)
ORDER BY count(p) DESC
LIMIT 10;
```

### Limit Results for Exploration

```cypher
// Always use LIMIT during development
MATCH (d:Disease)
RETURN d
LIMIT 25;
```

---

## 🔗 Useful Query Patterns

### Pattern Matching Template

```cypher
MATCH (source:Type)-[:RELATIONSHIP]->(target:Type)
WHERE source.property = 'value'
  AND target.property CONTAINS 'text'
RETURN source, target
ORDER BY source.name
LIMIT 100;
```

### Aggregation Template

```cypher
MATCH (n:Type)-[:RELATIONSHIP]->(m:Type)
WITH n, count(m) AS count
WHERE count > threshold
RETURN n.name, count
ORDER BY count DESC;
```

### Path Finding Template

```cypher
MATCH path = shortestPath(
  (start:Type {id: 'ID1'})-[*..maxHops]-(end:Type {id: 'ID2'})
)
RETURN path;
```

---

**Last Updated**: April 2026  
**Neo4j Version**: 5.15.0
