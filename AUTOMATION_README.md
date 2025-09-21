# 🤖 Unravel Automation - Single File Edition

Complete automated content generation and publishing pipeline in one file.

## ✨ Features

- **All-in-One**: Complete pipeline in a single `automation.py` file
- **Smart Validation**: AI-powered content validation using Gemini
- **Content Generation**: High-quality blog posts with images
- **Ghost Publishing**: Publishes 4 posts per run with full content
- **Database Stats**: Real-time progress tracking

## 🚀 Quick Start

### 1. Run Once
```bash
# Activate virtual environment and run
source .venv/bin/activate
python automation.py
```

### 2. Run with Script (Recommended)
```bash
# Uses the runner script (handles environment automatically)
./run_automation.sh
```

### 3. Set up 5-Hour Automation
```bash
# Add to crontab for every 5 hours
crontab -e

# Add this line:
0 */5 * * * /Users/ronakchavhan/Downloads/Unravel/run_automation.sh
```

## 📊 What It Does

### Pipeline Steps:
1. **🔍 Validation**: Validates unprocessed candidates using Gemini AI
2. **✍️ Writing**: Generates ~800 word blog posts with images 
3. **🚀 Publishing**: Publishes exactly 4 posts to Ghost CMS per run

### Output Example:
```
🤖 UNRAVEL AUTOMATION PIPELINE STARTED
🌐 Ghost URL: https://ghost-production-2c94.up.railway.app

📊 DATABASE STATISTICS:
   Total candidates: 100
   Unvalidated: 6
   Ready to publish: 0
   Published: 94

🔍 Running validation agent...
✓ Validated: Climate Home News... → Accept=True, Score=100
📊 Validation complete: 6 candidates validated

✍️ Running writer agent...
✓ Written: Climate Home News...
📝 Writing complete: 6 posts written

🚀 Running publisher agent...
✅ Published: Climate Home News...
🎉 Publishing complete: 4/4 posts published

✨ PIPELINE COMPLETE! Check your Ghost CMS for new posts.
```

## 📁 Files

- **`automation.py`** - Main automation pipeline (single file)
- **`run_automation.sh`** - Bash runner script for cron jobs
- **`automation.log`** - Execution log (created automatically)

## 🔧 Configuration

All configuration is handled via environment variables in `.env`:

```env
GEMINI_API_KEY=your_gemini_key
GHOST_ADMIN_API_KEY=id:secret  
GHOST_URL=https://your-ghost-site.com
```

## 📈 Benefits

- **Simple**: One file contains everything
- **Reliable**: Error handling and logging built-in
- **Efficient**: Processes 4 posts per run (prevents overwhelming)
- **Complete**: Full pipeline from validation to publishing
- **Monitored**: Built-in statistics and progress tracking

## 🕐 Automation Schedule

The system is designed to run every 5 hours:
- Validates new candidates
- Writes content for validated posts  
- Publishes 4 posts per run
- Logs execution for monitoring

Perfect for continuous, automated content generation! 🎉