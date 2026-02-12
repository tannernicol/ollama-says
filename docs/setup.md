# Setup Guide

Everything runs locally. No API keys or cloud services needed.

## Prerequisites
- Python 3.10+
- Ollama installed and running locally (optional -- simulate mode works without it)

## Step 1: Environment
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Step 2: Quick Demo (no Ollama needed)
Run the demo harness in simulate mode:
```bash
make demo
```
Expected output: a JSON report with 37 test cases and defense scoring.

## Step 3: Run Against a Model
1. Pull a model in Ollama:
   ```bash
   ollama pull qwen2.5:7b
   ```
2. Run the evaluation suite:
   ```bash
   python scripts/evaluate.py --config config/suite.yaml --policy config/policy.yaml
   ```

## Step 4: Benchmark
Compare defense quality over time:
```bash
make benchmark
```
