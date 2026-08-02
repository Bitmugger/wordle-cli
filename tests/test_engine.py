import unittest
from game.engine import LetterResult, GameState, score_guess, is_game_over, make_guess, MAX_GUESSES

C = LetterResult.CORRECT
P = LetterResult.PRESENT
A = LetterResult.ABSENT


class TestScoreGuess(unittest.TestCase):
    def test_all_correct(self):
        self.assertEqual(score_guess("WORLD", "WORLD"), [C, C, C, C, C])

    def test_all_absent(self):
        self.assertEqual(score_guess("ZZZZZ", "WORLD"), [A, A, A, A, A])

    def test_mixed(self):
        # W correct, O absent, R present (in CRANE at pos 2), L absent, D absent
        self.assertEqual(score_guess("CRANE", "RACED"), [P, P, P, A, P])

    def test_case_insensitive(self):
        self.assertEqual(score_guess("world", "WORLD"), [C, C, C, C, C])

    def test_duplicate_in_guess_answer_has_one(self):
        # guess=SPEED answer=SPELL: S=C P=C E=C E=A D=A (only one E in answer at pos2)
        self.assertEqual(score_guess("SPEED", "SPELL"), [C, C, C, A, A])

    def test_duplicate_in_guess_both_present(self):
        # guess=TEETH answer=GREET: T=P E=P E=C T=A H=A
        self.assertEqual(score_guess("TEETH", "GREET"), [P, P, C, A, A])

    def test_duplicate_in_answer_guess_has_one(self):
        # guess=EATER answer=CREEP: E=P A=A T=A E=C R=P (answer has 2 E's; R also matches)
        self.assertEqual(score_guess("EATER", "CREEP"), [P, A, A, C, P])

    def test_duplicate_letters_correct_takes_priority(self):
        # guess=AABBB answer=BAAAA: A=P A=C B=P B=A B=A
        self.assertEqual(score_guess("AABBB", "BAAAA"), [P, C, P, A, A])

    def test_no_yellow_beyond_answer_count(self):
        # guess=SPELL answer=WORLD: only 1 L in answer (pos3=CORRECT); second L in guess=ABSENT
        self.assertEqual(score_guess("SPELL", "WORLD"), [A, A, A, C, A])


class TestIsGameOver(unittest.TestCase):
    def test_in_progress_not_over(self):
        state = GameState(answer="WORLD")
        self.assertFalse(is_game_over(state))

    def test_won_is_over(self):
        state = GameState(answer="WORLD", status="won")
        self.assertTrue(is_game_over(state))

    def test_lost_is_over(self):
        state = GameState(answer="WORLD", status="lost")
        self.assertTrue(is_game_over(state))


class TestMakeGuess(unittest.TestCase):
    def test_correct_guess_sets_won(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "WORLD")
        self.assertEqual(state.status, "won")

    def test_wrong_guess_stays_in_progress(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "CRANE")
        self.assertEqual(state.status, "in_progress")

    def test_six_wrong_guesses_sets_lost(self):
        state = GameState(answer="WORLD")
        for _ in range(MAX_GUESSES):
            state = make_guess(state, "CRANE")
        self.assertEqual(state.status, "lost")

    def test_five_wrong_then_correct_sets_won(self):
        state = GameState(answer="WORLD")
        for _ in range(MAX_GUESSES - 1):
            state = make_guess(state, "CRANE")
        state = make_guess(state, "WORLD")
        self.assertEqual(state.status, "won")

    def test_guess_appended_to_state(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "crane")
        self.assertEqual(state.guesses, ["CRANE"])
        self.assertEqual(len(state.results), 1)

    def test_make_guess_does_not_mutate_original(self):
        original = GameState(answer="WORLD")
        make_guess(original, "CRANE")
        self.assertEqual(original.guesses, [])

    def test_lowercase_guess_normalized(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "world")
        self.assertEqual(state.status, "won")


if __name__ == "__main__":
    unittest.main()
