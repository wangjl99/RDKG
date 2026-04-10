# File Manifest

Complete listing of all files created for the RDKG Rare Disease Knowledge Graph GitHub repository.

## 📁 Repository Structure

```
RDKG/
├── README.md                      # Main repository documentation
├── LICENSE                        # MIT License
├── CONTRIBUTING.md                # Contribution guidelines
├── .gitignore                     # Git ignore rules
├── docker-compose.yml             # Docker services configuration
│
├── docs/                          # Documentation directory
│   ├── SCHEMA.md                  # Knowledge graph schema
│   ├── SETUP.md                   # Installation guide
│   ├── CYPHER_QUERIES.md         # Neo4j query examples
│   ├── SPARQL_QUERIES.md         # SPARQL query examples
│   └── API_GUIDE.md              # API usage guide
│
├── scripts/                       # Import and utility scripts
│   ├── export_from_mysql.py      # Export data from MySQL
│   ├── import_to_neo4j.py        # Import to Neo4j
│   └── export_to_rdf.py          # Convert to RDF
│
├── data/                          # Data files (gitignored)
│   ├── nodes_no_trials.csv       # Node data (not in repo)
│   ├── edges_no_trials.csv       # Edge data (not in repo)
│   └── rdaccelerate_kg.ttl       # RDF data (not in repo)
│
├── neo4j_data/                    # Neo4j database files (gitignored)
├── neo4j_logs/                    # Neo4j logs (gitignored)
├── neo4j_export/                  # CSV import directory
├── fuseki_data/                   # Fuseki database files (gitignored)
└── rdf_data/                      # RDF staging directory
```

---

## 📄 Core Files

### README.md

**Purpose**: Main repository documentation  
**Contains**:
- Project overview and features
- Statistics (72,368 entities, 834,260 relationships)
- Quick start guide
- Architecture diagram
- Integration information
- Citation details

**Key Sections**:
- Overview & Features
- Statistics table
- Data sources
- Quick start (3 options)
- Documentation links
- Example queries (Cypher & SPARQL)
- Architecture diagram
- FRINK OKN integration
- API access examples
- License & contact

---

### LICENSE

**Purpose**: MIT License for the project  
**Contains**:
- Copyright notice (UTHealth Houston 2024)
- MIT License full text
- Permissions and limitations

---

### CONTRIBUTING.md

**Purpose**: Contributor guidelines  
**Contains**:
- Code of conduct
- How to contribute
- Development setup
- Code style guidelines
- PR process
- Testing requirements
- Issue templates

**Sections**:
- Code of conduct
- Contribution types
- Development setup
- Code style (Python, Cypher, SPARQL)
- Commit message format
- Pull request process
- Data contribution guidelines
- Bug reporting
- Testing instructions

---

### .gitignore

**Purpose**: Exclude files from version control  
**Ignores**:
- Data directories (neo4j_data/, fuseki_data/)
- Large data files (*.csv, *.ttl, *.nt)
- Python artifacts (__pycache__/, *.pyc)
- IDE files (.vscode/, .idea/)
- Environment files (.env)
- Logs (*.log)
- OS files (.DS_Store, Thumbs.db)

---

### docker-compose.yml

**Purpose**: Docker services configuration  
**Defines**:
- Neo4j service (port 7474, 7687)
- Fuseki service (port 3030)
- Volume mounts
- Environment variables
- Network configuration

**Services**:

**Neo4j**:
- Image: neo4j:5.15.0
- Ports: 7474 (HTTP), 7687 (Bolt)
- Memory: 2-4GB heap
- APOC plugin enabled
- Volumes: data, logs, import

**Fuseki**:
- Image: stain/jena-fuseki:latest
- Port: 3030
- Memory: 4GB heap
- Volumes: fuseki data, staging

---

## 📚 Documentation Files

### docs/SCHEMA.md

**Purpose**: Complete schema documentation  
**File Size**: ~12KB  
**Contains**:
- Entity type definitions (6 types)
- Relationship type definitions (10+ types)
- Ontology descriptions
- Biolink Model compliance
- Namespace definitions
- Data model diagrams
- Query patterns

