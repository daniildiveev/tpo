import math
import pytest

from src.base.sin_series import sin_series
from src.base.ln_series import ln_series

TIGHT = 1e-6
MED = 1e-4
PI = 3.14159265358


class TestSinSeriesKnownValues:
    def test_sin_zero(self):
        assert sin_series(0.0) == pytest.approx(0.0, abs=TIGHT)

    def test_sin_pi_half(self):
        assert sin_series(PI / 2) == pytest.approx(1.0, abs=TIGHT)

    def test_sin_minus_pi_half(self):
        assert sin_series(-PI / 2) == pytest.approx(-1.0, abs=TIGHT)

    def test_sin_pi(self):
        assert sin_series(PI) == pytest.approx(0.0, abs=TIGHT)

    def test_sin_minus_pi(self):
        assert sin_series(-PI) == pytest.approx(0.0, abs=TIGHT)


class TestSinSeriesSmallInputs:
    @pytest.mark.parametrize("x", [0.1, 0.01, 0.001, 1e-6])
    def test_sin_small_positive(self, x):
        assert sin_series(x) == pytest.approx(math.sin(x), abs=TIGHT)

    @pytest.mark.parametrize("x", [-0.1, -0.5, -1.0])
    def test_sin_negative(self, x):
        assert sin_series(x) == pytest.approx(math.sin(x), abs=TIGHT)


class TestSinSeriesConvergence:
    @pytest.mark.parametrize("x", [0.5, 1.0, 2.0, -1.5, -3.0])
    def test_matches_math_sin(self, x):
        assert sin_series(x) == pytest.approx(math.sin(x), abs=MED)

    def test_high_precision_epsilon(self):
        x = 0.7
        result = sin_series(x, epsilon=1e-15)
        assert abs(result - math.sin(x)) < 1e-12

    def test_reduced_to_pi_range(self):
        assert sin_series(2 * PI) == pytest.approx(0.0, abs=TIGHT)
        assert sin_series(2 * PI + PI / 2) == pytest.approx(1.0, abs=TIGHT)


class TestLnSeriesKnownValues:
    def test_ln_one(self):
        assert ln_series(1.0) == pytest.approx(0.0, abs=TIGHT)

    def test_ln_e(self):
        e = 2.718281828459045
        assert ln_series(e) == pytest.approx(1.0, abs=TIGHT)


class TestLnSeriesConvergence:
    @pytest.mark.parametrize("x", [0.5, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0])
    def test_matches_math_log(self, x):
        assert ln_series(x) == pytest.approx(math.log(x), abs=MED)

    @pytest.mark.parametrize("x", [0.1, 0.2, 0.9])
    def test_small_positive(self, x):
        assert ln_series(x) == pytest.approx(math.log(x), abs=MED)

    def test_high_precision(self):
        x = 2.5
        result = ln_series(x, epsilon=1e-12)
        assert abs(result - math.log(x)) < 1e-9


class TestLnSeriesDomain:
    def test_zero_raises(self):
        with pytest.raises(ValueError, match="x > 0"):
            ln_series(0.0)

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="x > 0"):
            ln_series(-1.0)
