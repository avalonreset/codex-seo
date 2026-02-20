---
name: seo-competitor-pages
description: >
  Build SEO-focused competitor comparison pages and alternatives pages with
  source-aware feature matrices, schema output, keyword strategy, and
  conversion-ready structure. Use for prompts like "X vs Y", "alternatives to
  X", "best [category] tools", or "comparison chart".
---

# Competitor Comparison Builder

Generate deterministic comparison assets that preserve fairness rules and avoid unsupported claims.

## Runtime

- Main runner: `skills/seo-competitor-pages/scripts/run_competitor_pages.py`
- Dependencies: standard library only (see `skills/seo-competitor-pages/requirements.txt`)

## Quick Run

```bash
python skills/seo-competitor-pages/scripts/run_competitor_pages.py \
  --mode vs \
  --your-product "Acme CRM" \
  --competitors "HubSpot" \
  --category "CRM" \
  --use-case "B2B sales teams" \
  --canonical-url "https://example.com/compare/acme-vs-hubspot" \
  --output-dir seo-competitor-pages-output
```

## Inputs

- `mode` (required): `vs|alternatives|roundup|table`
- `your-product` (required): your product name
- `competitors` (required): comma-separated competitors
- `category` (optional): category label used in metadata and schema
- `use-case` (optional): audience/use-case phrase for title/H1 variants
- `canonical-url` (optional): final page URL used in output metadata/schema
- `pricing-as-of` (optional): pricing timestamp shown in the matrix
- `related-links` (optional): comma-separated internal links for related comparisons
- `data-file` (optional): JSON with product facts/sources

## Data File Contract (Optional)

```json
{
  "feature_order": ["Automation", "Analytics", "Support"],
  "products": {
    "Acme CRM": {
      "url": "https://acme.example",
      "pricing": "$49/user/mo",
      "pricing_source": "https://acme.example/pricing",
      "best_for": "SMB sales teams",
      "pros": ["Fast setup", "Strong automation"],
      "cons": ["Limited marketplace"],
      "features": {
        "Automation": "Advanced workflows",
        "Analytics": "Custom dashboards"
      },
      "feature_sources": {
        "Automation": "https://acme.example/docs/automation"
      },
      "sources": ["https://acme.example/docs"]
    }
  }
}
```

## Guardrails

1. Do not fabricate competitor facts: unresolved fields stay marked as `Needs source verification`.
2. Keep balanced framing: every product gets strengths and limitations.
3. Include clear affiliation disclosure and pricing timestamp.
4. Require source-backed pricing/feature claims before publishing.
5. Never use defamatory language about competitors.

## Output Contract

- `COMPARISON-PAGE.md`: implementation-ready page draft with:
  - SEO metadata draft (title/H1/meta description)
  - feature and pricing matrix
  - product breakdown sections
  - word-count target structure (minimum 1,500 words)
  - conversion layout and internal-linking plan
  - fairness/compliance checklist
- `comparison-schema.json`: JSON-LD graph (`SoftwareApplication` + `ItemList` when relevant)
- `KEYWORD-STRATEGY.md`: primary/secondary/long-tail keyword pack
- `SUMMARY.json`: mode/products/source coverage/output paths

## Mode Rules

- `vs`: exactly 1 competitor
- `alternatives`, `roundup`, `table`: at least 2 competitors

## Quality Target

- Publish only when source coverage is at least 80% and critical pre-publish issues are cleared.

