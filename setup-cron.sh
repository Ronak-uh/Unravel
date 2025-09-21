#!/bin/bash

# Setup Cron Job for Auto Content Generation
# This script sets up a cron job to run every 5 hours

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_COMMAND="0 */5 * * * cd $SCRIPT_DIR && ./auto-pipeline.sh"

echo "Setting up cron job for auto content generation..."
echo "Script directory: $SCRIPT_DIR"
echo "Cron command: $CRON_COMMAND"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "auto-pipeline.sh"; then
    echo "Cron job already exists. Removing old one..."
    crontab -l 2>/dev/null | grep -v "auto-pipeline.sh" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron job successfully created!"
    echo ""
    echo "📅 Schedule: Every 5 hours (00:00, 05:00, 10:00, 15:00, 20:00)"
    echo "📂 Logs will be saved in: $SCRIPT_DIR/logs/"
    echo ""
    echo "Current cron jobs:"
    crontab -l
    echo ""
    echo "🔍 To monitor: tail -f $SCRIPT_DIR/logs/auto-pipeline-*.log"
    echo "🛑 To remove: crontab -e (delete the auto-pipeline.sh line)"
else
    echo "❌ Failed to create cron job"
    exit 1
fi