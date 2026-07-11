import math
from geobane.precision import (
    float32_boundary_coordinate,
    nan_infinity_injection,
    absurd_overprecision,
    integer_where_float_expected,
)


def test_float32_boundary_shows_drift():
    result = float32_boundary_coordinate()
    assert "drift_meters_approx" in result
    assert result["drift_meters_approx"] >= 0


def test_nan_infinity_injection_produces_non_finite_value():
    result = nan_infinity_injection()
    lng = result["coordinates"][0]
    assert math.isnan(lng) or math.isinf(lng)


def test_absurd_overprecision_has_many_decimals():
    result = absurd_overprecision()
    assert result["decimal_places"] >= 10


def test_integer_where_float_expected_types_are_int():
    result = integer_where_float_expected()
    assert result["types"]["lat"] == "int"
    assert result["types"]["lng"] == "int"
