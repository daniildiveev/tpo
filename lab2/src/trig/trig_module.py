"""Trigonometric functions expressed through sin(x)."""

from ..base.sin_series import sin_series

PI = 3.14159265358979323846
PI_HALF = PI / 2


class TrigModule:
    """Trigonometric module: cos, tan, cot, sec, csc via sin series."""

    def __init__(self, epsilon: float = 1e-10):
        self._epsilon = epsilon

    def sin(self, x: float) -> float:
        return sin_series(x, self._epsilon)

    def cos(self, x: float) -> float:
        return sin_series(PI_HALF - x, self._epsilon)

    def tan(self, x: float) -> float:
        c = self.cos(x)
        if abs(c) < 1e-10:
            raise ValueError("tan undefined: cos(x)=0")
        return self.sin(x) / c

    def cot(self, x: float) -> float:
        s = self.sin(x)
        if abs(s) < 1e-10:
            raise ValueError("cot undefined: sin(x)=0")
        return self.cos(x) / s

    def sec(self, x: float) -> float:
        c = self.cos(x)
        if abs(c) < 1e-10:
            raise ValueError("sec undefined: cos(x)=0")
        return 1.0 / c

    def csc(self, x: float) -> float:
        s = self.sin(x)
        if abs(s) < 1e-10:
            raise ValueError("csc undefined: sin(x)=0")
        return 1.0 / s
