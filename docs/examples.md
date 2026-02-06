# Examples

## Quick Start

```
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp config/example.yaml config/local.yaml
python scripts/demo.py --config config/local.yaml
```

## Example Output

```
{
  "suite": "starter",
  "cases": [
    "direct-override",
    "indirect-injection"
  ],
  "score": "2/2",
  "notes": "demo harness only"
}
```
