# SPARQL Query Examples

Comprehensive SPARQL query examples for the RDAccelerate Rare Disease Knowledge Graph using Apache Jena Fuseki.

## 📋 Table of Contents

- [Basic Queries](#basic-queries)
- [Disease Queries](#disease-queries)
- [Phenotype Queries](#phenotype-queries)
- [Drug & Treatment Queries](#drug--treatment-queries)
- [Gene & Variant Queries](#gene--variant-queries)
- [Federated Queries](#federated-queries)
- [Aggregation & Analytics](#aggregation--analytics)

---

## 🌐 Namespace Prefixes

All queries use these standard prefixes:

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX mondo: <http://purl.obolibrary.org/obo/MONDO_>
PREFIX hp: <http://purl.obolibrary.org/obo/HP_>
PREFIX ncbigene: <http://identifiers.org/ncbigene/>
PREFIX drugbank: <http://identifiers.org/drugbank/>
PREFIX clinvar: <http://www.ncbi.nlm.nih.gov/clinvar/variation/>
PREFIX maxo: <http://purl.obolibrary.org/obo/MAXO_>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
```

---

## 🔍 Basic Queries

### Count All Triples

```sparql
SELECT (COUNT(*) AS ?count)
WHERE {
  ?s ?p ?o
}
```

### Count Entities by Type

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>

SELECT ?type (COUNT(?entity) AS ?count)
WHERE {
  ?entity rdf:type ?type .
  FILTER(STRSTARTS(STR(?type), "https://w3id.org/biolink/vocab/"))
}
GROUP BY ?type
ORDER BY DESC(?count)
```

### Count Relationships by Predicate

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>

SELECT ?predicate (COUNT(*) AS ?count)
WHERE {
  ?s ?predicate ?o .
  FILTER(STRSTARTS(STR(?predicate), "https://w3id.org/biolink/vocab/"))
  FILTER(?predicate != rdf:type)
}
GROUP BY ?predicate
ORDER BY DESC(?count)
```

### List All Diseases (First 100)

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease ?name
WHERE {
  ?disease rdf:type biolink:Disease ;
           rdfs:label ?name .
}
ORDER BY ?name
LIMIT 100
```

---

## 🏥 Disease Queries

### Find Disease by Name

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease ?disease_id ?name
WHERE {
  ?disease rdf:type biolink:Disease ;
           biolink:id ?disease_id ;
           rdfs:label ?name .
  FILTER(CONTAINS(LCASE(?name), "marfan"))
}
```

### Get Disease Details

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property ?value
WHERE {
  <http://purl.obolibrary.org/obo/MONDO_0007947> ?property ?value .
}
```

### Diseases with Most Phenotypes

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease_name (COUNT(?phenotype) AS ?phenotype_count)
WHERE {
  ?disease rdf:type biolink:Disease ;
           rdfs:label ?disease_name ;
           biolink:has_phenotype ?phenotype .
}
GROUP BY ?disease_name
ORDER BY DESC(?phenotype_count)
LIMIT 20
```

### Disease Hierarchy (Parents)

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease_name ?parent_name
WHERE {
  ?disease biolink:id "MONDO:0007947" ;
           rdfs:label ?disease_name ;
           biolink:subclass_of ?parent .
  ?parent rdfs:label ?parent_name .
}
```

### Disease Hierarchy (All Ancestors)

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease_name ?ancestor_name
WHERE {
  ?disease biolink:id "MONDO:0007947" ;
           rdfs:label ?disease_name ;
           biolink:subclass_of+ ?ancestor .
  ?ancestor rdfs:label ?ancestor_name .
}
ORDER BY ?ancestor_name
```

### Diseases in Category

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease_id ?disease_name
WHERE {
  ?disease rdf:type biolink:Disease ;
           biolink:id ?disease_id ;
           rdfs:label ?disease_name .
  FILTER(CONTAINS(LCASE(?disease_name), "dystrophy"))
}
ORDER BY ?disease_name
LIMIT 50
```

---

## 🩺 Phenotype Queries

### Find Phenotype by Name

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?phenotype ?phenotype_id ?name
WHERE {
  ?phenotype rdf:type biolink:PhenotypicFeature ;
             biolink:id ?phenotype_id ;
             rdfs:label ?name .
  FILTER(CONTAINS(LCASE(?name), "arachnodactyly"))
}
```

### Most Common Phenotypes

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?phenotype_name (COUNT(?disease) AS ?disease_count)
WHERE {
  ?disease rdf:type biolink:Disease ;
           biolink:has_phenotype ?phenotype .
  ?phenotype rdfs:label ?phenotype_name .
}
GROUP BY ?phenotype_name
ORDER BY DESC(?disease_count)
LIMIT 20
```

### Phenotypes for Disease

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?phenotype_id ?phenotype_name
WHERE {
  ?disease biolink:id "MONDO:0007947" ;
           biolink:has_phenotype ?phenotype .
  ?phenotype biolink:id ?phenotype_id ;
             rdfs:label ?phenotype_name .
}
ORDER BY ?phenotype_name
```

### Phenotype Co-occurrence

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?p1_name ?p2_name (COUNT(?disease) AS ?shared_diseases)
WHERE {
  ?disease rdf:type biolink:Disease ;
           biolink:has_phenotype ?p1, ?p2 .
  ?p1 rdfs:label ?p1_name .
  ?p2 rdfs:label ?p2_name .
  FILTER(?p1 != ?p2 && STR(?p1) < STR(?p2))
}
GROUP BY ?p1_name ?p2_name
HAVING (COUNT(?disease) > 10)
ORDER BY DESC(?shared_diseases)
LIMIT 20
```

---

## 💊 Drug & Treatment Queries

### Find Drug by Name

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?drug ?drug_id ?name
WHERE {
  ?drug rdf:type biolink:Drug ;
        biolink:id ?drug_id ;
        rdfs:label ?name .
  FILTER(CONTAINS(LCASE(?name), "aspirin"))
}
```

### Drugs Treating Disease

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?drug_name
WHERE {
  ?drug rdf:type biolink:Drug ;
        rdfs:label ?drug_name ;
        biolink:treats ?disease .
  ?disease biolink:id "MONDO:0007947" .
}
ORDER BY ?drug_name
```

### Diseases Treated by Drug

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease_id ?disease_name
WHERE {
  ?drug biolink:id "DrugBank:DB00945" ;
        biolink:treats ?disease .
  ?disease biolink:id ?disease_id ;
           rdfs:label ?disease_name .
}
ORDER BY ?disease_name
```

### Most Versatile Drugs

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?drug_name (COUNT(?disease) AS ?disease_count)
WHERE {
  ?drug rdf:type biolink:Drug ;
        rdfs:label ?drug_name ;
        biolink:treats ?disease .
}
GROUP BY ?drug_name
ORDER BY DESC(?disease_count)
LIMIT 20
```

### Medical Procedures (MAXO Treatments)

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?treatment_name (COUNT(?disease) AS ?disease_count)
WHERE {
  ?treatment rdf:type biolink:Treatment ;
             rdfs:label ?treatment_name ;
             biolink:treats ?disease .
}
GROUP BY ?treatment_name
ORDER BY DESC(?disease_count)
```

### Combined Drug + Procedure Treatments

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease_name 
       (GROUP_CONCAT(DISTINCT ?drug_name; separator=", ") AS ?drugs)
       (GROUP_CONCAT(DISTINCT ?treatment_name; separator=", ") AS ?procedures)
WHERE {
  ?disease biolink:id "MONDO:0007947" ;
           rdfs:label ?disease_name .
  
  OPTIONAL {
    ?drug rdf:type biolink:Drug ;
          rdfs:label ?drug_name ;
          biolink:treats ?disease .
  }
  
  OPTIONAL {
    ?treatment rdf:type biolink:Treatment ;
               rdfs:label ?treatment_name ;
               biolink:treats ?disease .
  }
}
GROUP BY ?disease_name
```

---

## 🧬 Gene & Variant Queries

### Find Gene by Symbol

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?gene ?gene_id ?name
WHERE {
  ?gene rdf:type biolink:Gene ;
        biolink:id ?gene_id ;
        rdfs:label ?name .
  FILTER(CONTAINS(?name, "FBN1"))
}
```

### Genes Associated with Disease

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?gene_id ?gene_name
WHERE {
  ?gene rdf:type biolink:Gene ;
        biolink:id ?gene_id ;
        rdfs:label ?gene_name ;
        biolink:related_to ?disease .
  ?disease biolink:id "MONDO:0007947" .
}
ORDER BY ?gene_name
```

### Diseases Associated with Gene

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease_id ?disease_name
WHERE {
  ?gene biolink:id "NCBIGene:2200" ;
        biolink:related_to ?disease .
  ?disease biolink:id ?disease_id ;
           rdfs:label ?disease_name .
}
ORDER BY ?disease_name
```

### Gene-Disease-Phenotype Pathway

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?gene_name ?disease_name (GROUP_CONCAT(?phenotype_name; separator=", ") AS ?phenotypes)
WHERE {
  ?gene biolink:id "NCBIGene:2200" ;
        rdfs:label ?gene_name ;
        biolink:related_to ?disease .
  ?disease rdfs:label ?disease_name ;
           biolink:has_phenotype ?phenotype .
  ?phenotype rdfs:label ?phenotype_name .
}
GROUP BY ?gene_name ?disease_name
LIMIT 10
```

### Variants Causing Disease

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?variant_id ?variant_name
WHERE {
  ?variant rdf:type biolink:SequenceVariant ;
           biolink:id ?variant_id ;
           rdfs:label ?variant_name ;
           biolink:causes_condition ?disease .
  ?disease biolink:id "MONDO:0007947" .
}
LIMIT 20
```

---

## 🌍 Federated Queries

### Query Multiple Endpoints (Example)

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease_name ?external_data
WHERE {
  # Local query
  ?disease rdf:type biolink:Disease ;
           biolink:id "MONDO:0007947" ;
           rdfs:label ?disease_name .
  
  # Federated query to external SPARQL endpoint
  SERVICE <http://external-endpoint.org/sparql> {
    ?external_resource owl:sameAs ?disease ;
                      rdfs:comment ?external_data .
  }
}
```

---

## 📊 Aggregation & Analytics

### Disease Statistics

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>

SELECT 
  (COUNT(DISTINCT ?disease) AS ?total_diseases)
  (AVG(?phenotype_count) AS ?avg_phenotypes_per_disease)
  (MAX(?phenotype_count) AS ?max_phenotypes)
WHERE {
  {
    SELECT ?disease (COUNT(?phenotype) AS ?phenotype_count)
    WHERE {
      ?disease rdf:type biolink:Disease ;
               biolink:has_phenotype ?phenotype .
    }
    GROUP BY ?disease
  }
}
```

### Entity Type Distribution

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>

SELECT ?type (COUNT(?entity) AS ?count)
WHERE {
  VALUES ?type {
    biolink:Disease
    biolink:PhenotypicFeature
    biolink:Gene
    biolink:Drug
    biolink:Treatment
    biolink:SequenceVariant
  }
  ?entity rdf:type ?type .
}
GROUP BY ?type
ORDER BY DESC(?count)
```

### Relationship Statistics

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>

SELECT ?predicate (COUNT(*) AS ?count)
WHERE {
  ?s ?predicate ?o .
  FILTER(?predicate IN (
    biolink:has_phenotype,
    biolink:treats,
    biolink:related_to,
    biolink:subclass_of
  ))
}
GROUP BY ?predicate
ORDER BY DESC(?count)
```

### Find Similar Diseases (Shared Phenotypes)

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease2_name (COUNT(?phenotype) AS ?shared_phenotypes)
WHERE {
  ?disease1 biolink:id "MONDO:0007947" ;
            biolink:has_phenotype ?phenotype .
  
  ?disease2 biolink:has_phenotype ?phenotype ;
            rdfs:label ?disease2_name .
  
  FILTER(?disease1 != ?disease2)
}
GROUP BY ?disease2_name
ORDER BY DESC(?shared_phenotypes)
LIMIT 20
```

### Drug Repurposing Candidates

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?drug_name (COUNT(DISTINCT ?shared_phenotype) AS ?shared_phenotypes)
WHERE {
  # Target disease and its phenotypes
  ?target_disease biolink:id "MONDO:0007947" ;
                  biolink:has_phenotype ?shared_phenotype .
  
  # Other diseases with shared phenotypes
  ?similar_disease biolink:has_phenotype ?shared_phenotype .
  FILTER(?target_disease != ?similar_disease)
  
  # Drugs treating similar diseases
  ?drug rdf:type biolink:Drug ;
        rdfs:label ?drug_name ;
        biolink:treats ?similar_disease .
  
  # But not treating target disease
  FILTER NOT EXISTS {
    ?drug biolink:treats ?target_disease .
  }
}
GROUP BY ?drug_name
HAVING (COUNT(DISTINCT ?shared_phenotype) > 5)
ORDER BY DESC(?shared_phenotypes)
LIMIT 10
```

---

## 🎯 Advanced Queries

### Construct New Graph

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT {
  ?disease biolink:has_phenotype ?phenotype .
  ?disease rdfs:label ?disease_name .
  ?phenotype rdfs:label ?phenotype_name .
}
WHERE {
  ?disease biolink:id "MONDO:0007947" ;
           rdfs:label ?disease_name ;
           biolink:has_phenotype ?phenotype .
  ?phenotype rdfs:label ?phenotype_name .
}
```

### ASK Query (Boolean)

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>

ASK {
  ?disease biolink:id "MONDO:0007947" ;
           biolink:has_phenotype ?phenotype .
  ?phenotype biolink:id "HP:0001166" .
}
```

### DESCRIBE Query

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>

DESCRIBE <http://purl.obolibrary.org/obo/MONDO_0007947>
```

---

## 🔧 Query Optimization Tips

### Use FILTER Early

```sparql
# Good - filter early
SELECT ?disease_name
WHERE {
  ?disease rdf:type biolink:Disease .
  FILTER(CONTAINS(LCASE(?disease_name), "marfan"))
  ?disease rdfs:label ?disease_name .
}

# Less efficient - filter late
SELECT ?disease_name
WHERE {
  ?disease rdf:type biolink:Disease ;
           rdfs:label ?disease_name .
  FILTER(CONTAINS(LCASE(?disease_name), "marfan"))
}
```

### Use LIMIT for Testing

```sparql
# Always limit during development
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
}
LIMIT 100
```

### Use Property Paths Wisely

```sparql
# Efficient for known depth
biolink:subclass_of/biolink:subclass_of/biolink:subclass_of

# Flexible but potentially slow
biolink:subclass_of+

# With depth limit
biolink:subclass_of{1,5}
```

---

## 📝 Query Templates

### Basic SELECT Template

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?variable1 ?variable2
WHERE {
  ?entity rdf:type biolink:Type ;
          biolink:property ?variable1 ;
          rdfs:label ?variable2 .
  FILTER(?condition)
}
ORDER BY ?variable1
LIMIT 100
```

### Aggregation Template

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>

SELECT ?group_var (COUNT(?count_var) AS ?count)
WHERE {
  ?entity rdf:type biolink:Type ;
          biolink:property ?group_var ;
          biolink:relation ?count_var .
}
GROUP BY ?group_var
HAVING (COUNT(?count_var) > threshold)
ORDER BY DESC(?count)
```

---

**Last Updated**: April 2026  
**SPARQL Version**: 1.1  
**Endpoint**: http://localhost:3030/rdaccelerate/sparql
