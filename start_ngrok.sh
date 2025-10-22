#!/bin/bash

echo "🚀 Starting ngrok for ChatGPT Apps Integration"
echo "=============================================="

# Check if server is running on port 8000
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Server is running on port 8000"
else
    echo "❌ Server is not running on port 8000"
    echo "Starting server..."
    python3 run.py &
    sleep 3
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Server started successfully on port 8000"
    else
        echo "❌ Failed to start server on port 8000"
        exit 1
    fi
fi

# Check if ngrok is configured
if ngrok config check &> /dev/null; then
    echo "✅ ngrok is configured"
else
    echo "❌ ngrok needs authentication"
    echo ""
    echo "Please configure ngrok first:"
    echo "1. Sign up: https://dashboard.ngrok.com/signup"
    echo "2. Get authtoken: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "3. Configure: ngrok config add-authtoken YOUR_AUTHTOKEN_HERE"
    echo ""
    read -p "Press Enter after configuring ngrok..."
fi

echo ""
echo "🌐 Starting ngrok tunnel on port 8000..."
echo "This will expose your server to the internet for ChatGPT Apps integration"
echo ""

# Start ngrok on the correct port (8000)
ngrok http 8000

echo ""
echo "🎉 ngrok tunnel started!"
echo "Copy the 'Forwarding' URL (e.g., https://abc123.ngrok.io)"
echo "Use this URL in your ChatGPT Apps connector settings"
