"""
Geobane - adversarial test-data generator for geospatial systems.

Generates known edge cases that break geospatial code: coordinate order
confusion, antimeridian crossings, degenerate geometry, CRS mismatches,
and floating-point precision bugs.

Usage:
    from geobane import coordinate_order, antimeridian, degenerate
    from geobane import crs_mismatch, precision

    bad_coord = coordinate_order.swapped_pair()
    tricky_polygon = antimeridian.crossing_polygon()
"""

from . import coordinate_order
from . import antimeridian
from . import degenerate
from . import crs_mismatch
from . import precision

__version__ = "0.1.0"

__all__ = [
    "coordinate_order",
    "antimeridian",
    "degenerate",
    "crs_mismatch",
    "precision",
]
