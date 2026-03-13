import math

_STUB_POINTS = [
    0.01, 0.1, 0.2, 0.5, 0.7, 0.9, 1.1, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0,
]


def _build_stub_table():
    table = {}
    for x in _STUB_POINTS:
        if x <= 0:
            continue
        table[x] = {
            "ln": math.log(x),
            "log3": math.log(x) / math.log(3),
            "log5": math.log(x) / math.log(5),
            "log10": math.log(x) / math.log(10),
        }
    return table


_STUB_TABLE = _build_stub_table()
_STUB_X_SORTED = sorted(_STUB_TABLE.keys())


def _find_nearest(x: float) -> float:
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


class LogStub:
    def ln(self, x: float) -> float:
        if x <= 0:
            raise ValueError("ln(x) requires x > 0")
        x_key = _find_nearest(x)
        return _STUB_TABLE[x_key]["ln"]

    def log3(self, x: float) -> float:
        if x <= 0:
            raise ValueError("log_3(x) requires x > 0")
        x_key = _find_nearest(x)
        return _STUB_TABLE[x_key]["log3"]

    def log5(self, x: float) -> float:
        if x <= 0:
            raise ValueError("log_5(x) requires x > 0")
        x_key = _find_nearest(x)
        return _STUB_TABLE[x_key]["log5"]

    def log10(self, x: float) -> float:
        if x <= 0:
            raise ValueError("log_10(x) requires x > 0")
        x_key = _find_nearest(x)
        return _STUB_TABLE[x_key]["log10"]