**Key Sections**:
- Entity Types:
  - Disease (26,106)
  - Phenotype (11,708)
  - Gene (9,326)
  - Drug (16,875)
  - Treatment (455)
  - Variant (7,367)

- Relationship Types:
  - has_phenotype (328,753)
  - treats (39,043)
  - related_to (225,579)
  - subclass_of (142,047)

- Ontologies:
  - Biolink Model
  - MONDO
  - Orphanet
  - HPO
  - DrugBank
  - ClinVar
  - MAXO

---

### docs/SETUP.md

**Purpose**: Installation and configuration guide  
**File Size**: ~8KB  
**Contains**:
- Prerequisites
- Quick start (3 steps)
- Detailed setup instructions
- Data import procedures
- Configuration options
- Troubleshooting
- Production deployment

**Key Sections**:
- Prerequisites (system & software)
- Quick start (clone, start, access)
- Detailed setup (directory structure, docker-compose, verification)
- Data import (Neo4j & Fuseki)
- Configuration (memory, ports)
- Troubleshooting (common issues)
- Production (security, SSL, backups)

---

### docs/CYPHER_QUERIES.md

**Purpose**: Neo4j Cypher query examples  
**File Size**: ~15KB  
**Contains**: 50+ query examples

**Categories**:
- Basic Queries (counts, types)
- Disease Queries (search, hierarchy, phenotypes)
- Phenotype Queries (search, co-occurrence)
- Drug & Treatment Queries (treatments, repurposing)
- Gene & Variant Queries (associations, pathways)
- Path Queries (shortest path, complex paths)
- Aggregation Queries (statistics, averages)
- Advanced Analytics (similarity, clustering)

**Example Queries**:
- Find diseases by name
- Diseases with most phenotypes
- Disease hierarchy navigation
- Phenotype co-occurrence
- Drug treatments
- Gene-disease associations
- Similar diseases (Jaccard similarity)
- Drug repurposing candidates

---

### docs/SPARQL_QUERIES.md

**Purpose**: SPARQL query examples for Fuseki  
**File Size**: ~12KB  
**Contains**: 40+ query examples

**Categories**:
- Basic Queries (count, list entities)
- Disease Queries (search, hierarchy)
- Phenotype Queries (associations, co-occurrence)
- Drug & Treatment Queries (treatments)
- Gene & Variant Queries (associations)
- Federated Queries (external endpoints)
- Aggregation & Analytics (statistics)

**Special Features**:
- Standard namespace prefixes
- Response format examples
- Query optimization tips
- CONSTRUCT, ASK, DESCRIBE examples

---

### docs/API_GUIDE.md

**Purpose**: Programmatic access guide  
**File Size**: ~10KB  
**Contains**:
- Neo4j Bolt API examples
- Neo4j HTTP API examples
- SPARQL HTTP API examples
- Multiple language examples (Python, JavaScript, R)
- Authentication methods
- Error handling
- Rate limiting

**Languages Covered**:
- Python (neo4j-driver, py2neo, requests, SPARQLWrapper)
- JavaScript (neo4j-driver, fetch)
- R (neo4r, SPARQL)
- cURL (command line)

**Complete Examples**:
- Disease Phenotype Analyzer (Python class)
- Drug Repurposing Finder (Python class)
- Connection pooling
- Error handling
- Response parsing

---

## 🔧 Scripts Directory

### scripts/export_from_mysql.py

**Purpose**: Export clean data from MySQL source database  
**What it does**:
- Connects to MySQL rare_disease database
- Exports nodes (excluding clinical trials)
- Exports edges (clean, no duplicates)
- Creates CSV files for Neo4j import

**Output Files**:
- `nodes_no_trials.csv` (72,369 lines)
- `edges_no_trials.csv` (834,261 lines)

**Usage**:
```bash
python3 export_from_mysql.py
# Prompts for MySQL password
```

---

### scripts/import_to_neo4j.py

**Purpose**: Import edges to Neo4j in batches  
**What it does**:
- Reads edges_no_trials.csv
- Batch imports (1,000 edges per batch)
- Uses APOC for dynamic relationship creation
- Shows progress

**Usage**:
```bash
# After importing nodes via Neo4j Browser
python3 import_to_neo4j.py
```

