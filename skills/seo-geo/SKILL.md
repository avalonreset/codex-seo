---
name: seo-geo
description: >
  Optimize content for AI Overviews (formerly SGE), ChatGPT web search,
  Perplexity, and other AI-powered search experiences. Generative Engine
  Optimization (GEO) analysis. Use when user says "AI Overviews", "SGE",
  "GEO", "AI search", "LLM optimization", "Perplexity", or "AI citations".
---

# AI Search / GEO Optimization

## Background

AI Overviews (rebranded from SGE in May 2024) now appear on ~15-25% of queries
across 200+ countries. AI-sourced search sessions are growing 500%+ year-over-year.
This is the largest shift in search since mobile-first indexing.

## GEO Analysis Criteria

### 1. Citability Score (25%)

How likely is this content to be cited by AI systems?

**Strong signals:**
- Clear, quotable sentences with specific facts/statistics
- Unique data points not found elsewhere
- Claims attributed with specific sources
- Answer-first formatting (conclusion, then explanation)
- Definitions following "X is..." or "X refers to..." patterns

**Weak signals:**
- Vague, general statements
- Opinion without evidence
- Buried conclusions
- No specific data points

### 2. Structural Readability (25%)

How easy is it for AI to parse and extract information?

**Strong signals:**
- Clean H1→H2→H3 heading hierarchy
- Short paragraphs (2-4 sentences)
- Tables for comparative data
- Ordered/unordered lists for step-by-step or multi-item content
- Definition patterns
- FAQ sections with clear Q&A format

**Weak signals:**
- Wall of text with no structure
- Inconsistent heading hierarchy
- No lists or tables
- Information buried in paragraphs

### 3. Entity Clarity (15%)

Are key concepts clearly defined and contextualized?

**Strong signals:**
- Key entities (people, organizations, concepts) clearly defined
- Sufficient context for AI to understand relationships
- Technical terms explained on first use
- Consistent terminology throughout

**Weak signals:**
- Undefined jargon
- Ambiguous references
- Inconsistent naming

### 4. Authority Signals (20%)

Does the content demonstrate credibility?

**Strong signals:**
- Author byline with credentials
- Publication date and last-updated date
- Citations to primary sources (studies, official docs, data)
- Organization credentials and affiliations
- Expert quotes with attribution

**Weak signals:**
- Anonymous authorship
- No dates
- No sources cited
- Generic content

### 5. Structured Data Support (15%)

Is there machine-readable context?

**Strong signals:**
- JSON-LD schema matching content type
- FAQ schema (gov/health sites only)
- Speakable schema for voice-search content
- BreadcrumbList for navigation context
- Author/Person schema

**Weak signals:**
- No structured data
- Invalid or incomplete schema
- Schema doesn't match content

## Recommendations Framework

For each page analyzed, provide:

1. **Current GEO readiness score (0-100)**
2. **Top 3 highest-impact changes**
3. **Content reformatting suggestions**
4. **Schema additions for AI discoverability**
5. **Comparison vs top-ranking competitors** (if query provided)

## Optimization Tactics

### Quick Wins
- Add "What is [topic]?" definition early in content
- Include specific statistics with sources
- Add table summarizing key points
- Structure with clear H2/H3 hierarchy
- Add publication/update dates

### Medium Effort
- Create FAQ section with common questions
- Add author bio with credentials
- Include original data or research
- Add comparison tables
- Implement appropriate schema markup

### High Impact
- Conduct original research/surveys
- Add expert interviews/quotes
- Create comprehensive topic coverage
- Build topical authority through content clusters
- Develop unique tools or calculators

## Output

- `GEO-ANALYSIS.md` — Full AI search optimization report
- GEO Readiness Score: XX/100
- Category breakdown
- Specific rewriting suggestions for key sections
- Schema recommendations
