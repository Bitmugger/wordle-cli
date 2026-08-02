import unittest
from pathlib import Path
import tempfile
import os

from words.words import load_word_list, is_valid_guess

WORDS_DIR = Path(__file__).parent.parent / "words"


class TestLoadWordList(unittest.TestCase):
    def test_returns_frozenset(self):
        result = load_word_list(WORDS_DIR / "valid_words.txt")
        self.assertIsInstance(result, frozenset)

    def test_words_are_uppercase(self):
        result = load_word_list(WORDS_DIR / "valid_words.txt")
        for word in list(result)[:100]:
            self.assertEqual(word, word.upper())

    def test_all_words_are_five_letters(self):
        result = load_word_list(WORDS_DIR / "valid_words.txt")
        for word in result:
            self.assertEqual(len(word), 5, f"Bad word: {word!r}")

    def test_minimum_word_count(self):
        result = load_word_list(WORDS_DIR / "valid_words.txt")
        self.assertGreater(len(result), 2000)

    def test_raises_on_invalid_word_length(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("hello\nworld\ntoolongword\n")
            tmp = f.name
        try:
            with self.assertRaises(ValueError):
                load_word_list(tmp)
        finally:
            os.unlink(tmp)

    def test_ignores_blank_lines(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("hello\n\nworld\n\n")
            tmp = f.name
        try:
            result = load_word_list(tmp)
            self.assertEqual(result, frozenset(["HELLO", "WORLD"]))
        finally:
            os.unlink(tmp)


class TestIsValidGuess(unittest.TestCase):
    def setUp(self):
        self.word_list = frozenset(["CRANE", "SLATE", "AUDIO", "JUMPY"])

    def test_valid_word_returns_true(self):
        self.assertTrue(is_valid_guess("crane", self.word_list))

    def test_uppercase_input_returns_true(self):
        self.assertTrue(is_valid_guess("CRANE", self.word_list))

    def test_invalid_word_returns_false(self):
        self.assertFalse(is_valid_guess("zzzzz", self.word_list))

    def test_strips_whitespace(self):
        self.assertTrue(is_valid_guess("  crane  ", self.word_list))

    def test_case_insensitive(self):
        self.assertTrue(is_valid_guess("Slate", self.word_list))


if __name__ == "__main__":
    unittest.main()
