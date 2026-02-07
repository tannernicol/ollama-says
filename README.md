<div align="center">
  <img src="logo.svg" width="96" height="96" alt="Ollama Says logo" />
  <h1>Ollama Says</h1>
  <p><strong>Structured prompt injection testing against local models — scored, tracked across versions, fully offline</strong></p>
  <p>
    <a href="https://tannner.com">tannner.com</a> ·
    <a href="https://github.com/tannernicol/ollama-says">GitHub</a>
  </p>
</div>

---

<p align="center">
  <img src="docs/demo.png" alt="Ollama Says demo" width="700" />
</p>

## What it does

Structured prompt injection testing against local models. Scored and tracked across model versions. Fully offline.

Ollama Says pits naive agents against guarded ones using synthetic canaries and full audit trails. It provides a repeatable harness with a scoring rubric and multi-format reporting so you can measure prompt injection risk, track regressions across model updates, and ship defensible defenses.

## Key features

- **47+ attack vectors** — direct and indirect injection with structured taxonomy
- **Scored results** — pass/fail per vector with overall defense rate
- **Version tracking** — compare results across model updates to catch regressions
- **Multi-format reports** — JSON, Markdown, and HTML (see below)
- **Fully offline** — runs entirely on local Ollama models, no data leaves your machine

<p align="center">
  <img src="docs/report.png" alt="HTML report output" width="700" />
</p>

## Quick start

```bash
git clone https://github.com/tannernicol/ollama-says.git
cd ollama-says
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run against a model
python scripts/evaluate.py --model llama3.2

# Generate an HTML report
python scripts/evaluate.py --model llama3.2 --report html
```

```
$ ollama-says run attacks/injection.yaml \
    --model llama3.2
→ 47 attack vectors...
→ 38/47 blocked (80.8%) — 9 bypasses logged
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally

## Author

**Tanner Nicol** — [tannner.com](https://tannner.com) · [GitHub](https://github.com/tannernicol) · [LinkedIn](https://linkedin.com/in/tanner-nicol-60b21126)
