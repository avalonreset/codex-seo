# Local Service Business SEO Strategy Template

## Industry Characteristics

- Geographic-focused searches
- High intent, quick decision making
- Reviews heavily influence decisions
- Phone calls are primary conversion
- Mobile-first user behavior
- Emergency/urgent service needs

## Recommended Site Architecture

```
/
├── Home
├── /services
│   ├── /service-1
│   ├── /service-2
│   └── ...
├── /locations
│   ├── /city-1
│   │   ├── /service-1-city-1
│   │   └── ...
│   ├── /city-2
│   └── ...
├── /about
├── /reviews
├── /gallery (or /portfolio)
├── /blog
├── /contact
├── /emergency (if applicable)
└── /faq
```

## Quality Gates

### Location Page Limits
- ⚠️ **WARNING** at 30+ location pages
- 🛑 **HARD STOP** at 50+ location pages

### Unique Content Requirements
| Page Type | Min Words | Unique % |
|-----------|-----------|----------|
| Primary Location | 600 | 60%+ |
| Service Area | 500 | 40%+ |
| Service Page | 800 | 100% |

### What Makes Location Pages Unique
- Local landmarks and neighborhoods
- Specific services offered at that location
- Local team members
- Location-specific testimonials
- Community involvement
- Local regulations or considerations

## Schema Recommendations

| Page Type | Schema Types |
|-----------|-------------|
| Homepage | LocalBusiness, Organization |
| Service Pages | Service, LocalBusiness |
| Location Pages | LocalBusiness (with geo) |
| Contact | ContactPage, LocalBusiness |
| Reviews | LocalBusiness (with AggregateRating) |

### LocalBusiness Schema Example
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345"
  },
  "telephone": "+1-555-555-5555",
  "openingHours": "Mo-Fr 08:00-18:00",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "40.7128",
    "longitude": "-74.0060"
  },
  "areaServed": ["City 1", "City 2"],
  "priceRange": "$$"
}
```

## Google Business Profile Integration

- Ensure NAP consistency (Name, Address, Phone)
- Sync service categories
- Regular post updates
- Photo uploads
- Review response strategy

## Content Priorities

### High Priority
1. Homepage with clear service area
2. Core service pages
3. Primary city page
4. Contact page with all locations

### Medium Priority
1. Service + location combination pages
2. FAQ page
3. About/team page
4. Reviews/testimonials page

### Blog Topics
- Seasonal maintenance tips
- How to choose a [service provider]
- Warning signs of [problem]
- DIY vs professional comparisons
- Local regulations and permits

## Key Metrics to Track

- Local pack rankings
- Phone call volume from organic
- Direction requests
- Google Business Profile insights
- Reviews count and rating
