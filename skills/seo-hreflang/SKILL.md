---
name: seo-hreflang
description: >
  Validate and generate hreflang implementations for international SEO.
  Checks self-referencing tags, return-tag reciprocity, x-default coverage,
  code validity, canonical alignment, protocol consistency, and cross-domain
  relationships. Use for prompts like "hreflang audit", "international SEO",
  "multi-language tags", or "generate hreflang sitemap".
---

# Hreflang and International SEO

Use deterministic execution for reproducible hreflang validation and generation.

## Runtime

- Main runner: `skills/seo-hreflang/scripts/run_hreflang.py`
- Dependencies: `skills/seo-hreflang/requirements.txt`

## Quick Run

Validate from a page URL:

```bash
python skills/seo-hreflang/scripts/run_hreflang.py validate \
  --url https://example.com/page \
  --output-dir seo-hreflang-output
```

Validate from sitemap XML:

```bash
python skills/seo-hreflang/scripts/run_hreflang.py validate \
  --sitemap-url https://example.com/hreflang-sitemap.xml \
  --output-dir seo-hreflang-output
```

Generate output from mapping JSON:

```bash
python skills/seo-hreflang/scripts/run_hreflang.py generate \
  --mapping-file hreflang-mapping.json \
  --method sitemap \
  --output-dir seo-hreflang-output
```

## Validate Inputs

- Source mode (choose one):
  - Page mode: `--url` or `--html-file` (exactly one)
  - Sitemap mode: `--sitemap-url` or `--sitemap-file` (exactly one)
- `--page-url` (optional): canonical URL for `--html-file`
- `--max-fetch` (default `25`): max alternate pages fetched in URL mode
- `--max-sitemaps` (default `20`): max child sitemaps traversed from index
- `--strict-return` (optional): unresolved return-tag targets become High severity
- `--strict-iso` (optional): include strict ISO notes when pycountry metadata is unavailable

## Generate Inputs

- `--mapping-file` (required): JSON list or `{ "sets": [...] }` with alternates
- `--method`: `html`, `header`, or `sitemap`
- `--default-locale` (optional): fallback locale used to auto-fill `x-default`

## Checks

1. Self-referencing hreflang tags
2. Return-tag reciprocity (A->B requires B->A)
3. x-default presence and multiplicity
4. Language/region/script code validity + formatting normalization
5. Canonical URL alignment
6. Protocol consistency within alternate set
7. Cross-domain hreflang visibility signals

## Guardrails

1. Accept only `http`/`https` URLs.
2. Reject localhost/private/reserved/loopback URL targets.
3. Re-check redirect targets for public-host safety.
4. Treat unresolved alternate targets as informational unless `--strict-return` is enabled.

## Output Contract

### Validate Mode

- `HREFLANG-VALIDATION-REPORT.md`
- `SUMMARY.json`

### Generate Mode

- `HREFLANG-GENERATION-REPORT.md`
- `SUMMARY.json`
- Method artifact:
  - `hreflang-tags.html` (HTML method), or
  - `hreflang-headers.txt` (Header method), or
  - `hreflang-sitemap.xml` (Sitemap method)
