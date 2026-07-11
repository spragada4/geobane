from geobane.degenerate import (
    zero_area_polygon,
    single_point_polygon,
    self_intersecting_bowtie,
    unclosed_ring,
)


def test_zero_area_polygon_all_same_latitude():
    result = zero_area_polygon()
    lats = [pt[1] for pt in result["coordinates"][0]]
    assert len(set(lats)) == 1  # all points share the same lat -> collinear


def test_single_point_polygon_only_one_unique_coord():
    result = single_point_polygon()
    coords = result["coordinates"][0]
    unique_coords = {tuple(c) for c in coords}
    assert len(unique_coords) == 1


def test_self_intersecting_bowtie_structure():
    result = self_intersecting_bowtie()
    assert result["type"] == "Polygon"
    coords = result["coordinates"][0]
    assert len(coords) == 5  # 4 distinct points + closing point


def test_unclosed_ring_first_last_differ():
    result = unclosed_ring()
    coords = result["coordinates"][0]
    assert coords[0] != coords[-1]  # deliberately unclosed
