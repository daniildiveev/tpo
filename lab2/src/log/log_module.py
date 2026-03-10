"""Logarithmic functions expressed through ln(x)."""

from ..base.ln_series import ln_series


class LogModule:
    """Logarithmic module: log_3, log_5, log_10 via ln series."""

    def __init__(self, epsilon: float = 1e-10):
        self._epsilon = epsilon
        self._ln3 = ln_series(3.0, epsilon)
        self._ln5 = ln_series(5.0, epsilon)
        self._ln10 = ln_series(10.0, epsilon)

    def ln(self, x: float) -> float:
        if x <= 0:
            raise ValueError("ln(x) requires x > 0")
        return ln_series(x, self._epsilon)

    def log3(self, x: float) -> float:
        if x <= 0:
            raise ValueError("log_3(x) requires x > 0")
        return self.ln(x) / self._ln3

    def log5(self, x: float) -> float:
        if x <= 0:
            raise ValueError("log_5(x) requires x > 0")
        return self.ln(x) / self._ln5

    def log10(self, x: float) -> float:
        if x <= 0:
            raise ValueError("log_10(x) requires x > 0")
        return self.ln(x) / self._ln10
