# 🚀 Deploy to Railway - Bypass CSP Restrictions

## Why Railway?
- ✅ **Trusted Domain**: Railway domains are in ChatGPT's CSP allowlist
- ✅ **Free Tier**: 500 hours/month free
- ✅ **Easy Setup**: Connect GitHub repo and auto-deploy
- ✅ **HTTPS**: Automatic SSL certificates
- ✅ **Custom Domains**: Optional custom domain support

## Step 1: Prepare for Deployment

### 1.1 Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (recommended)
3. Verify your email

### 1.2 Prepare Your Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

## Step 2: Deploy to Railway

### 2.1 Create New Project
1. Go to [railway.app/dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `gptintegration` repository
5. Click **"Deploy Now"**

### 2.2 Configure Environment
Railway will automatically detect your Python app and use the `requirements.txt` file.

### 2.3 Set Environment Variables (if needed)
In Railway dashboard:
1. Go to your project
2. Click on the service
3. Go to **"Variables"** tab
4. Add any environment variables from your `.env` file

## Step 3: Get Your Railway URL

### 3.1 Find Your URL
1. In Railway dashboard, click on your deployed service
2. Go to **"Settings"** tab
3. Copy the **"Domain"** URL (e.g., `https://your-app-name-production.up.railway.app`)

### 3.2 Test Your Deployment
```bash
# Test health endpoint
curl https://your-app-name-production.up.railway.app/health

# Test MCP tools endpoint
curl https://your-app-name-production.up.railway.app/mcp/tools

# Test a tool
curl -X POST https://your-app-name-production.up.railway.app/tools/calculator \
  -H "Content-Type: application/json" \
  -d '{"expression": "10 + 5"}'
```

## Step 4: Integrate with ChatGPT

### 4.1 Create ChatGPT Connector
1. Go to ChatGPT Settings → Connectors
2. Click **"Create Connector"**
3. Fill in:
   - **Name**: `GPT Integration Tools`
   - **Description**: `Weather, calculator, text analysis, and file search tools`
   - **Connector URL**: `https://your-app-name-production.up.railway.app/mcp`
4. Click **"Create"**

### 4.2 Test in ChatGPT
1. Open a new ChatGPT conversation
2. Enable Developer mode (if available)
3. Toggle on your connector
4. Test with prompts:
   - `"Use the GPT Integration Tools connector to get the weather in New York"`
   - `"Use the calculator tool to calculate 15 * 23 + 45"`

## Step 5: Optional - Custom Domain

### 5.1 Add Custom Domain
1. In Railway dashboard, go to **"Settings"**
2. Scroll to **"Domains"**
3. Click **"Custom Domain"**
4. Add your domain (e.g., `gpt-tools.yourdomain.com`)
5. Follow DNS configuration instructions

## Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check `requirements.txt` is correct
   - Ensure all dependencies are listed
   - Check Railway build logs

2. **App Crashes**
   - Check Railway logs in dashboard
   - Verify `run.py` works locally
   - Check environment variables

3. **CORS Issues**
   - Railway handles CORS automatically
   - If issues persist, check FastAPI CORS settings

4. **Health Check Fails**
   - Ensure `/health` endpoint returns 200
   - Check Railway health check settings

## Railway vs Heroku

| Feature | Railway | Heroku |
|---------|---------|---------|
| Free Tier | 500 hours/month | 550 hours/month |
| Setup | GitHub integration | Git push |
| Custom Domains | ✅ Free | ✅ Paid |
| SSL | ✅ Automatic | ✅ Automatic |
| Database | ✅ PostgreSQL | ✅ PostgreSQL |
| Monitoring | ✅ Built-in | ✅ Add-ons |

## Next Steps

1. **Deploy to Railway** using the steps above
2. **Test your deployment** with the provided curl commands
3. **Create ChatGPT connector** with your Railway URL
4. **Test integration** in ChatGPT conversations

Your GPT integration will be live and accessible to ChatGPT! 🎉
