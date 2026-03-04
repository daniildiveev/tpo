import math

_SERIES_THRESHOLD = 0.5


def arctan_series(x: float, epsilon: float = 1e-10, max_terms: int = 10000) -> float:
    if abs(x) > 1.0:
        sign = 1 if x > 0 else -1
        return sign * math.pi / 2.0 - arctan_series(1.0 / x, epsilon, max_terms)

    if abs(x) > _SERIES_THRESHOLD:
        sign = 1 if x > 0 else -1
        x_abs = abs(x)
        reduced = (x_abs - 1.0) / (x_abs + 1.0)
        return sign * (math.pi / 4.0 + arctan_series(reduced, epsilon, max_terms))

    result = 0.0
    x_power = x
    x_sq = x * x

    for k in range(max_terms):
        term = x_power / (2 * k + 1)
        if k % 2 == 0:
            result += term
        else:
            result -= term

        if abs(term) < epsilon:
            break

        x_power *= x_sq

    return result
