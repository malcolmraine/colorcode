from ..color import Color
from ..util import luma_from_rgb, LumaMethod, srgb_to_linear_rgb
import math


def weighted_euclidean_distance(
    color1: Color, color2: Color, weights: tuple[float, ...] | None = None
) -> float:
    if weights is None:
        # Use red mean
        r_mean = (color1.red + color2.red) / 2
        w_r = 2 + r_mean / 256
        w_g = 4
        w_b = 2 + (255 - r_mean) / 256
    else:
        if len(weights) != 3:
            raise ValueError("Invalid number of weights provided.")
        w_r, w_g, w_b = weights

    delta_r2 = (color2.red - color1.red) ** 2
    delta_g2 = (color2.green - color1.green) ** 2
    delta_b2 = (color2.blue - color1.blue) ** 2

    return math.sqrt(w_r * delta_r2 + w_g * delta_g2 + w_b * delta_b2)


def euclidean_distance(color1: Color, color2: Color) -> float:
    return weighted_euclidean_distance(color1, color2, weights=(1, 1, 1))


def delta_e76_lab(L1, a1, b1, L2, a2, b2) -> float:
    """
    Implementation of the CIE 1976 color difference formula.

    Parameters
    ----------
    L1
    a1
    b1
    L2
    a2
    b2

    Returns
    -------
    float
        The difference between the two colors.

    """
    return math.sqrt((L2 - L1) ** 2 + (a2 - a1) ** 2 + (b2 - b1) ** 2)


def delta_e76(color1: Color, color2: Color) -> float:
    """
    Calculate color difference using the CIE 1976 (ΔE*76) formula.

    Parameters
    ----------
    color1 : Color
        The first color.
    color2 : Color
        The second color.

    Returns
    -------
    float
        The color difference value.

    Notes
    -----
    Uses the formula: ΔE*76 = sqrt((ΔL*)² + (Δa*)² + (Δb*)²)
    This is a simple Euclidean distance in the L*a*b* color space.
    """
    from ..color_model import CIELAB_Model

    model = CIELAB_Model()
    L1, a1, b1 = model.from_rgb(color1.red, color1.green, color1.blue)
    L2, a2, b2 = model.from_rgb(color2.red, color2.green, color2.blue)
    return delta_e76_lab(L1, a1, b1, L2, a2, b2)


def delta_e94_lab(L1, a1, b1, L2, a2, b2) -> float:
    """
    Implementation of the CIE 1994 color difference formula.

    Parameters
    ----------
    L1
    a1
    b1
    L2
    a2
    b2

    Returns
    -------
    float
        The difference between the two colors.

    """
    delta_l = L1 - L2
    c1 = math.sqrt(a1**2 + b1**2)
    c2 = math.sqrt(a2**2 + b2**2)
    delta_c = c1 - c2
    delta_a = a1 - a2
    delta_b = b1 - b2
    delta_h = math.sqrt(delta_a**2 + delta_b**2 - delta_c**2)
    sl = 1
    kl = 1
    kc = 0.045
    kh = 0.015
    sc = 1 + kc * c1
    sh = 1 + kh * c1

    delta_e = math.sqrt(
        (delta_l / (kl * sl)) ** 2
        + (delta_c / (kc * sc)) ** 2
        + (delta_h / (kh * sh)) ** 2
    )

    return delta_e


def delta_e94(color1: Color, color2: Color) -> float:
    """
    Calculate color difference using the CIE 1994 (ΔE*94) formula.

    Parameters
    ----------
    color1 : Color
        The first color (reference color).
    color2 : Color
        The second color (test color).

    Returns
    -------
    float
        The color difference value.

    Notes
    -----
    Uses the formula:
    ΔE*94 = sqrt((ΔL/(kL*SL))² + (ΔC/(kC*SC))² + (ΔH/(kH*SH))²)

    where:
    - ΔL = L1 - L2
    - ΔC = C1 - C2 (chroma difference)
    - ΔH is calculated from a* and b* differences
    - SL = 1, SC = 1 + 0.045*C1, SH = 1 + 0.015*C1 (weighting functions)
    - kL = 1, kC = 1, kH = 1 (parametric factors, can be adjusted)
    """
    from ..color_model import CIELAB_Model

    model = CIELAB_Model()
    L1, a1, b1 = model.from_rgb(color1.red, color1.green, color1.blue)
    L2, a2, b2 = model.from_rgb(color2.red, color2.green, color2.blue)
    return delta_e94_lab(L1, a1, b1, L2, a2, b2)


