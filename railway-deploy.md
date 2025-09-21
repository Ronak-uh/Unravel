# Railway Deployment
Railway is the easiest way to deploy your Ghost blog. Here's how:

## 1. Quick Railway Deployment

### Install Railway CLI:
```bash
npm install -g @railway/cli
```

### Deploy:
```bash
# Login to Railway
railway login

# Initialize project
railway init

# Deploy your Ghost blog
railway up
```

## 2. Alternative: Deploy Button

You can also deploy directly from GitHub using Railway's deploy button.

## 3. Environment Variables

After deployment, set these environment variables in Railway dashboard:

- `GHOST_URL`: Your Railway app URL (e.g., https://your-app.railway.app)
- `NODE_ENV`: production
- `GEMINI_API_KEY`: Your Google Gemini API key
- `GOOGLE_API_KEY`: Your Google Custom Search API key
- `GOOGLE_CX`: Your Google Custom Search Engine ID

## 4. Automatic Updates

Your Ghost content and categories will be deployed automatically. The blog will be live with all your categorized posts!

**🤖 AUTOMATED CONTENT GENERATION:**
- New posts every 5 hours automatically
- GitHub Actions will handle the automation
- Expected: 48-96 new categorized posts per day

## 5. Custom Domain (Optional)

In Railway dashboard:
1. Go to your project
2. Click "Settings" 
3. Add your custom domain
4. Update `GHOST_URL` environment variable

Your Ghost blog with categories (World, Finance, Technology, Health, Business) will be live!