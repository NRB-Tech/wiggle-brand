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
| `wiggle-stacked.svg` | Header and footer in `../index.html`; header and footer in `../help/index.html`, `../help/ev-solar-battery-too-much-to-manage.html`, `../help/intelligent-octopus-go-ev-charging.html`, and `../help/solar-battery-not-saving-money.html`; header and footer in `../insights/index.html` and `../insights/solar-eclipse-home-energy-flexibility.html`; page header in `../privacy.html`, `../terms.html`, `../thanks.html`, and `../thanks-help.html`. |
| `favicon.svg` | SVG browser icon linked from every HTML page above. It matches the admin panel favicon: a transparent background, 32-unit stroke and tightly cropped viewBox. Keep this framing when regenerating browser derivatives. |
| `favicon.ico` | ICO fallback linked from every HTML page above. Generated from `favicon.svg`. |
| `favicon-32.png` | Standalone 32 px favicon derivative. It is not currently linked directly. |
| `apple-touch-icon.png` | Apple touch icon linked from every HTML page above. Retains the white-background artwork archived in `legacy/v2/favicon.svg`. |
| `og-image.png` | Open Graph preview for `../index.html` and `../insights/index.html`. Contains the horizontal lockup. |
| `twitter-image.png` | X/Twitter preview for `../index.html` and `../insights/index.html`. Contains the horizontal lockup. |
| `hero-connected-home.png` | Homepage hero illustration in `../index.html`. The central controller tile contains the Wiggle symbol, so this raster also needs review when the symbol changes. |

`solar-eclipse-flexibility-social.png` is the article-specific preview for the
solar-eclipse insight. It contains the words “Wiggle Insights” but not the logo
symbol.

`grid-use-more-electricity-og.png` is the article-specific preview for the
turn-up-flexibility insight. It uses the navy, amber and white illustration
language but contains no logo or text.

`device-conflict-og.png` is the article-specific preview and figure for the
device-conflict insight: at night, a home battery's last charge flows into an
electric car while the grid supply stays unused. It is exported at 1200 by 630
from its editable source, `device-conflict-og.svg`, with
`rsvg-convert -w 1200 -h 630 device-conflict-og.svg -o device-conflict-og.png`.
It contains no logo or text.

`problem-fragmented-home.png` is the "The problem" illustration in the
investor pitch deck. It is the opposite of `hero-connected-home.png`: the car,
heat pump and home battery each sit in a separate bubble with their own app on
a ring around the home, the links between them are broken, and rising bills and
emissions sit above the home. It is
exported at 1536 by 1024 from its editable source,
`problem-fragmented-home.svg`, with
`rsvg-convert -w 1536 -h 1024 problem-fragmented-home.svg -o problem-fragmented-home.png`.
It contains no logo or text. Its home, phones, car and charger are copies of
the components below.

Previous car drawings and their raster exports are preserved in `legacy/v3/`
and `legacy/v4/`. The current car uses a simplified, rounded fastback profile.
The emissions icon uses a chimney, rising smoke and an upward arrow; the
previous cloud version is preserved in `legacy/v5/`.
The chimney and smoke are amber, and both rising arrows share the same arrowhead geometry.
The former navy chimney and arrow treatment are preserved in `legacy/v6/`.
The version with navy smoke is preserved in `legacy/v7/`.
Coin stacks use one curved seam between adjacent coins, and the rising arrows
use the same navy as the illustration outlines. The previous coin and amber-arrow
version is preserved in `legacy/v8/`; the bright-blue arrows and previous carbon
arrow position are preserved in `legacy/v9/`.

## Illustration components

`components/` holds line-art parts to reuse in insight images and other
illustrations, so that the same object looks the same everywhere. Each
component is a standalone SVG in the light-background palette: navy `#0E3659`
lines, `#2C78FF` and `#F6A623` accents, and white fills where a part must hide
lines behind it. Its stroke is 7 units at its native size, which matches a
1536 by 1024 illustration. To reuse one, copy its contents into a
`<g transform="translate(x,y)">`; if you scale it, scale the stroke widths back
so that the lines keep the weight of the rest of the image.

| Component | What it shows |
| --- | --- |
| `components/house.svg` | Two-storey home with a solar roof, porch, garage, tree and bushes, as in `hero-connected-home.png`. Its ground line is at the bottom of the view box. |
| `components/phone.svg` | A device's own app on a phone: speaker slot, home bar and a simple blue screen. |
| `components/car.svg` | Electric car in side view: a fastback silhouette, windows and wheels, as in `problem-fragmented-home.svg`. |
| `components/car-charging.svg` | The same car plugged into a post charger with an orange cable. Its charger base line is at the bottom of the view box. |

## Brand and distribution assets

- `wiggle-symbol.svg` and `wiggle-symbol-dark.svg` are the current symbol
  masters.
- `wiggle-symbol.png` is the 1024 px transparent raster export of the current
  light symbol for uses that cannot accept SVG.
- `wiggle-symbol-cropped.png` is the light symbol export trimmed to the
  artwork, with a 4 px transparent margin (756 × 420 px). Use it where the
  square export's empty space is unwanted, such as a logo at the top of a
  Google Doc.
