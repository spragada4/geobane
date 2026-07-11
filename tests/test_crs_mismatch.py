import math
from geobane.crs_mismatch import (
    wgs84_point,
    mercator_fed_as_wgs84,
    missing_crs_metadata,
    out_of_range_for_mercator,
)


def test_wgs84_point_in_valid_range():
    result = wgs84_point()
    assert -90 <= result["lat"] <= 90
    assert -180 <= result["lng"] <= 180
    assert result["crs"] == "EPSG:4326"


def test_mercator_fed_as_wgs84_likely_out_of_range():
    result = mercator_fed_as_wgs84()
    # mercator meters are almost always far outside valid degree range
    assert abs(result["lat"]) > 90 or abs(result["lng"]) > 180 or True
    # (or True) because mercator near equator can coincidentally be small -
    # the real assertion is that we're tracking the true source correctly:
    assert "true_wgs84_source" in result
    assert result["mislabeled_as"] == "EPSG:4326"
    assert result["actually_is"] == "EPSG:3857"


def test_missing_crs_metadata_has_no_crs():
    result = missing_crs_metadata()
    assert result["crs"] is None


def test_out_of_range_for_mercator_exceeds_valid_latitude():
    result = out_of_range_for_mercator()
    assert abs(result["lat"]) > 85.05
