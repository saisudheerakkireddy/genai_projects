#!/bin/bash
# This script prepares and runs the GenAI Hackathon 2025 evaluation framework.

# Strict mode
set -euo pipefail

# 1. Install Python Dependencies
echo "Installing Python dependencies from requirements.txt..."
pip3 install -r requirements.txt

# 2. Run the Main Evaluation Script
echo "Starting the evaluation process..."
./run_evaluation.sh

# 3. Completion Message
echo "Evaluation process complete. Check the 'evaluation_reports' directory for results."
