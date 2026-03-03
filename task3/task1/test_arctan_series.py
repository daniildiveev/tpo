import math
import pytest

from arctan_series import arctan_series

TIGHT = 1e-9
MED   = 1e-6


class TestKnownValues:

    def test_arctan_zero(self):
        assert arctan_series(0.0) == pytest.approx(0.0, abs=TIGHT)

    def test_arctan_one(self):
        assert arctan_series(1.0) == pytest.approx(math.pi / 4, abs=TIGHT)

    def test_arctan_minus_one(self):
        assert arctan_series(-1.0) == pytest.approx(-math.pi / 4, abs=TIGHT)

    def test_arctan_one_over_sqrt3(self):
        assert arctan_series(1.0 / math.sqrt(3)) == pytest.approx(math.pi / 6, abs=TIGHT)

    def test_arctan_sqrt3(self):
        assert arctan_series(math.sqrt(3)) == pytest.approx(math.pi / 3, abs=TIGHT)

    def test_arctan_minus_sqrt3(self):
        assert arctan_series(-math.sqrt(3)) == pytest.approx(-math.pi / 3, abs=TIGHT)


class TestSmallInputs:

    def test_arctan_very_small_positive(self):
        x = 1e-10
        assert arctan_series(x) == pytest.approx(x, rel=1e-6)

    def test_arctan_very_small_negative(self):
        x = -1e-10
        assert arctan_series(x) == pytest.approx(x, rel=1e-6)

    def test_arctan_small_value_0_1(self):
        x = 0.1
        assert arctan_series(x) == pytest.approx(math.atan(x), abs=TIGHT)


class TestOddSymmetry:

    @pytest.mark.parametrize("x", [0.5, 1.0, 2.0, 10.0, 100.0])
    def test_odd_symmetry(self, x: float):
        assert arctan_series(-x) == pytest.approx(-arctan_series(x), abs=TIGHT)


class TestBranchBoundary:

    def test_continuity_at_plus_one(self):
        left  = arctan_series(0.9999)
        right = arctan_series(1.0001)
        assert abs(left - right) < 1e-3

    def test_continuity_at_minus_one(self):
        left  = arctan_series(-0.9999)
        right = arctan_series(-1.0001)
        assert abs(left - right) < 1e-3

    def test_exact_boundary_plus_one_both_branches(self):
        val_at_1       = arctan_series(1.0)
        val_just_above = arctan_series(1.0 + 1e-8)
        assert abs(val_at_1 - val_just_above) < 1e-5


class TestComplementaryIdentity:

    @pytest.mark.parametrize("x", [2.0, 3.0, 5.0, 10.0, 1000.0])
    def test_complementary_identity(self, x: float):
        total = arctan_series(x) + arctan_series(1.0 / x)
        assert total == pytest.approx(math.pi / 2, abs=TIGHT)


class TestConvergence:

    @pytest.mark.parametrize("x", [0.1, 0.3, 0.5, 0.7, 0.9, 1.0,
                                    -0.5, -1.0,
                                    1.5, 2.0, 5.0, 10.0])
    def test_matches_math_atan(self, x: float):
        assert arctan_series(x) == pytest.approx(math.atan(x), abs=MED)

    def test_high_precision_epsilon(self):
        x = 0.7
        result = arctan_series(x, epsilon=1e-15)
        assert abs(result - math.atan(x)) < 1e-12


class TestLargeX:

    def test_large_positive_approaches_pi_over_2(self):
        assert arctan_series(1e6) == pytest.approx(math.pi / 2, abs=1e-5)

    def test_large_negative_approaches_minus_pi_over_2(self):
        assert arctan_series(-1e6) == pytest.approx(-math.pi / 2, abs=1e-5)

    def test_very_large_x(self):
        assert arctan_series(1e12) == pytest.approx(math.pi / 2, abs=1e-5)


class TestEpsilonParameter:

    def test_loose_epsilon_still_in_bounds(self):
        x = 0.5
        loose_eps = 1e-3
        result = arctan_series(x, epsilon=loose_eps)
        assert abs(result - math.atan(x)) < loose_eps * 10

    def test_default_epsilon_is_tight(self):
        result = arctan_series(0.9)
        assert abs(result - math.atan(0.9)) < 1e-9

    def test_epsilon_1e_4_coarser_than_1e_10(self):
        x = 0.8
        coarse = arctan_series(x, epsilon=1e-4)
        fine   = arctan_series(x, epsilon=1e-10)
        assert abs(fine - math.atan(x)) <= abs(coarse - math.atan(x)) + 1e-12
