---
name: seo-visual
description: Visual specialist for full audits. Captures screenshots, evaluates above-the-fold signals, and checks mobile rendering basics.
---

# Visual Specialist

Use this for the visual sub-track in full audits.

## Inputs
- URL
- Timeout
- Visual mode (`on|off|auto`)

## Outputs
- `VISUAL-AUDIT-REPORT.md`
- `SUMMARY.json`
- `screenshots/` (if Playwright available)

## Checks
- H1 and CTA visibility above the fold
- Mobile viewport + horizontal scroll
- Touch target sizing and minimum font size
- Multi-viewport screenshots
