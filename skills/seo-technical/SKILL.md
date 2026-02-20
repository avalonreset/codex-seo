---
name: seo-technical
description: >
  Run technical SEO audits across crawlability, indexability, security, URL
  structure, mobile readiness, Core Web Vitals risk, structured data, and
  JavaScript rendering. Use when requests mention "technical SEO",
  "crawl/indexing issues", "robots.txt", "security headers", "site speed",
  or "rendering problems".
---

# Technical SEO Audit

Run a deterministic technical audit focused on implementation-level SEO risks.

## Runtime

- Runner: `skills/seo-technical/scripts/run_technical_audit.py`
- Dependencies: `skills/seo-technical/requirements.txt`
- Optional mobile probing uses Playwright (`python -m playwright install chromium`)

## Quick Run

```bash
python skills/seo-technical/scripts/run_technical_audit.py https://example.com --output-dir seo-technical-output --mobile-check auto
```

## Inputs

- `url` (required): target URL to audit
- `mobile_check` (optional): `auto|on|off` for Playwright-based mobile checks

## Guardrails

1. Accept only `http`/`https` URLs.
2. Reject localhost, loopback, private, and reserved IP targets.
3. Treat LCP/INP/CLS as risk indicators unless field/lab metrics are explicitly measured.
4. Never reference FID; use INP only.

## Categories Scored

1. Crawlability
2. Indexability
3. Security
4. URL Structure
5. Mobile
6. Core Web Vitals (risk-based)
7. Structured Data
8. JavaScript Rendering

## AI Crawler Policy Review

The audit parses `robots.txt` policy for:

- `GPTBot`
- `ChatGPT-User`
- `ClaudeBot`
- `PerplexityBot`
- `Bytespider`
- `Google-Extended`
- `CCBot`

Use this output to align crawler policy with AI visibility strategy.

## Output Contract

- `TECHNICAL-AUDIT-REPORT.md`: technical category scorecard and prioritized findings
- `TECHNICAL-ACTION-PLAN.md`: remediation plan grouped by priority
- `SUMMARY.json`: machine-readable payload for automation
