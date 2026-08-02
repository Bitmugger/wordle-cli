import os
import sys
from game.engine import GameState, LetterResult

KEYBOARD_ROWS = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

# ANSI color codes
_GREEN  = "\033[42m\033[30m"
_YELLOW = "\033[43m\033[30m"
_GRAY   = "\033[100m\033[37m"
_RESET  = "\033[0m"
_DIM    = "\033[2m"

_RESULT_COLOR = {
    LetterResult.CORRECT: _GREEN,
    LetterResult.PRESENT: _YELLOW,
    LetterResult.ABSENT:  _GRAY,
}

_PRIORITY = {
    LetterResult.CORRECT: 3,
    LetterResult.PRESENT: 2,
    LetterResult.ABSENT:  1,
}


def _color_supported() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def _tile(letter: str, result: LetterResult | None, color: bool) -> str:
    char = letter.upper() if letter else " "
    if not color:
        return f"[{char}]" if result else f"[{char}]"
    if result is None:
        return f"{_DIM}[ ]{_RESET}"
    return f"{_RESULT_COLOR[result]} {char} {_RESET}"


def build_keyboard_state(state: GameState) -> dict[str, LetterResult]:
    kb: dict[str, LetterResult] = {}
    for guess, result in zip(state.guesses, state.results):
        for letter, r in zip(guess, result):
            if letter not in kb or _PRIORITY[r] > _PRIORITY[kb[letter]]:
                kb[letter] = r
    return kb


def render(state: GameState) -> None:
    color = _color_supported()

    if color:
        print("\033[2J\033[H", end="")

    print()

    # Guess grid
    for i in range(6):
        if i < len(state.guesses):
            guess  = state.guesses[i]
            result = state.results[i]
            row = " ".join(_tile(ch, r, color) for ch, r in zip(guess, result))
        else:
            row = " ".join(_tile(" ", None, color) for _ in range(5))
        print(f"  {row}")

    print()

    # Keyboard
    kb = build_keyboard_state(state)
    for row in KEYBOARD_ROWS:
        keys = []
        for ch in row:
            r = kb.get(ch)
            if color and r is not None:
                keys.append(f"{_RESULT_COLOR[r]} {ch} {_RESET}")
            else:
                keys.append(f" {ch} ")
        print("  " + " ".join(keys))

    print()
