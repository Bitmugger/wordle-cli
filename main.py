import random
from pathlib import Path

from words.words import load_word_list, is_valid_guess
from game.engine import GameState, make_guess, is_game_over
from cli.renderer import render

WORDS_DIR = Path(__file__).parent / "words"


def get_guess(word_list: frozenset[str]) -> str:
    while True:
        raw = input("Guess: ").strip().upper()
        if len(raw) != 5:
            print("  Word must be exactly 5 letters.")
        elif not is_valid_guess(raw, word_list):
            print("  Not in word list — try again.")
        else:
            return raw


def show_result(state: GameState) -> None:
    if state.status == "won":
        guess_count = len(state.guesses)
        print(f"  You got it! Solved in {guess_count}/6.\n")
    else:
        print(f"  The word was {state.answer}. Better luck next time!\n")


def play_again() -> bool:
    return input("Play again? [y/n]: ").strip().lower().startswith("y")


def run_game(word_list: frozenset[str], answers: frozenset[str]) -> str:
    answer = random.choice(sorted(answers))
    state  = GameState(answer=answer)

    while not is_game_over(state):
        render(state)
        guess = get_guess(word_list)
        state = make_guess(state, guess)

    render(state)
    show_result(state)
    return state.status


def main() -> None:
    word_list = load_word_list(WORDS_DIR / "valid_words.txt")
    answers   = load_word_list(WORDS_DIR / "answers.txt")

    while True:
        run_game(word_list, answers)
        if not play_again():
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThanks for playing!")
