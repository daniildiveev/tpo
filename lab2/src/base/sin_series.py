"""sin(x) via Taylor series expansion. No use of math.sin or trig identities."""

# π computed as 4 * arctan(1) - constant for normalization
PI = 3.14159265358979323846
TWO_PI = 2 * PI


def _reduce_to_pi(x: float) -> float:
    """Reduce x to [-π, π] using only arithmetic (no math module)."""
    if x >= -PI and x <= PI:
        return x
    # x = k * 2π + r, we want r in [-π, π]
    k = int(x / TWO_PI)
    r = x - k * TWO_PI
    if r > PI:
        r -= TWO_PI
    elif r < -PI:
        r += TWO_PI
    return r


def sin_series(x: float, epsilon: float = 1e-10, max_terms: int = 1000) -> float:
    """
    Compute sin(x) via Taylor series: sin(x) = x - x³/3! + x⁵/5! - ...

    Args:
        x: Input value (radians)
        epsilon: Stop when |term| < epsilon
        max_terms: Maximum number of terms

    Returns:
        sin(x) approximation
    """
    x = _reduce_to_pi(x)
    result = 0.0
    term = x
    x_sq = x * x
    k = 0

    for _ in range(max_terms):
        result += term
        if abs(term) < epsilon:
            break
        # term_{k+1} = term_k * (-1) * x² / ((2k+2)(2k+3))
        term = -term * x_sq / ((2 * k + 2) * (2 * k + 3))
        k += 1

    return result
