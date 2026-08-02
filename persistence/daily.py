from datetime import date

EPOCH = date(2021, 6, 19)  # original Wordle launch date


def get_daily_answer(answers: frozenset[str]) -> str:
    answers_sorted = sorted(answers)
    day_index = (date.today() - EPOCH).days
    return answers_sorted[day_index % len(answers_sorted)]


def already_played_today(stats: dict) -> bool:
    return stats.get("daily_last_played") == date.today().isoformat()


def record_daily_result(stats: dict, result: str) -> dict:
    stats = stats.copy()
    stats["daily_last_played"] = date.today().isoformat()
    stats["daily_last_result"] = result
    return stats
