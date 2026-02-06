<div align="center">
  <img src="logo.svg" width="96" height="96" alt="Ollama Says logo" />
  <h1>Ollama Says</h1>
  <p><strong>Prompt injection defense testing for local LLM deployments</strong></p>
  <p>
    <a href="https://tannner.com">tannner.com</a> ·
    <a href="https://github.com/tannernicol/ollama-says">GitHub</a>
  </p>
</div>

---

## What it does

Ollama Says is an interactive attack/defense lab that pits naive agents against guarded ones using synthetic canaries and full audit trails. It provides a repeatable harness with a scoring rubric and multi-format reporting so security teams can measure prompt injection risk, track regressions across model updates, and ship defensible defenses.

## Key features

- Direct and indirect injection vectors with structured taxonomy
- Policy checks and detection signals for layered defense
- JSON, Markdown, and HTML report generation
- Repeatable harness with scoring rubric for measurable safety posture

## Stack

- Python
- Ollama

## Getting started

```bash
git clone https://github.com/tannernicol/ollama-says.git
cd ollama-says
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config/example.yaml config/local.yaml
python scripts/demo.py --config config/local.yaml

# Generate a defense report
python scripts/evaluate.py --config config/suite.yaml --simulate
```

## Author

**Tanner Nicol** — Principal Security Infrastructure Engineer
[tannner.com](https://tannner.com) · [GitHub](https://github.com/tannernicol) · [LinkedIn](https://linkedin.com/in/tanner-nicol-60b21126)
