#!/bin/bash
# Unravel Automation Runner
# This script runs the automation pipeline with proper environment setup

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

# Activate virtual environment and run automation
source .venv/bin/activate
python automation.py

# Log the run with timestamp
echo "$(date): Automation pipeline completed" >> automation.log