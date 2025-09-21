# Vercel Deployment Guide for Unravel

## 🚀 Quick Deploy to Vercel

### Prerequisites
1. GitHub repository with the Unravel project
2. Vercel account (free tier works)
3. Required API keys

### Step 1: Connect GitHub to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Import your `Unravel` repository

### Step 2: Configure Environment Variables
In Vercel dashboard, add these environment variables:

| Variable Name | Description | Example |
|---------------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSyC...` |
| `GOOGLE_API_KEY` | Google Custom Search API key | `AIzaSyD...` |
| `GOOGLE_CSE_ID` | Custom Search Engine ID | `017576662512468239146:omuauf_lfve` |
| `GHOST_ADMIN_API_KEY` | Ghost Admin API key | `507f1f77bcf86cd799439011:4b0b1b0b...` |
| `GHOST_URL` | Your Ghost blog URL | `https://yourblog.ghost.io` |

### Step 3: Deploy
1. Click "Deploy"
2. Vercel will automatically:
   - Install Node.js dependencies
   - Install Python dependencies
   - Build the project
   - Deploy to a public URL

## 📋 Project Structure for Vercel

```
/
├── index.js              # Main Node.js server
├── package.json          # Node.js dependencies
├── requirements.txt      # Python dependencies  
├── vercel.json          # Vercel configuration
├── api/                 # Serverless functions
│   ├── pipeline.py      # Main automation pipeline
│   └── research.py      # Research agent endpoint
├── agents/              # Python automation agents
└── data/               # Data storage (generated)
```

## 🔧 Available Endpoints

After deployment, your Vercel app will have:

- **`/`** - Status page with API information
- **`/api/status`** - Health check endpoint
- **`/api/pipeline`** - Run the complete content pipeline
- **`/api/research`** - Run research to find new topics

## 🤖 Automation Features

### Manual Triggers
- Visit `/api/pipeline` to manually run content generation
- Visit `/api/research` to find new content topics

### Scheduled Automation
The GitHub Actions workflow will continue to run every 5 hours and can trigger the Vercel endpoints.

## 🛠️ Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all environment variables are set
   - Verify API keys are correct format
   - Check Vercel build logs

2. **Python Dependencies**
   - Ensure `requirements.txt` is in root directory
   - Vercel supports Python 3.9 by default

3. **API Errors**
   - Check environment variables in Vercel dashboard
   - Verify Ghost URL is accessible
   - Test API keys individually

### Logs and Monitoring
- View logs in Vercel dashboard → Functions tab
- Monitor API calls in Vercel analytics
- Check GitHub Actions for scheduled runs

## 🔄 Continuous Deployment

Once connected:
1. Push changes to GitHub
2. Vercel automatically rebuilds and deploys
3. New features go live immediately

## 📊 Performance Optimization

- Serverless functions have cold start latency
- First request may be slower (~2-3 seconds)
- Subsequent requests are faster
- Consider upgrading to Vercel Pro for better performance

## 🔐 Security

- Environment variables are encrypted in Vercel
- API endpoints are public by default
- Consider adding authentication for production use
- Rate limiting can be added for heavy usage

## 💰 Cost Considerations

**Vercel Free Tier Includes:**
- 100GB bandwidth
- 100 deployments/month  
- Serverless function executions
- Custom domains

**Upgrade triggers:**
- High traffic blogs
- Frequent automation runs
- Multiple team members