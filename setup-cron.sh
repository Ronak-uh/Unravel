#!/bin/bash#!/bin/bash



# Setup cron job to run the Unravel pipeline every 5 hours using Gemini 2.5# Setup cron job to run the Unravel pipeline every 5 hours

# Usage: ./setup-cron.sh# Usage: ./setup-cron.sh



PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PYTHON_PATH="$PROJECT_DIR/.venv/bin/python"  # Use virtual environment PythonPYTHON_PATH="/usr/bin/python3"  # Adjust this to your Python path

CRON_JOB="0 */5 * * * cd $PROJECT_DIR && $PYTHON_PATH automation.py >> logs/cron.log 2>&1"CRON_JOB="0 */5 * * * cd $PROJECT_DIR && $PYTHON_PATH run_pipeline.py >> logs/cron.log 2>&1"



echo "Setting up cron job for Unravel automation with Gemini 2.5..."echo "Setting up cron job for Unravel automation..."

echo "Project directory: $PROJECT_DIR"echo "Project directory: $PROJECT_DIR"

echo "Python path: $PYTHON_PATH"echo "Cron job: $CRON_JOB"

echo "Cron job: $CRON_JOB"

# Check if cron job already exists

# Check if cron job already existsif crontab -l 2>/dev/null | grep -q "run_pipeline.py"; then

if crontab -l 2>/dev/null | grep -q "automation.py"; then    echo "Cron job already exists. Removing old one..."

    echo "Cron job already exists. Removing old one..."    crontab -l 2>/dev/null | grep -v "run_pipeline.py" | crontab -

    crontab -l 2>/dev/null | grep -v "automation.py" | crontab -fi

fi

# Add new cron job

# Add new cron job(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job added successfully!"

echo "✅ Cron job added successfully!"echo "The pipeline will run every 5 hours starting from the next hour."

echo "The Gemini 2.5 pipeline will run every 5 hours starting from the next hour."echo "Log file: $PROJECT_DIR/logs/cron.log"

echo "Log file: $PROJECT_DIR/logs/cron.log"

# Create logs directory if it doesn't exist

# Create logs directory if it doesn't existmkdir -p "$PROJECT_DIR/logs"

mkdir -p "$PROJECT_DIR/logs"

# Show current crontab

# Show current crontabecho ""

echo ""echo "Current crontab:"

echo "Current crontab:"crontab -l

crontab -l

echo ""

echo ""echo "To remove the cron job, run:"

echo "To remove the cron job, run:"echo "crontab -l | grep -v 'run_pipeline.py' | crontab -"
echo "crontab -l | grep -v 'automation.py' | crontab -"