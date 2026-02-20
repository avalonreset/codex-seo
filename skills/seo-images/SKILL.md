---
name: seo-images
description: >
  Audit image SEO and image performance quality: alt text, size thresholds,
  formats, responsive delivery, lazy loading, CLS safeguards, and optimization
  prioritization. Use for prompts like "image audit", "alt text issues",
  "image optimization", or "image SEO".
---

# Image SEO Audit

Use deterministic execution for reproducible image findings and optimization plans.

## Runtime

- Main runner: `skills/seo-images/scripts/run_image_audit.py`
- Dependencies: `skills/seo-images/requirements.txt`

## Quick Run

```bash
python skills/seo-images/scripts/run_image_audit.py \
  --url https://example.com/page \
  --output-dir seo-images-output
```

Local HTML:

```bash
python skills/seo-images/scripts/run_image_audit.py \
  --html-file page.html \
  --page-url https://example.com/page \
  --output-dir seo-images-output
```

## Inputs

- `--url` or `--html-file` (exactly one required)
- `--page-url` (optional, for local HTML mode)
- `--keyword` (optional): focus keyword for alt-text relevance signal
- `--head-sample-limit` (default `30`): image metadata probe limit

## Checks

1. Alt text coverage and quality:
   - Missing/empty alt
   - too short/too long
   - generic/file-name style
   - possible stuffing patterns
2. Size thresholds by category:
   - thumbnail, content, hero thresholds
3. Format guidance:
   - legacy format detection
   - WebP/AVIF fallback cues via `<picture>`
4. Responsive delivery:
   - `srcset`/`sizes` checks
5. Lazy loading and LCP handling:
   - below-fold lazy expectations
   - hero `loading="lazy"` anti-pattern
   - hero `fetchpriority="high"` reminder
6. CLS protection:
   - width/height or aspect-ratio presence
7. Filename quality heuristics
8. CDN/cache header signals from sampled image probes

## Guardrails

1. Accept only `http`/`https` page URLs.
2. Reject localhost/private/reserved targets.
3. Re-check redirect targets for public-host safety.
4. Treat sampled HEAD/GET image probes as partial coverage, not full certainty.

## Output Contract

- `IMAGE-AUDIT-REPORT.md`
- `IMAGE-OPTIMIZATION-PLAN.md`
- `SUMMARY.json`

