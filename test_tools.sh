#!/bin/bash

# Test script for GPT Integration Tools
BASE_URL="https://gptintegration-4l8whbu5h-vijays-projects-83d7f1fb.vercel.app"

echo "🧪 Testing GPT Integration Tools"
echo "================================="

# Test 1: Weather Tool
echo "🌤️  Testing Weather Tool..."
curl -s -X POST $BASE_URL/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "weather", "arguments": {"location": "Tokyo", "units": "celsius"}}}' | jq -r '.result.content[0].text'

echo -e "\n"

# Test 2: Calculator Tool
echo "🧮 Testing Calculator Tool..."
curl -s -X POST $BASE_URL/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "calculator", "arguments": {"expression": "15 * 8 - 20"}}}' | jq -r '.result.content[0].text'

echo -e "\n"

# Test 3: Text Analysis Tool (Sentiment)
echo "📝 Testing Text Analysis Tool (Sentiment)..."
curl -s -X POST $BASE_URL/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "text_analysis", "arguments": {"text": "This is terrible and awful!", "analysis_type": "sentiment"}}}' | jq -r '.result.content[0].text'

echo -e "\n"

# Test 4: Text Analysis Tool (Word Count)
echo "📊 Testing Text Analysis Tool (Word Count)..."
curl -s -X POST $BASE_URL/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "text_analysis", "arguments": {"text": "This is a test message with multiple words", "analysis_type": "word_count"}}}' | jq -r '.result.content[0].text'

echo -e "\n"

# Test 5: File Search Tool
echo "🔍 Testing File Search Tool..."
curl -s -X POST $BASE_URL/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "file_search", "arguments": {"query": "report", "file_type": "pdf"}}}' | jq -r '.result.content[0].text'

echo -e "\n"
echo "✅ All tests completed!"


