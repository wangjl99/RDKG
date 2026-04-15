# Data Files

The RDKG contains  Nodes: 72,368 (Disease: 26,106 | Phenotype: 11,709 | Gene: 9,326 | Drug: 16,875 | Variant: 7,367)
Edges: 834,260 (HAS_PHENOTYPE: 328,753 | TREATS: 39,043 | CONTRAINDICATED_FOR: 61,351 | SUBCLASS_OF: 142,047 | ...) Due to file size, data files are not included in this repository.

## 📊 Statistics

| File | Size | Records | Description |
|------|------|---------|-------------|
| `nodes_no_trials.csv` | 4.7 MB | 72,368 | All entities (diseases, genes, drugs, phenotypes, variants) |
| `edges_no_trials.csv` | 84 MB | 834,260 | All relationships (clean, no duplicates) |
| `rdaccelerate_kg.ttl` | ~180 MB | 1,181,391 triples | RDF/Turtle format for SPARQL |

---

## 📥 Download Options

### Option 1: Direct Download (Recommended)

**Coming Soon**: Data files will be available via:
- [ ] Zenodo (with DOI for citations)
- [ ] Figshare
- [ ] Google Drive

### Option 2: Generate from Source

If you have access to the source MySQL database:

```bash
# 1. Export from MySQL
cd scripts
python3 export_from_mysql.py

# 2. Files created in current directory
ls -lh *.csv *.ttl
```

See [docs/SETUP.md](docs/SETUP.md) for complete instructions.

---

## 🔄 Import Instructions

### Neo4j Import

1. **Copy CSV files**:
```bash
cp nodes_no_trials.csv neo4j_export/
cp edges_no_trials.csv neo4j_export/
```

2. **Import** (see [docs/SETUP.md](docs/SETUP.md)):
   - Create constraints (Neo4j Browser)
   - Import nodes (Neo4j Browser)
   - Import edges (Python script)

### Fuseki Import

1. **Copy RDF file**:
```bash
cp rdaccelerate_kg.ttl rdf_data/
```

2. **Import** (see [docs/SETUP.md](docs/SETUP.md)):
   - Create dataset
   - Upload TTL file
   - Verify with SPARQL query

---

## ✅ Data Quality

All data files have been:
- ✓ Cleaned (no duplicates)
- ✓ Validated (correct relationship directions)
- ✓ Standardized (Biolink Model format)
- ✓ Tested (all queries work)

**Quality Metrics**:
- **Duplicates removed**: 151,304
- **Backwards edges fixed**: 151,304
- **Biolink compliance**: 100%

---

## 📚 Data Sources

Data integrated from:
- **[Orphanet](https://www.orpha.net/)** - Rare disease classifications
- **[MONDO](http://obofoundry.org/ontology/mondo.html)** - Disease ontology
- **[HPO](https://hpo.jax.org/)** - Human Phenotype Ontology
- **[DrugBank](https://go.drugbank.com/)** - Drug information
- **[ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/)** - Genetic variants
- **[MAXO](https://github.com/monarch-initiative/MAxO)** - Medical procedures

---

## 📝 File Formats

### CSV Files (Neo4j)

**nodes_no_trials.csv**:
```csv
id:ID,name,:LABEL,category
MONDO:0007947,Marfan syndrome,Disease,biolink:Disease
HP:0001166,Arachnodactyly,Phenotype,biolink:PhenotypicFeature
```

**edges_no_trials.csv**:
```csv
:START_ID,:END_ID,:TYPE,predicate,subject_type,object_type
MONDO:0007947,HP:0001166,HAS_PHENOTYPE,biolink:has_phenotype,biolink:Disease,biolink:PhenotypicFeature
```

### RDF File (Fuseki)

**rdaccelerate_kg.ttl** (Turtle format):
```turtle
@prefix biolink: <https://w3id.org/biolink/vocab/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://purl.obolibrary.org/obo/MONDO_0007947>
    rdf:type biolink:Disease ;
    rdfs:label "Marfan syndrome" ;
    biolink:has_phenotype <http://purl.obolibrary.org/obo/HP_0001166> .
```

---

## 🔐 License

Data is aggregated from multiple public sources, each with their own licenses:
- Orphanet: CC BY 4.0
- MONDO: CC BY 4.0
- HPO: Custom (see HPO website)
- DrugBank: Multiple licenses (see DrugBank website)
- ClinVar: Public domain

Please cite all original sources when using this data.

---

## 📞 Questions?

- **Missing data?** Open an [issue](https://github.com/wangjl99/RDKG/issues)
- **Data quality concerns?** See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Custom export needed?** Contact maintainers

---

**Last Updated**: April 2026
