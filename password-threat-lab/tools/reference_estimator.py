"""Python reference model for the browser Password Threat Lab estimator.

The browser application is the public runtime. This standard-library-only module
provides repeatable local proof for the bounded heuristic model; it is not a
password-cracking engine, breach corpus, or security audit.
"""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import asdict, dataclass
from typing import Callable

COMMON_PASSWORDS = (
    "123456", "password", "123456789", "12345", "12345678", "qwerty",
    "1234567", "111111", "1234567890", "123123", "abc123", "1234",
    "password1", "iloveyou", "1q2w3e4r", "000000", "qwerty123", "zaq12wsx",
    "dragon", "sunshine", "princess", "letmein", "football", "monkey",
    "shadow", "master", "666666", "superman", "michael", "computer",
    "hello", "freedom", "whatever", "qazwsx", "trustno1", "starwars",
    "admin", "welcome", "login", "passw0rd", "secret", "changeme",
    "default", "guest", "root", "administrator", "user", "test",
    "baseball", "soccer", "hockey", "killer", "jordan", "harley",
    "hunter", "buster", "thomas", "tigger", "robert", "access",
    "love", "flower", "mustang", "batman", "summer", "winter",
    "spring", "autumn", "coffee", "cookie", "pepper", "cheese",
    "internet", "matrix", "pokemon", "naruto", "qwertyuiop", "asdfghjkl",
    "zxcvbnm", "1qaz2wsx", "q1w2e3r4", "987654321", "121212", "7777777",
    "555555", "112233", "159753", "654321", "696969", "888888",
    "linkedin", "facebook", "google", "youtube", "minecraft", "fortnite",
    "donald", "charlie", "jessica", "ashley", "daniel", "jennifer",
)

COMMON_WORDS = (
    "apple", "orange", "banana", "purple", "green", "blue", "black", "white",
    "happy", "lucky", "magic", "money", "family", "friend", "house", "home",
    "school", "work", "office", "music", "movie", "gaming", "gamer", "cat",
    "dog", "bird", "fish", "horse", "battery", "staple", "correct", "love",
    "baby", "angel", "summer", "winter", "spring", "autumn", "football",
    "baseball", "soccer", "hockey", "admin", "welcome", "secret", "dragon",
    "shadow", "master", "princess", "monkey", "sunshine", "flower", "coffee",
)

COMMON_INDEX = {value: index + 1 for index, value in enumerate(COMMON_PASSWORDS)}
WORD_INDEX = {value: index + 1 for index, value in enumerate(COMMON_WORDS)}
LEET_MAP = {
    "@": "a", "4": "a", "3": "e", "1": "i", "!": "i",
    "0": "o", "5": "s", "$": "s", "7": "t", "+": "t",
}
SEQUENCE_ROWS = (
    "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", "0123456789",
    "9876543210", "qwertyuiop", "poiuytrewq", "asdfghjkl", "lkjhgfdsa",
    "zxcvbnm", "mnbvcxz", "1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik9ol0p",
    "0pl9ok8ij7uh6yg5tf4rd3es2wa1q",
)
LABELS = ("Very weak", "Weak", "Fair", "Strong", "Very strong")
SECONDS_PER_YEAR = 31_557_600


@dataclass(frozen=True)
class Candidate:
    guess_bits: float
    method: str
    explanation: str
    signal: str


def safe_log2(value: float) -> float:
    return max(0.0, math.log2(max(1.0, value)))


def normalize_leetspeak(value: str) -> str:
    return "".join(LEET_MAP.get(character, character) for character in value.lower())


def case_variant_multiplier(value: str) -> int:
    letters = sum(character.isascii() and character.isalpha() for character in value)
    if letters == 0 or value == value.lower():
        return 1
    if value == value.upper() or re.fullmatch(r"[A-Z][a-z]+", value):
        return 2
    return min(2 ** min(letters, 12), 4096)


def leet_variant_multiplier(value: str) -> int:
    substitutions = sum(character in LEET_MAP for character in value)
    return min(4**substitutions, 4096) if substitutions else 1


def inferred_alphabet_size(password: str) -> int:
    size = 0
    if re.search(r"[a-z]", password):
        size += 26
    if re.search(r"[A-Z]", password):
        size += 26
    if re.search(r"[0-9]", password):
        size += 10
    if any(not char.isalnum() and not char.isspace() for char in password):
        size += 32
    if any(char.isspace() for char in password):
        size += 1
    if any(ord(char) > 127 for char in password):
        size += 100
    return max(2, size)


