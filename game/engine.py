from enum import Enum
from dataclasses import dataclass, field

MAX_GUESSES = 6


class LetterResult(Enum):
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT  = "absent"


@dataclass
class GameState:
    answer: str
    guesses: list[str] = field(default_factory=list)
    results: list[list[LetterResult]] = field(default_factory=list)
    status: str = "in_progress"  # "in_progress" | "won" | "lost"


def score_guess(guess: str, answer: str) -> list[LetterResult]:
    guess  = guess.upper()
    answer = answer.upper()
    result           = [LetterResult.ABSENT] * 5
    answer_remaining = list(answer)

    # Pass 1: lock greens
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            result[i]           = LetterResult.CORRECT
            answer_remaining[i] = None

    # Pass 2: assign yellows left-to-right from remaining answer letters
    for i, g in enumerate(guess):
        if result[i] == LetterResult.CORRECT:
            continue
        if g in answer_remaining:
            result[i] = LetterResult.PRESENT
            answer_remaining[answer_remaining.index(g)] = None

    return result


def is_game_over(state: GameState) -> bool:
    return state.status in ("won", "lost")


def make_guess(state: GameState, guess: str) -> GameState:
    guess      = guess.upper()
    result     = score_guess(guess, state.answer)
    new_guesses = state.guesses + [guess]
    new_results = state.results + [result]

    if all(r == LetterResult.CORRECT for r in result):
        status = "won"
    elif len(new_guesses) >= MAX_GUESSES:
        status = "lost"
    else:
        status = "in_progress"

    return GameState(state.answer, new_guesses, new_results, status)
