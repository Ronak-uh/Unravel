#!/bin/bash

echo "🚀 Deploying Ghost Blog to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

echo "📋 Please ensure you have:"
echo "1. A Railway account (signup at railway.app)"
echo "2. Your API keys ready:"
echo "   - GEMINI_API_KEY"
echo "   - GOOGLE_API_KEY" 
echo "   - GOOGLE_CX"

read -p "Press Enter when ready to deploy..."

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Initialize and deploy
echo "🚢 Deploying your Ghost blog..."
railway up

echo "✅ Deployment initiated!"
echo ""
echo "📝 Next steps:"
echo "1. Go to your Railway dashboard"
echo "2. Set environment variables:"
echo "   - GHOST_URL: https://your-app.railway.app"
echo "   - NODE_ENV: production"
echo "   - GEMINI_API_KEY: your-key"
echo "   - GOOGLE_API_KEY: your-key"
echo "   - GOOGLE_CX: your-search-engine-id"
echo ""
echo "🎉 Your Ghost blog with categories will be live!"