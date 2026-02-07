# E-commerce SEO Strategy Template

## Industry Characteristics

- High transaction intent
- Product comparison behavior
- Price sensitivity
- Visual-first decision making
- Seasonal demand patterns
- Competitive marketplace listings

## Recommended Site Architecture

```
/
├── Home
├── /collections (or /categories)
│   ├── /category-1
│   │   ├── /subcategory-1
│   │   └── ...
│   ├── /category-2
│   └── ...
├── /products
│   ├── /product-1
│   ├── /product-2
│   └── ...
├── /brands
│   ├── /brand-1
│   └── ...
├── /sale (or /deals)
├── /new-arrivals
├── /best-sellers
├── /gift-guide
├── /blog
│   ├── /buying-guides
│   ├── /how-to
│   └── /trends
├── /about
├── /contact
├── /shipping
├── /returns
└── /faq
```

## Schema Recommendations

| Page Type | Schema Types |
|-----------|-------------|
| Product Page | Product, Offer, AggregateRating, Review, BreadcrumbList |
| Category Page | CollectionPage, ItemList, BreadcrumbList |
| Brand Page | Brand, Organization |
| Blog | Article, BlogPosting |

### Product Schema Example
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": ["https://example.com/product.jpg"],
  "description": "Product description",
  "sku": "SKU123",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "price": "99.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/product"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "42"
  }
}
```

## Content Requirements

### Product Pages (min 400 words)
- Unique product descriptions (not manufacturer copy)
- Feature highlights
- Use cases / who it's for
- Specifications table
- Size/fit guide (for apparel)
- Care instructions
- Customer reviews

### Category Pages (min 400 words)
- Category introduction
- Buying guide excerpt
- Featured products
- Subcategory links
- Filter/sort options

## Technical Considerations

### Pagination
- Use rel="next"/rel="prev" or load-more
- Ensure all products are crawlable
- Canonical to main category page

### Faceted Navigation
- Noindex filter combinations that create duplicate content
- Use canonical tags appropriately
- Ensure popular filters are indexable

### Product Variations
- Single URL for parent product with variants
- Or separate URLs with canonical to parent
- Structured data for all variants

## Content Priorities

### High Priority
1. Category pages (top level)
2. Best-selling product pages
3. Homepage
4. Buying guides for main categories

### Medium Priority
1. Subcategory pages
2. Brand pages
3. Comparison content
4. Seasonal landing pages

### Blog Topics
- Buying guides ("How to Choose...")
- Product comparisons
- Trend reports
- Use cases and inspiration
- Care and maintenance guides

## Key Metrics to Track

- Revenue from organic search
- Product page rankings
- Category page rankings
- Click-through rate (rich results)
- Average order value from organic
