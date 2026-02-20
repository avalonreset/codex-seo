---
name: seo-geo
description: >
  Optimize content for AI Overviews, ChatGPT Search, and Perplexity with
  deterministic GEO analysis: crawler accessibility, llms.txt quality, brand
  mention signals, passage-level citability, and platform-specific readiness.
  Use for prompts like "GEO", "AI visibility", "AI citations", "AI search",
  "llms.txt", or "ChatGPT search optimization".
---

# AI Search / GEO Optimization

Use deterministic execution for reproducible GEO findings and action plans.

## Runtime

- Main runner: `skills/seo-geo/scripts/run_geo_analysis.py`
- Dependencies: `skills/seo-geo/requirements.txt`

## Quick Run

```bash
python skills/seo-geo/scripts/run_geo_analysis.py \
  --url https://example.com/page \
  --brand "Example Brand" \
  --output-dir seo-geo-output
```

Local HTML:

```bash
python skills/seo-geo/scripts/run_geo_analysis.py \
  --html-file page.html \
  --page-url https://example.com/page \
  --robots-file robots.txt \
  --llms-file llms.txt \
  --output-dir seo-geo-output
```

## Inputs

- `--url` or `--html-file` (exactly one required)
- `--page-url` (optional, local HTML canonical URL)
- `--brand` (optional): brand/entity name for mention signal
- `--keyword` (optional): topic keyword for citability scoring
- `--robots-file` (optional): local robots.txt override
- `--llms-file` (optional): local llms.txt override

## Checks

1. GEO readiness score by weighted criteria:
   - Citability (25%)
   - Structural readability (20%)
   - Multi-modal content (15%)
   - Authority/brand signals (20%)
   - Technical accessibility (20%)
2. Platform readiness breakdown:
   - Google AI Overviews
   - ChatGPT Search
   - Perplexity
   - Bing Copilot
3. AI crawler accessibility from robots.txt:
   - GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot
   - CCBot, anthropic-ai, Bytespider, cohere-ai
4. llms.txt presence and structure quality scoring
5. Brand mention/platform footprint signals:
   - Wikipedia, Reddit, YouTube, LinkedIn
6. Passage-level citability analysis with 134-167 word target blocks
7. SSR/CSR accessibility heuristic for AI crawler readability
8. Highest-impact remediation actions and schema recommendations

## Guardrails

1. Accept only `http`/`https` page URLs.
2. Reject localhost/private/reserved/loopback targets.
3. Re-check redirect targets for public-host safety.
4. Treat crawler and passage checks as sampled heuristics, not ranking guarantees.

## Output Contract

- `GEO-ANALYSIS.md`
- `SUMMARY.json`
- `CRAWLER-STATUS.json`
- `BRAND-SIGNALS.json`
