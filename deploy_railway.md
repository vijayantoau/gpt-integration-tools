# Deploy to Railway (Recommended)

Railway is a great platform for deploying your GPT integration server.

## 🚀 Quick Deploy Steps:

### 1. **Prepare for Deployment**
```bash
# Make sure your server is working locally
curl http://localhost:8000/health
```

### 2. **Deploy to Railway**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select your repository
6. Railway will automatically detect it's a Python app
7. Deploy!

### 3. **Environment Variables**
Add these in Railway dashboard:
- `HOST=0.0.0.0`
- `PORT=8000`
- `DEBUG=False`

### 4. **Get Your Public URL**
Railway will give you a URL like: `https://your-app-name.railway.app`

### 5. **Test Your Deployment**
```bash
# Test health
curl https://your-app-name.railway.app/health

# Test MCP tools
curl https://your-app-name.railway.app/mcp/tools

# Test a tool
curl -X POST https://your-app-name.railway.app/tools/calculator \
  -H "Content-Type: application/json" \
  -d '{"expression": "2 + 2"}'
```

### 6. **Use in ChatGPT**
- **Connector URL**: `https://your-app-name.railway.app/mcp`
- **Name**: "GPT Integration Tools"
- **Description**: "Weather, calculator, text analysis, and file search tools"
