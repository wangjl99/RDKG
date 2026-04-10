# Knowledge Graph Schema

This document defines the structure, ontologies, and relationships in the RDAccelerate Rare Disease Knowledge Graph.

## 📋 Table of Contents

- [Entity Types](#entity-types)
- [Relationship Types](#relationship-types)
- [Ontologies](#ontologies)
- [Biolink Model Compliance](#biolink-model-compliance)
- [Namespaces](#namespaces)
- [Data Model](#data-model)

---

## 🏷️ Entity Types

### Disease (26,106 entities)

**Label**: `Disease`  
**Category**: `biolink:Disease`  
**Primary Sources**: MONDO, Orphanet

**Properties**:
- `id`: Unique identifier (e.g., `MONDO:0007947`, `Orphanet:558`)
- `name`: Human-readable disease name
- `category`: Entity type (`biolink:Disease`)

**ID Patterns**:
- MONDO diseases: `MONDO:0000001` to `MONDO:9999999`
- Orphanet diseases: `Orphanet:1` to `Orphanet:999999`
- Grouped MONDO: `MONDO_GROUPED:GROUP_<hash>`

**Examples**:
```
MONDO:0007947 - "Marfan syndrome"
Orphanet:558 - "Marfan syndrome"
MONDO:0018949 - "hereditary connective tissue disorder"
```

---

### Phenotype (11,708 entities)

**Label**: `Phenotype`  
**Category**: `biolink:PhenotypicFeature`  
**Primary Source**: HPO (Human Phenotype Ontology)

**Properties**:
- `id`: HPO identifier (e.g., `HP:0000001`)
- `name`: Phenotype description
- `category`: `biolink:PhenotypicFeature`

**ID Pattern**: `HP:0000001` to `HP:9999999`

**Examples**:
```
HP:0001166 - "Arachnodactyly"
HP:0000789 - "Infertility"
HP:0001634 - "Mitral valve prolapse"
```

---

### Gene (9,326 entities)

**Label**: `Gene`  
**Category**: `biolink:Gene`  
**Primary Source**: NCBI Gene

**Properties**:
- `id`: NCBI Gene ID (e.g., `NCBIGene:2200`)
- `name`: Gene symbol or name
- `category`: `biolink:Gene`

**ID Pattern**: `NCBIGene:1` to `NCBIGene:999999999`

**Examples**:
```
NCBIGene:2200 - "FBN1" (Fibrillin-1)
NCBIGene:7040 - "TGFB1"
NCBIGene:7490 - "WT1"
```

---

### Drug (16,875 entities)

**Label**: `Drug`  
**Category**: `biolink:Drug`  
**Primary Sources**: DrugBank, ClinicalTrials.gov

**Properties**:
- `id`: DrugBank ID or custom ID (e.g., `DrugBank:DB00001`, `CTDRUG_<name>`)
- `name`: Drug name
- `category`: `biolink:Drug`

**ID Patterns**:
- DrugBank: `DrugBank:DB00001` to `DrugBank:DB99999`
- Clinical Trial Drugs: `CTDRUG_<drug_name>`

**Examples**:
```
DrugBank:DB00945 - "Aspirin"
DrugBank:DB01268 - "Sunitinib"
CTDRUG_losartan - "Losartan"
```

---

### Treatment (455 entities)

**Label**: `Treatment`  
**Category**: `biolink:Treatment`  
**Primary Source**: MAXO (Medical Action Ontology)

**Properties**:
- `id`: MAXO identifier (e.g., `MAXO:0000004`)
- `name`: Medical procedure/intervention name
- `category`: `biolink:Treatment`

**ID Pattern**: `MAXO:0000001` to `MAXO:9999999`

**Examples**:
```
MAXO:0000004 - "surgical procedure"
MAXO:0000011 - "physical therapy"
MAXO:0000014 - "radiation therapy"
MAXO:0000058 - "pharmacotherapy"
```

**Note**: `biolink:Treatment` (medical procedures) is distinct from `biolink:Drug` (pharmaceutical substances).

---

### Variant (7,367 entities)

**Label**: `Variant`  
**Category**: `biolink:SequenceVariant`  
**Primary Source**: ClinVar

**Properties**:
- `id`: ClinVar variation ID (e.g., `ClinVar:2`)
- `name`: Variant description
- `category`: `biolink:SequenceVariant`

**ID Pattern**: `ClinVar:1` to `ClinVar:999999999`

**Examples**:
```
ClinVar:2 - "NM_000352.3(ABCA4):c.5461-10T>C"
ClinVar:3 - "NM_014855.2(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA"
```

---

## 🔗 Relationship Types

### has_phenotype (328,753 relationships)

**Direction**: Disease → Phenotype  
**Biolink Predicate**: `biolink:has_phenotype`  
**Neo4j Type**: `HAS_PHENOTYPE`

**Description**: Associates a disease with its characteristic phenotypic features.

**Example**:
```cypher
(MONDO:0007947)-[:HAS_PHENOTYPE]->(HP:0001166)
// Marfan syndrome has phenotype Arachnodactyly
```

**SPARQL**:
```turtle
<MONDO:0007947> biolink:has_phenotype <HP:0001166> .
```

---

### treats (39,043 relationships)

**Direction**: Drug/Treatment → Disease  
**Biolink Predicate**: `biolink:treats`  
**Neo4j Type**: `TREATS`

**Variants**:
- **Drug → Disease** (38,588): Pharmaceutical treatments
- **Treatment → Disease** (455): Medical procedures (MAXO)

**Examples**:
```cypher
// Drug treatment
(DrugBank:DB00945)-[:TREATS]->(MONDO:0005812)
// Aspirin treats ischemic stroke

// Medical procedure
(MAXO:0000011)-[:TREATS]->(MONDO:0008315)
// Physical therapy treats muscular dystrophy
```

---

### related_to (225,579 relationships)

**Direction**: Disease → Disease, Gene → Disease, etc.  
**Biolink Predicate**: `biolink:related_to`  
**Neo4j Type**: `RELATED_TO`

**Description**: General association between entities when more specific predicates don't apply.

**Common Patterns**:
- Disease → Disease: Disease associations
- Gene → Disease: Gene-disease associations
- Disease → Gene: Disease-gene associations

**Example**:
```cypher
(NCBIGene:2200)-[:RELATED_TO]->(MONDO:0007947)
// FBN1 gene related to Marfan syndrome
```

---

### subclass_of (142,047 relationships)

**Direction**: Disease → Disease  
**Biolink Predicate**: `biolink:subclass_of`  
**Neo4j Type**: `SUBCLASS_OF`

**Description**: Hierarchical disease taxonomy (child → parent).

**Example**:
```cypher
(MONDO:0007947)-[:SUBCLASS_OF]->(MONDO:0018949)
// Marfan syndrome is a subclass of hereditary connective tissue disorder
```

---

### Other Relationships

| Relationship | Count | Direction | Description |
|--------------|-------|-----------|-------------|
| `gene_associated_with_condition` | ~45,000 | Gene → Disease | Gene causally linked to disease |
| `causes_condition` | ~12,000 | Variant → Disease | Pathogenic variant causes disease |
| `has_gene` | ~7,000 | Variant → Gene | Variant located in gene |
| `biomarker_for` | ~5,000 | Gene/Protein → Disease | Clinical biomarker |

---

## 📚 Ontologies

### Biolink Model

**Namespace**: `https://w3id.org/biolink/vocab/`  
**Purpose**: Standardized typing system for biomedical entities and relationships

**Entity Types Used**:
- `biolink:Disease`
- `biolink:PhenotypicFeature`
- `biolink:Gene`
- `biolink:SequenceVariant`
- `biolink:Drug`
- `biolink:Treatment`

**Relationship Types Used**:
- `biolink:has_phenotype`
- `biolink:treats`
- `biolink:related_to`
- `biolink:subclass_of`
- `biolink:gene_associated_with_condition`

---

### MONDO (Monarch Disease Ontology)

**Namespace**: `http://purl.obolibrary.org/obo/MONDO_`  
**Purpose**: Unified disease ontology integrating multiple sources

**Coverage**: 26,106 diseases  
**ID Format**: `MONDO:0000001` to `MONDO:9999999`

**Website**: http://obofoundry.org/ontology/mondo.html

---

### Orphanet

**Namespace**: `http://www.orpha.net/ORDO/Orphanet_`  
**Purpose**: Rare disease classifications and clinical information

**Coverage**: Subset of 26,106 diseases  
**ID Format**: `Orphanet:1` to `Orphanet:999999`

**Website**: https://www.orpha.net/

---

### HPO (Human Phenotype Ontology)

**Namespace**: `http://purl.obolibrary.org/obo/HP_`  
**Purpose**: Standardized phenotype descriptions

**Coverage**: 11,708 phenotypes  
**ID Format**: `HP:0000001` to `HP:9999999`

**Website**: https://hpo.jax.org/

---

### DrugBank

**Namespace**: `http://identifiers.org/drugbank/`  
**Purpose**: Comprehensive drug information

**Coverage**: 16,875 drugs  
**ID Format**: `DrugBank:DB00001` to `DrugBank:DB99999`

**Website**: https://go.drugbank.com/

---

### ClinVar

**Namespace**: `http://www.ncbi.nlm.nih.gov/clinvar/variation/`  
**Purpose**: Genetic variant clinical significance

**Coverage**: 7,367 variants  
**ID Format**: `ClinVar:1` to `ClinVar:999999999`

**Website**: https://www.ncbi.nlm.nih.gov/clinvar/

---

### MAXO (Medical Action Ontology)

**Namespace**: `http://purl.obolibrary.org/obo/MAXO_`  
**Purpose**: Medical procedures and interventions

**Coverage**: 455 treatments  
**ID Format**: `MAXO:0000001` to `MAXO:9999999`

**Website**: https://github.com/monarch-initiative/MAxO

---

## 🌐 Namespaces

### RDF/SPARQL Namespaces

```turtle
@prefix biolink: <https://w3id.org/biolink/vocab/> .
@prefix mondo: <http://purl.obolibrary.org/obo/MONDO_> .
@prefix ordo: <http://www.orpha.net/ORDO/Orphanet_> .
@prefix hp: <http://purl.obolibrary.org/obo/HP_> .
@prefix ncbigene: <http://identifiers.org/ncbigene/> .
@prefix drugbank: <http://identifiers.org/drugbank/> .
@prefix clinvar: <http://www.ncbi.nlm.nih.gov/clinvar/variation/> .
@prefix maxo: <http://purl.obolibrary.org/obo/MAXO_> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
```

---

## 🏗️ Data Model

### Property Graph (Neo4j)

```
Node Structure:
┌─────────────────────────────────┐
│ Disease                         │
├─────────────────────────────────┤
│ id: "MONDO:0007947"            │
│ name: "Marfan syndrome"         │
│ category: "biolink:Disease"     │
└─────────────────────────────────┘

Relationship Structure:
┌──────────────────────────────────────┐
│ [:HAS_PHENOTYPE]                     │
├──────────────────────────────────────┤
│ predicate: "biolink:has_phenotype"   │
│ subject_type: "biolink:Disease"      │
│ object_type: "biolink:PhenotypicFeature" │
└──────────────────────────────────────┘
```

### RDF Triple Model (SPARQL)

```turtle
# Entity Type
<http://purl.obolibrary.org/obo/MONDO_0007947>
    rdf:type biolink:Disease .

# Properties
<http://purl.obolibrary.org/obo/MONDO_0007947>
    biolink:id "MONDO:0007947" ;
    rdfs:label "Marfan syndrome" ;
    biolink:category biolink:Disease .

# Relationships
<http://purl.obolibrary.org/obo/MONDO_0007947>
    biolink:has_phenotype <http://purl.obolibrary.org/obo/HP_0001166> .
```

---

## ✅ Biolink Model Compliance

All entities and relationships in this knowledge graph follow [Biolink Model](https://biolink.github.io/biolink-model/) standards for maximum interoperability.

### Compliance Checklist

- ✅ All entities have `biolink:` prefixed categories
- ✅ All relationships use standard Biolink predicates
- ✅ Entity types map to Biolink classes
- ✅ Relationship directions follow Biolink specifications
- ✅ Properties use standard Biolink vocabulary

### Biolink Class Mappings

| Our Entity | Biolink Class | URI |
|-----------|---------------|-----|
| Disease | `biolink:Disease` | `https://w3id.org/biolink/vocab/Disease` |
| Phenotype | `biolink:PhenotypicFeature` | `https://w3id.org/biolink/vocab/PhenotypicFeature` |
| Gene | `biolink:Gene` | `https://w3id.org/biolink/vocab/Gene` |
| Drug | `biolink:Drug` | `https://w3id.org/biolink/vocab/Drug` |
| Treatment | `biolink:Treatment` | `https://w3id.org/biolink/vocab/Treatment` |
| Variant | `biolink:SequenceVariant` | `https://w3id.org/biolink/vocab/SequenceVariant` |

---

## 📊 Relationship Cardinality

### One-to-Many Relationships

- Disease → Phenotypes: 1 disease can have 0-825 phenotypes (avg: 12.6)
- Disease → Parent Diseases: 1 disease can have 0-10 parent classes (avg: 5.4)

### Many-to-Many Relationships

- Drugs ↔ Diseases: Many drugs can treat many diseases
- Genes ↔ Diseases: Many genes can be associated with many diseases
- Phenotypes ↔ Diseases: Many phenotypes can characterize many diseases

---

## 🔍 Query Patterns

### Pattern 1: Disease-Phenotype Association

**Cypher**:
```cypher
MATCH (d:Disease {id: 'MONDO:0007947'})-[:HAS_PHENOTYPE]->(p:Phenotype)
RETURN d.name, collect(p.name) as phenotypes
```

**SPARQL**:
```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
SELECT ?phenotype_name WHERE {
  <http://purl.obolibrary.org/obo/MONDO_0007947>
    biolink:has_phenotype ?phenotype .
  ?phenotype rdfs:label ?phenotype_name .
}
```

### Pattern 2: Disease Hierarchy Navigation

**Cypher**:
```cypher
MATCH path = (d:Disease {id: 'MONDO:0007947'})-[:SUBCLASS_OF*]->(parent:Disease)
RETURN path
```

**SPARQL**:
```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
SELECT ?ancestor WHERE {
  <http://purl.obolibrary.org/obo/MONDO_0007947>
    biolink:subclass_of+ ?ancestor .
}
```

---

**Last Updated**: April 2026  
**Schema Version**: 1.0.0
