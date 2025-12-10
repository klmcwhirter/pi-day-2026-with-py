
def palindrome(digits: str, double_middle=False) -> str:
    rev: str = digits[::-1]

    if not double_middle:
        rev = rev[1:]

    return digits + rev
