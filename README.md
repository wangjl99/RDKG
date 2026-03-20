Rare Disease Knowledge Graph (RDKG)
📊 Overview**

The Rare Disease Knowledge Graph (RDKG) is a FAIR-compliant semantic resource that harmonizes data from multiple authoritative sources to support:

- recision diagnosis through phenotype-driven similarity search
- Drug repurposing via integrated chemical-disease relationships
- Clinical trial matching using structured eligibility criteria
- Gene prioritization for rare disease genomics

### **Quick Stats**

| Component | Count | Source |
|-----------|-------|--------|
| **Rare Disorders** | 20,074 | ORDO, Mondo, GARD, NORD, MAxO |
| **Genes** | 4,485 | HGNC |
| **Phenotypes** | 8,600 | HPO |
| **RDF Triples** | 220,000 | Blazegraph |
| **Relationships** | 1,757 | LLM-extracted + Curated |
| **Drugs** | 2,000+ | DrugBank, CTD, MeSH → PubChem |

---

## 🚀 **Quick Start**

### **Option 1: Docker (Recommended)**

```bash
# Pull and run the RDKG container
docker pull uthouston/rdkg:latest
docker run -d -p 9999:9999 --name rdkg uthouston/rdkg:latest

# Access SPARQL endpoint
open http://localhost:9999/blazegraph/
```

### **Option 2: Local Installation**

```bash
# Clone repository
git clone https://github.com/wangjl99/rdkg.git
cd rare-disease-kg

# Install dependencies
pip install -r requirements.txt

# Load RDF data
python scripts/load_blazegraph.py --rdf data/rdkg_complete.ttl
```

### **Option 3: Public SPARQL Endpoint**

Access our public endpoint (available after Month 12 submission):
```
https://rdkg.uth.tmc.edu/sparql
```

---

## 📁 **Repository Structure**

```
rare-disease-kg/
├── README.md                          # This file
├── LICENSE                            # CC BY 4.0 license
├── CITATION.cff                       # Citation metadata
├── docker/
│   ├── Dockerfile                     # Docker image definition
│   ├── docker-compose.yml             # Multi-container setup
│   └── blazegraph.properties          # Blazegraph configuration
├── data/
│   ├── rdkg_complete.ttl              # Full RDF graph (Turtle)
│   ├── rdkg_complete.nt               # N-Triples format
│   ├── rdkg_complete.rdf              # RDF/XML format
│   ├── rdkg_complete.jsonld           # JSON-LD format
│   └── metadata/
│       ├── void.ttl                   # VoID metadata
│       └── provenance.ttl             # Provenance information
├── ontologies/
│   ├── ordo.owl                       # Orphanet Rare Disease Ontology
│   ├── mondo.owl                      # Mondo Disease Ontology
│   ├── hp.owl                         # Human Phenotype Ontology
│   └── maxo.owl                       # Medical Action Ontology
├── scripts/
│   ├── extract_ontologies.py         # OWL to RDF extraction
│   ├── standardize_chemicals.py      # DrugBank→PubChem conversion
│   ├── load_blazegraph.py            # Load data to Blazegraph
│   ├── validate_rdf.py               # RDF validation
│   └── llm_extraction/
│       ├── extract_relationships.py  # LLM-based extraction
│       └── validate_annotations.py   # Expert validation
├── queries/
│   ├── diagnosis_support.rq          # Phenotype similarity queries
│   ├── drug_repurposing.rq           # Treatment discovery
│   ├── gene_prioritization.rq        # Gene-disease queries
│   └── README.md                      # Query documentation
├── docs/
│   ├── SCHEMA.md                      # Knowledge graph schema
│   ├── ONTOLOGIES.md                  # Ontology alignment
│   ├── API_GUIDE.md                   # SPARQL endpoint usage
│   └── TUTORIALS.md                   # Step-by-step examples
├── validation/
│   ├── quality_metrics.json          # Data quality report
│   ├── test_queries.rq               # Validation queries
│   └── benchmark_results.json        # Performance benchmarks
└── requirements.txt                   # Python dependencies
```

---

## 🏗️ **Knowledge Graph Schema**

### **Core Entity Types**

