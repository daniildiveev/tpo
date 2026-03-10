"""Tests for system function."""

import math
import pytest

from src.system.system_function import SystemFunction, DomainError
from src.trig.trig_module import TrigModule
from src.trig.trig_stub import TrigStub
from src.log.log_module import LogModule
from src.log.log_stub import LogStub

TIGHT = 1e-5
PI = 3.14159265358979323846


class TestSystemTrigBranch:
    """x <= 0: trigonometric branch."""

    def test_negative_value_computes(self):
        sys_fn = SystemFunction()
        result = sys_fn.compute(-0.5)
        assert isinstance(result, float)

    @pytest.mark.parametrize("x", [-0.1, -0.5, -1.0, -2.0])
    def test_typical_negative_x(self, x):
        sys_fn = SystemFunction()
        result = sys_fn.compute(x)
        assert isinstance(result, float)
        assert not math.isnan(result)
        assert not math.isinf(result)

    def test_zero_raises_csc_undefined(self):
        """At x=0, sin(0)=0 so csc is undefined."""
        sys_fn = SystemFunction()
        with pytest.raises(DomainError):
            sys_fn.compute(0.0)


class TestSystemLogBranch:
    """x > 0: logarithmic branch."""

    def test_positive_value_computes(self):
        sys_fn = SystemFunction()
        result = sys_fn.compute(2.0)
        assert isinstance(result, float)

    @pytest.mark.parametrize("x", [0.5, 1.5, 2.0, 5.0, 10.0])
    def test_typical_positive_x(self, x):
        sys_fn = SystemFunction()
        result = sys_fn.compute(x)
        assert isinstance(result, float)
        assert not math.isnan(result)
        assert not math.isinf(result)

    def test_x_equal_one_raises(self):
        sys_fn = SystemFunction()
        with pytest.raises(DomainError, match="ln\\(x\\)=0"):
            sys_fn.compute(1.0)


class TestSystemBoundary:
    def test_near_zero_negative(self):
        sys_fn = SystemFunction()
        r = sys_fn.compute(-0.001)
        assert isinstance(r, float)

    def test_near_zero_positive(self):
        sys_fn = SystemFunction()
        r = sys_fn.compute(0.001)
        assert isinstance(r, float)


class TestSystemSingularities:
    def test_sin_zero_raises(self):
        sys_fn = SystemFunction()
        with pytest.raises(DomainError):
            sys_fn.compute(-PI)

    def test_cos_zero_raises(self):
        sys_fn = SystemFunction()
        with pytest.raises(DomainError):
            sys_fn.compute(-PI / 2)


class TestSystemWithStubs:
    def test_trig_stub_integration(self):
        sys_fn = SystemFunction(trig=TrigStub(), log=LogModule())
        result = sys_fn.compute(-0.5)
        assert isinstance(result, float)

    def test_log_stub_integration(self):
        sys_fn = SystemFunction(trig=TrigModule(), log=LogStub())
        result = sys_fn.compute(2.0)
        assert isinstance(result, float)
