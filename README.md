# Pravidhi Skills

A collection of open-source, reusable AI agent skills for autonomous coding workflows, research, and data intelligence.

## Overview

This repository provides portable, composable skills that enhance AI agents with structured capabilities for development tasks, web research, and startup intelligence. All skills follow the [Agent Skills specification](https://agentskills.io) format for consistency and interoperability.

## Skills

### 1. **Pravidhi Commit Protocol** (`pravidhi-commit-protocol`)

A complete, opinionated Git workflow skill that enforces quality, security, and atomic commits.

**What it does:**
- Repository hygiene checks (branch safety, remote sync, uncommitted changes)
- Dependency audits and security scanning
- Pre-coding quality validation (formatting, linting)
- CI/CD pre-validation with local mirrors
- Code refactoring with safety nets and rollback verification
- Post-coding validation (tests, coverage, build checks)
- Secret detection before commits
- Atomic commit generation with high-quality messages
- Automated pull request creation

**When to use:**
- Implementing features in a Git repository
- Fixing bugs with quality assurance
- Refactoring code safely
- Any task requiring professional-grade commit hygiene

**Key features:**
- Protected branch detection
- Formatting threshold (>10 files → ask before applying)
- Automatic .gitignore triage
- Secret leak prevention
- Customizable per project

[View Skill](skills/pravidhi-commit-protocol/SKILL.md)

---

### 2. **Internet Search Skill (DDGS)** (`pravidhi-ddgs-internet-search`)

Perform web searches using DuckDuckGo with soft-failure mode and context-safe output.

**What it does:**
- Query DuckDuckGo for web search results
- Configurable result limits
- Safe mode with extra delays for reliability
- Graceful error handling (no crashes on rate limits)

**When to use:**
- Research and fact-finding
- Gathering current information
- Augmenting agent context with web data

**Known limitations:**
- Cloud/datacenter IPs may trigger rate limiting
- Script includes soft-failure mode (returns JSON with error status rather than crashing)

[View Skill](skills/pravidhi-ddgs-internet-search/SKILL.md)

---

### 3. **Y Combinator Companies Intelligence** (`pravidhi-yc-oss`)

Robust tool to fetch and analyze Y Combinator company data without guessing URLs or crashes.

**What it does:**
- Search companies by name, batch, industry, or tag
- Filter by team size, launch year, or status
- Analyze top companies and trends
- Discover valid taxonomy programmatically

**When to use:**
- Finding startups in specific batches or industries
- Competitive analysis
- Identifying companies by hiring status
- Exploring YC ecosystem data

[View Skill](skills/pravidhi-yc-oss/SKILL.md)

---

## Installation

Add any skill to your agent using the skills command-line tool:

```bash
npx skills add https://github.com/pravidhi-net/skills --skill pravidhi-commit-protocol
```

```bash
npx skills add https://github.com/pravidhi-net/skills --skill pravidhi-ddgs-internet-search
```

```bash
npx skills add https://github.com/pravidhi-net/skills --skill pravidhi-yc-oss
```

Or add all skills at once:

```bash
npx skills add https://github.com/pravidhi-net/skills
```

See [Agent Skills documentation](https://agentskills.io) for setup and configuration details.

---

## License

Each skill is independently licensed. See individual SKILL.md files for license information:
- **pravidhi-commit-protocol:** MIT
- **pravidhi-ddgs-internet-search:** MIT
- **pravidhi-yc-oss:** MIT

---

## Resources

- [Agent Skills Specification](https://agentskills.io)
- [Agent Skills Registry](https://agentskills.io/llms.txt)
- [DuckDuckGo Search Library](https://github.com/deedy5/duckduckgo_search)
- [Y Combinator Data](https://github.com/ycombinator/ycdc_public)

