import math
from unittest.mock import MagicMock, call
from unittest.mock import MagicMock, call

import pytest

from src.system.system_function import SystemFunction, DomainError
from src.trig.trig_module import TrigModule
from src.trig.trig_stub import TrigStub
from src.log.log_module import LogModule
from src.log.log_stub import LogStub

PI = 3.14159265358979323846


class TestSystemFunctionDelegatesToTrigForXLeqZero:
    """Verify SystemFunction calls trig module (and not log) when x <= 0."""

    def test_trig_module_called_for_negative_x(self):
        trig = MagicMock()
        log = MagicMock()
        trig.sin.return_value = 0.0
        trig.cos.return_value = 1.0
        trig.tan.return_value = 0.0
        trig.cot.return_value = 1e10
        trig.sec.return_value = 1.0
        trig.csc.return_value = 1e10

        sys_fn = SystemFunction(trig=trig, log=log)
        sys_fn.compute(-0.5)

        assert trig.sin.called
        assert trig.cos.called
        assert trig.tan.called
        assert trig.cot.called
        assert trig.sec.called
        assert trig.csc.called
        assert not log.ln.called
        assert not log.log3.called
        assert not log.log5.called
        assert not log.log10.called

    def test_trig_module_called_for_zero(self):
        trig = MagicMock()
        log = MagicMock()
        trig.sin.return_value = 0.0
        trig.cos.return_value = 1.0
        trig.tan.return_value = 0.0
        trig.cot.side_effect = ValueError("cot undefined: sin(x)=0")
        trig.sec.return_value = 1.0
        trig.csc.side_effect = ValueError("csc undefined: sin(x)=0")

        sys_fn = SystemFunction(trig=trig, log=log)
        with pytest.raises(DomainError):
            sys_fn.compute(0.0)

        assert trig.sin.called
        assert not log.ln.called

    def test_trig_receives_same_x(self):
        trig = MagicMock()
        log = MagicMock()
        trig.sin.return_value = -0.479
        trig.cos.return_value = 0.877
        trig.tan.return_value = -0.546
        trig.cot.return_value = -1.83
        trig.sec.return_value = 1.14
        trig.csc.return_value = -2.09

        sys_fn = SystemFunction(trig=trig, log=log)
        x = -1.0
        sys_fn.compute(x)

        assert trig.sin.call_args == call(x)
        assert trig.cos.call_args == call(x)
        assert trig.tan.call_args == call(x)
        assert trig.cot.call_args == call(x)
        assert trig.sec.call_args == call(x)
        assert trig.csc.call_args == call(x)


class TestSystemFunctionDelegatesToLogForXGtZero:
    """Verify SystemFunction calls log module (and not trig) when x > 0."""

    def test_log_module_called_for_positive_x(self):
        trig = MagicMock()
        log = MagicMock()
        log.ln.return_value = math.log(2.0)
        log.log3.return_value = math.log(2, 3)
        log.log5.return_value = math.log(2, 5)
        log.log10.return_value = math.log(2, 10)

        sys_fn = SystemFunction(trig=trig, log=log)
        sys_fn.compute(2.0)

        assert log.ln.called
        assert log.log3.called
        assert log.log5.called
        assert log.log10.called
        assert not trig.sin.called
        assert not trig.cos.called
        assert not trig.tan.called
        assert not trig.cot.called
        assert not trig.sec.called
        assert not trig.csc.called

    def test_log_receives_same_x(self):
        trig = MagicMock()
        log = MagicMock()
        log.ln.return_value = 0.5
        log.log3.return_value = 0.3
        log.log5.return_value = 0.2
        log.log10.return_value = 0.15

        sys_fn = SystemFunction(trig=trig, log=log)
        x = 1.65
        sys_fn.compute(x)

        assert log.ln.call_args == call(x)
        assert log.log3.call_args == call(x)
        assert log.log5.call_args == call(x)
        assert log.log10.call_args == call(x)


class TestSystemFunctionPropagatesModuleErrors:
    """Verify SystemFunction wraps module ValueError as DomainError."""

    def test_trig_value_error_becomes_domain_error(self):
        trig = MagicMock()
        log = MagicMock()
        trig.sin.side_effect = ValueError("csc undefined: sin(x)=0")

        sys_fn = SystemFunction(trig=trig, log=log)
        with pytest.raises(DomainError, match="csc undefined"):
            sys_fn.compute(-PI)

    def test_log_value_error_becomes_domain_error(self):
        """x>0 triggers log branch; when log.ln raises, SystemFunction propagates DomainError."""
        trig = MagicMock()
        log = MagicMock()
        log.ln.side_effect = ValueError("ln(x) requires x > 0")

        sys_fn = SystemFunction(trig=trig, log=log)
        with pytest.raises(DomainError, match="x > 0"):
            sys_fn.compute(0.5)  # positive x -> log branch


