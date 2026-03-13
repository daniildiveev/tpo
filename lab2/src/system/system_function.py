from ..trig.trig_module import TrigModule
from ..log.log_module import LogModule


class DomainError(Exception):
    """Raised when x is outside domain or at singular points."""
    pass


class SystemFunction:
    def __init__(
        self,
        trig = None,
        log = None,
    ):
        self._trig = trig or TrigModule()
        self._log = log or LogModule()

    def compute(self, x: float) -> float:
        if x <= 0:
            return self._trig_branch(x)
        else:
            return self._log_branch(x)

    def _trig_branch(self, x: float) -> float:
        """x <= 0: ((((((((sin-csc)/sec)^2)^2)-cos)+cos)/sec) + ..."""
        try:
            s = self._trig.sin(x)
            c = self._trig.cos(x)
            t = self._trig.tan(x)
            cot = self._trig.cot(x)
            sec = self._trig.sec(x)
            csc = self._trig.csc(x)
        except ValueError as e:
            raise DomainError(str(e)) from e

        # Part 1: ((((((((sin(x) - csc(x)) / sec(x)) ^ 2) ^ 2) - cos(x)) + cos(x)) / sec(x))
        a = (s - csc) / sec
        b = a * a
        c_val = b * b
        d = c_val - c
        e = d + c
        part1 = e / sec

        # Part 2: (sec(x) - (sec(x) - sec(x))) + ((cot(x) * sec(x)) / csc(x))
        g = sec - (sec - sec)
        h = (cot * sec) / csc
        part2a = g + h

        # Part 3: cos(x) * ((((csc^2 + cos) * (cos - (sec^2 - sin))) + (cos * (sin * tan))))
        j = csc * csc + c
        k = sec * sec - s
        l_val = c - k
        m = j * l_val
        n = s * t
        o = c * n
        p = m + o
        q = c * p
        part2b = part2a - q

        return part1 + part2b

    def _log_branch(self, x: float) -> float:
        """x > 0: ((((0/ln)/(log5*(log10+ln)))-ln) * ((ln-log5)/ln))"""
        try:
            ln_x = self._log.ln(x)
        except ValueError as e:
            raise DomainError(str(e)) from e

        if abs(ln_x) < 1e-15:
            raise DomainError("ln(x)=0 at x=1: division by zero")

        log3_x = self._log.log3(x)
        log5_x = self._log.log5(x)
        log10_x = self._log.log10(x)

        # (log_3(x) - log_3(x)) / ln(x) = 0
        num_part1 = 0.0
        denom = log5_x * (log10_x + ln_x)
        if abs(denom) < 1e-15:
            raise DomainError("Denominator zero in log branch")
        first_frac = num_part1 / denom
        e = first_frac - ln_x  # = -ln(x)

        # (ln(x) - log_5(x)) / ln(x)
        f = ln_x - log5_x
        g = f / ln_x

        return e * g
