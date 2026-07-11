# Geobane

**Adversarial test-data generator for geospatial systems.**

Geobane generates the specific edge cases that silently break geospatial
code — not just random coordinates, but the exact failure patterns that
cause real bugs: coordinate order confusion, antimeridian crossings,
degenerate geometry, CRS mismatches, and floating-point precision issues.

## Install

```bash
pip install geobane
```

## Why

Most geospatial bugs don't crash — they silently produce wrong results.
A swapped lat/lng pair still looks like a valid coordinate. A polygon
crossing the date line still parses fine, right up until a bounding-box
calculation treats it as spanning the entire globe. Geobane exists to
throw these known failure patterns at your code *before* production does.

## Usage

```python
from geobane import coordinate_order, antimeridian, degenerate
from geobane import crs_mismatch, precision

# The single most common real-world geospatial bug
result = coordinate_order.swapped_pair(lat=51.5, lng=-0.12)
print(result["swapped"])  # (-0.12, 51.5) - fed to a system expecting (lat, lng)

# A polygon crossing the antimeridian - breaks naive bounding-box math
tricky_polygon = antimeridian.crossing_polygon()

# A self-intersecting "bowtie" polygon
bad_shape = degenerate.self_intersecting_bowtie()

# Web Mercator coordinates mislabeled as WGS84
wrong_crs = crs_mismatch.mercator_fed_as_wgs84()

# NaN/Infinity injected into a coordinate
broken = precision.nan_infinity_injection()
```

Every generator returns an `explanation` field describing the real-world
bug it simulates — useful for understanding *why* the edge case matters,
not just reproducing it.

## Categories

| Module | Covers |
|---|---|
| `coordinate_order` | lat/lng axis swap bugs |
| `antimeridian` | date-line crossing polygons, linestrings, bboxes |
| `degenerate` | zero-area, self-intersecting, unclosed geometry |
| `crs_mismatch` | WGS84/Web Mercator confusion, missing CRS metadata |
| `precision` | float32 boundaries, NaN/Infinity, over-precision |

See [TAXONOMY.md](./TAXONOMY.md) for the full edge-case reference,
including planned categories for future versions.

## Contributing

Found a geospatial bug pattern that isn't covered? Open an issue or PR —
the taxonomy doc is the place to propose new categories.

## License

MIT