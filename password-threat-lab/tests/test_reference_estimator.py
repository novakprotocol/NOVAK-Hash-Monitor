from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

from tools.reference_estimator import (
    estimate_password,
    format_duration,
    inferred_alphabet_size,
)

ROOT = Path(__file__).resolve().parents[1]


class ReferenceEstimatorTests(unittest.TestCase):
    def test_common_password_is_detected(self) -> None:
        result = estimate_password("password")
        self.assertEqual(result["pattern"]["method"], "common-password match")
        self.assertEqual(result["label"], "Very weak")

    def test_predictable_suffix_is_detected(self) -> None:
        result = estimate_password("Password1!")
        self.assertEqual(result["pattern"]["method"], "word with predictable suffix")
        self.assertEqual(result["label"], "Very weak")

    def test_keyboard_sequence_is_a_signal(self) -> None:
        result = estimate_password("qwerty")
        self.assertIn("Keyboard, alphabetic, or numeric sequence", result["signals"])

    def test_repeated_block_is_detected(self) -> None:
        result = estimate_password("abcabcabc")
        self.assertEqual(result["pattern"]["method"], "repeated block")

    def test_word_phrase_is_detected(self) -> None:
        result = estimate_password("correct-horse-battery-staple")
        self.assertIn("4-word phrase", result["signals"])

    def test_random_sample_scores_very_strong(self) -> None:
        result = estimate_password("m7Q!v2K@p9R#x4Tz")
        self.assertEqual(result["label"], "Very strong")

    def test_grover_query_bits_are_half_random_bits(self) -> None:
        result = estimate_password("m7Q!v2K@p9R#x4Tz")
        self.assertAlmostEqual(
            result["grover"]["query_bits"], result["random"]["guess_bits"] / 2
        )

    def test_unicode_alphabet_is_bounded(self) -> None:
        self.assertGreaterEqual(inferred_alphabet_size("пароль🔐"), 100)
        self.assertLess(inferred_alphabet_size("пароль🔐"), 200)

    def test_long_input_does_not_overflow(self) -> None:
        result = estimate_password("Ab9!" * 64)
        self.assertTrue(math.isfinite(result["random"]["guess_bits"]))
        self.assertEqual(result["length"], 256)

    def test_duration_rejects_non_positive_rate(self) -> None:
        with self.assertRaises(ValueError):
            format_duration(32, 0)

    def test_attack_profile_contract(self) -> None:
        payload = json.loads((ROOT / "data" / "attack-profiles.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], "n.password-threat.attack-profiles.v1")
        self.assertIn(payload["default_profile_id"], {item["id"] for item in payload["profiles"]})
        self.assertTrue(all(item["guesses_per_second"] > 0 for item in payload["profiles"]))

    def test_empty_input_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            estimate_password("")


if __name__ == "__main__":
    unittest.main()