- `wiggle-symbol-dark.png` is the same export of the dark symbol, for
  dark-background uses that cannot accept SVG, such as emails in dark mode.
- `wiggle-symbol-tile.svg` and `wiggle-symbol-tile.png` are the light symbol on
  a white rounded tile, the logo in Wiggle's emails. Gmail darkens an email's
  page in dark mode but leaves images alone, so the white tile keeps the navy
  symbol readable there. Its transparent corners are stored as white, not
  black: some mail apps scale the image without premultiplying alpha, and
  black corners then show as dark marks around the rounded tile.
- `wiggle-horizontal.svg` and `wiggle-horizontal-dark.svg` are the current
  side-by-side lockups. Their symbol is intentionally smaller than the wordmark;
  these supply the landscape social previews rather than the website chrome.
- `wiggle-stacked.svg` and `wiggle-stacked-dark.svg` are the current
  stacked lockups. Their symbol is slightly reduced relative to the wordmark so
  the two elements have comparable visual weight.
- `social-square.png` contains the current stacked lockup but is not referenced
  by the website.
- `linkedin-banner.svg` and `linkedin-banner.png` are not referenced by the
  website, but use the Wiggle wave-and-sun motif.
- `reddit-banner.svg` and `reddit-banner.png` are the Reddit community banner
  for desktop, exported at 2144 by 256 (twice Reddit's 1072 by 128 minimum).
  The tag line sits in the centre between two wave flanks, because Reddit crops
  the banner's sides in narrow windows and puts the community icon over its
  lower-left corner. `reddit-banner-mobile.svg` and `reddit-banner-mobile.png`
  are the mobile banner, exported at 2160 by 256 (twice the 1080 by 128
  minimum). They have no text, because the app shows the banner too small to
  read and puts the community name over it. Neither is referenced by the
  website. Use `#102D75` as the community key colour and `#F7F9FD` as the
  base colour.
- `legacy/v1/` contains the former symbol and full lockup. Legacy artwork is
  retained for provenance and is not referenced by the live HTML.

`legacy/v2/` preserves the former white-background, heavier-stroke browser favicons.

`legacy/v5/` preserves the LinkedIn banner with the former tag line, "Energy that moves with you." (replaced by "Home energy, on your terms." on 28 October 2026).

Current assets always use stable, versionless filenames. When a new design is
approved, move the superseded set into the appropriate `legacy/vN/` directory
before replacing the root-level masters and derivatives.

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
rsvg-convert --width 1024 --height 1024 --output wiggle-symbol.png wiggle-symbol.svg
rsvg-convert --width 1024 --height 1024 --output wiggle-symbol-dark.png wiggle-symbol-dark.svg
rsvg-convert --width 1024 --height 1024 wiggle-symbol-tile.svg \
  | magick - -background white -alpha background -define png:exclude-chunks=date,time wiggle-symbol-tile.png

# Trim the square export to the artwork and keep a 4 px transparent margin.
rsvg-convert --width 1024 --height 1024 --output /tmp/wiggle-symbol-1024.png wiggle-symbol.svg
magick /tmp/wiggle-symbol-1024.png -trim +repage -bordercolor none -border 4 wiggle-symbol-cropped.png

rsvg-convert --width 180 --height 180 --output apple-touch-icon.png legacy/v2/favicon.svg

# Build the ICO from rsvg output, not from the SVG directly. ImageMagick's own
# SVG renderer ignores the clip path and the stroke, which silently produced an
# ICO containing nothing but the orange sun dot.
# Preserve the wide SVG proportions inside square, transparent browser icons.
for size in 16 32 48; do
  rsvg-convert --keep-aspect-ratio --width "$size" --height "$size" --output "/tmp/favicon-$size.png" favicon.svg
  magick "/tmp/favicon-$size.png" -gravity center -background none -extent "${size}x${size}" "/tmp/favicon-$size.png"
done
cp /tmp/favicon-32.png favicon-32.png
magick /tmp/favicon-16.png /tmp/favicon-32.png /tmp/favicon-48.png favicon.ico

rsvg-convert --width 820 --output /tmp/wiggle-horizontal-social.png wiggle-horizontal.svg
rsvg-convert --width 700 --output /tmp/wiggle-stacked-social.png wiggle-stacked.svg
magick -size 1200x630 xc:white /tmp/wiggle-horizontal-social.png -gravity center -composite -depth 8 og-image.png
magick -size 1200x600 xc:white /tmp/wiggle-horizontal-social.png -gravity center -composite -depth 8 twitter-image.png
magick -size 1200x1200 xc:white /tmp/wiggle-stacked-social.png -gravity center -composite -depth 8 social-square.png

rsvg-convert -w 2144 -h 256 reddit-banner.svg -o reddit-banner.png
rsvg-convert -w 2160 -h 256 reddit-banner-mobile.svg -o reddit-banner-mobile.png
```

After an update, check the header and ™ alignment at desktop and mobile widths,
validate the SVGs with `xmllint --noout`, and inspect the small favicon at its
actual size.
