# Quick Start: Push to GitHub

Get your RDKG repository online in 5 minutes!

## 📋 Your Repository

**GitHub URL**: https://github.com/wangjl99/RDKG  
**Local Directory**: Files are in `/mnt/user-data/outputs/github-repo/`

---

## 🚀 Push to GitHub (3 Steps)

### Step 1: Clone Your Empty Repository

```bash
cd ~/Downloads
git clone https://github.com/wangjl99/RDKG.git
cd RDKG
```

### Step 2: Copy All Files

```bash
# Copy all documentation and configuration files
cp -r /mnt/user-data/outputs/github-repo/* .
cp /mnt/user-data/outputs/github-repo/.gitignore .

# Verify files copied
ls -la
```

You should see:
```
.gitignore
CONTRIBUTING.md
FILE_MANIFEST.md
LICENSE
README.md
docker-compose.yml
setup_github.sh
docs/
```

### Step 3: Push to GitHub

**Option A - Use Setup Script (Recommended)**:
```bash
chmod +x setup_github.sh
./setup_github.sh
```

**Option B - Manual**:
```bash
git add .
git commit -m "Initial commit: Complete rare disease knowledge graph with documentation"
git push -u origin main
```

---

## ✅ Verify on GitHub

Visit: https://github.com/wangjl99/RDKG

You should see:
- ✓ README.md with badges and documentation
- ✓ 11 files + docs/ folder
- ✓ Professional layout

---

## 📝 Update Repository Settings

### 1. Add Description

```
Comprehensive rare disease knowledge graph integrating Orphanet, MONDO, HPO, DrugBank, and ClinVar. Supports Neo4j (Cypher) and SPARQL access for biomedical research.
```

### 2. Add Topics

Click "⚙️ Settings" → Add topics:
```
rare-diseases
knowledge-graph
neo4j
sparql
biolink-model
biomedical-informatics
semantic-web
rdf
orphanet
mondo
```

### 3. Add Website (Optional)

If you deploy SPARQL endpoint publicly:
```
http://your-server.com:3030/rdaccelerate/sparql
```

---

## 📊 Optional: Add Data Files

The data files are **NOT** included in the repository (they're large and .gitignored).

**Option 1 - Provide Download Links** (Recommended):

Create a `DATA.md` file:
```markdown
# Data Files

Due to size constraints, data files are available separately:

## Download Links

- **Neo4j CSVs**: [Download](your-download-link)
  - nodes_no_trials.csv (4.7 MB, 72,368 nodes)
  - edges_no_trials.csv (84 MB, 834,260 edges)

- **RDF/SPARQL**: [Download](your-download-link)
  - rdaccelerate_kg.ttl (180 MB, 1,181,391 triples)

## Import Instructions

See [docs/SETUP.md](docs/SETUP.md) for complete import instructions.
```

**Option 2 - Use Git LFS** (For Large Files):
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.csv"
git lfs track "*.ttl"

# Add and commit
git add .gitattributes
git add data/*.csv data/*.ttl
git commit -m "Add data files via Git LFS"
git push
```

**Option 3 - Upload to Zenodo** (Academic Publishing):
- Upload to Zenodo: https://zenodo.org
- Get DOI for citation
- Link in README.md

---

## 🎯 After Publishing

### Enable GitHub Features

1. **GitHub Discussions** (Optional):
   - Settings → Features → ✓ Discussions
   - Good for Q&A and community

2. **GitHub Pages** (Optional):
   - Settings → Pages → Deploy from main branch
   - Host documentation online

3. **Issue Templates** (Optional):
   - Create `.github/ISSUE_TEMPLATE/bug_report.md`
   - Create `.github/ISSUE_TEMPLATE/feature_request.md`

### Register with FRINK OKN

1. Visit: https://github.com/frink-okn
2. Follow their registration process
3. Provide SPARQL endpoint details

### Share Your Work

**Twitter/X**:
```
🎉 Just published RDKG - a comprehensive #RareDisease knowledge graph!

✅ 72K+ entities (diseases, genes, drugs, phenotypes)
✅ 834K relationships
✅ Neo4j & SPARQL access
✅ Biolink Model compliant

Check it out: https://github.com/wangjl99/RDKG

#KnowledgeGraph #Bioinformatics
```

**Reddit** (r/bioinformatics):
```
I built a comprehensive rare disease knowledge graph

[RDKG](https://github.com/wangjl99/RDKG)

Integrates Orphanet, MONDO, HPO, DrugBank, and ClinVar into a unified graph database. Supports both Neo4j (Cypher) and SPARQL queries.

Looking for feedback and collaborators!
```

---

## 📞 Support

**Questions?**
- Open an issue: https://github.com/wangjl99/RDKG/issues
- Email: (add your email)

**Found a bug?**
- See CONTRIBUTING.md for reporting guidelines

**Want to contribute?**
- See CONTRIBUTING.md for contribution workflow

---

## ✅ Final Checklist

- [ ] Repository cloned
- [ ] Files copied
- [ ] Pushed to GitHub
- [ ] Repository description added
- [ ] Topics added
- [ ] README.md displays correctly
- [ ] Data files available (download link or Git LFS)
- [ ] Email address updated in README.md
- [ ] Announced to community
- [ ] Registered with FRINK OKN (if applicable)

---

**Your repository is ready!** 🎉

**Live at**: https://github.com/wangjl99/RDKG