def candidate(guess_bits: float, method: str, explanation: str, signal: str) -> Candidate:
    return Candidate(max(1.0, guess_bits), method, explanation, signal)


def common_password_candidate(password: str) -> Candidate | None:
    rank = COMMON_INDEX.get(password.lower()) or COMMON_INDEX.get(normalize_leetspeak(password))
    if not rank:
        return None
    guesses = rank * case_variant_multiplier(password) * leet_variant_multiplier(password)
    return candidate(
        safe_log2(guesses),
        "common-password match",
        "It matches a commonly attempted password after basic case or leetspeak normalization.",
        "Common password or trivial substitution",
    )


def word_plus_suffix_candidate(password: str) -> Candidate | None:
    match = re.fullmatch(r"([^A-Za-z]*)([A-Za-z]{3,})(\d{1,8})([^A-Za-z0-9]*)", password)
    if not match:
        return None
    prefix, word, digits, suffix = match.groups()
    normalized_word = normalize_leetspeak(word)
    base_rank = COMMON_INDEX.get(normalized_word) or WORD_INDEX.get(normalized_word)
    if not base_rank:
        return None
    decoration_multiplier = max(1, 33 ** min(len(prefix) + len(suffix), 2))
    guesses = base_rank * case_variant_multiplier(word) * (10 ** len(digits)) * decoration_multiplier
    return candidate(
        safe_log2(guesses),
        "word with predictable suffix",
        "Attackers commonly test familiar words followed by years, counters, or punctuation.",
        "Familiar word plus predictable digits or punctuation",
    )


def sequence_candidate(password: str) -> Candidate | None:
    lowered = password.lower()
    if len(lowered) < 3:
        return None
    for row in SEQUENCE_ROWS:
        if lowered in row:
            guesses = 200 * len(lowered) * case_variant_multiplier(password)
            return candidate(
                safe_log2(guesses),
                "keyboard or character sequence",
                "It is a straight keyboard, alphabetic, or numeric run that attackers test early.",
                "Keyboard, alphabetic, or numeric sequence",
            )
    return None


