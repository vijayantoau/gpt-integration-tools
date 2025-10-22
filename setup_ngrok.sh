#!/bin/bash

echo "🚀 Setting up ngrok for GPT Integration"
echo "======================================"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed. Please install it first:"
    echo "   brew install ngrok/ngrok/ngrok"
    exit 1
fi

echo "✅ ngrok is installed"

# Check if authtoken is configured
if ngrok config check &> /dev/null; then
    echo "✅ ngrok authtoken is configured"
else
    echo "❌ ngrok authtoken not configured"
    echo ""
    echo "Please follow these steps:"
    echo "1. Go to: https://dashboard.ngrok.com/signup"
    echo "2. Create a free account"
    echo "3. Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "4. Run: ngrok config add-authtoken YOUR_AUTHTOKEN_HERE"
    echo ""
    read -p "Press Enter after you've configured your authtoken..."
fi

# Start the server if not running
if ! curl -s http://localhost:8000/health &> /dev/null; then
    echo "🔄 Starting MCP server..."
    python3 run.py &
    SERVER_PID=$!
    sleep 3
    echo "✅ Server started (PID: $SERVER_PID)"
else
    echo "✅ MCP server is already running"
fi

# Start ngrok
echo "🌐 Starting ngrok tunnel..."
ngrok http 8000

echo ""
echo "🎉 Setup complete!"
echo "Copy the 'Forwarding' URL from ngrok (e.g., https://abc123.ngrok.io)"
echo "Use this URL in your ChatGPT App configuration"
