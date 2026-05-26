# FIPs (Font Improvement Proposals)

FIPs (Font Improvement Proposals) are a lightweight process where font tool developers gather to discuss and specify implementation ideas for font improvements.

These proposals are intended for ideas that live outside any specific file format or compiler specification, so that other toolmakers can review and adopt them across the ecosystem.

Typically (but not limited to it), such implementations are defined in private keys in font source formats such as `lib["com.schiftgestalt.corner_components"]`, but they may also simply carry vendor-agnostic FIP keys such as `lib["fip001"]`.

The community and toolmakers may decide at any point in time to incorporate a mature FIP into their own toolchain under permanent property names or different private lib keys.

## Proposal structure

Each proposal must be curated in a numbered folder such as:

- `FIP001/`

And must include:

- an explicit `FIP001.md` file describing the proposal in all clarity and detail
- a `fip.yaml` file carrying a mandatory `name` field (a human-readable title) and a mandatory `keywords` list of all-lowercase, single-word terms describing general concepts such as `kerning`, `components`, `outlines` etc. Example:

  ```yaml
  name: Corner Components
  keywords:
    - components
    - outlines
  ```

Additionally, they may include

- any number of supporting code examples
- ideally, an outright example implementation in Python or similar

The FIP numbers bear no meaning other than chronological ordering. As soon as the number of FIPS have crossed a certain threshold, the defined keywords will be used to auto-generate a convenient overview for this README file.

## Pull request policy

All proposal pull requests must be opened as **Draft** and stay in draft state until the proposal is finalized.

## License

This repository is licensed under the **Unlicense**, a permissive license that even waives attribution such that proposals may be incorporated into tools without the overhead of attribution
