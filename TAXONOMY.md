# Geobane Edge-Case Taxonomy

Each category below maps to a `geobane.<category>` module. For v0.1, build the
five marked **[v0.1]** — ship those before adding more.

---

## 1. Coordinate order & axis confusion **[v0.1 — build first]**
The single most common real-world geospatial bug. Different standards disagree
on lat/lng vs lng/lat order (GeoJSON spec says lng,lat; humans usually say
lat,lng; some APIs silently accept either and get it wrong).

- Valid lat/lng pair with order swapped (e.g. `(51.5, -0.12)` → `(-0.12, 51.5)`)
- Coordinates that are "plausible" in both orders (small lat/lng near equator,
  where swap doesn't obviously break bounds — the sneaky ones)
- Coordinates that are valid in one order but out-of-range in the other
  (should throw, but often silently wraps or clamps instead)

## 2. Antimeridian / date-line crossing **[v0.1]**
- Polygon spanning -179° to 179° longitude (naive bounding-box logic treats
  this as spanning the whole globe instead of a thin sliver)
- LineString crossing the date line
- Bounding box / viewport that wraps around 180°/-180°
- Fiji, Russia's Chukotka, Alaska's Aleutians — real places that trigger this

## 3. Degenerate & invalid geometry **[v0.1]**
- Zero-area polygon (all points collinear)
- Single-point "polygon" (fewer than 3 unique vertices)
- Duplicate consecutive points
- Self-intersecting "bowtie" polygon
- Unclosed polygon ring (first point ≠ last point)
- Polygon with holes that exceed the outer boundary

## 4. CRS / projection mismatch **[v0.1]**
- Valid WGS84 (EPSG:4326) coordinates fed to a system expecting Web Mercator
  (EPSG:3857) without transformation
- Coordinates with no CRS metadata at all (ambiguous — is this even WGS84?)
- Out-of-range values for a given projection (e.g. Mercator has no valid
  representation near the poles — values fed anyway should error, not silently
  produce Infinity)

## 5. Precision & numeric edge cases **[v0.1]**
- Coordinates at float32 precision boundary (causes visible drift in some
  rendering/calc pipelines that assume float64)
- `NaN` / `Infinity` injected into a geometry's coordinate array
- Absurd over-precision (16+ decimal places — technically sub-millimeter,
  often a symptom of unintentional floating-point accumulation upstream)
- Integer coordinates where floats were expected (or vice versa)

## 6. Known-bad / signal coordinates (build after v0.1)
- Null Island (0, 0) — the classic "geocoding failed silently" signature
- Poles (±90° latitude) and near-pole high-latitude distortion
- Coordinates exactly on state/country borders (ambiguous reverse-geocoding)

## 7. GPS drift / tracking noise simulation (build after v0.1)
- Realistic jitter patterns around a fixed point (not just uniform random
  noise — real GPS error has spatial/temporal correlation)
- Sudden "teleport" jumps (simulating GPS signal loss + reacquisition)
- Speed-implausible consecutive points (two points too far apart for the
  elapsed time — should flag as sensor error, not accepted as valid movement)

## 8. Address / geocoding ambiguity (build after v0.1)
- Addresses that match multiple locations (e.g. "123 Main St" exists in many
  cities)
- Partial/incomplete addresses
- Non-Latin script addresses fed to Latin-script-only geocoders

---

## Format notes for each generator function
Every function in v0.1 should:
1. Return output in at least one of: raw dict, GeoJSON, Shapely geometry
2. Include a `.explain()` or docstring describing the real bug this simulates
3. Have a corresponding test asserting the generator itself produces the
   intended malformed/edge condition (meta, but this is the credibility
   signal for an SDET-built tool)