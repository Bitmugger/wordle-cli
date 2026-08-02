from pathlib import Path


def load_word_list(path: str | Path) -> frozenset[str]:
    words = frozenset(
        word.strip().upper()
        for word in Path(path).read_text().splitlines()
        if word.strip()
    )
    invalid = [w for w in words if len(w) != 5]
    if invalid:
        raise ValueError(f"Word list contains non-5-letter words: {invalid[:5]}")
    return words


def is_valid_guess(word: str, word_list: frozenset[str]) -> bool:
    return word.strip().upper() in word_list
