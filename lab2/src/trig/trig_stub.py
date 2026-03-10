"""Table-based stub for trigonometric module."""

import math

# Precomputed table: x values (radians) for x <= 0, and sin, cos, tan, cot, sec, csc
# Domain: x in [-4*pi, 0], excluding n*pi and pi/2 + n*pi
_STUB_POINTS = [
    -6 * math.pi, -5.5 * math.pi, -5 * math.pi, -4.5 * math.pi, -4 * math.pi,
    -3.5 * math.pi, -3 * math.pi, -2.5 * math.pi, -2 * math.pi, -1.5 * math.pi,
    -1.25 * math.pi, -1.0 * math.pi, -0.75 * math.pi, -0.5 * math.pi, -0.25 * math.pi,
    -0.5, -0.1, -0.01, -0.001,
]


def _build_stub_table():
    table = {}
    for x in _STUB_POINTS:
        if abs(math.sin(x)) < 1e-10 or abs(math.cos(x)) < 1e-10:
            continue
        table[x] = {
            "sin": math.sin(x),
            "cos": math.cos(x),
            "tan": math.tan(x),
            "cot": 1.0 / math.tan(x) if math.tan(x) != 0 else None,
            "sec": 1.0 / math.cos(x) if math.cos(x) != 0 else None,
            "csc": 1.0 / math.sin(x) if math.sin(x) != 0 else None,
        }
    return table


_STUB_TABLE = _build_stub_table()
_STUB_X_SORTED = sorted(_STUB_TABLE.keys())


def _find_nearest(x: float) -> float:
    """Find nearest table point to x."""
    if not _STUB_X_SORTED:
        raise ValueError("Empty stub table")
    lo, hi = _STUB_X_SORTED[0], _STUB_X_SORTED[-1]
    if x <= lo:
        return lo
    if x >= hi:
        return hi
    for i, xi in enumerate(_STUB_X_SORTED):
        if xi >= x:
            if i == 0:
                return xi
            prev = _STUB_X_SORTED[i - 1]
            return xi if abs(xi - x) < abs(x - prev) else prev
    return _STUB_X_SORTED[-1]


class TrigStub:
    """Table-based stub returning precomputed trig values."""

    def sin(self, x: float) -> float:
        x_key = _find_nearest(x)
        return _STUB_TABLE[x_key]["sin"]

    def cos(self, x: float) -> float:
        x_key = _find_nearest(x)
        return _STUB_TABLE[x_key]["cos"]

    def tan(self, x: float) -> float:
        x_key = _find_nearest(x)
        v = _STUB_TABLE[x_key]["tan"]
        if v is None:
            raise ValueError("tan undefined: cos(x)=0")
        return v

    def cot(self, x: float) -> float:
        x_key = _find_nearest(x)
        v = _STUB_TABLE[x_key]["cot"]
        if v is None:
            raise ValueError("cot undefined: sin(x)=0")
        return v

    def sec(self, x: float) -> float:
        x_key = _find_nearest(x)
        v = _STUB_TABLE[x_key]["sec"]
        if v is None:
            raise ValueError("sec undefined: cos(x)=0")
        return v

    def csc(self, x: float) -> float:
        x_key = _find_nearest(x)
        v = _STUB_TABLE[x_key]["csc"]
        if v is None:
            raise ValueError("csc undefined: sin(x)=0")
        return v
