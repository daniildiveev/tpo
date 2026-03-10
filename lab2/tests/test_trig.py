"""Tests for trigonometric module."""

import math
import pytest

from src.trig.trig_module import TrigModule
from src.trig.trig_stub import TrigStub

TIGHT = 1e-6
PI = 3.14159265358979323846


class TestTrigModuleKnownValues:
    def test_sin_cos_tan(self):
        trig = TrigModule()
        x = -0.5
        assert trig.sin(x) == pytest.approx(math.sin(x), abs=TIGHT)
        assert trig.cos(x) == pytest.approx(math.cos(x), abs=TIGHT)
        assert trig.tan(x) == pytest.approx(math.tan(x), abs=TIGHT)

    def test_cot_sec_csc(self):
        trig = TrigModule()
        x = -0.3
        assert trig.cot(x) == pytest.approx(1.0 / math.tan(x), abs=TIGHT)
        assert trig.sec(x) == pytest.approx(1.0 / math.cos(x), abs=TIGHT)
        assert trig.csc(x) == pytest.approx(1.0 / math.sin(x), abs=TIGHT)


class TestTrigModuleParametrized:
    @pytest.mark.parametrize("x", [-0.1, -0.5, -1.0, -2.0, -PI / 4])
    def test_all_functions_vs_math(self, x):
        trig = TrigModule()
        if abs(math.sin(x)) > 1e-10 and abs(math.cos(x)) > 1e-10:
            assert trig.sin(x) == pytest.approx(math.sin(x), abs=TIGHT)
            assert trig.cos(x) == pytest.approx(math.cos(x), abs=TIGHT)
            assert trig.tan(x) == pytest.approx(math.tan(x), abs=TIGHT)
            assert trig.cot(x) == pytest.approx(1.0 / math.tan(x), abs=TIGHT)
            assert trig.sec(x) == pytest.approx(1.0 / math.cos(x), abs=TIGHT)
            assert trig.csc(x) == pytest.approx(1.0 / math.sin(x), abs=TIGHT)


class TestTrigModuleSingularities:
    def test_tan_at_pi_half_raises(self):
        trig = TrigModule()
        with pytest.raises(ValueError, match="tan undefined"):
            trig.tan(-PI / 2)

    def test_csc_at_zero_raises(self):
        trig = TrigModule()
        with pytest.raises(ValueError, match="csc undefined"):
            trig.csc(0.0)

    def test_cot_at_pi_raises(self):
        trig = TrigModule()
        with pytest.raises(ValueError, match="cot undefined"):
            trig.cot(-PI)


class TestTrigStub:
    def test_stub_returns_values(self):
        stub = TrigStub()
        x = -0.5
        s = stub.sin(x)
        c = stub.cos(x)
        assert abs(s - math.sin(x)) < 0.1
        assert abs(c - math.cos(x)) < 0.1
