# wordle-cli

A command-line Wordle game written in Python. Guess the hidden 5-letter word in 6 attempts. Each guess is scored with color-coded feedback:

- **Green** — right letter, right position
- **Yellow** — right letter, wrong position
- **Gray** — letter not in the word

A QWERTY keyboard tracker keeps score of every letter you've used.

## Requirements

- Python 3.10+
- No third-party dependencies (color output uses ANSI escape codes)

## How to play

```bash
python3 main.py
```

Type a valid 5-letter word and press Enter. Keep guessing until you solve it or run out of attempts. After each game you'll be prompted to play again.

To exit at any time, press `Ctrl-C`.

## Running the tests

```bash
python3 -m unittest discover -s tests
```
