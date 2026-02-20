---
name: seo-content
description: >
  Run content quality and E-E-A-T audits with readability, topical coverage,
  AI-content risk heuristics, freshness checks, and AI citation readiness scoring.
  Use for requests like "content audit", "E-E-A-T review", "thin content check",
  "readability analysis", or "is this page citation-ready for AI search?".
---

# Content Quality & E-E-A-T Analysis

Run a deterministic content audit for one URL and produce actionable output.

## Runtime

- Runner: `skills/seo-content/scripts/run_content_audit.py`
- Dependencies: `skills/seo-content/requirements.txt`
- E-E-A-T reference: `seo/references/eeat-framework.md`

## Quick Run

```bash
python skills/seo-content/scripts/run_content_audit.py https://example.com/blog/post --output-dir seo-content-output
```

## Inputs

- `url` (required): target page URL
- `keyword` (optional): focus keyword phrase for density checks

## Guardrails

1. Accept only `http`/`https` URLs.
2. Reject localhost, loopback, private, and reserved IP targets.
3. Treat word-count thresholds as topical-coverage floors, not ranking guarantees.
4. Treat AI-content markers as heuristics, not definitive classification.

## Analysis Scope

- E-E-A-T factor scoring:
  - Experience
  - Expertise
  - Authoritativeness
  - Trustworthiness
- Content quality:
  - topical coverage depth
  - readability
  - structure and heading hierarchy
  - optional keyword density checks
- AI quality heuristics:
  - generic phrasing patterns
  - repetitive opening patterns
  - specificity markers
- AI citation readiness:
  - lists/tables/headings
  - fact density
  - external citations
  - schema presence
- Freshness:
  - publication/update date extraction and age checks

## Output Contract

- `CONTENT-AUDIT-REPORT.md`: full content quality and E-E-A-T report
- `CONTENT-ACTION-PLAN.md`: prioritized remediation plan
- `SUMMARY.json`: machine-readable result payload