```turtle
@prefix rdkg: <http://rdaccelerate.org/ontology/> .
@prefix ordo: <http://www.orpha.net/ORDO/> .
@prefix mondo: <http://purl.obolibrary.org/obo/MONDO_> .
@prefix hp: <http://purl.obolibrary.org/obo/HP_> .
@prefix hgnc: <https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/> .
@prefix maxo: <http://purl.obolibrary.org/obo/MAXO_> .

# Disease
ordo:Orpha_521 a rdkg:RareDisease ;
    rdfs:label "Chronic Myeloid Leukemia" ;
    rdkg:has_mondo_id mondo:0011996 ;
    rdkg:has_phenotype hp:0001909 ;
    rdkg:has_gene hgnc:613 ;
    rdkg:has_treatment maxo:0000058 .

# Gene
hgnc:613 a rdkg:Gene ;
    rdfs:label "ABL1" ;
    rdkg:associated_with ordo:Orpha_521 .

# Phenotype
hp:0001909 a rdkg:Phenotype ;
    rdfs:label "Leukocytosis" ;
    rdkg:observed_in ordo:Orpha_521 .

# Treatment
maxo:0000058 a rdkg:Treatment ;
    rdfs:label "Pharmacotherapy" ;
    rdkg:treats ordo:Orpha_521 ;
    rdkg:has_drug drugbank:DB00619 .
```

### **Relationship Types**

| Relationship | Domain | Range | Example |
|-------------|---------|-------|---------|
| `rdkg:has_phenotype` | Disease | Phenotype | CML has_phenotype Leukocytosis |
| `rdkg:has_gene` | Disease | Gene | CML has_gene ABL1 |
| `rdkg:has_treatment` | Disease | Treatment | CML has_treatment Imatinib |
| `rdkg:treats` | Treatment | Disease | Imatinib treats CML |
| `rdkg:prevents` | Treatment | Disease | Aspirin prevents MI |
| `rdkg:contraindicated_for` | Treatment | Disease | Aspirin contraindicated_for Hemophilia |
| `rdkg:resistant_to` | Disease | Treatment | CML-T315I resistant_to Imatinib |

Full schema documentation: [docs/SCHEMA.md](docs/SCHEMA.md)

---

## 📖 **Data Sources & Provenance**

### **Ontologies Integrated**

| Ontology | Version | Release Date | Entities | Purpose |
|----------|---------|--------------|----------|---------|
| **ORDO** | v4.3 | 2024-10-15 | 11,074 diseases | Rare disease classification |
| **Mondo** | v2024-09-03 | 2024-09-03 | Harmonization | Disease ID mapping |
| **HPO** | v2024-10-02 | 2024-10-02 | 8,600 phenotypes | Clinical features |
| **HGNC** | 2024-10-01 | 2024-10-01 | 4,485 genes | Gene nomenclature |
| **MAxO** | v1.2.0 | 2024-08-15 | 1,902 actions | Medical treatments |
| **CHEBI** | v235 | 2024-09-01 | Chemical entities | Drug structure |

### **External Databases**

- **DrugBank** v5.1.10: Drug-disease relationships (2,070 drugs → PubChem CIDs)
- **CTD** v2024-08: Chemical-disease associations
- **MeSH** 2024: Biomedical indexing terms
- **ClinVar** 2024-09: Genetic variant annotations
- **PubChem**: Chemical entity identifiers (97% conversion success)

### **Extraction Methods**

1. **Ontology Parsing**: owlready2 (Python)
2. **LLM Extraction**: GPT-4 via OntoGPT/SPIRES (95.6% coverage, 706 case reports)
3. **Manual Curation**: Expert-validated (Monarch Initiative standards)
4. **Chemical Standardization**: UniChem bulk mapping + PubChem API

Full provenance: [data/metadata/provenance.ttl](data/metadata/provenance.ttl)

---

## 🔍 **Example SPARQL Queries**

### **Query 1: Find Treatments for Disease**

```sparql
PREFIX rdkg: <http://rdaccelerate.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?diseaseName ?treatmentName ?drugName
WHERE {
  ?disease rdfs:label "Chronic Myeloid Leukemia" ;
           rdkg:has_treatment ?treatment .
  ?treatment rdfs:label ?treatmentName ;
             rdkg:has_drug ?drug .
  ?drug rdfs:label ?drugName .
}
```

### **Query 2: Phenotype Similarity Search**

