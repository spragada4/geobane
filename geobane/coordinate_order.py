"""
Coordinate order / axis confusion generators.

The single most common real-world geospatial bug: different standards
disagree on whether coordinates are (lat, lng) or (lng, lat). GeoJSON spec
says (lng, lat). Humans and many APIs say (lat, lng). Systems that assume
the wrong order fail silently instead of erroring, because both orders often
produce numerically "valid" coordinates.
"""

import random


def swapped_pair(lat=None, lng=None):
    """
    Returns a (lat, lng) pair alongside its incorrectly-swapped (lng, lat)
    version, to test whether a system distinguishes between them correctly.

    If lat/lng aren't provided, generates a random valid coordinate.

    Returns a dict:
        {
            "correct": (lat, lng),
            "swapped": (lng, lat),
            "explanation": str
        }
    """
    if lat is None:
        lat = round(random.uniform(-90, 90), 6)
    if lng is None:
        lng = round(random.uniform(-180, 180), 6)

    return {
        "correct": (lat, lng),
        "swapped": (lng, lat),
        "explanation": (
            f"Correct order is (lat={lat}, lng={lng}). "
            f"A system with an axis-order bug would instead receive "
            f"(lat={lng}, lng={lat}), which may silently pass validation "
            f"if both values happen to fall in valid range."
        ),
    }


def plausible_swap_near_equator():
    """
    Generates a coordinate near the equator/prime meridian where both the
    correct and swapped order are numerically plausible (small values,
    both within -90..90 range) — the sneakiest version of this bug, since
    range-based validation won't catch it.
    """
    lat = round(random.uniform(-45, 45), 6)
    lng = round(random.uniform(-45, 45), 6)
    return swapped_pair(lat=lat, lng=lng)


def invalid_when_swapped():
    """
    Generates a coordinate that is valid as (lat, lng) but becomes
    out-of-range when swapped — e.g. a high-latitude point with a longitude
    value that exceeds ±90, which would be invalid as a latitude.
    This is the case a correct system SHOULD reject if swapped, and a
    buggy one might clamp or wrap instead of erroring.
    """
    lat = round(random.uniform(-90, 90), 6)
    lng = round(random.uniform(91, 180) * random.choice([1, -1]), 6)
    return swapped_pair(lat=lat, lng=lng)
