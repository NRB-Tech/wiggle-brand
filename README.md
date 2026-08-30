# Wiggle brand assets

This repository is the canonical, version-controlled source for Wiggle brand
assets and the website artwork distributed with them. The Wiggle site consumes
a pinned commit from this repository at its `brand/` path; do not maintain a
second copied asset set in the site repository.

Use this inventory when the logo geometry or colours change.

## Live website uses

The paths below are relative to the brand submodule when it is checked out in
the Wiggle site repository.

| Asset | Where it appears |
| --- | --- |
| `wiggle-v2-stacked.svg` | Header and footer in `../index.html`; header and footer in `../help/index.html`, `../help/ev-solar-battery-too-much-to-manage.html`, `../help/intelligent-octopus-go-ev-charging.html`, and `../help/solar-battery-not-saving-money.html`; header and footer in `../insights/index.html` and `../insights/solar-eclipse-home-energy-flexibility.html`; page header in `../privacy.html`, `../terms.html`, `../thanks.html`, and `../thanks-help.html`. |
| `favicon.svg` | SVG browser icon linked from every HTML page above. It contains its own small-size copy of the symbol geometry on white: the viewBox is cropped to the symbol and the stroke and sun are enlarged so the mark survives a 16 px browser tab. Do not sync it back to `wiggle-symbol-v2.svg`. |
| `favicon.ico` | ICO fallback linked from every HTML page above. Generated from `favicon.svg`. |
| `favicon-32.png` | Standalone 32 px favicon derivative. It is not currently linked directly. |
| `apple-touch-icon.png` | Apple touch icon linked from every HTML page above. Generated from `favicon.svg`. |
| `og-image.png` | Open Graph preview for `../index.html` and `../insights/index.html`. Contains the horizontal lockup. |
| `twitter-image.png` | X/Twitter preview for `../index.html` and `../insights/index.html`. Contains the horizontal lockup. |
| `hero-connected-home.png` | Homepage hero illustration in `../index.html`. The central controller tile contains the Wiggle symbol, so this raster also needs review when the symbol changes. |

`solar-eclipse-flexibility-social.png` is the article-specific preview for the
solar-eclipse insight. It contains the words “Wiggle Insights” but not the logo
symbol.

`grid-use-more-electricity-og.png` is the article-specific preview for the
turn-up-flexibility insight. It uses the navy, amber and white illustration
language but contains no logo or text.

## Brand and distribution assets

- `wiggle-symbol-v2.svg` and `wiggle-symbol-v2-dark.svg` are the current symbol
  masters.
- `wiggle-symbol-v2.png` is the 1024 px transparent raster export of the light
  v2 symbol for uses that cannot accept SVG.
- `wiggle-v2-horizontal.svg` and `wiggle-v2-horizontal-dark.svg` are the current
  side-by-side lockups. Their symbol is intentionally smaller than the wordmark;
  these supply the landscape social previews rather than the website chrome.
- `wiggle-v2-stacked.svg` and `wiggle-v2-stacked-dark.svg` are the current
  stacked lockups. Their symbol is slightly reduced relative to the wordmark so
  the two elements have comparable visual weight.
- `social-square.png` contains the current stacked lockup but is not referenced
  by the website.
- `linkedin-banner.svg` and `linkedin-banner.png` are not referenced by the
  website, but use the Wiggle wave-and-sun motif.
- `wiggle-symbol-v1.svg` and `wiggle.svg` are retained legacy artwork and are
  not referenced by the live HTML.

## Trade mark

The ™ is deliberately not part of the SVG lockup. Each visible website logo
has an adjacent `<span class="tm">&trade;</span>`. Its positioning lives in:

- the inline styles in `../index.html`, `../thanks.html`, and
  `../thanks-help.html`;
- `../help/help.css` and `../insights/help.css`;
- `../legal.css` for the privacy and terms pages.

The footer legal copy also contains `Wiggle&trade;`. Preserve both the visible
mark and the legal copy when replacing a logo asset.

## Regenerating derivatives

The current files were rendered with `rsvg-convert` and ImageMagick:

```sh
rsvg-convert --width 1024 --height 1024 --output wiggle-symbol-v2.png wiggle-symbol-v2.svg

rsvg-convert --width 32 --height 32 --output favicon-32.png favicon.svg
rsvg-convert --width 180 --height 180 --output apple-touch-icon.png favicon.svg

# Build the ICO from rsvg output, not from the SVG directly. ImageMagick's own
# SVG renderer ignores the clip path and the stroke, which silently produced an
# ICO containing nothing but the orange sun dot.
rsvg-convert --width 16 --height 16 --background-color white --output /tmp/favicon-16.png favicon.svg
rsvg-convert --width 32 --height 32 --background-color white --output /tmp/favicon-32.png favicon.svg
rsvg-convert --width 48 --height 48 --background-color white --output /tmp/favicon-48.png favicon.svg
magick /tmp/favicon-16.png /tmp/favicon-32.png /tmp/favicon-48.png -background white -alpha remove favicon.ico

rsvg-convert --width 820 --output /tmp/wiggle-v2-horizontal-social.png wiggle-v2-horizontal.svg
rsvg-convert --width 700 --output /tmp/wiggle-v2-stacked-social.png wiggle-v2-stacked.svg
magick -size 1200x630 xc:white /tmp/wiggle-v2-horizontal-social.png -gravity center -composite -depth 8 og-image.png
magick -size 1200x600 xc:white /tmp/wiggle-v2-horizontal-social.png -gravity center -composite -depth 8 twitter-image.png
magick -size 1200x1200 xc:white /tmp/wiggle-v2-stacked-social.png -gravity center -composite -depth 8 social-square.png
```

After an update, check the header and ™ alignment at desktop and mobile widths,
validate the SVGs with `xmllint --noout`, and inspect the small favicon at its
actual size.
