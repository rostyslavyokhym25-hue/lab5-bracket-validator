PAIRS = {
    ")": "(",
    "}": "{",
    ">": "<",
}
OPENING = set(PAIRS.values())
CLOSING = set(PAIRS.keys())


def format_highlight(text: str, invalid_positions: list[int]) -> str:
    pos_set = set(invalid_positions)
    carets = "".join("^" if i in pos_set else " " for i in range(len(text))).rstrip()
    return f"{text}\n{carets}" if carets else text


def validate_brackets(text: str, advanced: bool = True) -> None:
    allowed_open = OPENING if advanced else {"("}
    allowed_close = CLOSING if advanced else {")"}

    stack: list[tuple[str, int]] = []
    invalid_positions: list[int] = []

    for idx, ch in enumerate(text):
        if ch in allowed_open:
            stack.append((ch, idx))
        elif ch in allowed_close:
            if stack and stack[-1][0] == PAIRS[ch]:
                stack.pop()
            else:
                invalid_positions.append(idx)

    for _, idx in stack:
        invalid_positions.append(idx)

    if invalid_positions:
        positions = sorted(set(invalid_positions))
        if not advanced:
            raise ValueError("Дужки незбалансовані")
        pos_str = ", ".join(str(p) for p in positions)
        highlight = format_highlight(text, positions)
        raise ValueError(
            f"Дужки незбалансовані на позиціях {pos_str}\n{highlight}"
        )


def main() -> None:
    text = input("Введіть строку")
    try:
        validate_brackets(text, advanced=True)
    except ValueError as exc:
        print(exc)
        raise
    print("Строка валідна")


if __name__ == "__main__":
    main()