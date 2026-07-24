from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from reference_estimator import (  # noqa: E402
    estimate_password,
    format_count_from_bits,
    format_duration,
    inferred_alphabet_size,
)


class ReferenceEstimatorTests(unittest.TestCase):
    def test_common_password_uses_shortcut(self) -> None:
        result = estimate_password("password")
        self.assertEqual(result.pattern.method, "common-password match")
        self.assertLess(result.pattern.guess_bits, result.random.guess_bits)
        self.assertEqual(result.label, "Very weak")

    def test_predictable_suffix_is_not_treated_as_uniform_random(self) -> None:
        result = estimate_password("Password1!")
        self.assertEqual(result.pattern.method, "word with predictable suffix")
        self.assertLess(result.pattern.guess_bits, result.random.guess_bits)

    def test_sequence_detection(self) -> None:
        result = estimate_password("qwerty")
        methods = {result.pattern.method, *(signal for signal in result.signals)}
        self.assertIn("common-password match", methods)
        self.assertIn("Keyboard, alphabetic, or numeric sequence", result.signals)

    def test_repeated_block_detection(self) -> None:
        result = estimate_password("abcabcabc")
        self.assertEqual(result.pattern.method, "repeated block")

    def test_phrase_candidate_is_bounded(self) -> None:
        result = estimate_password("correct-horse-battery-staple")
        self.assertIn("4-word phrase", result.signals)
        self.assertLessEqual(result.pattern.guess_bits, result.random.guess_bits)

    def test_random_generated_style_sample_scores_high(self) -> None:
        result = estimate_password("m7Q!v2K@p9R#x4Tz")
        self.assertGreaterEqual(result.random.guess_bits, 100)
        self.assertEqual(result.label, "Very strong")

    def test_grover_proxy_halves_random_query_bits(self) -> None:
        result = estimate_password("m7Q!v2K@p9R#x4Tz")
        self.assertAlmostEqual(result.grover_query_bits, result.random.guess_bits / 2)

    def test_unicode_increases_bounded_alphabet(self) -> None:
        self.assertGreaterEqual(inferred_alphabet_size("correct-🔐-sample"), 100)

    def test_long_input_does_not_overflow(self) -> None:
        result = estimate_password("Ab9!" * 64)
        text = format_count_from_bits(result.random.guess_bits)
        self.assertIn("10^", text)

    def test_duration_requires_positive_finite_rate(self) -> None:
        with self.assertRaises(ValueError):
            format_duration(32, 0)

    def test_attack_profile_contract(self) -> None:
        data = json.loads((ROOT / "data" / "attack-profiles.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "n.password-threat.attack-profiles.v1")
        self.assertGreaterEqual(len(data["profiles"]), 4)
        self.assertTrue(all(item["guesses_per_second"] > 0 for item in data["profiles"]))

    def test_empty_value_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            estimate_password("")


if __name__ == "__main__":
    unittest.main()
