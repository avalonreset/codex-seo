---
name: seo-page
description: >
  Run deep single-page SEO analysis with scoring, prioritized issues,
  schema opportunities, and actionable fixes. Use for requests like
  "analyze this page", "check this URL SEO", "single-page audit",
  or when the user provides one page URL for review.
---

# Single Page Analysis

Run a deterministic single-page audit and generate a report plus machine-readable summary.

## Runtime

- Main runner: `skills/seo-page/scripts/run_page_audit.py`
- Install dependencies from `skills/seo-page/requirements.txt`
- Optional screenshot capture uses Playwright Chromium

## Quick Run

```bash
python skills/seo-page/scripts/run_page_audit.py https://example.com/about --output-dir seo-page-output --visual auto
```

## Inputs

- `url` (required): page URL to audit
- `keyword` (optional): explicit focus keyword phrase
- `visual` (optional): `auto|on|off` screenshot mode

## Guardrails

1. Accept only `http` or `https`.
2. Reject localhost, loopback, private, and reserved IP targets.
3. Do not claim lab-measured CWV metrics from static HTML analysis.
4. Flag deprecated `HowTo` schema and restricted `FAQPage` usage.

## Analysis Scope

- On-page SEO: title/meta/H1/heading hierarchy/URL shape
- Content quality: word count, readability, keyword density, E-E-A-T signals
- Technical tags: canonical, robots, OG, Twitter tags, redirects
- Schema: JSON-LD detection/validation and opportunity generation
- Images: alt text, dimensions, lazy loading, size risk via sampled HEAD checks
- CWV risk signals: potential LCP/INP/CLS risk indicators

## Output Contract

- `PAGE-AUDIT-REPORT.md`: human-readable analysis with priority-grouped issues
- `SUMMARY.json`: structured result payload for automation
- `screenshots/page-desktop.png` when visual mode is available
