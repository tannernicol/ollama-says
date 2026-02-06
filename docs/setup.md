# Setup Guide

## Prerequisites
- Ollama installed and running locally
- Python 3.11+

## Step 1: Environment
1. Create a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`

## Step 2: Configuration
1. Copy `config/example.yaml` to `config/local.yaml`.
2. Choose a local model in Ollama.

## Step 3: Dry Run
Run the demo harness to validate wiring:
```
python scripts/demo.py --config config/local.yaml
```

Expected output: a short report with test cases and pass/fail scoring.
