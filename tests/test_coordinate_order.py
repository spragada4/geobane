from geobane.coordinate_order import (
    swapped_pair,
    plausible_swap_near_equator,
    invalid_when_swapped,
)


def test_swapped_pair_structure():
    result = swapped_pair(lat=51.5, lng=-0.12)
    assert result["correct"] == (51.5, -0.12)
    assert result["swapped"] == (-0.12, 51.5)
    assert "explanation" in result


def test_swapped_pair_random_generation():
    result = swapped_pair()
    lat, lng = result["correct"]
    assert -90 <= lat <= 90
    assert -180 <= lng <= 180


def test_plausible_swap_near_equator_both_orders_in_range():
    result = plausible_swap_near_equator()
    lat, lng = result["correct"]
    swapped_lat, swapped_lng = result["swapped"]
    # both orders should be numerically "valid" - that's the point
    assert -90 <= lat <= 90 and -180 <= lng <= 180
    assert -90 <= swapped_lat <= 90 and -180 <= swapped_lng <= 180


def test_invalid_when_swapped_breaks_range():
    result = invalid_when_swapped()
    swapped_lat, _ = result["swapped"]
    # the swapped latitude should be out of valid lat range (-90..90)
    assert swapped_lat < -90 or swapped_lat > 90
