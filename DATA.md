# Data Files

The RDKG contains **72,368 entities** and **834,260 relationships**. 

## Download

Data files are available in the GitHub Release:
https://github.com/wangjl99/RDKG/releases/tag/v1.0.0

| File | Size | Records | Description |
|------|------|---------|-------------|
| `nodes_no_trials.csv` | 4.7 MB | 72,368 | All entities (Disease, Phenotype, Gene, Drug, Variant) |
| `edges_no_trials.csv` | 84 MB | 834,260 | All relationships (15 types) |

## Source Database Versions

| Database | Version / Date | License | URL |
|---|---|---|---|
| MONDO | mondo-rare.owl, Sep 24 2025 | CC BY 4.0 | https://mondo.monarchinitiative.org |
| Orphanet (ORDO) | Aug 25 2025 | CC BY 4.0 | https://www.orphadata.com |
| HPO / HPOA | phenotype.hpoa, Jul 22 2025 | Custom | https://hpo.jax.org |
| ClinVar | Jan 10 2025 | Public domain | https://www.ncbi.nlm.nih.gov/clinvar |
| MAxO | Jul 22 2025 | CC BY 4.0 | https://github.com/monarch-initiative/MAxO |
| DrugBank | Aug 25 2025 | CC BY-NC 4.0 | https://go.drugbank.com |

## Graph Statistics

| Node type | Count |
|---|---|
| Disease | 26,106 |
| Phenotype | 11,709 |
| Drug | 16,875 |
| Gene | 9,326 |
| Variant | 7,367 |
| **Total** | **72,368** |

| Relationship type | Count |
|---|---|
| HAS_PHENOTYPE | 328,753 |
| SUBCLASS_OF | 142,047 |
| CONTRAINDICATED_FOR | 61,351 |
| TREATS | 39,043 |
| RELATED_TO | 225,579 |
| HAS_ONSET | 11,548 |
| HAS_MODE_OF_INHERITANCE | 5,216 |
| CAUSES_CONDITION | 7,971 |
| HAS_GENE | 7,397 |
| GENETIC_ASSOCIATION | 546 |
| Others | 4,809 |
| **Total** | **834,260** |

## Import Instructions

### Neo4j Import

```bash
# Copy CSV files to the data/ folder
cp nodes_no_trials.csv data/
cp edges_no_trials.csv data/

# Start Docker stack
docker compose up -d neo4j
sleep 30

# Load data
python scripts/rdkg_load_csv.py
```

### Verify

```bash
curl http://localhost:8000/health
curl http://localhost:8000/stats
```

## Data Quality

- Duplicates removed: 151,304
- Biolink Model format compliance: 100%
- Cross-database ID harmonization via MONDO

## License

Code: MIT License  
Data: subject to source database licenses listed above.  
Please cite all original sources when using this data.
