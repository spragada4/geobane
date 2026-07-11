"""
CRS / projection mismatch generators.

Coordinates are meaningless without a known reference system attached, but
many pipelines pass raw (x, y) or (lng, lat) values around without CRS
metadata, or transform between systems incorrectly. The two most common
real-world systems are:
  - EPSG:4326 (WGS84) - lng/lat in degrees, the GPS/GeoJSON default
  - EPSG:3857 (Web Mercator) - x/y in meters, used by most web map tiles

Feeding EPSG:3857 values into code expecting EPSG:4326 (or vice versa)
doesn't crash - it just produces wrong, often plausible-looking results.
"""

import math
import random


def wgs84_point():
    """
    Generates a valid EPSG:4326 (WGS84) point in degrees - the 'correct'
    baseline this module's other functions will misrepresent.
    """
    lat = round(random.uniform(-85, 85), 6)
    lng = round(random.uniform(-180, 180), 6)
    return {"lat": lat, "lng": lng, "crs": "EPSG:4326"}


def _wgs84_to_web_mercator(lat, lng):
    """Standard WGS84 -> Web Mercator (EPSG:3857) conversion."""
    x = lng * 20037508.34 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    y = y * 20037508.34 / 180
    return round(x, 4), round(y, 4)


def mercator_fed_as_wgs84():
    """
    Generates a valid EPSG:3857 (Web Mercator) coordinate pair, but labels
    it as if it were EPSG:4326 - simulating the extremely common bug of
    forgetting to transform between CRSs before use.

    Web Mercator x/y values are in meters and routinely exceed +/-180 or
    +/-90, so this either causes an obvious range error (best case) or,
    for values that happen to fall in range, silently produces a wildly
    wrong location (worst case).
    """
    source = wgs84_point()
    merc_x, merc_y = _wgs84_to_web_mercator(source["lat"], source["lng"])

    return {
        "mislabeled_as": "EPSG:4326",
        "actually_is": "EPSG:3857",
        "lat": merc_y,   # mercator y mislabeled as lat
        "lng": merc_x,   # mercator x mislabeled as lng
        "true_wgs84_source": source,
        "explanation": (
            f"These values ({merc_x}, {merc_y}) are real Web Mercator "
            f"meters, mislabeled as WGS84 degrees. They likely fall wildly "
            f"outside the valid -180..180 / -90..90 degree range, which a "
            f"correct system should reject - but far too many systems "
            f"instead clamp, wrap, or silently accept them, placing the "
            f"'point' in the wrong hemisphere entirely."
        ),
    }


def missing_crs_metadata():
    """
    Generates a raw coordinate pair with NO CRS information attached at
    all - just two numbers. Simulates data exported from a system that
    doesn't tag its CRS, leaving the receiving system to guess (often
    wrongly) whether it's WGS84 degrees or a projected CRS in meters.
    """
    # deliberately ambiguous magnitude - could plausibly be either
    x = round(random.uniform(-179, 179), 4)
    y = round(random.uniform(-89, 89), 4)

    return {
        "x": x,
        "y": y,
        "crs": None,
        "explanation": (
            f"Coordinate pair ({x}, {y}) has no CRS metadata. Magnitude "
            f"alone can't disambiguate WGS84 degrees from a local/projected "
            f"CRS with a similar numeric range - a system must fail loudly "
            f"on missing CRS rather than assuming a default."
        ),
    }


def out_of_range_for_mercator():
    """
    Generates coordinates near the poles (beyond ~85.05 degrees latitude)
    where Web Mercator's projection formula produces Infinity or extremely
    large values, since Mercator cannot represent the poles. Tests whether
    a system correctly rejects/clips these instead of producing Inf/NaN.
    """
    lat = round(random.uniform(85.06, 90) * random.choice([1, -1]), 6)
    lng = round(random.uniform(-180, 180), 6)

    return {
        "lat": lat,
        "lng": lng,
        "crs": "EPSG:4326",
        "explanation": (
            f"Latitude {lat} exceeds Web Mercator's valid range "
            f"(~+/-85.05 degrees). Projecting this to EPSG:3857 produces "
            f"Infinity or an extremely large y-value - a correct system "
            f"should clip or reject this before projecting, not propagate "
            f"Infinity downstream."
        ),
    }
