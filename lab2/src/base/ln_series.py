"""ln(x) via series expansion. No use of math.log or log identities."""


def _ln_1_plus_u(u: float, epsilon: float, max_terms: int) -> float:
    """ln(1+u) = u - u²/2 + u³/3 - ... for |u| < 1."""
    if abs(u) >= 1:
        raise ValueError("|u| must be < 1 for ln(1+u) series")
    result = 0.0
    term = u
    k = 1
    u_power = u

    for _ in range(max_terms):
        result += term
        if abs(term) < epsilon:
            break
        k += 1
        u_power *= u
        term = ((-1) ** (k - 1)) * u_power / k

    return result


def ln_series(x: float, epsilon: float = 1e-10, max_terms: int = 10000) -> float:
    """
    Compute ln(x) via series. Uses ln(1+u) for 0 < x <= 2, recursion for x > 2.

    Args:
        x: Input value (must be > 0)
        epsilon: Stop when |term| < epsilon
        max_terms: Maximum number of terms

    Returns:
        ln(x) approximation

    Raises:
        ValueError: if x <= 0
    """
    if x <= 0:
        raise ValueError("ln(x) requires x > 0")

    # ln(2) = -ln(0.5), ln(1-u) = -u - u²/2 - u³/3 - ... for |u| < 1
    def _ln_half(eps: float) -> float:
        r = 0.0
        u = 0.5
        up = u
        k = 1
        for _ in range(max_terms):
            t = -up / k
            r += t
            if abs(t) < eps:
                break
            k += 1
            up *= u
        return r

    LN2 = -_ln_half(epsilon)

    val = x
    result = 0.0
    while val >= 2:
        result += LN2
        val /= 2
    while val < 1:
        result -= LN2
        val *= 2
    # 1 <= val <= 2: ln(val) = ln(1 + (val-1))
    u = val - 1
    result += _ln_1_plus_u(u, epsilon, max_terms)
    return result
