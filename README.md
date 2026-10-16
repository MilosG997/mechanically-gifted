# mechanicallygifted.rs

Source of [mechanicallygifted.rs](https://mechanicallygifted.rs), the site for my work: Shopify development, simple websites for small businesses and QA test automation.

![Mechanically Gifted](sajt/og-image.png)

## What is in it

- **Two real language pages**: `/` (Serbian) and `/en/` (English), each with its own title, description, canonical and `hreflang` links, so Google indexes both. The SR/EN switch is a plain link, no JavaScript.
- **Structured data**: `ProfessionalService` + `FAQPage` JSON-LD in the page language.
- **Open Graph / Twitter cards** with a 1200 × 630 share image, `favicon.svg`, `apple-touch-icon.png`, `sitemap.xml` with hreflang alternates, `robots.txt`.
- **Animated network hero** on a `<canvas>`: fewer points on phones, pauses when off screen or in a background tab, respects `prefers-reduced-motion`.
- **No framework, no build step for the visitor**: one HTML file per language, inline CSS, about 25 KB.
- Tested with Selenium in [qa-automation](https://github.com/MilosG997/qa-automation).

## How it is generated

| File | Role |
|---|---|
| `dizajn.html` | The design: markup plus the SR/EN text dictionary |
| `stil.css` | All styles (Geist + Geist Mono) |
| `napravi-sajt.py` | Builds `sajt/index.html` and `sajt/en/index.html` from the design: puts the right language text into the HTML, adds SEO tags, JSON-LD, contact and portfolio links |
| `napravi-slike.py` | Renders the share image, Apple icon and portfolio screenshots with headless Chrome, converts to WebP (Pillow) |
| `sajt/` | The finished site, deployed to Netlify |
| `mechanically-gifted-tech.html` | The original single-file design this started from |

```bash
python napravi-slike.py   # only when images change
python napravi-sajt.py
```

Hosting: Netlify (Netlify DNS, automatic HTTPS).
