"""Tests for logarithmic module."""

import math
import pytest

from src.log.log_module import LogModule
from src.log.log_stub import LogStub

TIGHT = 1e-5


class TestLogModuleKnownValues:
    def test_ln(self):
        log = LogModule()
        assert log.ln(1.0) == pytest.approx(0.0, abs=TIGHT)
        assert log.ln(2.0) == pytest.approx(math.log(2), abs=TIGHT)

    def test_log3_log5_log10(self):
        log = LogModule()
        x = 10.0
        assert log.log3(x) == pytest.approx(math.log(x) / math.log(3), abs=TIGHT)
        assert log.log5(x) == pytest.approx(math.log(x) / math.log(5), abs=TIGHT)
        assert log.log10(x) == pytest.approx(math.log(x) / math.log(10), abs=TIGHT)


class TestLogModuleParametrized:
    @pytest.mark.parametrize("x", [0.5, 1.5, 2.0, 3.0, 5.0, 10.0])
    def test_logs_vs_math(self, x):
        log = LogModule()
        assert log.ln(x) == pytest.approx(math.log(x), abs=TIGHT)
        assert log.log3(x) == pytest.approx(math.log(x, 3), abs=TIGHT)
        assert log.log5(x) == pytest.approx(math.log(x, 5), abs=TIGHT)
        assert log.log10(x) == pytest.approx(math.log(x, 10), abs=TIGHT)


class TestLogModuleDomain:
    def test_ln_zero_raises(self):
        log = LogModule()
        with pytest.raises(ValueError, match="x > 0"):
            log.ln(0.0)

    def test_ln_negative_raises(self):
        log = LogModule()
        with pytest.raises(ValueError, match="x > 0"):
            log.ln(-1.0)

    def test_log3_negative_raises(self):
        log = LogModule()
        with pytest.raises(ValueError, match="x > 0"):
            log.log3(-1.0)


class TestLogStub:
    def test_stub_returns_values(self):
        stub = LogStub()
        x = 2.0
        assert abs(stub.ln(x) - math.log(x)) < 0.1
        assert abs(stub.log3(x) - math.log(x, 3)) < 0.1
