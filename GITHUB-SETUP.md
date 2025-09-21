# 📋 GitHub Setup Instructions

## 🔐 Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and log in
2. Click the "+" icon → "New repository"
3. Repository name: `automated-ghost-blog` (or your preferred name)
4. Description: `🤖 Automated Ghost CMS Blog Generator with AI-powered content pipeline`
5. Set to **Public** (for free GitHub Actions) or **Private** (if you have Pro)
6. **Don't** initialize with README (we already have one)
7. Click "Create repository"

## 🚀 Step 2: Push Your Code

After creating the repository, run these commands:

```bash
# Add your GitHub repository as origin (replace with your username/repo)
git remote add origin https://github.com/YOUR-USERNAME/automated-ghost-blog.git

# Push to GitHub
git push -u origin main
```

## 🔑 Step 3: Set Up GitHub Secrets (for automation)

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these repository secrets:

```
GEMINI_API_KEY=your-gemini-api-key
GOOGLE_API_KEY=your-google-api-key  
GOOGLE_CX=your-search-engine-id
GHOST_ADMIN_API_KEY=your-ghost-admin-key
GHOST_API_URL=https://your-domain.com/ghost/api/admin
```

## ⚡ Step 4: Enable GitHub Actions

1. Go to your repository → Actions tab
2. Click "I understand my workflows and want to enable them"
3. The automation will start running every 5 hours automatically!

## 🎯 Step 5: Deploy Your Blog

Choose your deployment method:

### Option A: Railway (Recommended)
```bash
./deploy-railway.sh
```

### Option B: One-Click Deploy to Railway
Add this button to your README by clicking:
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template)

### Option C: Other Platforms
- **Heroku**: Use `Dockerfile` 
- **DigitalOcean**: Use `docker-compose.prod.yml`
- **VPS**: Use `setup-cron.sh`

## 📊 Step 6: Monitor Automation

After deployment, you can monitor your automation:

- **GitHub Actions**: Check the Actions tab in your repository
- **Live Dashboard**: Run `python monitor.py` in your deployed environment
- **Logs**: Check `logs/` directory for automation logs

## 🔄 What Happens Next

Once set up:

1. **Every 5 hours** GitHub Actions will run the content pipeline
2. **New posts** will be automatically researched, validated, written, and published
3. **Categories** (World, Finance, Technology, Health, Business) will be assigned automatically
4. **Your Ghost blog** will grow with fresh content continuously!

## ⚠️ Important Notes

- Make sure your Ghost CMS is accessible from the internet
- Verify all API keys are correctly set in GitHub Secrets
- The automation needs your Ghost admin API key to publish posts
- Check the Actions tab if automation fails

**Your automated Ghost blog is ready to go live! 🚀**