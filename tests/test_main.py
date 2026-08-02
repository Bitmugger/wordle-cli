import unittest
from unittest.mock import patch
from main import get_guess, show_result, play_again, run_game
from game.engine import GameState

WORD_LIST = frozenset(["CRANE", "WORLD", "SLATE", "AUDIO", "JUMPY", "GREET"])
ANSWERS   = frozenset(["WORLD", "CRANE", "SLATE"])


class TestGetGuess(unittest.TestCase):
    def test_valid_guess_returned(self):
        with patch("builtins.input", return_value="crane"):
            result = get_guess(WORD_LIST)
        self.assertEqual(result, "CRANE")

    def test_reprompts_on_wrong_length(self):
        with patch("builtins.input", side_effect=["HI", "crane"]):
            with patch("builtins.print"):
                result = get_guess(WORD_LIST)
        self.assertEqual(result, "CRANE")

    def test_reprompts_on_invalid_word(self):
        with patch("builtins.input", side_effect=["ZZZZZ", "crane"]):
            with patch("builtins.print"):
                result = get_guess(WORD_LIST)
        self.assertEqual(result, "CRANE")

    def test_uppercase_normalisation(self):
        with patch("builtins.input", return_value="SLATE"):
            result = get_guess(WORD_LIST)
        self.assertEqual(result, "SLATE")


class TestShowResult(unittest.TestCase):
    def test_win_message(self):
        state = GameState(answer="WORLD", guesses=["WORLD"], status="won")
        with patch("builtins.print") as mock_print:
            show_result(state)
        output = " ".join(str(a) for call in mock_print.call_args_list for a in call[0])
        self.assertIn("1/6", output)

    def test_loss_message_shows_answer(self):
        state = GameState(answer="WORLD", status="lost")
        with patch("builtins.print") as mock_print:
            show_result(state)
        output = " ".join(str(a) for call in mock_print.call_args_list for a in call[0])
        self.assertIn("WORLD", output)


class TestPlayAgain(unittest.TestCase):
    def test_y_returns_true(self):
        with patch("builtins.input", return_value="y"):
            self.assertTrue(play_again())

    def test_yes_returns_true(self):
        with patch("builtins.input", return_value="yes"):
            self.assertTrue(play_again())

    def test_n_returns_false(self):
        with patch("builtins.input", return_value="n"):
            self.assertFalse(play_again())

    def test_empty_returns_false(self):
        with patch("builtins.input", return_value=""):
            self.assertFalse(play_again())


class TestRunGame(unittest.TestCase):
    def test_win_on_correct_guess(self):
        with patch("random.choice", return_value="WORLD"):
            with patch("builtins.input", return_value="world"):
                with patch("cli.renderer.render"):
                    with patch("builtins.print"):
                        result = run_game(WORD_LIST, ANSWERS)
        self.assertEqual(result, "won")

    def test_loss_after_six_wrong_guesses(self):
        with patch("random.choice", return_value="WORLD"):
            with patch("builtins.input", return_value="crane"):
                with patch("cli.renderer.render"):
                    with patch("builtins.print"):
                        result = run_game(WORD_LIST, ANSWERS)
        self.assertEqual(result, "lost")

    def test_win_on_last_guess(self):
        inputs = ["CRANE"] * 5 + ["WORLD"]
        with patch("random.choice", return_value="WORLD"):
            with patch("builtins.input", side_effect=inputs):
                with patch("cli.renderer.render"):
                    with patch("builtins.print"):
                        result = run_game(WORD_LIST, ANSWERS)
        self.assertEqual(result, "won")


if __name__ == "__main__":
    unittest.main()
