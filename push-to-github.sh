#!/bin/bash

echo "🚀 GitHub Setup Helper"
echo "======================"

# Get GitHub username and repository name
read -p "Enter your GitHub username: " username
read -p "Enter repository name (default: automated-ghost-blog): " repo_name

# Set default repo name if empty
if [ -z "$repo_name" ]; then
    repo_name="automated-ghost-blog"
fi

echo ""
echo "📋 Repository URL: https://github.com/$username/$repo_name"
echo ""

# Check if remote already exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "⚠️  Remote 'origin' already exists. Removing..."
    git remote remove origin
fi

# Add remote
echo "🔗 Adding GitHub remote..."
git remote add origin "https://github.com/$username/$repo_name.git"

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Go to: https://github.com/$username/$repo_name"
    echo "2. Set up GitHub Secrets (see GITHUB-SETUP.md)"
    echo "3. Deploy using: ./deploy-railway.sh"
    echo ""
    echo "📊 Your automation will run every 5 hours automatically!"
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "1. Repository exists on GitHub"
    echo "2. You have push access"
    echo "3. GitHub authentication is set up"
    echo ""
    echo "💡 Manual commands:"
    echo "git remote add origin https://github.com/$username/$repo_name.git"
    echo "git push -u origin main"
fi