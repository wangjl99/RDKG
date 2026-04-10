#!/bin/bash

# Quick Setup Script for RDKG GitHub Repository
# https://github.com/wangjl99/RDKG

echo "=========================================="
echo "RDKG GitHub Repository Setup"
echo "=========================================="
echo ""

# Step 1: Navigate to your local RDKG directory
echo "Step 1: Checking directory..."
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git branch -M main
else
    echo "✓ Git repository already initialized"
fi

# Step 2: Add remote
echo ""
echo "Step 2: Setting up remote..."
if ! git remote get-url origin > /dev/null 2>&1; then
    git remote add origin https://github.com/wangjl99/RDKG.git
    echo "✓ Remote 'origin' added"
else
    echo "✓ Remote 'origin' already exists"
fi

# Step 3: Stage all files
echo ""
echo "Step 3: Staging files..."
git add .
echo "✓ Files staged"

# Step 4: Show status
echo ""
echo "Git Status:"
git status --short

# Step 5: Commit
echo ""
read -p "Commit message (default: 'Initial commit: Complete knowledge graph with documentation'): " commit_msg
commit_msg=${commit_msg:-"Initial commit: Complete knowledge graph with documentation"}

git commit -m "$commit_msg"
echo "✓ Changes committed"

# Step 6: Push
echo ""
echo "Step 6: Pushing to GitHub..."
echo "Note: You may need to authenticate with GitHub"
git push -u origin main

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Your repository is now live at:"
echo "https://github.com/wangjl99/RDKG"
echo ""
echo "Next steps:"
echo "1. Visit your repository on GitHub"
echo "2. Add a description: 'Comprehensive rare disease knowledge graph'"
echo "3. Add topics: rare-diseases, knowledge-graph, neo4j, sparql, biolink-model"
echo "4. Enable GitHub Discussions (optional)"
echo "5. Register with FRINK OKN: https://github.com/frink-okn"
echo ""
