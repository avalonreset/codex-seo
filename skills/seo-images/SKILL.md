---
name: seo-images
description: >
  Image optimization analysis for SEO and performance. Checks alt text, file
  sizes, formats, responsive images, lazy loading, and CLS prevention. Use when
  user says "image optimization", "alt text", "image SEO", "image size",
  or "image audit".
---

# Image Optimization Analysis

## Checks

### Alt Text
- Present on all `<img>` elements (except decorative: `role="presentation"`)
- Descriptive: describes the image content, not "image.jpg" or "photo"
- Includes relevant keywords where natural, not keyword-stuffed
- Length: 10-125 characters

**Good examples:**
- "Professional plumber repairing kitchen sink faucet"
- "Red 2024 Toyota Camry sedan front view"
- "Team meeting in modern office conference room"

**Bad examples:**
- "image.jpg" (filename, not description)
- "plumber plumbing plumber services" (keyword stuffing)
- "Click here" (not descriptive)

### File Size
| Status | Threshold |
|--------|-----------|
| ✅ Good | <100KB |
| ⚠️ Warning | >200KB |
| 🛑 Critical | >500KB |

Recommend compression to <100KB where possible without quality loss.

### Format
| Format | Browser Support | Use Case |
|--------|-----------------|----------|
| WebP | 97%+ | Default recommendation |
| AVIF | 92%+ | Best compression, newer |
| JPEG | 100% | Fallback for photos |
| PNG | 100% | Graphics with transparency |
| SVG | 100% | Icons, logos, illustrations |

Recommend WebP/AVIF over JPEG/PNG. Check for `<picture>` element with format fallbacks.

### Responsive Images
- `srcset` attribute for multiple sizes
- `sizes` attribute matching layout breakpoints
- Appropriate resolution for device pixel ratios

```html
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Description"
>
```

### Lazy Loading
- `loading="lazy"` on below-fold images
- Do NOT lazy-load above-fold/hero images (hurts LCP)
- Check for native vs JavaScript-based lazy loading

```html
<!-- Below fold - lazy load -->
<img src="photo.jpg" loading="lazy" alt="Description">

<!-- Above fold - eager load (default) -->
<img src="hero.jpg" alt="Hero image">
```

### CLS Prevention
- `width` and `height` attributes set on all `<img>` elements
- `aspect-ratio` CSS as alternative
- Flag images without dimensions

```html
<!-- Good - dimensions set -->
<img src="photo.jpg" width="800" height="600" alt="Description">

<!-- Good - CSS aspect ratio -->
<img src="photo.jpg" style="aspect-ratio: 4/3" alt="Description">

<!-- Bad - no dimensions -->
<img src="photo.jpg" alt="Description">
```

### File Names
- Descriptive: `blue-running-shoes.webp` not `IMG_1234.jpg`
- Hyphenated, lowercase, no special characters
- Include relevant keywords

### CDN Usage
- Check if images served from CDN (different domain, CDN headers)
- Recommend CDN for image-heavy sites
- Check for edge caching headers

## Output

### Image Audit Summary

| Metric | Status | Count |
|--------|--------|-------|
| Total Images | - | XX |
| Missing Alt Text | ❌ | XX |
| Oversized (>200KB) | ⚠️ | XX |
| Wrong Format | ⚠️ | XX |
| No Dimensions | ⚠️ | XX |
| Not Lazy Loaded | ⚠️ | XX |

### Prioritized Optimization List

Sorted by file size impact (largest savings first):

| Image | Current Size | Format | Issues | Est. Savings |
|-------|--------------|--------|--------|--------------|
| ... | ... | ... | ... | ... |

### Recommendations
1. Convert X images to WebP format (est. XX KB savings)
2. Add alt text to X images
3. Add dimensions to X images
4. Enable lazy loading on X below-fold images
5. Compress X oversized images
