#!/bin/bash

# Unravel Auto Pipeline Script
# Runs the complete content generation pipeline with error handling and logging

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/logs/pipeline.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Ensure logs directory exists
mkdir -p "$SCRIPT_DIR/logs"

# Logging function
log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# Error handling
handle_error() {
    log "ERROR: Pipeline failed at step: $1"
    exit 1
}

log "=== Starting Unravel Content Pipeline ==="

# Check if .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    log "ERROR: .env file not found. Please create it from .env.example"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    log "ERROR: Python3 is not installed or not in PATH"
    exit 1
fi

# Install/update dependencies if requirements.txt exists
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    log "Installing/updating Python dependencies..."
    python3 -m pip install -r "$SCRIPT_DIR/requirements.txt" >> "$LOG_FILE" 2>&1 || handle_error "dependency installation"
fi

# Change to script directory
cd "$SCRIPT_DIR"

# Step 1: Database setup (if needed)
log "Step 1: Setting up database..."
python3 agents/db_setup.py >> "$LOG_FILE" 2>&1 || handle_error "database setup"

# Step 2: Research (optional - you might want to run this separately)
log "Step 2: Running research agent..."
python3 agents/research_agent.py >> "$LOG_FILE" 2>&1 || handle_error "research agent"

# Step 3: Run main pipeline
log "Step 3: Running main pipeline..."
python3 run_pipeline.py >> "$LOG_FILE" 2>&1 || handle_error "main pipeline"

# Step 4: Cleanup old files (optional)
log "Step 4: Cleaning up old files..."
find "$SCRIPT_DIR/data" -name "post_*.md" -mtime +30 -delete 2>/dev/null || true

log "=== Pipeline completed successfully ==="
log "Check Ghost CMS for new published posts"

# Optional: Send notification (uncomment if you want email notifications)
# echo "Unravel pipeline completed at $TIMESTAMP" | mail -s "Unravel Content Pipeline Success" your@email.com