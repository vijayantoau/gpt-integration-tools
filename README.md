# GPT Integration Tools

A comprehensive MCP (Model Context Protocol) server providing weather, calculator, text analysis, and file search tools for ChatGPT and Cursor integration.

## 🚀 Live Deployment

**Vercel URL**: `https://gptintegration-osno2ng5z-vijays-projects-83d7f1fb.vercel.app`

## 🛠️ Available Tools

1. **Weather** - Get current weather information for any location
2. **Calculator** - Perform mathematical calculations
3. **Text Analysis** - Analyze text for sentiment, word count, or summary
4. **File Search** - Search for files in the system

## 📁 Project Structure

```
gptintegration/
├── app.py                    # Main FastAPI MCP server (Vercel deployment)
├── mcp_server_stdio.py       # Local MCP server for Cursor
├── mcp_proxy_server.py       # Proxy server (Cursor → Vercel)
├── app_manifest.json         # ChatGPT Apps manifest
├── vercel.json              # Vercel deployment config
├── requirements.txt         # Python dependencies
├── components/              # UI components
│   ├── weather-widget.html
│   ├── calculator-widget.html
│   ├── text-analysis-widget.html
│   └── file-search-widget.html
├── tests/                   # Test files
│   ├── debug_tool_calls.py
│   ├── chatgpt_sdk_example.py
│   ├── simple_tool_test.py
│   └── test_chatgpt_sdk.py
└── docs/                    # Documentation
    ├── CHATGPT_INTEGRATION.md
    ├── DEPLOY_INSTRUCTIONS.md
    └── TROUBLESHOOTING.md
```

## 🔧 Integration Methods

### ChatGPT Integration
- **URL**: `https://gptintegration-osno2ng5z-vijays-projects-83d7f1fb.vercel.app`
- **Protocol**: MCP (Model Context Protocol)
- **Method**: HTTP/JSON-RPC 2.0

### Cursor Integration
- **Local Server**: `mcp_server_stdio.py` (stdio transport)
- **Proxy Option**: `mcp_proxy_server.py` (forwards to Vercel)
- **Config**: `~/.cursor/mcp.json`

## 🧪 Testing

### Quick Test
```bash
python3 simple_tool_test.py
```

### Full Debug (requires OpenAI API key)
```bash
export OPENAI_API_KEY='your-key-here'
python3 debug_tool_calls.py
```

### Direct MCP Test
```bash
curl -X POST https://gptintegration-osno2ng5z-vijays-projects-83d7f1fb.vercel.app/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "weather", "arguments": {"location": "New York"}}}'
```

## 🚀 Deployment

### Vercel (Current)
```bash
vercel --prod
```

### Local Development
```bash
python3 run.py
```

## 📋 Endpoints

- **MCP**: `/mcp` - Main MCP protocol endpoint
- **Health**: `/health` - Health check
- **Manifest**: `/manifest` - App manifest
- **Validation**: `/mcp/validate` - Connector validation
- **Tools**: `/mcp/tools` - Tools list
- **Web UI**: `/` - Web interface

## 🔍 Architecture

The system supports multiple integration patterns:

1. **Direct HTTP**: ChatGPT → Vercel MCP Server
2. **Local Stdio**: Cursor → Local MCP Server
3. **Proxy**: Cursor → Proxy Server → Vercel MCP Server

## 📝 License

MIT License