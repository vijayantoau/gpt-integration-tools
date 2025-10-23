#!/bin/bash

# GPT Integration Tools - Deployment Script

set -e

echo "🚀 GPT Integration Tools - Deployment Script"
echo "=" * 50

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run from project root."
    exit 1
fi

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Error: Vercel CLI not found. Please install it first:"
    echo "   npm install -g vercel"
    exit 1
fi

# Clean up
echo "🧹 Cleaning up..."
rm -rf __pycache__/
rm -rf .vercel/
rm -f *.pyc

# Run tests
echo "🧪 Running tests..."
if [ -f "tests/run_tests.py" ]; then
    python3 tests/run_tests.py
    if [ $? -ne 0 ]; then
        echo "⚠️  Some tests failed, but continuing with deployment..."
    fi
fi

# Commit changes
echo "📝 Committing changes..."
git add .
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"

# Push to repository
echo "📤 Pushing to repository..."
git push origin main

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "🔗 Check your Vercel dashboard for the deployment URL"
