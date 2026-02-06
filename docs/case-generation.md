# Case Generation

Use the generator to create a fresh baseline suite with safe, synthetic cases.

## Generate a Suite
```
python scripts/generate_cases.py --out config/suite.generated.yaml
```

## Customize
- Update `--model` and `--endpoint` for your local Ollama setup.
- Edit the generated YAML to add organization-specific scenarios.

## Notes
- Keep cases synthetic and non-sensitive.
- Avoid real domains, IPs, or credentials.
