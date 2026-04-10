# Setup Guide

Complete installation and configuration guide for the RDAccelerate Rare Disease Knowledge Graph.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Data Import](#data-import)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## ✅ Prerequisites

### System Requirements

- **Operating System**: macOS, Linux, or Windows with WSL2
- **RAM**: 8GB minimum (16GB recommended)
- **Disk Space**: 10GB free space
- **Network**: Internet connection for Docker image downloads

### Software Requirements

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Python**: 3.8+ (for data import scripts)
- **Web Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

### Install Docker

**macOS**:
```bash
brew install --cask docker
```

**Linux (Ubuntu)**:
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER
```

**Windows**:
Download Docker Desktop from https://docker.com/products/docker-desktop

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/rdaccelerate-kg.git
cd rdaccelerate-kg
```

### 2. Start Services

```bash
# Start both Neo4j and Fuseki
docker-compose up -d

# Or start individual services
docker-compose up -d neo4j    # Neo4j only
docker-compose up -d fuseki    # Fuseki only
```

### 3. Wait for Startup

```bash
# Check logs
docker-compose logs -f

# Look for:
# - Neo4j: "Remote interface available at http://localhost:7474/"
# - Fuseki: "Started"
```

### 4. Access Services

- **Neo4j Browser**: http://localhost:7474
  - Username: `neo4j`
  - Password: `rdaccelerate2024`

- **Fuseki UI**: http://localhost:3030
  - Username: `admin`
  - Password: `rdaccelerate2024`

---

## 📖 Detailed Setup

### Step 1: Prepare Directory Structure

```bash
mkdir -p rdaccelerate-kg
cd rdaccelerate-kg

# Create data directories
mkdir -p neo4j_data neo4j_logs neo4j_export neo4j_plugins
mkdir -p fuseki_data rdf_data
```

### Step 2: Create Docker Compose File

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.15.0
    container_name: rdaccelerate-neo4j
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/rdaccelerate2024
      - NEO4J_PLUGINS=["apoc"]
      - NEO4J_dbms_memory_heap_initial__size=2G
      - NEO4J_dbms_memory_heap_max__size=4G
    volumes:
      - ./neo4j_data:/data
      - ./neo4j_logs:/logs
      - ./neo4j_export:/var/lib/neo4j/import
    restart: unless-stopped

  fuseki:
    image: stain/jena-fuseki:latest
    container_name: rdaccelerate-fuseki
    ports:
      - "3030:3030"
    environment:
      - ADMIN_PASSWORD=rdaccelerate2024
      - JVM_ARGS=-Xmx4g
    volumes:
      - ./fuseki_data:/fuseki
      - ./rdf_data:/staging
    restart: unless-stopped
```

### Step 3: Start Services

```bash
# Pull Docker images
docker-compose pull

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f neo4j
docker-compose logs -f fuseki
```

### Step 4: Verify Installation

```bash
# Check Neo4j
curl http://localhost:7474

# Check Fuseki
curl http://localhost:3030
```

---

## 📥 Data Import

### Option 1: Load Pre-built Data (Recommended)

If CSV and RDF files are provided:

**Neo4j Import**:

1. Copy data files:
```bash
cp nodes_no_trials.csv neo4j_export/
cp edges_no_trials.csv neo4j_export/
```

2. Open Neo4j Browser: http://localhost:7474

3. Create constraints:
```cypher
CREATE CONSTRAINT node_id_unique IF NOT EXISTS FOR (n:Disease) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT gene_id_unique IF NOT EXISTS FOR (n:Gene) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT phenotype_id_unique IF NOT EXISTS FOR (n:Phenotype) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT variant_id_unique IF NOT EXISTS FOR (n:Variant) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT drug_id_unique IF NOT EXISTS FOR (n:Drug) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT treatment_id_unique IF NOT EXISTS FOR (n:Treatment) REQUIRE n.id IS UNIQUE;
```

4. Import nodes:
```cypher
LOAD CSV WITH HEADERS FROM 'file:///nodes_no_trials.csv' AS row
CALL apoc.create.node([row.`:LABEL`], {
  id: row.`id:ID`,
  name: row.name,
  category: row.category
}) YIELD node
RETURN count(node);
```

5. Import edges (use Python script):
```bash
cd scripts
python3 import_edges.py
```

**Fuseki Import**:

1. Copy RDF file:
```bash
cp rdaccelerate_kg.ttl rdf_data/
```

2. Create dataset:
```bash
curl -X POST http://localhost:3030/$/datasets \
  --user admin:rdaccelerate2024 \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "dbName=rdaccelerate&dbType=tdb2"
```

3. Upload data:
```bash
curl -X POST http://localhost:3030/rdaccelerate/data \
  --user admin:rdaccelerate2024 \
  --data-binary @rdf_data/rdaccelerate_kg.ttl \
  -H "Content-Type: text/turtle"
```

4. Verify:
```bash
curl -X POST http://localhost:3030/rdaccelerate/sparql \
  --user admin:rdaccelerate2024 \
  --data-urlencode "query=SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }" \
  -H "Accept: text/csv"
```

### Option 2: Build from Source MySQL

If rebuilding from MySQL source:

1. Export from MySQL (see `scripts/export_from_mysql.py`)
2. Follow steps above for Neo4j and Fuseki import

---

## ⚙️ Configuration

### Neo4j Memory Settings

Edit `docker-compose.yml`:

```yaml
environment:
  # Heap size (adjust based on available RAM)
  - NEO4J_dbms_memory_heap_initial__size=2G
  - NEO4J_dbms_memory_heap_max__size=4G
  
  # Page cache (adjust based on data size)
  - NEO4J_dbms_memory_pagecache_size=2G
  
  # Transaction timeout
  - NEO4J_db_transaction_timeout=10m
```

### Fuseki JVM Settings

```yaml
environment:
  # Heap size
  - JVM_ARGS=-Xmx4g
```

### Port Configuration

Change ports in `docker-compose.yml` if defaults conflict:

```yaml
ports:
  - "7474:7474"  # Neo4j HTTP (change first number)
  - "7687:7687"  # Neo4j Bolt
  - "3030:3030"  # Fuseki
```

---

## 🔧 Troubleshooting

### Neo4j Won't Start

**Problem**: Container exits immediately

**Solution**:
```bash
# Check logs
docker-compose logs neo4j

# Common issues:
# 1. Port already in use
sudo lsof -i :7474
kill -9 <PID>

# 2. Insufficient memory
# Reduce heap size in docker-compose.yml

# 3. Permission issues
sudo chown -R $(id -u):$(id -g) neo4j_data/
```

### Fuseki Won't Start

**Problem**: Cannot access http://localhost:3030

**Solution**:
```bash
# Check if running
docker ps | grep fuseki

# Restart
docker-compose restart fuseki

# Check logs
docker-compose logs fuseki
```

### Import Fails

**Problem**: CSV import returns errors

**Solution**:
```bash
# Check file location
ls -lh neo4j_export/nodes_no_trials.csv

# Verify CSV format
head -5 neo4j_export/nodes_no_trials.csv

# Check Docker volume mount
docker exec rdaccelerate-neo4j ls -lh /var/lib/neo4j/import/
```

### Out of Memory

**Problem**: "Transaction timeout" or "Out of memory"

**Solution**:
```bash
# Increase heap size
# Edit docker-compose.yml:
NEO4J_dbms_memory_heap_max__size=6G

# Restart
docker-compose down
docker-compose up -d
```

### Connection Refused

**Problem**: Cannot connect to Neo4j/Fuseki

**Solution**:
```bash
# Check if services are running
docker-compose ps

# Check network
docker network ls
docker network inspect rdaccelerate-network

# Restart Docker
sudo systemctl restart docker
```

---

## 🌐 Production Deployment

### Security Considerations

1. **Change Default Passwords**:
```bash
# Neo4j
docker exec -it rdaccelerate-neo4j cypher-shell -u neo4j -p rdaccelerate2024
:ALTER USER neo4j SET PASSWORD FROM 'rdaccelerate2024' TO 'NEW_SECURE_PASSWORD';

# Fuseki - set in docker-compose.yml:
ADMIN_PASSWORD=NEW_SECURE_PASSWORD
```

2. **Enable SSL/TLS**:
```yaml
# Neo4j SSL
environment:
  - NEO4J_dbms_ssl_policy_bolt_enabled=true
  - NEO4J_dbms_ssl_policy_https_enabled=true
volumes:
  - ./ssl/certificates:/ssl
```

3. **Firewall Configuration**:
```bash
# Allow only specific IPs
sudo ufw allow from 192.168.1.0/24 to any port 7474
sudo ufw allow from 192.168.1.0/24 to any port 3030
```

### Reverse Proxy (Nginx)

```nginx
# /etc/nginx/sites-available/rdaccelerate

# Neo4j
server {
    listen 80;
    server_name neo4j.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:7474;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Fuseki
server {
    listen 80;
    server_name sparql.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:3030;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Backup Strategy

```bash
# Neo4j backup
docker exec rdaccelerate-neo4j neo4j-admin database dump neo4j \
  --to-path=/backups/neo4j-$(date +%Y%m%d).dump

# Fuseki backup
docker exec rdaccelerate-fuseki tar -czf /fuseki/backup-$(date +%Y%m%d).tar.gz /fuseki/databases/
```

### Monitoring

```bash
# Resource usage
docker stats rdaccelerate-neo4j rdaccelerate-fuseki

# Neo4j metrics
curl http://localhost:7474/db/neo4j/metrics

# Fuseki stats
curl http://localhost:3030/$/stats
```

---

## 🔄 Maintenance

### Update Docker Images

```bash
# Pull latest images
docker-compose pull

# Recreate containers
docker-compose up -d --force-recreate
```

### Clear Data (Reset)

```bash
# Stop services
docker-compose down

# Remove data
rm -rf neo4j_data/* fuseki_data/*

# Restart
docker-compose up -d
```

### Logs Management

```bash
# View logs
docker-compose logs --tail=100 neo4j
docker-compose logs --tail=100 fuseki

# Clear logs
docker-compose down
rm -rf neo4j_logs/*
docker-compose up -d
```

---

## 📊 Verify Installation

### Check Neo4j

```bash
# Via browser
open http://localhost:7474

# Via command line
docker exec rdaccelerate-neo4j cypher-shell -u neo4j -p rdaccelerate2024 \
  "MATCH (n) RETURN count(n) AS node_count;"
```

### Check Fuseki

```bash
# Via browser
open http://localhost:3030

# Via command line
curl -X POST http://localhost:3030/rdaccelerate/sparql \
  --user admin:rdaccelerate2024 \
  --data-urlencode "query=SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }" \
  -H "Accept: text/csv"
```

### Expected Results

- **Neo4j**: 72,368 nodes, 834,260 relationships
- **Fuseki**: 1,181,391 triples

---

## 📞 Support

For issues not covered here:

1. Check [GitHub Issues](https://github.com/YOUR_USERNAME/rdaccelerate-kg/issues)
2. Review [documentation](docs/)
3. Contact maintainers

---

**Last Updated**: April 2026  
**Version**: 1.0.0
