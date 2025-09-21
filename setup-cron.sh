#!/bin/bash

# Setup cron job to run the Unravel pipeline every 5 hours
# Usage: ./setup-cron.sh

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH="/usr/bin/python3"  # Adjust this to your Python path
CRON_JOB="0 */5 * * * cd $PROJECT_DIR && $PYTHON_PATH run_pipeline.py >> logs/cron.log 2>&1"

echo "Setting up cron job for Unravel automation..."
echo "Project directory: $PROJECT_DIR"
echo "Cron job: $CRON_JOB"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "run_pipeline.py"; then
    echo "Cron job already exists. Removing old one..."
    crontab -l 2>/dev/null | grep -v "run_pipeline.py" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job added successfully!"
echo "The pipeline will run every 5 hours starting from the next hour."
echo "Log file: $PROJECT_DIR/logs/cron.log"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_DIR/logs"

# Show current crontab
echo ""
echo "Current crontab:"
crontab -l

echo ""
echo "To remove the cron job, run:"
echo "crontab -l | grep -v 'run_pipeline.py' | crontab -"