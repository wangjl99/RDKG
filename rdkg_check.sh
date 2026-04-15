#!/bin/bash
# rdkg_check.sh — run this to find out what's happening
# Usage: bash rdkg_check.sh

echo "========================================"
echo " RDKG Environment Check"
echo "========================================"

echo ""
echo "── Docker containers ───────────────────"
docker compose ps 2>/dev/null || echo "  (not in a compose directory — cd to rdkg_deploy first)"

echo ""
echo "── Port 7687 (Neo4j Bolt) ──────────────"
lsof -i :7687 2>/dev/null | head -5 || echo "  Nothing on port 7687"

echo ""
echo "── Port 7474 (Neo4j HTTP) ──────────────"
lsof -i :7474 2>/dev/null | head -5 || echo "  Nothing on port 7474"

echo ""
echo "── Port 8000 (FastAPI) ─────────────────"
lsof -i :8000 2>/dev/null | head -3 || echo "  Nothing on port 8000"

echo ""
echo "── Local Neo4j installation ────────────"
which neo4j 2>/dev/null && neo4j status 2>/dev/null || echo "  neo4j not in PATH"
ls ~/Library/Application\ Support/Neo4j\ Desktop/ 2>/dev/null | head -5 || true
ls /usr/local/bin/neo4j 2>/dev/null || true

echo ""
echo "── Docker Neo4j logs (last 20 lines) ───"
docker logs rdkg_neo4j --tail 20 2>/dev/null || echo "  Container rdkg_neo4j not found"

echo ""
echo "── Existing RDKG Neo4j data ────────────"
# Check common locations for Neo4j data
for p in \
    ~/neo4j/data \
    ~/Library/Application\ Support/Neo4j\ Desktop/Application/relate-data \
    /usr/local/var/neo4j/data \
    ~/.neo4j/data; do
    [ -d "$p" ] && echo "  Found: $p" && ls "$p" 2>/dev/null | head -3
done

echo ""
echo "========================================"
echo "Paste the output above so we can fix it"
echo "========================================"
