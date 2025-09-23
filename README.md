# 🤖 Unravel - Automated Ghost CMS Blog Generator

A comprehensive, intelligent content generation system that automatically researches, validates, and publishes engaging blog posts to Ghost CMS using Google Gemini 2.0 Flash AI.

## 🌟 Features

- **🔄 Dual Pipeline Architecture**: Main `automation.py` (614 lines) + Modular agent system
- **🤖 AI-Powered**: Google Gemini 2.0 Flash for content research, validation and writing  
- **� Smart Research**: Automatic trending topic discovery and content candidate sourcing
- **📊 Intelligent Validation**: AI-powered quality scoring and content assessment
- **🖼️ Rich Content**: HTML-formatted posts with embedded images and structured layouts
- **⏰ Automated Scheduling**: Cron-based automation every 5 hours via `setup-cron.sh`
- **� Rate Limiting**: Smart publishing limits (4 posts per run) for optimal quality
- **☁️ Railway Hosted**: Ghost CMS deployed on Railway for production hosting

## 📈 Current Status

- **Dual Automation Systems**: Both unified and modular pipelines available
- **614-line main pipeline** in `automation.py` 
- **Modular agent system** for granular control
- **Intelligent research phase** for fresh content discovery
- **HTML-based content** with structured formatting

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
# Create .env file with your API keys
cat > .env << EOF
GEMINI_API_KEY=your-gemini-api-key
GHOST_ADMIN_API_KEY=your-ghost-admin-key-id:secret
GHOST_URL=https://your-ghost-site.up.railway.app
EOF
```

### 3. Choose Your Pipeline

**Option A: Unified Pipeline (Recommended)**
```bash
# Single run
source .venv/bin/activate
python automation.py

# Setup automated cron job (every 5 hours)
chmod +x setup-cron.sh
./setup-cron.sh
```

**Option B: Modular Pipeline (Advanced)**
```bash
# Run full modular pipeline
python run_modular_automation.py

# Run individual phases
python run_modular_automation.py research
python run_modular_automation.py validation
python run_modular_automation.py writing
python run_modular_automation.py publishing
```

## 🛠️ Architecture

### Unified Pipeline (automation.py)
```
Research → Validation → Writing → Publishing → Logging
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Trend Mining│───▶│  AI Quality │───▶│ HTML Content│───▶│ Ghost CMS   │
│ & Discovery │    │ Validation  │    │ Generation  │    │ Publishing  │
│ (Multi-src) │    │(Gemini 2.0) │    │(Gemini 2.0) │    │ (Admin API) │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Modular Agent System (run_modular_automation.py)
```
ResearchAgent → ValidationAgent → WriterAgent → PublisherAgent
┌──────────────┐   ┌───────────────┐   ┌─────────────┐   ┌──────────────┐
│ • Google     │──▶│ • AI Scoring  │──▶│ • HTML Posts│──▶│ • Ghost API  │
│   Trends     │   │ • Quality     │   │ • Images    │   │ • Rate Limit │
│ • Tech News  │   │   Check       │   │ • Structure │   │ • Publishing │
│ • Topic Gen  │   │ • Relevance   │   │ • SEO Meta  │   │ • Tracking   │
└──────────────┘   └───────────────┘   └─────────────┘   └──────────────┘
```

## 📂 Project Structure

```
├── automation.py              # 🎯 Main unified pipeline (614 lines)
├── run_modular_automation.py  # 🔧 Modular agent orchestrator
├── setup-cron.sh             # ⏰ Cron job automation setup
├── AUTOMATION_README.md       # 📖 Detailed pipeline documentation
├── agents/                    # 🤖 Modular agent system
│   ├── validation_agent.py    # AI quality validation
│   └── writer_agent.py        # Content generation
├── data/                      # 💾 Database and generated content
│   ├── sqlite.db             # SQLite database
│   └── post_*.md             # Generated content files
├── logs/                      # 📝 Execution and cron logs
├── .env                       # 🔐 Environment variables
├── .venv/                     # 🐍 Python virtual environment
├── requirements.txt           # 📦 Python dependencies
└── railway-deploy.md          # 🚂 Railway deployment guide
```

## 🔧 Configuration

### Required API Keys

1. **Google Gemini API**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Ghost Admin API**: From your Ghost Admin → Integrations → Custom Integrations

### Environment Variables (.env)

```bash
# Google Gemini 2.0 Flash API
GEMINI_API_KEY=your-gemini-api-key

# Ghost CMS Configuration
GHOST_URL=https://your-ghost-site.up.railway.app
GHOST_ADMIN_API_KEY=id:secret-from-ghost-admin

# Optional: Google Search (for enhanced research)
GOOGLE_API_KEY=your-google-search-api-key
GOOGLE_CSE_ID=your-custom-search-engine-id
```