```sparql
PREFIX rdkg: <http://rdaccelerate.org/ontology/>
PREFIX hp: <http://purl.obolibrary.org/obo/HP_>

SELECT ?disease1 ?disease2 (COUNT(?phenotype) as ?similarity)
WHERE {
  ?disease1 rdkg:has_phenotype hp:0002094 .  # Progressive dyspnea
  ?disease1 rdkg:has_phenotype ?phenotype .
  ?disease2 rdkg:has_phenotype ?phenotype .
  FILTER (?disease1 != ?disease2)
}
GROUP BY ?disease1 ?disease2
HAVING (COUNT(?phenotype) >= 3)
ORDER BY DESC(?similarity)
```

More queries: [queries/README.md](queries/README.md)

---

## 🐳 **Docker Deployment**

### **Quick Start**

```bash
# Build image
docker build -t rdkg:latest docker/

# Run with docker-compose
docker-compose up -d

# Check status
docker ps

# View logs
docker logs rdkg-blazegraph
```

### **Configuration**

Edit `docker/blazegraph.properties`:
```properties
com.bigdata.journal.AbstractJournal.file=/var/lib/blazegraph/blazegraph.jnl
com.bigdata.journal.AbstractJournal.bufferMode=DiskRW
com.bigdata.namespace.kb.lex.com.bigdata.btree.BTree.branchingFactor=1024
```

Full Docker guide: [docs/DOCKER_GUIDE.md](docs/DOCKER_GUIDE.md)

---

## 📊 **Data Quality Metrics**

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **RDF Triple Validity** | 100% | 100% | ✅ |
| **Ontology Term Coverage** | 98.5% | >95% | ✅ |
| **Identifier Mapping** | 97% | >90% | ✅ |
| **Zero Orphaned Nodes** | 0 | 0 | ✅ |
| **FAIR Score** | 4.2/5 | >4.0 | ✅ |
| **Query Response Time** | <500ms | <1s | ✅ |

Detailed report: [validation/quality_metrics.json](validation/quality_metrics.json)

---

## 🤝 **Contributing**

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code style guidelines
- How to submit issues
- Pull request process
- Curation standards

### **Areas for Contribution**

- 🧬 Additional disease-gene associations
- 💊 New drug-disease relationships
- 🔬 Clinical trial mappings
- 📝 Documentation improvements
- 🐛 Bug reports and fixes

---

## 📄 **License**

This work is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

### **Citation**

```bibtex
@software{rdkg2025,
  title = {Rare Disease Knowledge Graph (RDKG)},
  author = {Liu, Hongfang and Wang, Jinlian and Li, Xin},
  year = {2025},
  institution = {UTHealth Houston, McWilliams School of Biomedical Informatics},
  doi = {10.5281/zenodo.XXXXXXX},
  url = {https://github.com/UTHealth-SBMI/rare-disease-kg}
}
```

---

## 👥 **Team**

**Principal Investigator:**
- Dr. Hongfang Liu, PhD, FACMI - Vice President of Learning Health System, UTHealth Houston

**Co-Investigator:**
- Dr. Jinlian Wang - Assistant Professor, McWilliams School of Biomedical Informatics

**Data Scientist:**
- Dr. Xin Li - LLM-based information extraction and semantic web technologies

---

## 🔗 **Links**

- **Documentation**: https://rdkg.uth.tmc.edu/docs
- **SPARQL Endpoint**: https://rdkg.uth.tmc.edu/sparql
- **Issue Tracker**: https://github.com/UTHealth-SBMI/rare-disease-kg/issues
- **Proto-OKN Registry**: https://protoOKN.net (after Month 12 submission)
- **Contact**: hongfang.liu@uth.tmc.edu, jinlian.wang@uth.tmc.edu

---

## 📊 **Funding**

This work is supported by:
- NIH Grant R01 HG012748: "Learning Precision Medicine for Rare Diseases Empowered by Knowledge-driven Data Mining"
- NSF Proto-OKN Integration Award

---

## 🎯 **Project Status**

- [x] **Months 1-2**: RDF Conversion & Ontology Alignment
- [x] **Months 3-4**: Query Infrastructure & Metadata
- [x] **Months 5-6**: Documentation & Code Release
- [x] **Months 7-10**: Community Testing (Current Phase)
- [ ] **Months 11-12**: Final Submission to Proto-OKN (Q1 2026)

Last Updated: December 2025
