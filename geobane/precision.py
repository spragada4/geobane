"""
Precision & numeric edge case generators.

Geospatial coordinates are floating-point numbers, which means they inherit
every classic floating-point failure mode: precision loss at type
boundaries, NaN/Infinity propagation, and misleading over-precision that
implies false accuracy. These bugs are especially nasty because the values
often "look" like normal coordinates until they're used in arithmetic.
"""

import random
import struct


def float32_boundary_coordinate():
    """
    Generates a coordinate with more precision than a 32-bit float can
    represent, then shows the value after being round-tripped through
    float32. Simulates pipelines that assume float64 throughout but hit a
    float32 boundary somewhere (e.g. a graphics/rendering library, a
    binary format, or a poorly configured database column).
    """
    lat = round(random.uniform(-90, 90), 10)
    lng = round(random.uniform(-180, 180), 10)

    # round-trip through 32-bit float to show precision loss
    lat_f32 = struct.unpack("f", struct.pack("f", lat))[0]
    lng_f32 = struct.unpack("f", struct.pack("f", lng))[0]

    return {
        "original_float64": {"lat": lat, "lng": lng},
        "after_float32_roundtrip": {"lat": lat_f32, "lng": lng_f32},
        "drift_meters_approx": round(abs(lat - lat_f32) * 111320, 4),
        "explanation": (
            f"Original coordinate had 10 decimal places of precision "
            f"(sub-millimeter). After passing through a float32 boundary, "
            f"it drifted to {lat_f32}. This looks like a tiny difference "
            f"but compounds badly in repeated calculations, distance sums, "
            f"or anything comparing coordinates for exact equality."
        ),
    }


def nan_infinity_injection():
    """
    Generates a geometry with NaN or Infinity injected into one coordinate
    value - simulating output from a failed calculation (e.g. division by
    zero in a projection formula) that gets passed downstream instead of
    being caught.
    """
    bad_value = random.choice([float("nan"), float("inf"), float("-inf")])
    lat = round(random.uniform(-90, 90), 4)

    return {
        "type": "Point",
        "coordinates": [bad_value, lat],
        "bad_value_type": (
            "NaN" if bad_value != bad_value
            else ("Infinity" if bad_value > 0 else "-Infinity")
        ),
        "explanation": (
            f"Longitude is {bad_value!r} instead of a real number - "
            f"typically the result of an upstream division-by-zero or "
            f"undefined trig operation (e.g. projecting a pole through "
            f"Mercator). JSON itself has no native representation for "
            f"NaN/Infinity, so serialization behavior here is itself a "
            f"meaningful test: does the system error, or silently emit "
            f"invalid JSON?"
        ),
    }


def absurd_overprecision():
    """
    Generates a coordinate with unrealistically high precision (16+
    decimal places - sub-nanometer scale), which usually signals
    unintended floating-point accumulation upstream rather than genuine
    measurement precision. GPS itself is only accurate to a few meters.
    """
    lat = round(random.uniform(-90, 90), 4) + random.random() * 1e-14
    lng = round(random.uniform(-180, 180), 4) + random.random() * 1e-14

    return {
        "lat": lat,
        "lng": lng,
        "decimal_places": len(str(lat).split(".")[-1]),
        "explanation": (
            "Coordinate precision here implies sub-nanometer accuracy, "
            "which is physically meaningless for GPS-derived data (typical "
            "real-world accuracy is 1-5 meters). This pattern usually "
            "signals floating-point error accumulation rather than genuine "
            "precision, and can bloat storage/transmission size "
            "significantly at scale."
        ),
    }


def integer_where_float_expected():
    """
    Generates a coordinate pair as plain integers instead of floats -
    e.g. (51, 0) instead of (51.0, 0.0). Valid in most languages, but can
    break strict type-checking code, some serialization formats, or
    calculations that behave differently under integer vs float division.
    """
    lat = random.randint(-90, 90)
    lng = random.randint(-180, 180)

    return {
        "lat": lat,
        "lng": lng,
        "types": {"lat": type(lat).__name__, "lng": type(lng).__name__},
        "explanation": (
            f"Coordinates ({lat}, {lng}) are plain integers, not floats. "
            f"Structurally valid, but code performing division or "
            f"expecting float-typed input (common in strictly-typed "
            f"languages, or Python 2-style integer division bugs) may "
            f"behave unexpectedly."
        ),
    }