### Database Schema

The SQLite database (`data/sqlite.db`) contains:
- **candidates** table: Content ideas with validation scores
- **Columns**: id, title, url, snippet, validated, score, published, created_at

## 📊 Monitoring & Operations

### Manual Execution
```bash
# Unified pipeline
source .venv/bin/activate
python automation.py

# Modular pipeline
python run_modular_automation.py

# Individual agent phases
python run_modular_automation.py validation
```

### Check System Status
```bash
# View automation logs
tail -f logs/automation-*.log
tail -f logs/cron.log

# Check cron job status
crontab -l

# Database statistics
sqlite3 data/sqlite.db "SELECT COUNT(*) as total FROM candidates;"
sqlite3 data/sqlite.db "SELECT COUNT(*) as published FROM candidates WHERE published=1;"
```

### Cron Management
```bash
# Setup automation (every 5 hours)
./setup-cron.sh

# Remove automation
crontab -l | grep -v 'automation.py' | crontab -
```

## ⚙️ How It Works

### 1. Research Phase
- **Trend Discovery**: Scrapes Google Trends, tech news sources
- **Topic Generation**: AI-powered topic suggestion
- **Candidate Storage**: Stores potential content ideas in SQLite

### 2. Validation Phase  
- **AI Quality Check**: Gemini 2.0 Flash analyzes content relevance
- **Scoring System**: 1-100 score based on factual accuracy, relevance, quality
- **Smart Filtering**: Only high-quality candidates proceed

### 3. Content Generation
- **HTML Creation**: Structured HTML posts with proper formatting
- **Image Integration**: Automatic featured and inline image placement
- **SEO Optimization**: Meta descriptions, tags, and structured content

### 4. Publishing
- **Ghost API**: Direct publishing via Ghost Admin API
- **Rate Limiting**: Maximum 4 posts per run for quality control
- **Status Tracking**: Complete audit trail of published content

## 🖼️ Content Strategy

- **HTML Format**: Modern HTML structure for better Ghost compatibility
- **Featured Images**: Auto-generated tech-themed images via placeholder services  
- **Inline Images**: Strategic image placement within content sections
- **Structured Layout**: Consistent H1/H2 headings, paragraphs, and lists
- **SEO Ready**: Meta descriptions, tags, and semantic HTML structure
- **Theme Agnostic**: Works with all Ghost themes and custom designs

## 🔒 Security & Best Practices

- ✅ **Environment isolation**: Virtual environment and .env files
- ✅ **API key security**: No hardcoded credentials, gitignore protection
- ✅ **Rate limiting**: Respectful API usage with built-in delays
- ✅ **Error handling**: Comprehensive exception handling and logging
- ✅ **Audit trail**: Complete logging of all pipeline operations
- ✅ **Database integrity**: SQLite with proper transaction handling

## 📈 Performance & Statistics

```
🤖 AUTOMATION STATUS
   Pipeline Type: Dual (Unified + Modular)
   Main File Size: 614 lines (automation.py)
   Execution Frequency: Every 5 hours
   Rate Limiting: 4 posts per run
   
🧠 AI CAPABILITIES  
   Model: Google Gemini 2.0 Flash
   Research: Multi-source trending topics
   Validation: Quality scoring (1-100)
   Content: HTML with embedded images
   
🏗️ TECH STACK
   Language: Python 3.11+
   Database: SQLite with audit trail
   CMS: Ghost (Railway hosted)
   Scheduling: Unix cron
   Architecture: Agent-based pipeline
   
📊 PIPELINE METRICS
   Research Sources: Google Trends + Tech News
   Validation Pass Rate: AI-determined
   Content Format: Structured HTML
   Publishing Success: Ghost Admin API
```

## � Production Ready Features

- **🔄 Dual Architecture**: Choose between unified or modular pipeline
- **🤖 Advanced AI**: Gemini 2.0 Flash for superior content quality
- **📈 Smart Research**: Multi-source trending topic discovery
- **🎨 Rich Content**: HTML formatting with embedded images
- **⚡ Production Hosting**: Railway deployment with custom domains
- **📊 Comprehensive Logging**: Full audit trail and error tracking
- **🔧 Easy Setup**: One-command cron automation

## 🎉 Ready to Deploy!

Your automated blog system is **production-ready and highly configurable**. Choose your preferred pipeline, set up cron automation, and watch high-quality content appear on your Ghost blog every 5 hours!

For detailed setup and configuration, see:
- `AUTOMATION_README.md` - Complete pipeline documentation
- `railway-deploy.md` - Railway hosting setup guide
