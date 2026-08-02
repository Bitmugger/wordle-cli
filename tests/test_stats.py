import json
import os
import tempfile
import unittest
from pathlib import Path
from persistence.stats import load_stats, save_stats, update_stats, format_stats, DEFAULT_STATS


class TestLoadStats(unittest.TestCase):
    def test_returns_default_when_no_file(self):
        result = load_stats(Path("/tmp/nonexistent_wordle_stats.json"))
        self.assertEqual(result, DEFAULT_STATS)

    def test_loads_existing_file(self):
        data = {**DEFAULT_STATS, "games_played": 5, "wins": 3}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            tmp = Path(f.name)
        try:
            result = load_stats(tmp)
            self.assertEqual(result["games_played"], 5)
            self.assertEqual(result["wins"], 3)
        finally:
            tmp.unlink()


class TestSaveStats(unittest.TestCase):
    def test_round_trips_correctly(self):
        stats = {**DEFAULT_STATS, "games_played": 10, "wins": 7}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "stats.json"
            save_stats(stats, path)
            loaded = load_stats(path)
        self.assertEqual(loaded["games_played"], 10)
        self.assertEqual(loaded["wins"], 7)

    def test_creates_parent_directory(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "nested" / "dir" / "stats.json"
            save_stats(DEFAULT_STATS.copy(), path)
            self.assertTrue(path.exists())

    def test_no_tmp_file_left_behind(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "stats.json"
            save_stats(DEFAULT_STATS.copy(), path)
            leftover = list(Path(d).glob("*.tmp"))
            self.assertEqual(leftover, [])


class TestUpdateStats(unittest.TestCase):
    def test_increments_games_played_on_win(self):
        result = update_stats(DEFAULT_STATS.copy(), won=True)
        self.assertEqual(result["games_played"], 1)

    def test_increments_games_played_on_loss(self):
        result = update_stats(DEFAULT_STATS.copy(), won=False)
        self.assertEqual(result["games_played"], 1)

    def test_increments_wins_on_win(self):
        result = update_stats(DEFAULT_STATS.copy(), won=True)
        self.assertEqual(result["wins"], 1)

    def test_does_not_increment_wins_on_loss(self):
        result = update_stats(DEFAULT_STATS.copy(), won=False)
        self.assertEqual(result["wins"], 0)

    def test_increments_streak_on_win(self):
        result = update_stats(DEFAULT_STATS.copy(), won=True)
        self.assertEqual(result["current_streak"], 1)

    def test_resets_streak_on_loss(self):
        stats = {**DEFAULT_STATS, "current_streak": 5}
        result = update_stats(stats, won=False)
        self.assertEqual(result["current_streak"], 0)

    def test_updates_max_streak(self):
        stats = {**DEFAULT_STATS, "current_streak": 4, "max_streak": 4}
        result = update_stats(stats, won=True)
        self.assertEqual(result["max_streak"], 5)

    def test_max_streak_not_lowered(self):
        stats = {**DEFAULT_STATS, "current_streak": 1, "max_streak": 10}
        result = update_stats(stats, won=True)
        self.assertEqual(result["max_streak"], 10)

    def test_does_not_mutate_input(self):
        original = DEFAULT_STATS.copy()
        update_stats(original, won=True)
        self.assertEqual(original["games_played"], 0)


class TestFormatStats(unittest.TestCase):
    def test_shows_all_fields(self):
        stats = {**DEFAULT_STATS, "games_played": 10, "wins": 7, "current_streak": 3, "max_streak": 8}
        result = format_stats(stats)
        self.assertIn("10", result)
        self.assertIn("70", result)
        self.assertIn("3", result)
        self.assertIn("8", result)

    def test_zero_games_no_division_error(self):
        try:
            format_stats(DEFAULT_STATS.copy())
        except ZeroDivisionError:
            self.fail("format_stats raised ZeroDivisionError on zero games")


if __name__ == "__main__":
    unittest.main()
