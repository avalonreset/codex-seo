---
name: seo-schema
description: >
  Detect, validate, and generate Schema.org structured data in JSON-LD format.
  Use for prompts like "schema audit", "structured data check", "JSON-LD",
  or "generate schema markup".
---

# Schema Analysis and Generation

Use deterministic execution for reproducible schema audits and template output.

## Runtime

- Main runner: `skills/seo-schema/scripts/run_schema.py`
- Dependencies: `skills/seo-schema/requirements.txt`

## Quick Run

Analyze a page:

```bash
python skills/seo-schema/scripts/run_schema.py analyze \
  --url https://example.com/blog/post \
  --output-dir seo-schema-output
```

Generate a template:

```bash
python skills/seo-schema/scripts/run_schema.py generate \
  --template article \
  --page-url https://example.com/blog/post \
  --output-dir seo-schema-output
```

## Analyze Mode

### Inputs

- `--url` or `--html-file` (exactly one required)
- `--page-url` (optional canonical URL when using `--html-file`)
- `--timeout` (default `20`)

### Detection Scope

1. JSON-LD scripts: `<script type="application/ld+json">`
2. Microdata markers: `itemscope`, `itemprop`
3. RDFa markers: `typeof`, `property`

### Validation Rules

1. `@context` should resolve to `https://schema.org` (inherited context accepted).
2. `@type` must be valid and non-deprecated.
3. Required properties must exist for recognized types.
4. URL-like properties must be absolute URLs.
5. Date fields should use ISO-8601 formatting.
6. Placeholder text must be replaced before publishing.
7. Restricted FAQ behavior:
   - `FAQPage` is flagged for non-authority domains.

### Deprecated/Restricted Handling

- Deprecated/restricted for rich results: `HowTo`, `SpecialAnnouncement`, `CourseInfo`, `EstimatedSalary`, `LearningVideo`, `ClaimReview`, `VehicleListing`, `PracticeProblem`, `Dataset`
- Restricted: `FAQPage` (authority domains only)

### Analyze Output

- `SCHEMA-REPORT.md`
- `generated-schema.json` (opportunity templates)
- `SUMMARY.json`

## Generate Mode

### Inputs

- `--template` (required):
  - `organization`
  - `localbusiness`
  - `article`
  - `product`
  - `website`
  - `breadcrumb`
  - `faq`
- `--page-url` (required)
- `--metadata-file` (optional JSON overrides)

### Generate Output

- `generated-schema.json`
- `SUMMARY.json`

## Guardrails

1. Prefer JSON-LD output.
2. Keep only truthful/verifiable values in production.
3. Placeholder tokens in generated templates must be replaced before publishing.
4. Avoid recommending deprecated schema types.

