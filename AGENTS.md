# Wiggle brand repository

Canonical source for Wiggle logos, favicons, social previews and website brand
artwork. The website consumes this repository as the `brand/` Git submodule.

## Rules

- Current brand assets use stable, versionless filenames. Move superseded
  artwork into the appropriate `legacy/vN/` directory before replacing it.
- `wiggle-symbol.svg` is the current light-background symbol master;
  `wiggle-symbol-dark.svg` is its dark-background counterpart.
- Keep source SVGs editable and validate them with `xmllint --noout`.
- `wiggle-symbol.png` is a 1024 by 1024 transparent export generated from
  the current light SVG with `rsvg-convert`; regenerate it after master geometry or
  colour changes.
- `wiggle-symbol-dark.png` is the same export of `wiggle-symbol-dark.svg`;
  regenerate it with `wiggle-symbol.png`.
- `wiggle-symbol-tile.svg` is the light symbol on a white rounded tile, for
  emails: Gmail darkens an email's page but never its images, so the tile keeps
  the navy symbol readable. Keep its symbol identical to `wiggle-symbol.svg` and
  regenerate `wiggle-symbol-tile.png` with the other symbol exports.
- `favicon.svg` intentionally matches the admin panel: transparent background,
  32-unit stroke and tightly cropped viewBox. Preserve this framing rather than
  copying the square symbol master mechanically.
- Do not add secrets, private business material or proprietary product code.
- After each coherent brand change, commit this repository, then update and
  commit the pinned submodule revision in every affected consumer repository.
