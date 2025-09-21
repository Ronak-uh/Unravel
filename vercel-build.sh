#!/bin/bash
# Vercel build script for Python automation

echo "🔧 Setting up Python environment for Vercel..."

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python packages..."
    pip install -r requirements.txt
fi

# Create necessary directories
mkdir -p /tmp/ghost-content
mkdir -p /tmp/logs

echo "✅ Vercel build setup complete!"