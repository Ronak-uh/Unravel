# 🤖 Automated Ghost CMS Blog Generator

An intelligent content generation system that automatically creates, validates, and publishes categorized blog posts to Ghost CMS every 5 hours using AI.

## 🌟 Features

- **🔄 Automated Content Pipeline**: Research → Validate → Write → Publish
- **🏷️ Smart Categorization**: Auto-assigns posts to World, Finance, Technology, Health, Business categories
- **🤖 AI-Powered**: Uses Google Gemini for content validation and writing
- **🖼️ Image Integration**: Automatic image search and upload to Ghost CMS
- **📊 Monitoring Dashboard**: Real-time stats and automation monitoring
- **☁️ Cloud Ready**: Deploy to Railway, Heroku, DigitalOcean with one command

## 📈 Performance

- **68 Published Posts** with categories already generated
- **2-4 new posts** every 5 hours
- **48-96 posts per day** potential output
- **6 categories** for organized content

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/automated-ghost-blog.git
cd automated-ghost-blog

# Install dependencies
pip install -r requirements.txt
npm install
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your API keys:
# - GEMINI_API_KEY
# - GOOGLE_API_KEY  
# - GOOGLE_CX
# - GHOST_ADMIN_API_KEY
```

### 3. Deploy (Choose One)

**Option A: Railway (Easiest)**
```bash
./deploy-railway.sh
```

**Option B: Docker Compose**
```bash
docker-compose -f docker-compose.prod.yml up
```

**Option C: Manual VPS**
```bash
./setup-cron.sh  # Sets up 5-hour automation
python monitor.py  # View dashboard
```

## 🛠️ Architecture

```
Research Agent → Validation Agent → Writer Agent → Publisher Agent
     ↓              ↓                ↓               ↓
  Find Topics   Validate Quality  Create Articles  Publish to Ghost
     ↓              ↓                ↓               ↓
  Google API    Gemini AI API    Gemini AI API   Ghost Admin API
```

## 📂 Project Structure

```
├── agents/                 # AI agents for content pipeline
│   ├── research_agent.py   # Finds trending topics
│   ├── validation_agent.py # Validates content quality
│   ├── writer_agent.py     # Creates markdown articles
│   └── publisher_agent.py  # Publishes to Ghost CMS
├── docker/                 # Docker configuration
│   ├── docker-compose.yml  # Development setup
│   └── ghost_content/      # Ghost CMS data
├── .github/workflows/      # GitHub Actions automation
├── data/                   # SQLite database and generated posts
├── logs/                   # Automation logs
├── auto-pipeline.sh        # Main automation script
├── monitor.py             # Monitoring dashboard
└── deploy-railway.sh      # One-click deployment
```

## 🔧 Configuration

### Required API Keys

1. **Google Gemini API**: For content validation and writing
2. **Google Custom Search API**: For topic research and images
3. **Ghost Admin API**: For publishing posts

### Environment Variables

```bash
# Ghost CMS
GHOST_URL=https://your-domain.com
GHOST_ADMIN_API_KEY=your-ghost-admin-key
GHOST_API_URL=https://your-domain.com/ghost/api/admin

# Google APIs
GEMINI_API_KEY=your-gemini-key
GOOGLE_API_KEY=your-google-key
GOOGLE_CX=your-search-engine-id

# Optional: Email notifications
MAIL_SERVICE=Gmail
MAIL_USER=your-email@gmail.com
MAIL_PASS=your-app-password
```

## 📊 Monitoring

### Dashboard
```bash
python monitor.py
```

### Live Logs
```bash
tail -f logs/auto-pipeline-*.log
```

### Manual Run
```bash
./auto-pipeline.sh
```

## 🕐 Automation Schedule

- **Every 5 Hours**: 00:00, 05:00, 10:00, 15:00, 20:00
- **GitHub Actions**: Automatic on cloud platforms
- **Cron Jobs**: For VPS/server deployments

## 📱 Deployment Platforms

| Platform | Cost | Setup Time | Features |
|----------|------|------------|----------|
| Railway | Free/$5 | 5 minutes | Auto HTTPS, Custom domains |
| DigitalOcean | $5-12 | 10 minutes | Scalable, Monitoring |
| Heroku | $7+ | 5 minutes | Easy deploy, Add-ons |
| VPS | $5-10 | 30 minutes | Full control, SSH access |

## 🏷️ Categories

Content is automatically categorized into:

- **World** (5 posts) - Global news and events
- **Finance** (8 posts) - Financial markets, stocks, crypto
- **Technology** (20 posts) - Tech trends, AI, innovation
- **Health** (5 posts) - Medical breakthroughs, wellness
- **Business** (4 posts) - Business trends, productivity
- **General** (26+ posts) - Uncategorized content

## 🔒 Security

- ✅ Environment variables for API keys
- ✅ `.gitignore` excludes sensitive data
- ✅ No hardcoded credentials
- ✅ SSL/HTTPS ready configurations

## 📈 Performance Stats

```
📊 DATABASE STATISTICS
   Total Candidates: 100
   Validated: 73
   Published: 68
   Ready to Publish: 5

📂 PUBLISHED POSTS BY CATEGORY
   Technology: 20 posts
   General: 26 posts
   Finance: 8 posts
   Health: 5 posts
   World: 5 posts
   Business: 4 posts
```

*Generate fresh, categorized content for your Ghost blog every 5 hours automatically!*
