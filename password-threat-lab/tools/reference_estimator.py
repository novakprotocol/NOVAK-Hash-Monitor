"""Reference model for the Password Threat Lab.

The public interface runs in the browser. This standard-library module mirrors
its bounded heuristic so repository checks can prove deterministic behavior
without processing a real credential or contacting a network service.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
import re
import string
from typing import Callable

COMMON_PASSWORDS = [
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
]

COMMON_WORDS = [
    "apple", "orange", "banana", "purple", "green", "blue", "black", "white",
    "happy", "lucky", "magic", "money", "family", "friend", "house", "home",
    "school", "work", "office", "music", "movie", "gaming", "gamer", "cat",
    "dog", "bird", "fish", "horse", "battery", "staple", "correct", "love",
    "baby", "angel", "summer", "winter", "spring", "autumn", "football",
    "baseball", "soccer", "hockey", "admin", "welcome", "secret", "dragon",
    "shadow", "master", "princess", "monkey", "sunshine", "flower", "coffee",
]

COMMON_INDEX = {value: index + 1 for index, value in enumerate(COMMON_PASSWORDS)}
WORD_INDEX = {value: index + 1 for index, value in enumerate(COMMON_WORDS)}
LEET_TRANSLATION = str.maketrans(
    {"@": "a", "4": "a", "3": "e", "1": "i", "!": "i", "0": "o", "5": "s", "$": "s", "7": "t", "+": "t"}
)
SEQUENCE_ROWS = [
    "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", "0123456789",
    "9876543210", "qwertyuiop", "poiuytrewq", "asdfghjkl", "lkjhgfdsa",
    "zxcvbnm", "mnbvcxz", "1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik9ol0p",
    "0pl9ok8ij7uh6yg5tf4rd3es2wa1q",
]
LABELS = ("Very weak", "Weak", "Fair", "Strong", "Very strong")


@dataclass(frozen=True)
class Candidate:
    guess_bits: float
    method: str
    explanation: str
    signal: str


@dataclass(frozen=True)
class Estimate:
    length: int
    label: str
    score: int
    pattern: Candidate
    random: Candidate
    signals: tuple[str, ...]
    suggestions: tuple[str, ...]

    @property
    def grover_query_bits(self) -> float:
        return self.random.guess_bits / 2.0


def _safe_log2(value: float) -> float:
    return max(0.0, math.log2(max(1.0, value)))


def _normalize_leetspeak(value: str) -> str:
    return value.lower().translate(LEET_TRANSLATION)


def _case_variant_multiplier(value: str) -> int:
    letters = sum(character.isalpha() and character.isascii() for character in value)
    if letters == 0 or value.islower():
        return 1
    if value.isupper() or value.istitle():
        return 2
    return min(2 ** min(letters, 12), 4096)


def _leet_variant_multiplier(value: str) -> int:
    substitutions = sum(character in "@431!05$7+" for character in value)
    return min(4 ** substitutions, 4096) if substitutions else 1


def inferred_alphabet_size(password: str) -> int:
    size = 0
    if any(character.islower() and character.isascii() for character in password):
        size += 26
    if any(character.isupper() and character.isascii() for character in password):
        size += 26
    if any(character.isdigit() and character.isascii() for character in password):
        size += 10
    if any(character in string.punctuation for character in password):
        size += len(string.punctuation)
    if any(character.isspace() for character in password):
        size += 1
    if any(not character.isascii() and not character.isspace() for character in password):
        size += 100
    return max(2, size)


def _random_candidate(password: str) -> Candidate:
    alphabet = inferred_alphabet_size(password)
    bits = max(1.0, len(password) * math.log2(alphabet) - 1.0)
    return Candidate(
        bits,
        "character-space estimate",
        f"The random model uses an inferred alphabet of about {alphabet} characters and the average position in that space.",
        f"Random {alphabet}-character alphabet model",
    )


def _common_candidate(password: str) -> Candidate | None:
    rank = COMMON_INDEX.get(password.lower()) or COMMON_INDEX.get(_normalize_leetspeak(password))
    if rank is None:
        return None
    guesses = rank * _case_variant_multiplier(password) * _leet_variant_multiplier(password)
    return Candidate(
        _safe_log2(guesses),
        "common-password match",
        "It matches a commonly attempted password after basic case or leetspeak normalization.",
        "Common password or trivial substitution",
    )


def _word_suffix_candidate(password: str) -> Candidate | None:
    match = re.fullmatch(r"([^A-Za-z]*)([A-Za-z]{3,})(\d{1,8})([^A-Za-z0-9]*)", password)
    if not match:
        return None
    prefix, word, digits, suffix = match.groups()
    normalized_word = _normalize_leetspeak(word)
    base_rank = COMMON_INDEX.get(normalized_word) or WORD_INDEX.get(normalized_word)
    if base_rank is None:
        return None
    decorations = max(1, 33 ** min(len(prefix) + len(suffix), 2))
    guesses = base_rank * _case_variant_multiplier(word) * 10 ** len(digits) * decorations
    return Candidate(
        _safe_log2(guesses),
        "word with predictable suffix",
        "Attackers commonly test familiar words followed by years, counters, or punctuation.",
        "Familiar word plus predictable digits or punctuation",
    )


def _sequence_candidate(password: str) -> Candidate | None:
    lowered = password.lower()
    if len(lowered) < 3:
        return None
    if any(lowered in row for row in SEQUENCE_ROWS):
        guesses = 200 * len(lowered) * _case_variant_multiplier(password)
        return Candidate(
            _safe_log2(guesses),
            "keyboard or character sequence",
            "It is a straight keyboard, alphabetic, or numeric run that attackers test early.",
            "Keyboard, alphabetic, or numeric sequence",
        )
    return None


def _repeat_candidate(password: str) -> Candidate | None:
    if not password:
        return None
    if len(set(password)) == 1:
        return Candidate(
            _safe_log2(50 * len(password)),
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
            bits = block_length * math.log2(inferred_alphabet_size(block)) + math.log2(repeats) + 2
            return Candidate(
                max(1.0, bits),
                "repeated block",
                "A short block repeats, so an attacker can search the block and repetition count instead of every character.",
                "Repeated block",
            )
    return None


def _date_candidate(password: str) -> Candidate | None:
    compact = re.sub(r"[-/. ]", "", password)
    if not compact.isdigit():
        return None
    looks_like_year = bool(re.fullmatch(r"(?:19|20)\d{2}", compact))
    looks_like_date = len(compact) in {6, 8}
    if not (looks_like_year or looks_like_date):
        return None
    guesses = 50_000 if looks_like_year else 5_000_000
    return Candidate(
        _safe_log2(guesses),
        "date-like pattern",
        "Dates and years occupy a much smaller search space than arbitrary digits.",
        "Date or year pattern",
    )


def _phrase_candidate(password: str) -> Candidate | None:
    tokens = re.findall(r"[A-Za-z]+", password)
    separators = re.findall(r"[^A-Za-z]+", password)
    if not (2 <= len(tokens) <= 10 and separators):
        return None
    if sum(map(len, tokens)) + sum(map(len, separators)) != len(password):
        return None
    bits = len(tokens) * math.log2(10_000)
    bits += min(8.0, len(separators) * 2.0)
    bits += min(12.0, sum(token != token.lower() for token in tokens) * 2.0)
    return Candidate(
        max(1.0, bits - 1.0),
        "word-based phrase",
        "The model assumes an attacker tests combinations of common dictionary words and separators.",
        f"{len(tokens)}-word phrase",
    )


def _score(bits: float) -> int:
    if bits < 20:
        return 0
    if bits < 32:
        return 1
    if bits < 48:
        return 2
    if bits < 64:
        return 3
    return 4


def estimate_password(password: str) -> Estimate:
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    if not password:
        raise ValueError("password cannot be empty")

    random = _random_candidate(password)
    candidates = [random]
    builders: tuple[Callable[[str], Candidate | None], ...] = (
        _common_candidate,
        _word_suffix_candidate,
        _sequence_candidate,
        _repeat_candidate,
        _date_candidate,
        _phrase_candidate,
    )
    for builder in builders:
        result = builder(password)
        if result is not None:
            candidates.append(result)
    selected = min(candidates, key=lambda item: item.guess_bits)
    score = _score(selected.guess_bits)
    signals = tuple(item.signal for item in candidates if item.method != "character-space estimate")
    suggestions: list[str] = []
    if selected.method != "character-space estimate" and selected.method != "word-based phrase":
        suggestions.append("Replace words, dates, sequences, and substitutions with genuinely random choices.")
    if selected.guess_bits < 64:
        suggestions.append("Use a password manager to generate at least 16 random characters, or use 4–6 randomly selected words.")
    suggestions.append("Use a unique password for every account and enable phishing-resistant MFA where available.")
    return Estimate(
        length=len(password),
        label=LABELS[score],
        score=score,
        pattern=selected,
        random=random,
        signals=signals,
        suggestions=tuple(suggestions[:3]),
    )


def log10_count_from_bits(bits: float) -> float:
    return bits * math.log10(2.0)


def format_count_from_bits(bits: float) -> str:
    logarithm = log10_count_from_bits(bits)
    if logarithm < 15:
        return f"{max(1, round(10 ** logarithm)):,}"
    exponent = math.floor(logarithm)
    mantissa = 10 ** (logarithm - exponent)
    return f"≈ {mantissa:.2f} × 10^{exponent}"


def format_duration(guess_bits: float, guesses_per_second: float) -> str:
    if not math.isfinite(guesses_per_second) or guesses_per_second <= 0:
        raise ValueError("guesses_per_second must be a positive finite number")
    seconds_log10 = log10_count_from_bits(guess_bits) - math.log10(guesses_per_second)
    if seconds_log10 < -6:
        return "under 1 microsecond"
    if seconds_log10 < -3:
        return _format_scaled(seconds_log10 + 6, "microsecond")
    if seconds_log10 < 0:
        return _format_scaled(seconds_log10 + 3, "millisecond")
    if seconds_log10 < math.log10(60):
        return _format_scaled(seconds_log10, "second")
    if seconds_log10 < math.log10(3600):
        return _format_scaled(seconds_log10 - math.log10(60), "minute")
    if seconds_log10 < math.log10(86_400):
        return _format_scaled(seconds_log10 - math.log10(3600), "hour")
    if seconds_log10 < math.log10(31_557_600):
        return _format_scaled(seconds_log10 - math.log10(86_400), "day")
    years_log10 = seconds_log10 - math.log10(31_557_600)
    if years_log10 < 6:
        return _format_scaled(years_log10, "year")
    exponent = math.floor(years_log10)
    mantissa = 10 ** (years_log10 - exponent)
    return f"≈ {mantissa:.2f} × 10^{exponent} years"


def _format_scaled(log10_value: float, unit: str) -> str:
    value = 10 ** log10_value
    text = f"{value:.2f}" if value < 10 else f"{value:.1f}" if value < 100 else f"{value:.0f}"
    plural = "" if abs(value - 1) < 0.005 else "s"
    return f"{text} {unit}{plural}"


def _demo_payload() -> dict[str, object]:
    examples = ["password", "Password1!", "correct-horse-battery-staple", "m7Q!v2K@p9R#x4Tz"]
    return {
        "schema_version": "n.password-threat.reference-demo.v1",
        "examples": [
            {
                "sample_label": f"example-{index + 1}",
                "estimate": {
                    **asdict(estimate_password(value)),
                    "grover_query_bits": estimate_password(value).grover_query_bits,
                },
            }
            for index, value in enumerate(examples)
        ],
        "claim_boundary": "Built-in examples only; no real credential was processed.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Password Threat Lab reference-model demo.")
    parser.add_argument("--demo", action="store_true", help="Emit deterministic built-in sample results as JSON.")
    args = parser.parse_args()
    if not args.demo:
        parser.print_help()
        return 0
    print(json.dumps(_demo_payload(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
