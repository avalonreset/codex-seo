# Publisher/Media SEO Strategy Template

## Industry Characteristics

- High content volume
- Time-sensitive content (news)
- Ad revenue dependent on traffic
- Authority and trust critical
- Competing with social platforms
- AI Overviews impact on traffic

## Recommended Site Architecture

```
/
├── Home
├── /news (or /latest)
├── /topics
│   ├── /topic-1
│   ├── /topic-2
│   └── ...
├── /authors
│   ├── /author-1
│   └── ...
├── /opinion
├── /reviews
├── /guides
├── /videos
├── /podcasts
├── /newsletter
├── /about
│   ├── /editorial-policy
│   ├── /corrections
│   └── /contact
└── /[year]/[month]/[slug] (article URLs)
```

## Schema Recommendations

| Page Type | Schema Types |
|-----------|-------------|
| Article | NewsArticle or Article, Person (author), Organization (publisher) |
| Author Page | Person, ProfilePage |
| Topic Page | CollectionPage, ItemList |
| Homepage | WebSite, Organization |
| Video | VideoObject |
| Podcast | PodcastEpisode, PodcastSeries |

### NewsArticle Schema Example
```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "Article Headline",
  "datePublished": "2026-02-07T10:00:00Z",
  "dateModified": "2026-02-07T14:30:00Z",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/authors/author-name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publication Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "image": ["https://example.com/article-image.jpg"],
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/article-url"
  }
}
```

## E-E-A-T Requirements

Publishers face highest E-E-A-T scrutiny.

### Author Pages Must Include
- Full name and photo
- Bio and credentials
- Areas of expertise
- Contact information
- Social profiles (sameAs)
- Previous articles by this author

### Editorial Standards
- Clear correction policy
- Transparent editorial process
- Fact-checking procedures
- Conflict of interest disclosures

## Content Priorities

### High Priority
1. Breaking news (speed matters)
2. Evergreen guides on core topics
3. Author pages with credentials
4. Topic hubs/pillar pages

### Medium Priority
1. Opinion/analysis pieces
2. Video content
3. Interactive content
4. Newsletter landing pages

### GEO Considerations
- Clear, quotable facts in articles
- Tables for data-heavy content
- Expert quotes with attribution
- Update dates prominently displayed
- Structured headings (H2/H3)

## Technical Considerations

### Core Web Vitals
- Ad placement affects CLS
- Lazy load ads and images below fold
- Optimize hero images for LCP
- Minimize render-blocking resources

### AMP (if used)
- Consider dropping AMP (no longer required for Top Stories)
- Ensure canonical setup is correct
- Monitor performance vs non-AMP

### Pagination
- Proper pagination for multi-page articles
- Or infinite scroll with proper indexing
- Canonical to page 1 or full article

## Key Metrics to Track

- Page views from organic
- Time on page
- Pages per session
- Newsletter signups from organic
- Google News/Discover traffic
- AI Overview appearances
