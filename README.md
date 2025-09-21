# 🤖 Unravel - Automated Ghost CMS Blog Generator

A unified, intelligent content generation system that automatically creates, validates, and publishes engaging blog posts to Ghost CMS every 5 hours using Google Gemini AI.

## 🌟 Features

- **🔄 Unified Automation**: Single `automation.py` file handles complete pipeline
- **🤖 AI-Powered**: Google Gemini 1.5 Flash for content validation and writing  
- **🖼️ Embedded Images**: Automatic image generation within post content
- **⏰ Cron Automation**: Runs every 5 hours automatically via `run_automation.sh`
- **📊 Smart Publishing**: Limits to 4 posts per run to maintain quality
- **☁️ Railway Hosted**: Ghost CMS deployed on Railway for free hosting

## 📈 Performance

- **100 Candidates** in database (all validated and published)
- **4 posts per run** with smart rate limiting
- **Every 5 hours** automated publishing  
- **Embedded images** for reliable display across all Ghost themes

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/Ronak-uh/Unravel.git
cd Unravel

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your API keys:
# - GEMINI_API_KEY=your-gemini-api-key
# - GHOST_ADMIN_API_KEY=your-ghost-admin-key  
# - GHOST_URL=https://your-ghost-site.up.railway.app
```

### 3. Run Automation

**Manual Single Run:**
```bash
source .venv/bin/activate
python automation.py
```

**5-Hour Automated Run:**
```bash
chmod +x run_automation.sh
(crontab -l 2>/dev/null; echo "0 */5 * * * /path/to/Unravel/run_automation.sh") | crontab -
```

## 🛠️ Architecture

```
Unified automation.py Pipeline:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Validate   │───▶│    Write    │───▶│   Publish   │───▶│   Logging   │
│  Content    │    │   Article   │    │  to Ghost   │    │   System    │
│ (Gemini AI) │    │ (Gemini AI) │    │ (Ghost API) │    │ (File logs) │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 📂 Project Structure (Simplified)

```
├── automation.py           # 🎯 Main automation pipeline (755 lines)
├── run_automation.sh       # ⏰ Cron job wrapper script
├── AUTOMATION_README.md    # 📖 Complete documentation
├── data/                   # 💾 SQLite database and generated posts
│   ├── sqlite.db          # Database with 100 candidates
│   └── post_*.md          # Generated markdown files
├── logs/                   # 📝 Automation execution logs
├── .env                    # 🔐 Environment variables
├── .venv/                  # 🐍 Python virtual environment
└── requirements.txt        # 📦 Python dependencies
```

## 🔧 Configuration

### Required API Keys

1. **Google Gemini API**: For content validation and writing
2. **Ghost Admin API**: For publishing posts to your Ghost CMS

### Environment Variables

```bash
# Ghost CMS (Railway hosted)
GHOST_URL=https://your-ghost-site.up.railway.app
GHOST_ADMIN_API_KEY=your-ghost-admin-key

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key
```

## 📊 Monitoring

### Manual Run with Output
```bash
source .venv/bin/activate
python automation.py
```

### Check Automation Logs
```bash
tail -f logs/automation-*.log
```

### Check Cron Job Status
```bash
crontab -l  # View active cron jobs
```

## � How It Works

1. **Validation**: Checks candidate topics using Gemini AI for quality
2. **Content Writing**: Creates engaging articles with embedded images
3. **Publishing**: Publishes to Ghost CMS using mobiledoc format
4. **Rate Limiting**: Publishes maximum 4 posts per run
5. **Logging**: Tracks all operations with timestamps

## 🖼️ Image Strategy

- **Embedded Images**: Uses `![Alt Text](image-url)` format in content
- **Placeholder Service**: Generates tech-themed images via via.placeholder.com
- **Theme Compatible**: Works with all Ghost themes (no featured image dependency)

## 🔒 Security

- ✅ Environment variables for API keys
- ✅ `.gitignore` excludes sensitive data  
- ✅ Virtual environment isolation
- ✅ No hardcoded credentials

## 📈 Performance Stats

```
📊 DATABASE STATUS
   Total Candidates: 100
   All Validated: ✅
   All Published: ✅
   Ready for Fresh Content: ✅

🤖 AUTOMATION FEATURES
   Unified Pipeline: automation.py (755 lines)
   Cron Automation: Every 5 hours
   Rate Limiting: 4 posts per run
   Image Strategy: Embedded in content
   
🏗️ TECH STACK
   Language: Python 3.13.7
   AI: Google Gemini 1.5 Flash
   CMS: Ghost (Railway hosted)
   Database: SQLite
   Scheduling: Unix cron
```

## 🎉 Ready to Use!

Your automated blog is now **simplified, production-ready, and maintenance-free**. Just set up the cron job and watch fresh content appear on your Ghost blog every 5 hours!

For detailed setup instructions, see `AUTOMATION_README.md`.