def delta_e2000(color1: Color, color2: Color) -> float:
    """
    Calculate color difference using the CIE 2000 (ΔE00) formula.

    Parameters
    ----------
    color1 : Color
        The first color (reference color).
    color2 : Color
        The second color (test color).

    Returns
    -------
    float
        The color difference value.

    Notes
    -----
    The CIE 2000 formula improves upon ΔE*94 by considering:
    - Hue-dependent chroma weighting
    - Non-uniform weighting in lightness
    - Rotation term for hue/chroma interaction

    Formula:
    ΔE00 = sqrt((ΔL'/(SL*kL))² + (ΔC'/(SC*kC))² + (ΔH'/(SH*kH))² + RT*(ΔC'/(SC*kC))*(ΔH'/(SH*kH)))
    """
    from ..color_model import CIELAB_Model

    model = CIELAB_Model()
    L1, a1, b1 = model.from_rgb(color1.red, color1.green, color1.blue)
    L2, a2, b2 = model.from_rgb(color2.red, color2.green, color2.blue)
    return delta_e2000_lab(L1, a1, b1, L2, a2, b2)


def delta_e2000_lab(
    L1: float, a1: float, b1: float, L2: float, a2: float, b2: float
) -> float:
    """
    Implementation of the CIE 2000 color difference formula in L*a*b* space.

    Parameters
    ----------
    L1, a1, b1 : float
        L*a*b* components of the reference color.
    L2, a2, b2 : float
        L*a*b* components of the test color.

    Returns
    -------
    float
        The color difference value (ΔE00).
    """
    # Step 1: Calculate Cab values (chroma of the reference)
    C1ab = math.sqrt(a1**2 + b1**2)
    C2ab = math.sqrt(a2**2 + b2**2)
    Cab_mean = (C1ab + C2ab) / 2

    # Step 2: Calculate G and modified chroma
    G = 0.5 * (1 - math.sqrt(Cab_mean**7 / (Cab_mean**7 + 25**7)))
    a1_prime = (1 + G) * a1
    a2_prime = (1 + G) * a2

    # Step 3: Calculate C'ab and h' (hue angle in degrees)
    C1 = math.sqrt(a1_prime**2 + b1**2)
    C2 = math.sqrt(a2_prime**2 + b2**2)
    h1 = math.degrees(math.atan2(b1, a1_prime)) % 360
    h2 = math.degrees(math.atan2(b2, a2_prime)) % 360

    # Step 4: Calculate differences
    dL_prime = L2 - L1
    dC_prime = C2 - C1
    dh_prime = h2 - h1

    # Handle hue difference wraparound
    if abs(dh_prime) > 180:
        if dh_prime > 180:
            dh_prime -= 360
        else:
            dh_prime += 360

    dH_prime = 2 * math.sqrt(C1 * C2) * math.sin(math.radians(dh_prime / 2))

    # Step 5: Calculate L', C', H' mean values
    L_prime_mean = (L1 + L2) / 2
    C_prime_mean = (C1 + C2) / 2

    # Calculate mean hue
    h_mean = (h1 + h2) / 2
    if abs(h1 - h2) > 180:
        h_mean = (h_mean + 180) % 360

    # Step 6: Calculate weighting functions (SL, SC, SH)
    SL = 1 + (0.015 * (L_prime_mean - 50) ** 2) / math.sqrt(
        20 + (L_prime_mean - 50) ** 2
    )
    SC = 1 + 0.045 * C_prime_mean
    SH = 1 + 0.015 * C_prime_mean * (
        1
        - 0.17 * math.cos(math.radians(h_mean - 30))
        + 0.24 * math.cos(math.radians(2 * h_mean))
        - 0.32 * math.cos(math.radians(3 * h_mean + 6))
        + 0.20 * math.cos(math.radians(4 * h_mean - 63))
    )

    # Step 7: Calculate rotation term
    T = (
        1
        - 0.17 * math.cos(math.radians(h_mean - 30))
        + 0.24 * math.cos(math.radians(2 * h_mean))
        - 0.32 * math.cos(math.radians(3 * h_mean + 6))
        + 0.20 * math.cos(math.radians(4 * h_mean - 63))
    )

    dtheta = 30 * math.exp(-(((h_mean - 275) / 25) ** 2))
    RC = 2 * math.sqrt(C_prime_mean**7 / (C_prime_mean**7 + 25**7))
    RT = -math.sin(math.radians(2 * dtheta)) * RC

    # Step 8: Calculate ΔE00
    delta_e = math.sqrt(
        (dL_prime / (SL)) ** 2
        + (dC_prime / (SC)) ** 2
        + (dH_prime / (SH)) ** 2
        + RT * (dC_prime / SC) * (dH_prime / SH)
    )

    return delta_e


def contrast_ratio(color1: Color, color2: Color) -> float:
    linear_rgb1 = srgb_to_linear_rgb(*color1.srgb)
    linear_rgb2 = srgb_to_linear_rgb(*color2.srgb)
    luma_1 = luma_from_rgb(*linear_rgb1, LumaMethod.BT709)
    luma_2 = luma_from_rgb(*linear_rgb2, LumaMethod.BT709)

    if luma_1 >= luma_2:
        return (luma_1 + 0.05) / (luma_2 + 0.05)
    else:
        return (luma_2 + 0.05) / (luma_1 + 0.05)
