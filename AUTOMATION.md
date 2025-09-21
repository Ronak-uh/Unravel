# Unravel Automation Guide

This guide explains how to set up automatic content generation every 5 hours using different methods.

## 🚀 Quick Start

### Option 1: Local Automation (Cron Job)
```bash
# Set up cron job to run every 5 hours
./setup-cron.sh
```

### Option 2: Cloud Automation (GitHub Actions)
1. Add these secrets to your GitHub repository:
   - `GEMINI_API_KEY`
   - `GOOGLE_API_KEY` 
   - `GOOGLE_CSE_ID`
   - `GHOST_ADMIN_API_KEY`
   - `GHOST_URL`

2. Push the workflow file (already included in `.github/workflows/auto-content.yml`)

## 📋 Prerequisites

### Required Environment Variables
Create a `.env` file with:
```
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
GHOST_ADMIN_API_KEY=id:secret_from_ghost
GHOST_URL=http://localhost:2368
```

### Dependencies
```bash
pip install -r requirements.txt
```

## 🔧 Available Scripts

### 1. `setup-cron.sh` - Local Cron Setup
- Sets up a cron job to run every 5 hours
- Logs output to `logs/cron.log`
- Automatically handles existing cron jobs

**Usage:**
```bash
./setup-cron.sh
```

**Schedule:** Runs at 00:00, 05:00, 10:00, 15:00, 20:00 daily

### 2. `auto-pipeline.sh` - Pipeline Runner
- Complete pipeline with error handling
- Logs all activities
- Includes dependency management
- Cleanup of old files

**Manual run:**
```bash
./auto-pipeline.sh
```

### 3. GitHub Actions Workflow
- Runs in the cloud every 5 hours
- No local setup required
- Automatically commits generated content
- Uses GitHub secrets for API keys

## 📊 Monitoring

### Log Files
- **Cron logs:** `logs/cron.log`
- **Pipeline logs:** `logs/pipeline.log`

### Manual Commands
```bash
# Check cron jobs
crontab -l

# View recent logs
tail -f logs/pipeline.log

# Run pipeline manually
python run_pipeline.py

# Run individual agents
python agents/research_agent.py
python agents/validation_agent.py
python agents/writer_agent.py
python agents/publisher_agent.py
```

## 🛠️ Troubleshooting

### Remove Cron Job
```bash
crontab -l | grep -v 'run_pipeline.py' | crontab -
```

### Check Pipeline Status
```bash
# Check if Ghost is running
curl http://localhost:2368

# Check database
ls -la data/sqlite.db

# Check generated posts
ls -la data/post_*.md
```

### GitHub Actions Issues
1. Check repository secrets are set correctly
2. Verify workflow permissions in repository settings
3. Check Actions tab for error logs

## 🔄 Automation Flow

1. **Research Agent** - Finds new content topics
2. **Validation Agent** - Fact-checks and scores content  
3. **Writer Agent** - Generates blog posts
4. **Publisher Agent** - Publishes to Ghost CMS

Each step is logged and tracked in the database to prevent duplicates.

## ⚙️ Customization

### Change Frequency
**Cron (Local):**
```bash
# Every 3 hours: 0 */3 * * *
# Every 6 hours: 0 */6 * * *
# Daily at 9 AM: 0 9 * * *
```

**GitHub Actions:**
Edit `.github/workflows/auto-content.yml` cron expression:
```yaml
schedule:
  - cron: '0 */3 * * *'  # Every 3 hours
```

### Content Settings
Modify the agents in `/agents/` directory to customize:
- Search terms and topics
- Content validation criteria
- Writing style and length
- Publishing settings