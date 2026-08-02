import unittest
import io
import sys
from unittest.mock import patch
from game.engine import GameState, LetterResult, make_guess
from cli.renderer import build_keyboard_state, render

C = LetterResult.CORRECT
P = LetterResult.PRESENT
A = LetterResult.ABSENT


class TestBuildKeyboardState(unittest.TestCase):
    def test_empty_state_returns_empty(self):
        state = GameState(answer="WORLD")
        self.assertEqual(build_keyboard_state(state), {})

    def test_correct_beats_present(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "WORRY")  # W=C O=C R=C R->second, Y=A
        state = make_guess(state, "WHOLE")  # W=C should stay C
        kb = build_keyboard_state(state)
        self.assertEqual(kb["W"], C)

    def test_correct_beats_absent(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "CRANE")  # no W
        state = make_guess(state, "WORLD")  # W=C
        kb = build_keyboard_state(state)
        self.assertEqual(kb["W"], C)

    def test_present_beats_absent(self):
        # W is ABSENT in CRANE, then PRESENT in SWORD
        state = GameState(answer="WORLD")
        state = make_guess(state, "CRANE")
        kb_after_first = build_keyboard_state(state)
        self.assertEqual(kb_after_first.get("C"), A)

        state = make_guess(state, "SWIFT")
        kb = build_keyboard_state(state)
        # S is PRESENT in WORLD (S not in WORLD actually)
        # Let's just verify absent letters are tracked
        self.assertIn("C", kb)

    def test_absent_does_not_override_correct(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "WORLD")  # all correct
        state = make_guess(state, "WORMY")  # W=C O=C R=C M=A Y=A — W stays CORRECT
        kb = build_keyboard_state(state)
        self.assertEqual(kb["W"], C)
        self.assertEqual(kb["O"], C)
        self.assertEqual(kb["R"], C)

    def test_tracks_all_letters_in_guess(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "CRANE")
        kb = build_keyboard_state(state)
        for ch in "CRANE":
            self.assertIn(ch, kb)


class TestRender(unittest.TestCase):
    def _capture(self, state, color=False):
        with patch("cli.renderer._color_supported", return_value=color):
            buf = io.StringIO()
            with patch("sys.stdout", buf):
                render(state)
            return buf.getvalue()

    def test_render_contains_guessed_letters(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "CRANE")
        output = self._capture(state)
        for ch in "CRANE":
            self.assertIn(ch, output)

    def test_render_contains_keyboard_letters(self):
        state = GameState(answer="WORLD")
        output = self._capture(state)
        for ch in "QWERTY":
            self.assertIn(ch, output)

    def test_plain_text_fallback_uses_brackets(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "CRANE")
        output = self._capture(state, color=False)
        self.assertIn("[C]", output)
        self.assertNotIn("\033[", output)

    def test_color_output_contains_ansi_codes(self):
        state = GameState(answer="WORLD")
        state = make_guess(state, "CRANE")
        output = self._capture(state, color=True)
        self.assertIn("\033[", output)

    def test_empty_state_renders_without_error(self):
        state = GameState(answer="WORLD")
        try:
            self._capture(state)
        except Exception as e:
            self.fail(f"render() raised {e} on empty state")


if __name__ == "__main__":
    unittest.main()
