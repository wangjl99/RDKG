# Contributing to RDKG Knowledge Graph

Thank you for your interest in contributing to the RDKG Rare Disease Knowledge Graph! This document provides guidelines for contributions.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Pull Request Process](#pull-request-process)
- [Data Contributions](#data-contributions)
- [Bug Reports](#bug-reports)

---

## 🤝 Code of Conduct

This project adheres to a code of conduct adapted from the [Contributor Covenant](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code.

### Our Standards

- **Be respectful** and inclusive
- **Be collaborative** and constructive
- **Focus on what's best** for the community
- **Show empathy** towards other community members

---

## 🎯 How to Contribute

### Types of Contributions

We welcome:

1. **Bug Reports**: Found a bug? Report it!
2. **Feature Requests**: Have ideas? Share them!
3. **Code Contributions**: Fix bugs, add features
4. **Documentation**: Improve or add documentation
5. **Data Quality**: Report data errors or improvements
6. **Query Examples**: Add useful query patterns
7. **Use Cases**: Share how you're using the knowledge graph

---

## 🛠️ Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Git
- Neo4j knowledge (for graph contributions)
- SPARQL knowledge (for RDF contributions)

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/wangjl99/RDKG.git
cd rdaccelerate-kg

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start services
docker-compose up -d

# Verify installation
python scripts/verify_installation.py
```

---

## 📝 Contribution Guidelines

### Code Style

**Python**:
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 100 characters

**Cypher Queries**:
- Use uppercase for keywords (`MATCH`, `WHERE`, `RETURN`)
- Use meaningful variable names
- Include comments for complex queries

**SPARQL Queries**:
- Use standard prefixes
- Format for readability
- Include comments

### Documentation

- Update README.md if adding features
- Add query examples to appropriate docs
- Include inline code comments
- Update CHANGELOG.md

### Commit Messages

Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

Example:
```
feat(queries): Add drug repurposing SPARQL query

Added new SPARQL query to identify drug repurposing candidates
based on shared phenotypes between diseases.

Closes #42
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Create an Issue**: Discuss changes before starting work
2. **Fork Repository**: Create your own fork
3. **Create Branch**: `git checkout -b feature/your-feature-name`
4. **Make Changes**: Implement your contribution
5. **Test Thoroughly**: Ensure everything works
6. **Update Documentation**: Add/update relevant docs

### Submission Process

1. **Commit Changes**:
```bash
git add .
git commit -m "feat: your feature description"
```

2. **Push to Fork**:
```bash
git push origin feature/your-feature-name
```

3. **Create Pull Request**:
   - Go to original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in PR template
   - Link related issues

4. **Code Review**:
   - Respond to feedback
   - Make requested changes
   - Re-request review when ready

5. **Merge**:
   - Maintainers will merge when approved
   - Delete your branch after merge

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Linked to related issue(s)

---

## 📊 Data Contributions

### Adding New Data Sources

If contributing new ontology or data source integration:

1. **Document Source**:
   - Name and version
   - License information
   - Access method
   - Update frequency

2. **Mapping to Biolink**:
   - Map entity types to Biolink classes
   - Map relationships to Biolink predicates
   - Document any custom types

3. **Quality Checks**:
   - Validate data format
   - Check for duplicates
   - Verify relationship directions
   - Ensure referential integrity

4. **Update Schema**:
   - Add to SCHEMA.md
   - Update statistics
   - Add query examples

### Reporting Data Errors

Use the issue template:

```markdown
**Error Type**: [Incorrect mapping/Missing data/Duplicate/Other]
**Entity ID**: [e.g., MONDO:0007947]
**Description**: [Describe the error]
**Expected**: [What should it be?]
**Evidence**: [Links to authoritative sources]
```

---

## 🐛 Bug Reports

### Before Reporting

- Check [existing issues](https://github.com/wangjl99/RDKG/issues)
- Verify with latest version
- Collect relevant information

### Bug Report Template

```markdown
**Describe the Bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run query '...'
2. Get result '...'
3. See error

**Expected Behavior**
What you expected to happen

**Environment**
- OS: [e.g., macOS 12.0]
- Docker version: [e.g., 20.10.8]
- Neo4j version: [e.g., 5.15.0]
- Browser: [e.g., Chrome 120]

**Screenshots/Logs**
If applicable, add screenshots or logs

**Additional Context**
Any other relevant information
```

---

## 🧪 Testing

### Running Tests

```bash
# Unit tests
python -m pytest tests/

# Integration tests
python -m pytest tests/integration/

# Query validation
python scripts/validate_queries.py
```

### Writing Tests

```python
import pytest
from neo4j import GraphDatabase

def test_disease_query():
    driver = GraphDatabase.driver("bolt://localhost:7687", 
                                   auth=("neo4j", "test_password"))
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Disease {id: 'MONDO:0007947'})
            RETURN d.name
        """)
        assert result.single()["d.name"] == "Marfan syndrome"
    driver.close()
```

---

## 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested
- `wontfix`: Will not be worked on
- `duplicate`: Already exists

---

## 📞 Getting Help

- **Questions**: Open a [GitHub Discussion](https://github.com/wangjl99/RDKG/discussions)
- **Chat**: Join our [Discord/Slack channel]
- **Email**: [maintainer email]

---

## 🎖️ Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Acknowledged in release notes
- Mentioned in publications (if applicable)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Your contributions make this project better for the rare disease research community!

---

**Last Updated**: April 2026
