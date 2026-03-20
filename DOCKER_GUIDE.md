# Docker Deployment Guide for RDKG

This guide covers Docker deployment for the Rare Disease Knowledge Graph (RDKG) using Blazegraph RDF triplestore.

## 📋 **Prerequisites**

- Docker Engine 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose 1.29+ ([Install Docker Compose](https://docs.docker.com/compose/install/))
- Minimum 8GB RAM available for Docker
- Minimum 20GB disk space

**Verify installation:**
```bash
docker --version
docker-compose --version
```

---

## 🚀 **Quick Start (3 Steps)**

### **Step 1: Clone Repository**

```bash
git clone https://github.com/UTHealth-SBMI/rare-disease-kg.git
cd rare-disease-kg/docker
```

### **Step 2: Start Services**

```bash
# Start Blazegraph and YASGUI query interface
docker-compose up -d

# Check status
docker-compose ps
```

### **Step 3: Access Interfaces**

- **Blazegraph UI**: http://localhost:9999/blazegraph/
- **YASGUI Query Interface**: http://localhost:8080/
- **SPARQL Endpoint**: http://localhost:9999/blazegraph/sparql

---

## 🏗️ **Detailed Setup**

### **Option 1: Using Docker Compose (Recommended)**

Docker Compose manages multiple containers (Blazegraph + YASGUI) with one command.

#### **1. Create docker-compose.yml**

Place this file in your project root:

```yaml
version: '3.8'

services:
  blazegraph:
    build:
      context: ./docker
      dockerfile: Dockerfile
    container_name: rdkg-blazegraph
    ports:
      - "9999:9999"
    environment:
      - JAVA_OPTS=-Xmx4g -Xms2g
    volumes:
      - blazegraph-data:/var/lib/blazegraph
      - ./data:/data:ro
    restart: unless-stopped

  yasgui:
    image: erikap/yasgui:latest
    container_name: rdkg-yasgui
    ports:
      - "8080:80"
    environment:
      - DEFAULT_SPARQL_ENDPOINT=http://blazegraph:9999/blazegraph/sparql
    depends_on:
      - blazegraph
    restart: unless-stopped

volumes:
  blazegraph-data:
```

#### **2. Start All Services**

```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f blazegraph

# Check health
docker-compose ps
```

#### **3. Load RDF Data**

**Option A: Manual load via UI**
1. Open http://localhost:9999/blazegraph/
2. Click "UPDATE" tab
3. Choose "RDF Data" → "File"
4. Upload `data/rdkg_complete.ttl`
5. Click "Update"

**Option B: Automated load via API**
```bash
# Load Turtle file
curl -X POST \
  -H 'Content-Type: text/turtle' \
  --data-binary '@data/rdkg_complete.ttl' \
  http://localhost:9999/blazegraph/sparql

# Or load N-Triples (faster for large files)
curl -X POST \
  -H 'Content-Type: application/n-triples' \
  --data-binary '@data/rdkg_complete.nt' \
  http://localhost:9999/blazegraph/sparql
```

#### **4. Verify Data Loaded**

```bash
# Count total triples
curl -X POST \
  -H 'Content-Type: application/sparql-query' \
  --data 'SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }' \
  http://localhost:9999/blazegraph/sparql

# Expected output: ~220,000 triples
```

---

### **Option 2: Using Docker Only (No Compose)**

If you prefer to manage containers manually:

#### **1. Build Image**

```bash
cd docker
docker build -t rdkg:latest .
```

#### **2. Create Volume**

```bash
docker volume create rdkg-data
```

#### **3. Run Container**

```bash
docker run -d \
  --name rdkg-blazegraph \
  -p 9999:9999 \
  -e JAVA_OPTS="-Xmx4g -Xms2g" \
  -v rdkg-data:/var/lib/blazegraph \
  -v $(pwd)/../data:/data:ro \
  --restart unless-stopped \
  rdkg:latest
```

#### **4. Check Logs**

```bash
docker logs -f rdkg-blazegraph
```

---

## 🔧 **Configuration**

### **Memory Settings**

Adjust Java heap size based on your data size:

```yaml
# docker-compose.yml
environment:
  - JAVA_OPTS=-Xmx8g -Xms4g  # 8GB max, 4GB initial
```

**Recommendations:**
- Small dataset (<100K triples): `-Xmx2g -Xms1g`
- Medium dataset (<1M triples): `-Xmx4g -Xms2g`
- Large dataset (>1M triples): `-Xmx8g -Xms4g`
- **RDKG (220K triples)**: `-Xmx4g -Xms2g` ✅

### **Port Configuration**

Change default ports if needed:

```yaml
ports:
  - "9999:9999"  # Change first number: "8080:9999"
```

### **Data Persistence**

Data persists in Docker volumes:

```bash
# View volume location
docker volume inspect rdkg-data

# Backup data
docker run --rm \
  -v rdkg-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/rdkg-backup.tar.gz -C /data .

# Restore data
docker run --rm \
  -v rdkg-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/rdkg-backup.tar.gz -C /data
```

---

## 📊 **Performance Tuning**

### **Blazegraph Configuration**

Edit `blazegraph.properties` for optimization:

```properties
# Increase branching factor for better read performance
com.bigdata.namespace.kb.lex.com.bigdata.btree.BTree.branchingFactor=1024

# Increase query timeout (milliseconds)
com.bigdata.rdf.sparql.ast.QueryHints.queryTimeout=300000

# Increase memory per query
com.bigdata.rdf.sparql.ast.QueryHints.analyticMaxMemoryPerQuery=536870912
```

### **Docker Resource Limits**

```yaml
# docker-compose.yml
services:
  blazegraph:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          memory: 4G
```

---

## 🔍 **Testing Your Deployment**

### **1. Health Check**

```bash
# Check service health
docker-compose ps

# Should show "healthy" status
curl http://localhost:9999/blazegraph/status
```

### **2. Run Test Queries**

```bash
# Query 1: Count triples
curl -X POST \
  -H 'Accept: application/sparql-results+json' \
  -H 'Content-Type: application/sparql-query' \
  --data 'SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }' \
  http://localhost:9999/blazegraph/sparql

# Query 2: Find all diseases
curl -X POST \
  -H 'Accept: application/sparql-results+json' \
  -H 'Content-Type: application/sparql-query' \
  --data 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
          SELECT ?disease ?label WHERE {
            ?disease a <http://rdaccelerate.org/ontology/RareDisease> ;
                     rdfs:label ?label .
          } LIMIT 10' \
  http://localhost:9999/blazegraph/sparql
```

### **3. Performance Benchmark**

```bash
# Run benchmark queries
cd ../validation
python benchmark_queries.py --endpoint http://localhost:9999/blazegraph/sparql

# Expected: <500ms average response time
```

---

## 🐛 **Troubleshooting**

### **Problem: Container Won't Start**

```bash
# Check logs for errors
docker-compose logs blazegraph

# Common issues:
# 1. Port already in use
sudo lsof -i :9999
# Solution: Change port in docker-compose.yml

# 2. Insufficient memory
# Solution: Increase Docker memory limit or reduce JAVA_OPTS
```

### **Problem: Data Not Loading**

```bash
# Check file permissions
ls -la data/rdkg_complete.ttl

# Verify file format
head -n 20 data/rdkg_complete.ttl

# Try loading smaller file first
curl -X POST \
  -H 'Content-Type: text/turtle' \
  --data-binary '@data/test_sample.ttl' \
  http://localhost:9999/blazegraph/sparql
```

### **Problem: Slow Query Performance**

```bash
# 1. Check memory usage
docker stats rdkg-blazegraph

# 2. Increase Java heap
docker-compose stop
# Edit JAVA_OPTS in docker-compose.yml
docker-compose up -d

# 3. Optimize queries
# Use LIMIT clause
# Add appropriate filters
# Check query plan with EXPLAIN
```

### **Problem: Container Keeps Restarting**

```bash
# Remove restart policy temporarily
docker update --restart=no rdkg-blazegraph

# Check what's causing crashes
docker logs rdkg-blazegraph --tail 100

# Common causes:
# - OutOfMemoryError: Increase heap size
# - Port conflict: Change port mapping
# - Corrupted journal: Delete volume and reload data
```

---

## 📦 **Production Deployment**

### **Best Practices**

1. **Use SSL/TLS**
   - Run behind Nginx reverse proxy
   - Enable HTTPS
   - Configure CORS if needed

2. **Enable Authentication**
   - Configure Blazegraph security
   - Use API keys
   - Implement rate limiting

3. **Backup Strategy**
   ```bash
   # Daily backup script
   #!/bin/bash
   DATE=$(date +%Y%m%d)
   docker exec rdkg-blazegraph \
     java -cp blazegraph.jar com.bigdata.rdf.sail.webapp.BackupServlet \
     > backup_${DATE}.jnl
   ```

4. **Monitoring**
   - Enable Prometheus metrics
   - Set up alerting
   - Monitor query performance

### **Sample Nginx Configuration**

```nginx
server {
    listen 443 ssl;
    server_name rdkg.uth.tmc.edu;

    ssl_certificate /etc/ssl/certs/rdkg.crt;
    ssl_certificate_key /etc/ssl/private/rdkg.key;

    location /blazegraph/ {
        proxy_pass http://localhost:9999/blazegraph/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🛑 **Stopping and Cleaning Up**

### **Stop Services**

```bash
# Stop without removing containers
docker-compose stop

# Stop and remove containers (keeps data)
docker-compose down

# Stop and remove everything including data
docker-compose down -v
```

### **Clean Up System**

```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune
```

---

## 📚 **Additional Resources**

- **Blazegraph Documentation**: https://github.com/blazegraph/database/wiki
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **SPARQL Tutorial**: https://www.w3.org/TR/sparql11-query/
- **RDKG Schema**: [../docs/SCHEMA.md](../docs/SCHEMA.md)
- **Example Queries**: [../queries/README.md](../queries/README.md)

---

## 📞 **Support**

Issues with Docker deployment?

1. Check troubleshooting section above
2. Search [GitHub Issues](https://github.com/UTHealth-SBMI/rare-disease-kg/issues)
3. Create new issue with:
   - Docker version
   - Error logs
   - Steps to reproduce
4. Contact: jinlian.wang@uth.tmc.edu

---

## 🎯 **Next Steps**

After successful deployment:

1. ✅ Load your RDF data
2. ✅ Test example queries
3. ✅ Configure backups
4. ✅ Set up monitoring
5. ✅ Review security settings
6. ✅ Document your SPARQL endpoint URL

**Production Checklist**: [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)
