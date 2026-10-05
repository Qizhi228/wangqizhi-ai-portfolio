def add(left: int, right: int) -> int:
    return left + right


def divide(left: float, right: float) -> float:
    if right == 0:
        raise ValueError("right cannot be zero")
    return left / right
