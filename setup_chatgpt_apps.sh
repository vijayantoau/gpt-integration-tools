#!/bin/bash

echo "🚀 ChatGPT Apps Integration Setup"
echo "================================="

# Check if server is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Server is running on http://localhost:8000"
else
    echo "❌ Server is not running. Starting server..."
    python3 run.py &
    sleep 3
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Server started successfully"
    else
        echo "❌ Failed to start server"
        exit 1
    fi
fi

echo ""
echo "📋 Next Steps for ChatGPT Apps Integration:"
echo "=========================================="
echo ""
echo "1. 🌐 EXPOSE YOUR SERVER PUBLICLY:"
echo "   - Sign up for ngrok: https://dashboard.ngrok.com/signup"
echo "   - Get your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken"
echo "   - Configure ngrok: ngrok config add-authtoken YOUR_AUTHTOKEN_HERE"
echo "   - Expose server: ngrok http 8000"
echo "   - Copy the public URL (e.g., https://abc123.ngrok.io)"
echo ""
echo "2. 🔧 ENABLE DEVELOPER MODE IN CHATGPT:"
echo "   - For Enterprise: Contact your OpenAI partner for access"
echo "   - Go to Settings → Connectors → Advanced"
echo "   - Toggle on Developer mode"
echo ""
echo "3. 🛠️ CREATE YOUR CONNECTOR:"
echo "   - In ChatGPT: Settings → Connectors → Create"
echo "   - Connector Name: 'GPT Integration Tools'"
echo "   - Description: 'Weather, calculator, text analysis, and file search tools'"
echo "   - Connector URL: 'https://your-ngrok-url.ngrok.io/mcp'"
echo ""
echo "4. 🧪 TEST YOUR INTEGRATION:"
echo "   - Open new chat in ChatGPT"
echo "   - Click '+' button → Select Developer mode"
echo "   - Toggle on your connector"
echo "   - Test with: 'Use the GPT Integration Tools connector to get weather in New York'"
echo ""
echo "📊 Your Server Endpoints:"
echo "========================="
echo "• Main MCP: http://localhost:8000/mcp"
echo "• Tools: http://localhost:8000/mcp/tools"
echo "• Health: http://localhost:8000/health"
echo "• Web UI: http://localhost:8000"
echo "• API Docs: http://localhost:8000/docs"
echo ""
echo "🛠️ Available Tools:"
echo "==================="
echo "• Weather Tool: Get weather for any location"
echo "• Calculator Tool: Perform mathematical calculations"
echo "• Text Analysis Tool: Analyze sentiment, word count, summaries"
echo "• File Search Tool: Search for files in the system"
echo ""
echo "📚 Documentation:"
echo "================="
echo "• Integration Guide: CHATGPT_APPS_INTEGRATION.md"
echo "• OpenAI Apps SDK: https://developers.openai.com/apps-sdk/"
echo "• ChatGPT Apps Intro: https://openai.com/index/introducing-apps-in-chatgpt/"
echo ""
echo "🎉 Your GPT integration is ready for ChatGPT Apps!"
echo "   Follow the steps above to complete the integration."
