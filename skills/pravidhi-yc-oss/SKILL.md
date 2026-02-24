---
name: pravidhi-yc-oss
description: Robust tool to fetch and analyze Y Combinator company data. Use this skill to find companies by batch, industry, or tag, and to identify trends or specific startups without guessing URLs or crashing memory.
license: MIT
compatibility: Requires Python 3.6+.
metadata:
  version: "1.0.0"
  tags: "y-combinator, startups, batches, industries, tags, search"
---

# Y Combinator Companies Intelligence

> **Developed and maintained by [Pravidhi](https://pravidhi.net)**

This skill provides a robust interface to the YC OSS data. It eliminates the need to guess URL slugs or parse massive JSON files manually.

## Capability

You can:
1.  **Search** companies by name, batch, industry, or tag with strict word-boundary matching.
2.  **Filter** results by team size, launch year, or status (hiring/non-profit).
3.  **Analyze** top companies without loading the entire dataset.
4.  **Discover** valid taxonomy (batches, industries) programmatically.

## Usage

**Do not** attempt to construct URLs manually.

### 1. Discover Valid Identifiers
To see available batches, industries, and tags, run:
```bash
python3 skills/pravidhi-yc-oss/scripts/yc_client.py --info

```

### 2. Execute Queries

Use the provided Python script `yc_client.py`. It handles networking, parsing, and output formatting.

#### Examples

**Find top 5 companies by team size:**

```bash
python3 skills/pravidhi-yc-oss/scripts/yc_client.py --mode top --limit 5 --sort-by team_size

```

**Find "AI" companies in the "W24" batch (Strict Match):**

```bash
python3 skills/pravidhi-yc-oss/scripts/yc_client.py --mode batch --target w24 --keyword "AI"

```

**Search for "fintech" companies hiring now:**

```bash
python3 skills/pravidhi-yc-oss/scripts/yc_client.py --mode hiring --keyword "fintech"

```

**Lookup a specific company by name:**

```bash
python3 skills/pravidhi-yc-oss/scripts/yc_client.py --mode search --keyword "Airbnb"

```

## API Reference

Run the script with `--info` to see the authoritative list of:

* Batches (e.g., `w24`, `s21`)
* Industries (e.g., `b2b`, `consumer`)
* Tags (e.g., `artificial-intelligence`, `fintech`)