---

### scripts/export_to_rdf.py

**Purpose**: Convert Neo4j graph to RDF  
**What it does**:
- Connects to Neo4j
- Exports all nodes as RDF triples
- Exports all relationships as RDF triples
- Adds ontology metadata
- Serializes to Turtle and N-Triples

**Output Files**:
- `rdaccelerate_kg.ttl` (Turtle format, human-readable)
- `rdaccelerate_kg.nt` (N-Triples format)

**Statistics**:
- Input: 72,368 nodes, 834,260 edges
- Output: 1,181,391 triples

**Usage**:
```bash
python3 export_to_rdf.py
```

---

## 📊 Data Files (Not in Repository)

### nodes_no_trials.csv

**Size**: 4.7 MB  
**Format**: CSV with headers  
**Columns**:
- `id:ID` - Unique identifier
- `name` - Entity name
- `:LABEL` - Node label (Disease, Gene, etc.)
- `category` - Biolink category

**Rows**: 72,369 (72,368 + header)

---

### edges_no_trials.csv

**Size**: 84 MB  
**Format**: CSV with headers  
**Columns**:
- `:START_ID` - Source entity ID
- `:END_ID` - Target entity ID
- `:TYPE` - Relationship type
- `predicate` - Biolink predicate
- `subject_type` - Source entity category
- `object_type` - Target entity category

**Rows**: 834,261 (834,260 + header)

---

### rdaccelerate_kg.ttl

**Size**: ~180 MB  
**Format**: RDF Turtle  
**Triples**: 1,181,391  
**Content**:
- Entity type declarations
- Entity properties (id, name, category)
- Relationships with predicates
- Ontology metadata

---

## 🚀 Getting Started

### 1. Copy Files to Your Repository

```bash
# Copy all files from github-repo/ to your local repository
cd ~/your-repository
cp -r ~/Downloads/neo4j_export/github-repo/* .
```

### 2. Add Data Files

```bash
# Copy clean CSV and RDF files
mkdir -p data
cp ~/Downloads/neo4j_export/nodes_no_trials.csv data/
cp ~/Downloads/neo4j_export/edges_no_trials.csv data/
cp ~/Downloads/neo4j_export/rdaccelerate_kg.ttl data/
```

### 3. Update Placeholders

Edit these files to replace placeholders:

**README.md**:
- Replace `wangjl99` with your GitHub username
- Replace `[your-email@uth.tmc.edu]` with your email

**CONTRIBUTING.md**:
- Replace `wangjl99` with your GitHub username
- Add Discord/Slack links if applicable

### 4. Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit: RDKG Knowledge Graph"
git branch -M main
git remote add origin https://github.com/wangjl99/RDKG.git
git push -u origin main
```

---

## 📋 Checklist Before Publishing

- [ ] Review all documentation for accuracy
- [ ] Update email addresses
- [ ] Replace placeholder URLs
- [ ] Test Docker Compose setup
- [ ] Verify all query examples work
- [ ] Add sample data (if providing)
- [ ] Create GitHub repository
- [ ] Add repository description
- [ ] Add topics/tags
- [ ] Enable GitHub Discussions (optional)
- [ ] Set up GitHub Actions (optional)

---

## 📈 Statistics Summary

**Files Created**: 11 core files + 3 scripts = 14 total  
**Documentation**: ~60 KB  
**Query Examples**: 90+ examples  
**Code Examples**: 20+ complete examples  
**Languages Covered**: Python, JavaScript, R, bash

**Knowledge Graph**:
- Entities: 72,368
- Relationships: 834,260
- RDF Triples: 1,181,391
- Ontologies: 7 (Biolink, MONDO, Orphanet, HPO, DrugBank, ClinVar, MAXO)

---

## 🎯 Next Steps

1. **Review all files** in the `github-repo/` directory
2. **Update placeholders** with your information
3. **Test the setup** locally with Docker
4. **Create GitHub repository**
5. **Push to GitHub**
6. **Add data files** (or instructions to obtain them)
7. **Announce** to FRINK OKN community

---

**Repository Ready**: ✅  
**Last Updated**: April 2026
