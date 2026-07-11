from geobane.antimeridian import (
    crossing_polygon,
    crossing_linestring,
    wraparound_bbox,
)


def test_crossing_polygon_structure():
    result = crossing_polygon()
    assert result["type"] == "Polygon"
    lngs = [pt[0] for pt in result["coordinates"][0]]
    # confirm it actually crosses - both very high and very low longitudes present
    assert any(l > 170 for l in lngs)
    assert any(l < -170 for l in lngs)


def test_crossing_polygon_naive_bbox_is_misleadingly_wide():
    result = crossing_polygon()
    bbox = result["naive_bbox"]
    # the naive bbox should span nearly the whole globe (the bug we're demonstrating)
    span = bbox["max_lng"] - bbox["min_lng"]
    assert span > 300


def test_crossing_linestring_spans_date_line():
    result = crossing_linestring()
    start_lng, end_lng = result["coordinates"][0][0], result["coordinates"][1][0]
    assert start_lng > 170
    assert end_lng < -170


def test_wraparound_bbox_min_greater_than_max():
    result = wraparound_bbox()
    # this is the whole point: min > max signals a wraparound bbox
    assert result["min_lng"] > result["max_lng"]