def repeat_candidate(password: str) -> Candidate | None:
    if not password:
        return None
    if len(set(password)) == 1:
        return candidate(
            safe_log2(50 * len(password)),
            "repeated character",
            "Repeating one character creates very few plausible patterns to test.",
            "Repeated character",
        )
    for block_length in range(1, len(password) // 2 + 1):
        if len(password) % block_length:
            continue
        block = password[:block_length]
        repeats = len(password) // block_length
        if repeats >= 2 and block * repeats == password:
            block_bits = block_length * math.log2(inferred_alphabet_size(block))
            return candidate(
                block_bits + math.log2(repeats) + 2,
                "repeated block",
                "A short block repeats, so an attacker can search the block and repetition count instead of every character.",
                "Repeated block",
            )
    return None


def date_candidate(password: str) -> Candidate | None:
    compact = re.sub(r"[-/. ]", "", password)
    if not compact.isdigit():
        return None
    looks_like_year = bool(re.fullmatch(r"(?:19|20)\d{2}", compact))
    looks_like_date = len(compact) in {6, 8}
    if not looks_like_year and not looks_like_date:
        return None
    guesses = 50_000 if looks_like_year else 5_000_000
    return candidate(
        safe_log2(guesses),
        "date-like pattern",
        "Dates and years occupy a much smaller search space than arbitrary digits.",
        "Date or year pattern",
    )


def phrase_candidate(password: str) -> Candidate | None:
    tokens = re.findall(r"[A-Za-z]+", password)
    separators = re.findall(r"[^A-Za-z]+", password)
    if not tokens or not separators or not 2 <= len(tokens) <= 10:
        return None
    if len("".join(tokens)) + len("".join(separators)) != len(password):
        return None
    dictionary_bits = len(tokens) * math.log2(10_000)
    separator_bits = min(8, len(separators) * 2)
    case_bits = min(12, sum(token != token.lower() for token in tokens) * 2)
    return candidate(
        dictionary_bits + separator_bits + case_bits - 1,
        "word-based phrase",
        "The model assumes an attacker tests combinations of common dictionary words and separators.",
        f"{len(tokens)}-word phrase",
    )


def random_space_candidate(password: str) -> Candidate:
    alphabet = inferred_alphabet_size(password)
    average_guess_bits = max(1.0, len(password) * math.log2(alphabet) - 1)
    return candidate(
        average_guess_bits,
        "character-space estimate",
        f"The random model uses an inferred alphabet of about {alphabet} characters and the average position in that space.",
        f"Random {alphabet}-character alphabet model",
    )


def score_from_bits(bits: float) -> int:
    if bits < 20:
        return 0
    if bits < 32:
        return 1
    if bits < 48:
        return 2
    if bits < 64:
        return 3
    return 4


def build_suggestions(selected: Candidate, bits: float) -> list[str]:
    suggestions: list[str] = []
    predictable = {
        "common-password match",
        "word with predictable suffix",
        "keyboard or character sequence",
        "repeated character",
        "repeated block",
        "date-like pattern",
    }
    if selected.method in predictable:
        suggestions.append(
            "Replace words, dates, sequences, and substitutions with genuinely random choices."
        )
    if bits < 64:
        suggestions.append(
            "Use a password manager to generate at least 16 random characters, or use 4–6 randomly selected words."
        )
    suggestions.append(
        "Use a unique password for every account and enable phishing-resistant MFA where available."
    )
    return suggestions[:3]


def estimate_password(password: str) -> dict[str, object]:
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    if not password:
        raise ValueError("password cannot be empty")
    random = random_space_candidate(password)
    candidates = [random]
    builders: tuple[Callable[[str], Candidate | None], ...] = (
        common_password_candidate,
        word_plus_suffix_candidate,
        sequence_candidate,
        repeat_candidate,
        date_candidate,
        phrase_candidate,
    )
    for builder in builders:
        result = builder(password)
        if result:
            candidates.append(result)
    candidates.sort(key=lambda item: item.guess_bits)
    selected = candidates[0]
    score = score_from_bits(selected.guess_bits)
    return {
        "length": len(password),
        "pattern": asdict(selected),
        "random": asdict(random),
        "candidates": [asdict(item) for item in candidates],
        "score": score,
        "label": LABELS[score],
        "suggestions": build_suggestions(selected, selected.guess_bits),
        "signals": [item.signal for item in candidates if item.method != "character-space estimate"],
        "grover": {
            "query_bits": random.guess_bits / 2,
            "basis": "random-space square-root query proxy",
        },
    }


def log10_count_from_bits(bits: float) -> float:
    return bits * math.log10(2)


def format_count_from_bits(bits: float) -> str:
    log10_value = log10_count_from_bits(bits)
    if log10_value < 15:
        return f"{max(1, round(10**log10_value)):,}"
    exponent = math.floor(log10_value)
    mantissa = 10 ** (log10_value - exponent)
    return f"≈ {mantissa:.2f} × 10^{exponent}"


def _format_scaled(log10_value: float, unit: str) -> str:
    value = 10**log10_value
    if value < 10:
        text = f"{value:.2f}"
    elif value < 100:
        text = f"{value:.1f}"
    else:
        text = f"{value:.0f}"
    suffix = "" if abs(value - 1) < 0.005 else "s"
    return f"{text} {unit}{suffix}"


def format_duration(guess_bits: float, guesses_per_second: float) -> str:
    if not math.isfinite(guesses_per_second) or guesses_per_second <= 0:
        raise ValueError("guesses_per_second must be a positive finite number")
    value = log10_count_from_bits(guess_bits) - math.log10(guesses_per_second)
    if value < -6:
        return "under 1 microsecond"
    if value < -3:
        return _format_scaled(value + 6, "microsecond")
    if value < 0:
        return _format_scaled(value + 3, "millisecond")
    if value < math.log10(60):
        return _format_scaled(value, "second")
    if value < math.log10(3600):
        return _format_scaled(value - math.log10(60), "minute")
    if value < math.log10(86_400):
        return _format_scaled(value - math.log10(3600), "hour")
    if value < math.log10(SECONDS_PER_YEAR):
        return _format_scaled(value - math.log10(86_400), "day")
    years = value - math.log10(SECONDS_PER_YEAR)
    if years < 6:
        return _format_scaled(years, "year")
    exponent = math.floor(years)
    return f"≈ {10 ** (years - exponent):.2f} × 10^{exponent} years"


def _describe_character(char: str) -> str:
    """Return a bounded descriptor for diagnostic messages without echoing input."""
    if ord(char) < 128:
        return "ASCII"
    return unicodedata.category(char)


__all__ = [
    "estimate_password",
    "format_count_from_bits",
    "format_duration",
    "inferred_alphabet_size",
    "log10_count_from_bits",
    "normalize_leetspeak",
]
