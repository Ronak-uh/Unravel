#!/bin/bash

# Auto Content Generation Script
# Runs the complete pipeline: research -> validation -> writing -> publishing

# Set script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Create logs directory
mkdir -p logs

# Log file with timestamp
LOG_FILE="logs/auto-pipeline-$(date +%Y%m%d-%H%M%S).log"

echo "========================================" >> "$LOG_FILE"
echo "Auto Pipeline Started: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Function to log and execute
run_agent() {
    local agent_name=$1
    local script_path=$2
    
    echo "$(date): Starting $agent_name..." >> "$LOG_FILE"
    
    if python "$script_path" >> "$LOG_FILE" 2>&1; then
        echo "$(date): $agent_name completed successfully" >> "$LOG_FILE"
        return 0
    else
        echo "$(date): $agent_name failed" >> "$LOG_FILE"
        return 1
    fi
}

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "$(date): Virtual environment activated" >> "$LOG_FILE"
fi

# Run the complete pipeline
run_agent "Research Agent" "agents/research_agent.py"
if [ $? -eq 0 ]; then
    run_agent "Validation Agent" "agents/validation_agent.py"
    if [ $? -eq 0 ]; then
        run_agent "Writer Agent" "agents/writer_agent.py"
        if [ $? -eq 0 ]; then
            run_agent "Publisher Agent" "agents/publisher_agent.py"
        fi
    fi
fi

# Check results
python -c "
import sqlite3
conn = sqlite3.connect('data/sqlite.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM candidates WHERE published=1')
total_published = c.fetchone()[0]
c.execute('SELECT COUNT(*) FROM candidates WHERE validated=1 AND published=0')
ready_to_publish = c.fetchone()[0]
print(f'Total published posts: {total_published}')
print(f'Ready to publish: {ready_to_publish}')
conn.close()
" >> "$LOG_FILE" 2>&1

echo "========================================" >> "$LOG_FILE"
echo "Auto Pipeline Completed: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Keep only last 10 log files
find logs/ -name "auto-pipeline-*.log" -type f | sort | head -n -10 | xargs rm -f

echo "Pipeline completed. Check $LOG_FILE for details."