#!/bin/bash
echo "Starting Bias Analysis Pipeline..."

python scripts/preprocess_bias_data.py
python scripts/run_bias_analysis.py

echo "Bias Analysis Pipeline Complete."