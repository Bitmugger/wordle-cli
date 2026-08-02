import unittest
from datetime import date
from unittest.mock import patch
from persistence.daily import get_daily_answer, already_played_today, record_daily_result

ANSWERS = frozenset(["CRANE", "WORLD", "SLATE", "AUDIO", "JUMPY"])


class TestGetDailyAnswer(unittest.TestCase):
    def test_returns_word_from_answer_list(self):
        result = get_daily_answer(ANSWERS)
        self.assertIn(result, ANSWERS)

    def test_same_date_returns_same_word(self):
        fixed = date(2024, 1, 15)
        with patch("persistence.daily.date") as mock_date:
            mock_date.today.return_value = fixed
            mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
            r1 = get_daily_answer(ANSWERS)
            r2 = get_daily_answer(ANSWERS)
        self.assertEqual(r1, r2)

    def test_different_dates_may_return_different_words(self):
        answers = frozenset([f"WOR{c}D" for c in "LMNOP"])  # 5 distinct words
        results = set()
        for day in range(5):
            d = date(2024, 1, day + 1)
            with patch("persistence.daily.date") as mock_date:
                mock_date.today.return_value = d
                mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
                results.add(get_daily_answer(answers))
        self.assertGreater(len(results), 1)

    def test_index_wraps_within_list_bounds(self):
        for day_offset in range(100):
            d = date(2021, 6, 19)
            from datetime import timedelta
            d = d + timedelta(days=day_offset)
            with patch("persistence.daily.date") as mock_date:
                mock_date.today.return_value = d
                mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
                result = get_daily_answer(ANSWERS)
            self.assertIn(result, ANSWERS)


class TestAlreadyPlayedToday(unittest.TestCase):
    def test_returns_false_when_never_played(self):
        self.assertFalse(already_played_today({}))

    def test_returns_true_when_played_today(self):
        stats = {"daily_last_played": date.today().isoformat()}
        self.assertTrue(already_played_today(stats))

    def test_returns_false_when_played_yesterday(self):
        from datetime import timedelta
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        stats = {"daily_last_played": yesterday}
        self.assertFalse(already_played_today(stats))


class TestRecordDailyResult(unittest.TestCase):
    def test_records_date_and_result(self):
        stats = {}
        result = record_daily_result(stats, "won")
        self.assertEqual(result["daily_last_played"], date.today().isoformat())
        self.assertEqual(result["daily_last_result"], "won")

    def test_records_loss(self):
        stats = {}
        result = record_daily_result(stats, "lost")
        self.assertEqual(result["daily_last_result"], "lost")

    def test_does_not_mutate_input(self):
        stats = {"daily_last_played": "2024-01-01"}
        record_daily_result(stats, "won")
        self.assertEqual(stats["daily_last_played"], "2024-01-01")


if __name__ == "__main__":
    unittest.main()
