# API Guide

Programmatic access patterns for the RDAccelerate Rare Disease Knowledge Graph.

## 📋 Table of Contents

- [Neo4j Bolt API](#neo4j-bolt-api)
- [Neo4j HTTP API](#neo4j-http-api)
- [SPARQL HTTP API](#sparql-http-api)
- [Python Examples](#python-examples)
- [JavaScript Examples](#javascript-examples)
- [R Examples](#r-examples)
- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)

---

## 🔌 Neo4j Bolt API

### Connection Details

- **Protocol**: Bolt
- **Host**: `localhost` (or your server)
- **Port**: `7687`
- **Username**: `neo4j`
- **Password**: `rdaccelerate2024`

### Python (neo4j-driver)

```python
from neo4j import GraphDatabase

# Connect
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "rdaccelerate2024")
)

# Query
def find_disease_phenotypes(disease_id):
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Disease {id: $disease_id})-[:HAS_PHENOTYPE]->(p:Phenotype)
            RETURN d.name AS disease, collect(p.name) AS phenotypes
        """, disease_id=disease_id)
        return result.single()

# Execute
data = find_disease_phenotypes("MONDO:0007947")
print(f"Disease: {data['disease']}")
print(f"Phenotypes: {data['phenotypes']}")

# Close
driver.close()
```

### Python (py2neo)

```python
from py2neo import Graph

# Connect
graph = Graph("bolt://localhost:7687", auth=("neo4j", "rdaccelerate2024"))

# Query
query = """
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
RETURN d.name, count(p) as phenotype_count
ORDER BY phenotype_count DESC
LIMIT 10
"""

results = graph.run(query).data()
for row in results:
    print(f"{row['d.name']}: {row['phenotype_count']} phenotypes")
```

### JavaScript (neo4j-driver)

```javascript
const neo4j = require('neo4j-driver');

// Connect
const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'rdaccelerate2024')
);

// Query
async function findDiseasePhenotypes(diseaseId) {
  const session = driver.session();
  try {
    const result = await session.run(
      'MATCH (d:Disease {id: $diseaseId})-[:HAS_PHENOTYPE]->(p:Phenotype) ' +
      'RETURN d.name AS disease, collect(p.name) AS phenotypes',
      { diseaseId }
    );
    
    const record = result.records[0];
    return {
      disease: record.get('disease'),
      phenotypes: record.get('phenotypes')
    };
  } finally {
    await session.close();
  }
}

// Execute
findDiseasePhenotypes('MONDO:0007947')
  .then(data => console.log(data))
  .finally(() => driver.close());
```

---

## 🌐 Neo4j HTTP API

### Connection Details

- **Endpoint**: `http://localhost:7474/db/neo4j/tx/commit`
- **Method**: POST
- **Authentication**: Basic Auth

### Python (requests)

```python
import requests
from requests.auth import HTTPBasicAuth

url = "http://localhost:7474/db/neo4j/tx/commit"
auth = HTTPBasicAuth("neo4j", "rdaccelerate2024")

payload = {
    "statements": [{
        "statement": """
            MATCH (d:Disease {id: $disease_id})-[:HAS_PHENOTYPE]->(p:Phenotype)
            RETURN d.name AS disease, collect(p.name) AS phenotypes
        """,
        "parameters": {
            "disease_id": "MONDO:0007947"
        }
    }]
}

response = requests.post(url, json=payload, auth=auth)
data = response.json()

# Extract results
results = data['results'][0]['data'][0]['row']
print(f"Disease: {results[0]}")
print(f"Phenotypes: {results[1]}")
```

### cURL

```bash
curl -X POST http://localhost:7474/db/neo4j/tx/commit \
  -u neo4j:rdaccelerate2024 \
  -H "Content-Type: application/json" \
  -d '{
    "statements": [{
      "statement": "MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype) RETURN d.name, count(p) LIMIT 10"
    }]
  }'
```

---

## 📡 SPARQL HTTP API

### Connection Details

- **Endpoint**: `http://localhost:3030/rdaccelerate/sparql`
- **Method**: POST (preferred) or GET
- **Authentication**: Basic Auth
- **Accept Headers**: 
  - `application/sparql-results+json` (JSON)
  - `text/csv` (CSV)
  - `application/sparql-results+xml` (XML)

### Python (requests)

```python
import requests
from requests.auth import HTTPBasicAuth

url = "http://localhost:3030/rdaccelerate/sparql"
auth = HTTPBasicAuth("admin", "rdaccelerate2024")

query = """
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
"""

response = requests.post(
    url,
    data={"query": query},
    headers={"Accept": "application/sparql-results+json"},
    auth=auth
)

results = response.json()
for binding in results['results']['bindings']:
    disease = binding['disease_name']['value']
    count = binding['count']['value']
    print(f"{disease}: {count} phenotypes")
```

### Python (SPARQLWrapper)

```python
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:3030/rdaccelerate/sparql")
sparql.setHTTPAuth("BASIC")
sparql.setCredentials("admin", "rdaccelerate2024")

sparql.setQuery("""
    PREFIX biolink: <https://w3id.org/biolink/vocab/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?disease_name ?phenotype_name
    WHERE {
      ?disease biolink:id "MONDO:0007947" ;
               rdfs:label ?disease_name ;
               biolink:has_phenotype ?phenotype .
      ?phenotype rdfs:label ?phenotype_name .
    }
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(f"{result['disease_name']['value']}: {result['phenotype_name']['value']}")
```

### JavaScript (fetch)

```javascript
const url = 'http://localhost:3030/rdaccelerate/sparql';
const auth = 'Basic ' + btoa('admin:rdaccelerate2024');

const query = `
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
`;

fetch(url, {
  method: 'POST',
  headers: {
    'Authorization': auth,
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/sparql-results+json'
  },
  body: `query=${encodeURIComponent(query)}`
})
  .then(response => response.json())
  .then(data => {
    data.results.bindings.forEach(row => {
      console.log(`${row.disease_name.value}: ${row.count.value}`);
    });
  });
```

### cURL

```bash
curl -X POST http://localhost:3030/rdaccelerate/sparql \
  -u admin:rdaccelerate2024 \
  -H "Accept: text/csv" \
  --data-urlencode "query=PREFIX biolink: <https://w3id.org/biolink/vocab/>
SELECT ?disease ?phenotype WHERE {
  ?disease a biolink:Disease ;
           biolink:has_phenotype ?phenotype .
} LIMIT 10"
```

---

## 🐍 Python Examples

### Complete Example: Disease Phenotype Analyzer

```python
from neo4j import GraphDatabase
import pandas as pd

class DiseaseAnalyzer:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def get_disease_phenotypes(self, disease_id):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Disease {id: $disease_id})-[:HAS_PHENOTYPE]->(p:Phenotype)
                RETURN d.id AS disease_id,
                       d.name AS disease_name,
                       p.id AS phenotype_id,
                       p.name AS phenotype_name
            """, disease_id=disease_id)
            
            return pd.DataFrame([dict(record) for record in result])
    
    def find_similar_diseases(self, disease_id, min_shared=5):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d1:Disease {id: $disease_id})-[:HAS_PHENOTYPE]->(p:Phenotype)
                      <-[:HAS_PHENOTYPE]-(d2:Disease)
                WHERE d1 <> d2
                WITH d2, count(p) AS shared_phenotypes
                WHERE shared_phenotypes >= $min_shared
                RETURN d2.id AS disease_id,
                       d2.name AS disease_name,
                       shared_phenotypes
                ORDER BY shared_phenotypes DESC
            """, disease_id=disease_id, min_shared=min_shared)
            
            return pd.DataFrame([dict(record) for record in result])

# Usage
analyzer = DiseaseAnalyzer("bolt://localhost:7687", "neo4j", "rdaccelerate2024")

# Get phenotypes
phenotypes = analyzer.get_disease_phenotypes("MONDO:0007947")
print(phenotypes)

# Find similar diseases
similar = analyzer.find_similar_diseases("MONDO:0007947")
print(similar)

analyzer.close()
```

### Complete Example: Drug Repurposing Finder

```python
import requests
from requests.auth import HTTPBasicAuth

class DrugRepurposingFinder:
    def __init__(self, sparql_endpoint, username, password):
        self.endpoint = sparql_endpoint
        self.auth = HTTPBasicAuth(username, password)
    
    def find_candidates(self, target_disease_id, min_shared_phenotypes=5):
        query = f"""
        PREFIX biolink: <https://w3id.org/biolink/vocab/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?drug_name (COUNT(DISTINCT ?shared_phenotype) AS ?shared_count)
        WHERE {{
          ?target_disease biolink:id "{target_disease_id}" ;
                          biolink:has_phenotype ?shared_phenotype .
          
          ?similar_disease biolink:has_phenotype ?shared_phenotype .
          FILTER(?target_disease != ?similar_disease)
          
          ?drug a biolink:Drug ;
                rdfs:label ?drug_name ;
                biolink:treats ?similar_disease .
          
          FILTER NOT EXISTS {{
            ?drug biolink:treats ?target_disease .
          }}
        }}
        GROUP BY ?drug_name
        HAVING (COUNT(DISTINCT ?shared_phenotype) >= {min_shared_phenotypes})
        ORDER BY DESC(?shared_count)
        LIMIT 20
        """
        
        response = requests.post(
            self.endpoint,
            data={"query": query},
            headers={"Accept": "application/sparql-results+json"},
            auth=self.auth
        )
        
        results = response.json()
        candidates = []
        for binding in results['results']['bindings']:
            candidates.append({
                'drug': binding['drug_name']['value'],
                'shared_phenotypes': int(binding['shared_count']['value'])
            })
        
        return pd.DataFrame(candidates)

# Usage
finder = DrugRepurposingFinder(
    "http://localhost:3030/rdaccelerate/sparql",
    "admin",
    "rdaccelerate2024"
)

candidates = finder.find_candidates("MONDO:0007947")
print(candidates)
```

---

## 🔐 Authentication

### Neo4j Authentication

```python
# Token-based (if configured)
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=neo4j.auth.bearer_token("YOUR_TOKEN")
)

# Custom auth
from neo4j import GraphDatabase, Auth

custom_auth = Auth("custom", principal="user", credentials="pass")
driver = GraphDatabase.driver("bolt://localhost:7687", auth=custom_auth)
```

### Fuseki Authentication

```python
# Basic Auth
auth = HTTPBasicAuth("admin", "rdaccelerate2024")

# Token-based (if configured)
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Accept": "application/sparql-results+json"
}
```

---

## ⏱️ Rate Limiting

### Best Practices

1. **Batch Queries**: Combine multiple operations
```python
# Good - single query
MATCH (d:Disease)-[:HAS_PHENOTYPE]->(p:Phenotype)
WHERE d.id IN ['MONDO:0007947', 'MONDO:0005089', 'MONDO:0001072']
RETURN d.name, collect(p.name)

# Bad - multiple queries
for disease_id in disease_ids:
    MATCH (d:Disease {id: $id})-[:HAS_PHENOTYPE]->(p:Phenotype)
    RETURN d.name, collect(p.name)
```

2. **Use LIMIT**: Always limit results during development
```python
MATCH (d:Disease)
RETURN d
LIMIT 100  # Always include
```

3. **Connection Pooling**: Reuse connections
```python
# Good
driver = GraphDatabase.driver(...)  # Once
with driver.session() as session:  # Reuse
    session.run(query1)
    session.run(query2)

# Bad
for query in queries:
    driver = GraphDatabase.driver(...)  # Multiple times
    driver.session().run(query)
```

---

## 📊 Response Formats

### Neo4j Response (JSON)

```json
{
  "results": [{
    "columns": ["disease_name", "phenotype_count"],
    "data": [{
      "row": ["Marfan syndrome", 42],
      "meta": [null, null]
    }]
  }]
}
```

### SPARQL Response (JSON)

```json
{
  "head": {
    "vars": ["disease_name", "count"]
  },
  "results": {
    "bindings": [{
      "disease_name": {"type": "literal", "value": "Marfan syndrome"},
      "count": {"type": "literal", "value": "42"}
    }]
  }
}
```

---

## 🔧 Error Handling

### Neo4j

```python
from neo4j.exceptions import ServiceUnavailable, AuthError

try:
    with driver.session() as session:
        result = session.run(query)
except ServiceUnavailable:
    print("Database unavailable")
except AuthError:
    print("Authentication failed")
except Exception as e:
    print(f"Query failed: {e}")
```

### SPARQL

```python
try:
    response = requests.post(url, data={"query": query}, auth=auth)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.ConnectionError:
    print("Connection failed")
except ValueError:
    print("Invalid JSON response")
```

---

## 📚 Additional Resources

- **Neo4j Driver Documentation**: https://neo4j.com/docs/api/python-driver/
- **SPARQL 1.1 Specification**: https://www.w3.org/TR/sparql11-query/
- **Biolink Model**: https://biolink.github.io/biolink-model/

---

**Last Updated**: April 2026  
**API Version**: 1.0.0
