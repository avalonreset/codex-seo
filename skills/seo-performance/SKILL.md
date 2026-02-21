---
name: seo-performance
description: Performance specialist for full audits. Measures CWV (LCP/INP/CLS), Lighthouse score signals, and emits deterministic report artifacts.
---

# Performance Specialist

Use this for the performance sub-track in full audits.

## Inputs
- URL
- Timeout
- Optional PageSpeed API key (`PAGESPEED_API_KEY`)

## Outputs
- `PERFORMANCE-AUDIT-REPORT.md`
- `SUMMARY.json`

## Core checks
- Lighthouse performance score (mobile + desktop if available)
- LCP, INP, CLS thresholds
- Fallback guidance when API data is unavailable

## Priority Rules
- **High**: Performance score < 70 or LCP > 2500ms or INP > 200ms or CLS > 0.1
- **Medium**: Performance score 70-79
- **Low**: Data-source limitations
