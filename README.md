# RDKG Rare Disease Knowledge Graph

A comprehensive, semantically integrated knowledge graph for rare disease research, combining data from Orphanet, MONDO, HPO, DrugBank, ClinVar, and MAXO ontologies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.15.0-blue.svg)](https://neo4j.com/)
[![Biolink](https://img.shields.io/badge/Biolink-Model-green.svg)](https://biolink.github.io/biolink-model/)

## 🎯 Overview

This knowledge graph integrates multiple rare disease data sources into a unified, queryable resource supporting both graph database (Neo4j/Cypher) and semantic web (RDF/SPARQL) access patterns.

### Key Features

- **Comprehensive Coverage**: 72,368 biomedical entities across 6 entity types
- **Rich Relationships**: 834,260 semantically typed relationships
- **Multi-Access**: Both Neo4j (Cypher) and Apache Jena Fuseki (SPARQL) endpoints
- **Biolink Compliant**: Follows Biolink Model standards for interoperability
- **Quality Assured**: No duplicates, verified relationship directions, standardized types

## 📊 Statistics

| Category | Count |
|----------|-------|
| **Total Entities** | 72,368 |
| **Diseases** | 26,106 |
| **Drugs** | 16,875 |
| **Phenotypes** | 11,708 |
| **Genes** | 9,326 |
| **Variants** | 7,367 |
| **Treatments** | 455 |
| **Total Relationships** | 834,260 |
| **RDF Triples** | 1,181,391 |

### Relationship Types

| Relationship | Count | Description |
|-------------|--------|-------------|
| `has_phenotype` | 328,753 | Disease → Phenotype associations |
| `related_to` | 225,579 | General disease relationships |
| `subclass_of` | 142,047 | Disease hierarchy |
| `treats` (Drug) | 38,588 | Drug treatments |
| `treats` (Procedure) | 455 | Medical procedures (MAXO) |
| Others | 98,838 | Gene associations, variants, etc. |

## 🗄️ Data Sources

- **[Orphanet](https://www.orpha.net/)**: Rare disease classifications and phenotypes
- **[MONDO](http://obofoundry.org/ontology/mondo.html)**: Disease ontology integration
- **[HPO](https://hpo.jax.org/)**: Human Phenotype Ontology
- **[DrugBank](https://go.drugbank.com/)**: Drug information and treatments
- **[ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/)**: Genetic variant data
- **[MAXO](https://github.com/monarch-initiative/MAxO)**: Medical Action Ontology

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- 8GB RAM minimum (16GB recommended)
- 10GB disk space

### Option 1: Neo4j Graph Database

```bash
# Start Neo4j
docker-compose up -d neo4j

# Access Neo4j Browser
open http://localhost:7474

# Login: neo4j / rdaccelerate2024
```

### Option 2: SPARQL Endpoint

```bash
# Start Fuseki
docker-compose up -d fuseki

# Access Fuseki UI
open http://localhost:3030

# Login: admin / rdaccelerate2024
```

### Option 3: Both Services

```bash
# Start everything
docker-compose up -d

# Neo4j: http://localhost:7474
# Fuseki: http://localhost:3030
```

## 📖 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed installation and configuration
- **[Schema Documentation](docs/SCHEMA.md)** - Knowledge graph structure and ontologies
- **[Cypher Queries](docs/CYPHER_QUERIES.md)** - Neo4j query examples
- **[SPARQL Queries](docs/SPARQL_QUERIES.md)** - RDF query examples
- **[API Guide](docs/API_GUIDE.md)** - Programmatic access patterns
- **[Data Statistics](docs/DATA_STATISTICS.md)** - Detailed entity and relationship counts

## 🔍 Example Queries

### Neo4j Cypher

```cypher
// Find diseases with most phenotypes
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
RETURN d.name, count(p) as phenotype_count
ORDER BY phenotype_count DESC
LIMIT 10;
```

### SPARQL

```sparql
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?disease_name (COUNT(?phenotype) AS ?count)
WHERE {
  ?disease a biolink:Disease ;
           rdfs:label ?disease_name ;
           biolink:has_phenotype ?phenotype .
}
GROUP BY ?disease_name
ORDER BY DESC(?count)
LIMIT 10
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                              │
│  Orphanet │ MONDO │ HPO │ DrugBank │ ClinVar │ MAXO        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  MySQL Database                              │
│              (Source data integration)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│   Neo4j Graph    │      │   RDF Triples    │
│   (Cypher)       │      │   (Turtle/NT)    │
└────────┬─────────┘      └────────┬─────────┘
         │                         │
         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│  Neo4j Browser   │      │ Apache Fuseki    │
│  localhost:7474  │      │  localhost:3030  │
└──────────────────┘      └──────────────────┘
```

## 🔗 Integration

### FRINK Open Knowledge Network

This knowledge graph is designed for integration with the [FRINK Open Knowledge Network](https://github.com/frink-okn).

**SPARQL Endpoint**: `http://your-server:3030/rdaccelerate/sparql`

### API Access

**Neo4j Bolt Protocol**:
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "rdaccelerate2024")
)
```

**SPARQL HTTP API**:
```python
import requests

query = """
PREFIX biolink: <https://w3id.org/biolink/vocab/>
SELECT * WHERE { ?s a biolink:Disease } LIMIT 10
"""

response = requests.post(
    "http://localhost:3030/rdaccelerate/sparql",
    data={"query": query},
    headers={"Accept": "application/json"},
    auth=("admin", "rdaccelerate2024")
)
```

## 📦 Docker Images

- **Neo4j**: `neo4j:5.15.0` with APOC plugin
- **Fuseki**: `stain/jena-fuseki:latest`

## 🛠️ Data Import Scripts

Import scripts are provided for:
- CSV export from MySQL
- Neo4j bulk import
- RDF conversion and export
- Fuseki dataset creation

See `scripts/` directory for details.

## 📊 Data Quality

**Quality Assurance Measures**:
- ✅ No duplicate relationships (deduplicated 151,304 duplicates)
- ✅ All relationship directions verified (fixed 151,304 backwards edges)
- ✅ Biolink Model compliance (all types standardized)
- ✅ Entity type consistency (Drug vs Treatment properly distinguished)
- ✅ Referential integrity (all edges reference valid nodes)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 Citation

If you use this knowledge graph in your research, please cite:

```bibtex
@misc{rdaccelerate2024,
  title={RDKG Rare Disease Knowledge Graph},
  author={UTHealth Houston},
  year={2024},
  publisher={GitHub},
  url={https://github.com/wangjl99/RDKG}
}
```

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🏥 Institutional Affiliation

**UTHealth Houston**  
School of Biomedical Informatics

## 📧 Contact

For questions or collaborations:
- Open an issue on GitHub
- Email: [dada.bio2014@gmail.com]

## 🙏 Acknowledgments

- Orphanet for rare disease data
- Monarch Initiative for ontology development
- Biolink Model community for standardization
- Neo4j and Apache Jena teams for database technologies

---

**Last Updated**: April 2026  
**Version**: 1.0.0