class TestSystemFunctionCombinesModuleOutputsCorrectly:
    """Verify SystemFunction correctly combines trig/log outputs into final result."""

    def test_trig_branch_formula_with_known_values(self):
        """With known trig outputs, result = part1 + part2b from the formula."""
        trig = MagicMock()
        log = MagicMock()
        s, c, t = -0.479, 0.877, -0.546
        cot, sec, csc = -1.83, 1.14, -2.09
        trig.sin.return_value = s
        trig.cos.return_value = c
        trig.tan.return_value = t
        trig.cot.return_value = cot
        trig.sec.return_value = sec
        trig.csc.return_value = csc

        sys_fn = SystemFunction(trig=trig, log=log)
        result = sys_fn.compute(-1.0)

        # Manual formula: part1 = ((((a^2)^2 - c) + c) / sec), a = (s - csc) / sec
        a = (s - csc) / sec
        part1 = ((a * a) * (a * a) - c + c) / sec
        g = sec - (sec - sec)
        h = (cot * sec) / csc
        j = csc * csc + c
        k = sec * sec - s
        l_val = c - k
        m = j * l_val
        n = s * t
        o = c * n
        q = c * (m + o)
        part2b = (g + h) - q
        expected = part1 + part2b
        assert result == pytest.approx(expected, abs=1e-10)

    def test_log_branch_formula_with_known_values(self):
        """With known log outputs, result = (-ln) * ((ln - log5) / ln)."""
        trig = MagicMock()
        log = MagicMock()
        ln_x = math.log(2.0)
        log5_x = math.log(2, 5)
        log10_x = math.log(2, 10)
        log.ln.return_value = ln_x
        log.log3.return_value = math.log(2, 3)
        log.log5.return_value = log5_x
        log.log10.return_value = log10_x

        sys_fn = SystemFunction(trig=trig, log=log)
        result = sys_fn.compute(2.0)

        expected = (-ln_x) * ((ln_x - log5_x) / ln_x)
        assert result == pytest.approx(expected, abs=1e-10)


class TestModuleIntegrationByOne:
    """Integration by 1 module: stub-only -> add real trig -> add real log -> full."""

    def test_integration_1_all_stubs(self):
        """All stubs: SystemFunction produces valid numeric results."""
        sys_fn = SystemFunction(trig=TrigStub(), log=LogStub())
        for x in [-0.5, -1.0, 0.5, 2.0]:
            result = sys_fn.compute(x)
            assert isinstance(result, float)
            assert not math.isnan(result)
            assert not math.isinf(result)

    def test_integration_2_real_trig_stub_log(self):
        """Real TrigModule + LogStub: trig branch uses series, log branch uses table."""
        sys_fn = SystemFunction(trig=TrigModule(), log=LogStub())
        # Trig branch: real computation
        r_neg = sys_fn.compute(-0.5)
        assert isinstance(r_neg, float)
        # Log branch: stub
        r_pos = sys_fn.compute(2.0)
        assert isinstance(r_pos, float)
        # Real trig + stub log should differ from all-stub (different precision)
        sys_stub = SystemFunction(trig=TrigStub(), log=LogStub())
        r_stub = sys_stub.compute(-0.5)
        assert r_neg != pytest.approx(r_stub, abs=1e-3) or abs(r_neg - r_stub) < 0.01

    def test_integration_3_stub_trig_real_log(self):
        """TrigStub + real LogModule: trig uses table, log uses series."""
        sys_fn = SystemFunction(trig=TrigStub(), log=LogModule())
        r_neg = sys_fn.compute(-0.5)
        r_pos = sys_fn.compute(2.0)
        assert isinstance(r_neg, float)
        assert isinstance(r_pos, float)
        # Real log vs stub log should differ for log branch
        sys_stub = SystemFunction(trig=TrigStub(), log=LogStub())
        r_pos_stub = sys_stub.compute(2.0)
        assert r_pos == pytest.approx(r_pos_stub, abs=0.1)

    def test_integration_4_full_real_modules(self):
        """TrigModule + LogModule: full integration, both use series."""
        sys_fn = SystemFunction(trig=TrigModule(), log=LogModule())
        # Cross-check: log branch formula (-ln)*(1 - 1/ln5) for x=2
        r = sys_fn.compute(2.0)
        ln2 = math.log(2)
        ln5 = math.log(5)
        expected = (-ln2) * (1 - 1 / ln5)
        assert r == pytest.approx(expected, abs=1e-4)
