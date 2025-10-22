# ChatGPT Apps Integration Guide

## 🎯 Official ChatGPT Apps Integration

This guide will help you integrate your GPT server with the official ChatGPT Apps platform announced by OpenAI.

## 📋 Prerequisites

✅ **Your server is ready**: Running on `http://localhost:8000`  
✅ **All tools working**: Weather, Calculator, Text Analysis, File Search  
✅ **MCP compliant**: Following Model Context Protocol standards  
✅ **HTTPS ready**: Need public URL for ChatGPT integration  

## 🚀 Step 1: Expose Your Server Publicly

### Option A: Using ngrok (Recommended for testing)

1. **Sign up for ngrok** (free): https://dashboard.ngrok.com/signup
2. **Get your authtoken**: https://dashboard.ngrok.com/get-started/your-authtoken
3. **Configure ngrok**:
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
   ```
4. **Expose your server**:
   ```bash
   ngrok http 8000
   ```
5. **Copy the public URL** (e.g., `https://abc123.ngrok.io`)

### Option B: Deploy to Cloud Platform

Deploy your server to:
- **Heroku**: Use the provided configuration
- **Railway**: Deploy from GitHub
- **DigitalOcean App Platform**: Use Python buildpack
- **AWS/GCP/Azure**: Use container services

## 🔗 Step 2: Enable Developer Mode in ChatGPT

### For ChatGPT Enterprise Users:
1. **Contact your OpenAI partner** to request access to the connectors developer experiment
2. **Have your workspace admin** enable connector creation for your account
3. **In ChatGPT**: Go to Settings → Connectors → Advanced
4. **Toggle on Developer mode**

### For Regular ChatGPT Users:
- Developer mode access is currently limited to enterprise users
- Monitor OpenAI announcements for broader access

## 🛠️ Step 3: Create Your Connector

1. **In ChatGPT**: Go to Settings → Connectors → Create
2. **Fill in the metadata**:
   - **Connector Name**: "GPT Integration Tools"
   - **Description**: "A comprehensive set of tools including weather, calculator, text analysis, and file search capabilities"
   - **Connector URL**: `https://your-ngrok-url.ngrok.io/mcp`
3. **Click "Create"** to establish the connection

## 🧪 Step 4: Test Your Integration

1. **Open a new chat** in ChatGPT
2. **Click the "+" button** near the message composer
3. **Select Developer mode**
4. **Toggle on your connector** from the list of available tools
5. **Test with prompts** like:
   - "Use the GPT Integration Tools connector to get the weather in New York"
   - "Use the calculator tool to calculate 15 * 23 + 45"
   - "Use the text analysis tool to analyze the sentiment of 'I love this new feature!'"
   - "Use the file search tool to find files containing 'report'"

## 📊 Your Server Endpoints

### Main MCP Endpoint
- **URL**: `https://your-url.com/mcp`
- **Purpose**: Main entry point for ChatGPT Apps
- **Response**: App metadata and available endpoints

### Tools Manifest
- **URL**: `https://your-url.com/mcp/tools`
- **Purpose**: Lists all available tools
- **Response**: Tool definitions and schemas

### Individual Tools
- **Weather**: `POST https://your-url.com/tools/weather`
- **Calculator**: `POST https://your-url.com/tools/calculator`
- **Text Analysis**: `POST https://your-url.com/tools/text-analysis`
- **File Search**: `POST https://your-url.com/tools/file-search`

### Health Check
- **URL**: `https://your-url.com/health`
- **Purpose**: Server status monitoring

## 🎨 UI Components

Your server includes beautiful UI components for each tool:
- `weather-widget.html` - Weather display with icons
- `calculator-widget.html` - Calculator with results
- `text-analysis-widget.html` - Text analysis results
- `file-search-widget.html` - File search results

## 🔧 Testing Commands

### Test MCP Endpoint
```bash
curl https://your-ngrok-url.ngrok.io/mcp
```

### Test Tools Manifest
```bash
curl https://your-ngrok-url.ngrok.io/mcp/tools
```

### Test a Tool
```bash
curl -X POST https://your-ngrok-url.ngrok.io/tools/calculator \
  -H "Content-Type: application/json" \
  -d '{"expression": "2 + 2"}'
```

### Test Health
```bash
curl https://your-ngrok-url.ngrok.io/health
```

## 📱 Web Interface

Your server includes a beautiful web interface for testing:
- **Local**: `http://localhost:8000`
- **Public**: `https://your-ngrok-url.ngrok.io`

## 🚀 Step 5: Prepare for App Store Submission

### App Design Guidelines
- Review OpenAI's [App Design Guidelines](https://developers.openai.com/apps-sdk/concepts/design-guidelines/)
- Ensure your app meets quality and safety standards
- Follow best practices for user experience

### Submission Process
- App submissions for the ChatGPT app directory will open later this year
- Stay updated on OpenAI announcements
- Prepare your app for monetization opportunities

## 🔍 Troubleshooting

### Common Issues

1. **"Connector not found"**
   - Ensure your server is publicly accessible via HTTPS
   - Check that the `/mcp` endpoint returns valid JSON
   - Verify the URL in your connector settings

2. **"Tools not working"**
   - Test individual tool endpoints directly
   - Check server logs for errors
   - Verify CORS configuration

3. **"Developer mode not available"**
   - Ensure you have enterprise access
   - Contact your OpenAI partner for access
   - Check if your workspace admin has enabled connector creation

### Debug Commands

```bash
# Check if server is running
curl http://localhost:8000/health

# Test MCP endpoint
curl http://localhost:8000/mcp

# Test tools manifest
curl http://localhost:8000/mcp/tools

# Test a specific tool
curl -X POST http://localhost:8000/tools/calculator \
  -H "Content-Type: application/json" \
  -d '{"expression": "1 + 1"}'
```

## 📞 Support Resources

- **OpenAI Apps SDK Documentation**: https://developers.openai.com/apps-sdk/
- **App Design Guidelines**: https://developers.openai.com/apps-sdk/concepts/design-guidelines/
- **ChatGPT Apps Introduction**: https://openai.com/index/introducing-apps-in-chatgpt/
- **Help Center**: https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk

## 🎉 Success Checklist

- ✅ Server running and accessible
- ✅ Public HTTPS URL available
- ✅ MCP endpoint responding correctly
- ✅ All tools working via API
- ✅ Developer mode enabled in ChatGPT
- ✅ Connector created successfully
- ✅ Tools responding in ChatGPT
- ✅ Ready for app store submission

Your GPT integration is now ready for the official ChatGPT Apps platform!
