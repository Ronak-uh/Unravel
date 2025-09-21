#!/bin/bash

echo "🚀 Deploying Ghost Blog to Vercel from GitHub..."
echo "=========================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo ""
echo "🔗 GitHub Deployment Options:"
echo ""
echo "Option 1: Quick Deploy from GitHub"
echo "=================================="
echo "1. Go to https://vercel.com/new"
echo "2. Click 'Import Git Repository'"
echo "3. Select 'Ronak-uh/Unravel'"
echo "4. Vercel will auto-detect and deploy!"
echo ""

echo "Option 2: CLI Deployment"
echo "======================="
echo "1. Connect this project to Vercel"
echo "2. Deploy with automatic GitHub integration"
echo ""

read -p "🤔 Choose deployment method (1 for GitHub, 2 for CLI): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "🌐 Opening Vercel deployment page..."
    echo "👆 Go to: https://vercel.com/new"
    echo ""
    echo "📋 Steps:"
    echo "1. Click 'Import Git Repository'"
    echo "2. Find and select 'Ronak-uh/Unravel'"
    echo "3. Set these environment variables:"
    echo "   - GEMINI_API_KEY: your-gemini-key"
    echo "   - GOOGLE_API_KEY: your-google-key" 
    echo "   - GOOGLE_CX: your-search-engine-id"
    echo "   - NODE_ENV: production"
    echo "4. Click 'Deploy'!"
    echo ""
    echo "🎉 Your Ghost blog will be live in ~2 minutes!"
    
    # Open Vercel in browser
    open "https://vercel.com/new" 2>/dev/null || echo "Please visit: https://vercel.com/new"
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "🔐 Logging into Vercel..."
    vercel login
    
    echo ""
    echo "🚀 Deploying to Vercel..."
    vercel --prod
    
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "📝 Next steps:"
    echo "1. Go to your Vercel dashboard"
    echo "2. Add environment variables:"
    echo "   - GEMINI_API_KEY: your-gemini-key"
    echo "   - GOOGLE_API_KEY: your-google-key"
    echo "   - GOOGLE_CX: your-search-engine-id"
    echo "   - NODE_ENV: production"
    echo "3. Redeploy for env vars to take effect"
    
else
    echo "❌ Invalid choice. Please run the script again."
    exit 1
fi

echo ""
echo "🎯 Vercel Features You Get:"
echo "- ⚡ Instant deployments from GitHub"
echo "- 🔄 Auto-deployments on git push"
echo "- 🌍 Global CDN"
echo "- 📊 Analytics and monitoring"
echo "- 🔒 Automatic HTTPS"
echo ""
echo "🎉 Your automated Ghost blog is ready!"