# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.3] - 2026-07-12
### Fixed
- `TAXONOMY.md` link in README pointed to a broken relative path on PyPI;
  now points to the file on GitHub directly.

## [0.1.2] - 2026-07-12
### Fixed
- `absurd_overprecision()` in `precision.py` could silently lose its
  injected extra precision due to float64's significant-digit limit.
  Now builds the value as a string first, then converts, guaranteeing
  the intended decimal precision is preserved.
- Corrected `__version__` string in `geobane/__init__.py`, which had
  incorrectly still read `0.1.0` in the 0.1.1 release.

## [0.1.1] - 2026-07-12
### Fixed
- Attempted fix for the `absurd_overprecision()` issue above.
- Note: this release retained an incorrect `__version__` string; use
  0.1.2 or later.

## [0.1.0] - 2026-07-12
### Added
- Initial real release with five generator modules:
  `coordinate_order`, `antimeridian`, `degenerate`, `crs_mismatch`,
  `precision`.
- 20 passing tests covering all five modules.
- Full edge-case taxonomy documented in `TAXONOMY.md`.

## [0.0.1] - 2026-07-12
### Added
- Placeholder release to reserve the `geobane` name on PyPI.