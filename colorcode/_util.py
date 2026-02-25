def clamp(value: float | int, lower: float | int, upper: float | int) -> float | int:
    return min(max(value, lower), upper)
