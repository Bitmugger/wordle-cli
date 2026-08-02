import json
import os
from pathlib import Path

STATS_PATH = Path.home() / ".wordle-cli" / "stats.json"

DEFAULT_STATS: dict = {
    "schema_version": 1,
    "games_played": 0,
    "wins": 0,
    "current_streak": 0,
    "max_streak": 0,
}


def load_stats(path: Path = STATS_PATH) -> dict:
    if not path.exists():
        return DEFAULT_STATS.copy()
    return json.loads(path.read_text())


def save_stats(stats: dict, path: Path = STATS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(stats, indent=2))
    os.replace(tmp, path)


def update_stats(stats: dict, won: bool) -> dict:
    stats = stats.copy()
    stats["games_played"] += 1
    if won:
        stats["wins"] += 1
        stats["current_streak"] += 1
        stats["max_streak"] = max(stats["max_streak"], stats["current_streak"])
    else:
        stats["current_streak"] = 0
    return stats


def format_stats(stats: dict) -> str:
    played = stats["games_played"]
    win_pct = round(stats["wins"] / played * 100) if played else 0
    return (
        f"  Games: {played} | "
        f"Win%: {win_pct} | "
        f"Streak: {stats['current_streak']} | "
        f"Best: {stats['max_streak']}"
    )
