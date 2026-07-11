"""
Degenerate & invalid geometry generators.

Malformed geometries that are structurally "shaped like" valid GeoJSON but
violate geometric rules - zero area, self-intersection, unclosed rings, or
too few points. Many parsers accept these without validation and only fail
later, deep in area/intersection/rendering calculations.
"""

import random


def zero_area_polygon():
    """
    Generates a polygon where all points are collinear, giving it zero area.
    Passes basic "is this a polygon" structural checks but any area
    calculation should return 0, and many downstream systems (e.g. anything
    dividing by area) will break.
    """
    lat = round(random.uniform(-80, 80), 4)
    lngs = sorted(round(random.uniform(-170, 170), 4) for _ in range(3))
    coords = [[lngs[0], lat], [lngs[1], lat], [lngs[2], lat], [lngs[0], lat]]

    return {
        "type": "Polygon",
        "coordinates": [coords],
        "explanation": (
            "All points share the same latitude, making this polygon "
            "collinear with zero area. Structurally valid GeoJSON, but "
            "geometrically degenerate - area calculations return 0, and "
            "point-in-polygon tests behave unpredictably."
        ),
    }


def single_point_polygon():
    """
    Generates a 'polygon' with fewer than 3 unique vertices - not actually
    a valid polygon at all, but sometimes produced by buggy upstream code
    (e.g. a bounding box collapsed to a point).
    """
    lat = round(random.uniform(-90, 90), 4)
    lng = round(random.uniform(-180, 180), 4)
    coords = [[lng, lat], [lng, lat], [lng, lat]]

    return {
        "type": "Polygon",
        "coordinates": [coords],
        "explanation": (
            "Only one unique coordinate repeated - not a valid polygon "
            "(needs at least 3 distinct vertices plus closure), but "
            "structurally parses as one in permissive GeoJSON readers."
        ),
    }


def self_intersecting_bowtie():
    """
    Generates a classic 'bowtie' polygon - four points where the edges
    cross each other, creating two triangular lobes that overlap at the
    center. Common source of silent area/intersection bugs.
    """
    return {
        "type": "Polygon",
        "coordinates": [[
            [0.0, 0.0],
            [1.0, 1.0],
            [1.0, 0.0],
            [0.0, 1.0],
            [0.0, 0.0],
        ]],
        "explanation": (
            "This ring self-intersects at the center, forming a bowtie "
            "shape instead of a simple polygon. The OGC Simple Features "
            "spec considers this invalid, but naive parsers accept it - "
            "area and centroid calculations on it produce misleading "
            "results rather than errors."
        ),
    }


def unclosed_ring():
    """
    Generates a polygon ring where the first and last points don't match -
    technically required by GeoJSON spec but frequently violated by
    hand-written or buggy exporters.
    """
    coords = [
        [round(random.uniform(-170, 170), 4), round(random.uniform(-80, 80), 4)]
        for _ in range(4)
    ]
    # deliberately NOT closing the ring (no repeat of first point at end)

    return {
        "type": "Polygon",
        "coordinates": [coords],
        "explanation": (
            "GeoJSON spec (RFC 7946) requires the first and last positions "
            "of a polygon ring to be identical. This ring is left "
            "unclosed - some parsers auto-close it silently, others error, "
            "and some produce an invalid/open shape."
        ),
    }
