(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.PasswordThreatEstimator = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const COMMON_PASSWORDS = [
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
    "donald", "charlie", "jessica", "ashley", "daniel", "jennifer"
  ];
  const COMMON_WORDS = [
    "apple", "orange", "banana", "purple", "green", "blue", "black", "white",
    "happy", "lucky", "magic", "money", "family", "friend", "house", "home",
    "school", "work", "office", "music", "movie", "gaming", "gamer", "cat",
    "dog", "bird", "fish", "horse", "battery", "staple", "correct", "love",
    "baby", "angel", "summer", "winter", "spring", "autumn", "football",
    "baseball", "soccer", "hockey", "admin", "welcome", "secret", "dragon",
    "shadow", "master", "princess", "monkey", "sunshine", "flower", "coffee"
  ];
  const COMMON_INDEX = new Map(COMMON_PASSWORDS.map((value, index) => [value, index + 1]));
  const WORD_INDEX = new Map(COMMON_WORDS.map((value, index) => [value, index + 1]));
  const LEET_MAP = Object.freeze({
    "@": "a", "4": "a", "3": "e", "1": "i", "!": "i",
    "0": "o", "5": "s", "$": "s", "7": "t", "+": "t"
  });
  const SEQUENCE_ROWS = [
    "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", "0123456789",
    "9876543210", "qwertyuiop", "poiuytrewq", "asdfghjkl", "lkjhgfdsa",
    "zxcvbnm", "mnbvcxz", "1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik9ol0p",
    "0pl9ok8ij7uh6yg5tf4rd3es2wa1q"
  ];
  const LABELS = ["Very weak", "Weak", "Fair", "Strong", "Very strong"];
  const LOG10_2 = Math.log10(2);
  const SECONDS_PER_YEAR = 31_557_600;

  function codePointLength(value) { return Array.from(value).length; }
  function safeLog2(value) { return Math.max(0, Math.log2(Math.max(1, value))); }
  function normalizeLeetspeak(value) {
    return Array.from(value.toLowerCase(), (character) => LEET_MAP[character] || character).join("");
  }
  function caseVariantMultiplier(value) {
    const letters = Array.from(value).filter((character) => /[A-Za-z]/.test(character)).length;
    if (letters === 0 || value === value.toLowerCase()) return 1;
    if (value === value.toUpperCase() || /^[A-Z][a-z]+$/.test(value)) return 2;
    return Math.min(2 ** Math.min(letters, 12), 4096);
  }
  function leetVariantMultiplier(value) {
    const substitutions = Array.from(value).filter((character) => Object.hasOwn(LEET_MAP, character)).length;
    return substitutions ? Math.min(4 ** substitutions, 4096) : 1;
  }
  function inferredAlphabetSize(password) {
    let size = 0;
    if (/[a-z]/.test(password)) size += 26;
    if (/[A-Z]/.test(password)) size += 26;
    if (/[0-9]/.test(password)) size += 10;
    if (/[^\p{L}\p{N}\s]/u.test(password)) size += 32;
    if (/\s/u.test(password)) size += 1;
    if (/[^\x00-\x7F]/u.test(password)) size += 100;
    return Math.max(2, size);
  }
  function candidate(guessBits, method, explanation, signal) {
    return { guessBits: Math.max(1, guessBits), method, explanation, signal };
  }
  function commonPasswordCandidate(password) {
    const rank = COMMON_INDEX.get(password.toLowerCase()) || COMMON_INDEX.get(normalizeLeetspeak(password));
    if (!rank) return null;
    const guesses = rank * caseVariantMultiplier(password) * leetVariantMultiplier(password);
    return candidate(safeLog2(guesses), "common-password match",
      "It matches a commonly attempted password after basic case or leetspeak normalization.",
      "Common password or trivial substitution");
  }
  function wordPlusSuffixCandidate(password) {
    const match = password.match(/^([^A-Za-z]*)([A-Za-z]{3,})(\d{1,8})([^A-Za-z0-9]*)$/);
    if (!match) return null;
    const [, prefix, word, digits, suffix] = match;
    const normalizedWord = normalizeLeetspeak(word);
    const baseRank = COMMON_INDEX.get(normalizedWord) || WORD_INDEX.get(normalizedWord);
    if (!baseRank) return null;
    const decorationMultiplier = Math.max(1, 33 ** Math.min(prefix.length + suffix.length, 2));
    const guesses = baseRank * caseVariantMultiplier(word) * (10 ** digits.length) * decorationMultiplier;
    return candidate(safeLog2(guesses), "word with predictable suffix",
      "Attackers commonly test familiar words followed by years, counters, or punctuation.",
      "Familiar word plus predictable digits or punctuation");
  }
  function sequenceCandidate(password) {
    const lowered = password.toLowerCase();
    if (codePointLength(lowered) < 3) return null;
    for (const row of SEQUENCE_ROWS) {
      if (row.includes(lowered)) {
        const guesses = 200 * codePointLength(lowered) * caseVariantMultiplier(password);
        return candidate(safeLog2(guesses), "keyboard or character sequence",
          "It is a straight keyboard, alphabetic, or numeric run that attackers test early.",
          "Keyboard, alphabetic, or numeric sequence");
      }
    }
    return null;
  }
  function repeatCandidate(password) {
    const characters = Array.from(password);
    if (!characters.length) return null;
    if (new Set(characters).size === 1) {
      return candidate(safeLog2(50 * characters.length), "repeated character",
        "Repeating one character creates very few plausible patterns to test.", "Repeated character");
    }
    for (let blockLength = 1; blockLength <= Math.floor(characters.length / 2); blockLength += 1) {
      if (characters.length % blockLength !== 0) continue;
      const block = characters.slice(0, blockLength).join("");
      const repeats = characters.length / blockLength;
      if (repeats >= 2 && block.repeat(repeats) === password) {
        const blockBits = blockLength * Math.log2(inferredAlphabetSize(block));
        return candidate(blockBits + Math.log2(repeats) + 2, "repeated block",
          "A short block repeats, so an attacker can search the block and repetition count instead of every character.",
          "Repeated block");
      }
    }
    return null;
  }
  function dateCandidate(password) {
    const compact = password.replace(/[-/. ]/g, "");
    if (!/^\d+$/.test(compact)) return null;
    const looksLikeYear = /^(?:19|20)\d{2}$/.test(compact);
    const looksLikeDate = compact.length === 6 || compact.length === 8;
    if (!looksLikeYear && !looksLikeDate) return null;
    const guesses = looksLikeYear ? 50_000 : 5_000_000;
    return candidate(safeLog2(guesses), "date-like pattern",
      "Dates and years occupy a much smaller search space than arbitrary digits.", "Date or year pattern");
  }
  function phraseCandidate(password) {
    const tokens = password.match(/[A-Za-z]+/g);
    const separators = password.match(/[^A-Za-z]+/g);
    if (!tokens || !separators || tokens.length < 2 || tokens.length > 10) return null;
    if (tokens.join("").length + separators.join("").length !== password.length) return null;
    const dictionaryBits = tokens.length * Math.log2(10_000);
    const separatorBits = Math.min(8, separators.length * 2);
    const caseBits = Math.min(12, tokens.filter((token) => token !== token.toLowerCase()).length * 2);
    return candidate(dictionaryBits + separatorBits + caseBits - 1, "word-based phrase",
      "The model assumes an attacker tests combinations of common dictionary words and separators.",
      `${tokens.length}-word phrase`);
  }
  function randomSpaceCandidate(password) {
    const alphabet = inferredAlphabetSize(password);
    const averageGuessBits = Math.max(1, codePointLength(password) * Math.log2(alphabet) - 1);
    return candidate(averageGuessBits, "character-space estimate",
      `The random model uses an inferred alphabet of about ${alphabet} characters and the average position in that space.`,
      `Random ${alphabet}-character alphabet model`);
  }
  function scoreFromBits(bits) {
    if (bits < 20) return 0;
    if (bits < 32) return 1;
    if (bits < 48) return 2;
    if (bits < 64) return 3;
    return 4;
  }
  function buildSuggestions(selected, bits) {
    const suggestions = [];
    const predictable = new Set(["common-password match", "word with predictable suffix",
      "keyboard or character sequence", "repeated character", "repeated block", "date-like pattern"]);
    if (predictable.has(selected.method)) suggestions.push("Replace words, dates, sequences, and substitutions with genuinely random choices.");
    if (bits < 64) suggestions.push("Use a password manager to generate at least 16 random characters, or use 4–6 randomly selected words.");
    suggestions.push("Use a unique password for every account and enable phishing-resistant MFA where available.");
    return suggestions.slice(0, 3);
  }
  function estimatePassword(password) {
    if (typeof password !== "string") throw new TypeError("password must be a string");
    if (!password) throw new Error("password cannot be empty");
    const random = randomSpaceCandidate(password);
    const candidates = [random];
    for (const builder of [commonPasswordCandidate, wordPlusSuffixCandidate, sequenceCandidate, repeatCandidate, dateCandidate, phraseCandidate]) {
      const result = builder(password);
      if (result) candidates.push(result);
    }
    candidates.sort((left, right) => left.guessBits - right.guessBits);
    const selected = candidates[0];
    const score = scoreFromBits(selected.guessBits);
    return {
      length: codePointLength(password), pattern: selected, random, candidates, score, label: LABELS[score],
      suggestions: buildSuggestions(selected, selected.guessBits),
      signals: candidates.filter((item) => item.method !== "character-space estimate").map((item) => item.signal),
      grover: { queryBits: random.guessBits / 2, basis: "random-space square-root query proxy" }
    };
  }
  function log10CountFromBits(bits) { return bits * LOG10_2; }
  function formatCountFromBits(bits) {
    const log10Value = log10CountFromBits(bits);
    if (log10Value < 15) return new Intl.NumberFormat("en-US").format(Math.max(1, Math.round(10 ** log10Value)));
    const exponent = Math.floor(log10Value);
    const mantissa = 10 ** (log10Value - exponent);
    return `≈ ${mantissa.toFixed(2)} × 10^${exponent}`;
  }
  function formatScaled(log10Value, unit) {
    const value = 10 ** log10Value;
    const text = value < 10 ? value.toFixed(2) : value < 100 ? value.toFixed(1) : value.toFixed(0);
    return `${text} ${unit}${Math.abs(value - 1) < 0.005 ? "" : "s"}`;
  }
  function formatDuration(guessBits, guessesPerSecond) {
    if (!Number.isFinite(guessesPerSecond) || guessesPerSecond <= 0) throw new Error("guessesPerSecond must be a positive finite number");
    const value = log10CountFromBits(guessBits) - Math.log10(guessesPerSecond);
    if (value < -6) return "under 1 microsecond";
    if (value < -3) return formatScaled(value + 6, "microsecond");
    if (value < 0) return formatScaled(value + 3, "millisecond");
    if (value < Math.log10(60)) return formatScaled(value, "second");
    if (value < Math.log10(3600)) return formatScaled(value - Math.log10(60), "minute");
    if (value < Math.log10(86_400)) return formatScaled(value - Math.log10(3600), "hour");
    if (value < Math.log10(SECONDS_PER_YEAR)) return formatScaled(value - Math.log10(86_400), "day");
    const years = value - Math.log10(SECONDS_PER_YEAR);
    if (years < 6) return formatScaled(years, "year");
    const exponent = Math.floor(years);
    return `≈ ${(10 ** (years - exponent)).toFixed(2)} × 10^${exponent} years`;
  }
  function formatRate(rate) {
    if (rate < 1_000) return `${rate.toLocaleString("en-US")}/s`;
    for (const [divisor, label] of [[1e15, "quadrillion"], [1e12, "trillion"], [1e9, "billion"], [1e6, "million"], [1e3, "thousand"]]) {
      if (rate >= divisor) return `${(rate / divisor).toLocaleString("en-US", { maximumFractionDigits: 2 })} ${label}/s`;
    }
    return `${rate.toLocaleString("en-US")}/s`;
  }
  return Object.freeze({ estimatePassword, formatCountFromBits, formatDuration, formatRate,
    inferredAlphabetSize, log10CountFromBits, normalizeLeetspeak });
});
