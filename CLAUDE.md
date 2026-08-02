# Wordle CLI — Claude Instructions

## Project
Python CLI Wordle game with a story/narrative mode. Each chapter unlocks a themed set of five-letter words. Solving a puzzle advances the story. The project is treated as a professional-grade product — think sprint ceremonies, acceptance criteria, regression safety, and clean git history.

GitHub repo: https://github.com/Bitmugger/wordle-cli

## Terminology
- "tickets" / "stories" = GitHub Issues at https://github.com/Bitmugger/wordle-cli/issues
- "chapter" = one narrative arc, made up of a set of themed words
- "puzzle" = one five-letter word guess challenge

## GitHub Issue Format
Every issue body must start with this metadata header:
```
**Status:** Open | In Progress | Done
**Priority:** High | Medium | Low
**Estimate:** Small | Medium | Large
**Branch:** —
**Commits:** —
```

Issues should be written as user stories where applicable:
> As a [role], I want [feature] so that [benefit].

Each story must include **Acceptance Criteria** (bulleted checklist) and a **Notes** section for implementation hints or open questions.

### Field Definitions
- **Status** — current state. Set to `In Progress` when work begins, `Done` when the issue is closed.
- **Priority** — `High` = core/blocking, `Medium` = important but not blocking, `Low` = polish or stretch goals.
- **Estimate** — `Small` = a few minutes to an hour, `Medium` = a few hours, `Large` = a day or more.
- **Branch** — the git branch being used for this ticket (e.g. `feature/1-word-list`). Update when work begins.
- **Commits** — comma-separated short SHAs once work is merged.

### Workflow
1. When starting a ticket: create a branch named `feature/<id>-<short-slug>`, set Status → `In Progress`, set Branch field.
2. When work is done: set Status → `Done`, add Commit SHAs, close the issue.

### Branch Rules
- One ticket per branch.
- If the user asks to implement work spanning more than one ticket on the same branch, warn: "⚠️ This would put multiple tickets on one branch. Want to split into separate branches?"

## Displaying Tickets
When the user asks to see tickets, fetch from GitHub and display as a markdown table sorted by issue ID:

| # | Title | Priority | Status | Branch |
|---|-------|----------|--------|--------|
| 1 | Word list — curated five-letter words | High | Open | — |

Only deviate from this format if the user explicitly asks.

## Testing
Write unit tests for every ticket wherever possible. Use Python's built-in `unittest` module. Tests live in `tests/` with filenames matching `test_<module>.py`. Run with `python -m pytest` or `python -m unittest discover`.

**Do not close a ticket without tests** unless the functionality is untestable (e.g. pure display/rendering with no logic).

Every PR-equivalent unit of work should leave the test suite green.

## Project Conventions
- Python 3.10+; no third-party runtime dependencies (stdlib + optional `colorama` for color output).
- Keep functions small and single-purpose.
- Use f-strings over `.format()`.
- All game state should be serializable to JSON for save/load.
- Story content (chapter text, word sets) lives in `stories/` as JSON files, not hardcoded in Python.
- Word validation uses a single canonical word list in `words/`.

## Architecture Overview (evolving)
```
wordle-cli/
├── game/           # Core game engine (guess logic, scoring, state)
├── stories/        # Chapter JSON files (narrative text + themed word lists)
├── words/          # Full valid-word list for guess validation
├── cli/            # Terminal rendering, color output, input handling
├── persistence/    # Save/load player progress (JSON)
├── tests/          # Unit tests (mirrors source structure)
└── main.py         # Entry point
```

## Big-Project Ground Rules
- No story is "done" without passing tests and a closed GitHub issue.
- Prefer small, focused commits — one logical change per commit.
- Acceptance criteria in the issue drive what gets built — nothing more, nothing less.
- When in doubt about scope, keep it small and open a follow-up ticket rather than scope-creeping.
