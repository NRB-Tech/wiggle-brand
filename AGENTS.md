# Wiggle brand repository

Canonical source for Wiggle logos, favicons, social previews and website brand
artwork. The website consumes this repository as the `brand/` Git submodule.

## Rules

- `wiggle-symbol-v2.svg` is the current light-background symbol master;
  `wiggle-symbol-v2-dark.svg` is its dark-background counterpart.
- Keep source SVGs editable and validate them with `xmllint --noout`.
- `wiggle-symbol-v2.png` is a 1024 by 1024 transparent export generated from
  the light v2 SVG with `rsvg-convert`; regenerate it after master geometry or
  colour changes.
- `favicon.svg` is an intentionally adjusted small-size derivative. Do not
  replace its geometry mechanically from the symbol master.
- Do not add secrets, private business material or proprietary product code.
- After each coherent brand change, commit this repository, then update and
  commit the pinned submodule revision in every affected consumer repository.
