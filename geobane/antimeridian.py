"""
Antimeridian / date-line crossing generators.

The antimeridian (±180° longitude) is where naive geospatial logic breaks:
a polygon or bounding box that "wraps" across this line often gets
misinterpreted by systems using simple min/max longitude math, which assume
the shape spans the entire globe instead of a thin sliver near the date line.

Real places this affects: Fiji, Russia's Chukotka Peninsula, and the
Aleutian Islands (Alaska) all straddle or sit near the antimeridian.
"""

import random


def crossing_polygon():
    """
    Generates a simple polygon (list of [lng, lat] points, GeoJSON order)
    that crosses the antimeridian - e.g. spanning from 179° to -179°.

    A naive bounding-box calculation on this polygon would compute a
    bounding box spanning nearly the entire globe (-179 to 179), instead
    of recognizing it's actually a narrow sliver near the date line.

    Returns a dict with the polygon, its "naive" (incorrect) bounding box,
    and the correct bounding box a date-line-aware system should produce.
    """
    # a small polygon straddling the date line
    coords = [
        [179.0, 10.0],
        [-179.0, 10.0],
        [-179.0, -10.0],
        [179.0, -10.0],
        [179.0, 10.0],  # closed ring
    ]

    lngs = [c[0] for c in coords]
    naive_bbox = {
        "min_lng": min(lngs),
        "max_lng": max(lngs),
        "min_lat": -10.0,
        "max_lat": 10.0,
    }

    return {
        "type": "Polygon",
        "coordinates": [coords],
        "naive_bbox": naive_bbox,
        "explanation": (
            "This polygon crosses the antimeridian (179° to -179°). A naive "
            "min/max bounding box calculation gives min_lng=-179, max_lng=179 "
            "- which looks like it spans nearly the whole globe (358 degrees) "
            "when the actual polygon is a 2-degree-wide sliver near the date "
            "line. Systems must detect the crossing and split the bbox, or "
            "represent it as two boxes, instead of taking a naive min/max."
        ),
    }


def crossing_linestring():
    """
    Generates a LineString (GeoJSON [lng, lat] order) that crosses the
    antimeridian - simulating e.g. a flight path or shipping route from
    Alaska to Russia.
    """
    start_lng = round(random.uniform(170, 179.9), 4)
    end_lng = round(random.uniform(-179.9, -170), 4)
    lat = round(random.uniform(-60, 60), 4)

    return {
        "type": "LineString",
        "coordinates": [[start_lng, lat], [end_lng, lat]],
        "explanation": (
            f"LineString from lng={start_lng} to lng={end_lng} crosses the "
            f"antimeridian. Naive distance/interpolation math will compute "
            f"this as a ~{abs(end_lng - start_lng):.1f} degree journey "
            f"(nearly halfway around the world) instead of the true short "
            f"distance across the date line."
        ),
    }


def wraparound_bbox():
    """
    Generates a bounding box / map viewport that wraps around 180/-180,
    e.g. simulating a map view centered near the date line.

    Returns min_lng > max_lng, which is a valid way to represent a
    wraparound bbox but breaks systems that assume min_lng < max_lng always.
    """
    min_lng = round(random.uniform(170, 179), 4)
    max_lng = round(random.uniform(-179, -170), 4)

    return {
        "min_lng": min_lng,
        "max_lng": max_lng,
        "min_lat": round(random.uniform(-90, 45), 4),
        "max_lat": round(random.uniform(45, 90), 4),
        "explanation": (
            f"This bbox has min_lng ({min_lng}) > max_lng ({max_lng}), "
            f"which correctly represents a viewport wrapping around the "
            f"date line - but will break any code with an unchecked "
            f"assumption that min_lng < max_lng."
        ),
    }
