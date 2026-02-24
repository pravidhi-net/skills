# Script Options Reference

> **Note:** These options apply to the `scripts/search.py` wrapper.

## Usage

```bash
python scripts/search.py [-h] -q QUERY [-m MAX_RESULTS] [--safe]
```

## Arguments

| Flag | Long Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `-q` | `--query` | **Required.** The search query string. | N/A |
| `-m` | `--max-results` | Maximum number of results to return. Hard capped at 10. | `5` |
| `-s` | `--safe` | Enables "Paranoid Mode": longer sleep, simpler backend. | `False` |

## Examples

**Basic Search:**
```bash
python scripts/search.py -q "python 3.12 features"
```

**Deep Research (Safe Mode):**
```bash
python scripts/search.py -q "quantum computing startups" -m 10 --safe
```