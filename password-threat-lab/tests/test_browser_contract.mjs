import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const estimator = require("../assets/estimator.js");

const common = estimator.estimatePassword("password");
assert.equal(common.pattern.method, "common-password match");
assert.ok(common.pattern.guessBits < common.random.guessBits);

const suffix = estimator.estimatePassword("Password1!");
assert.equal(suffix.pattern.method, "word with predictable suffix");

const repeated = estimator.estimatePassword("abcabcabc");
assert.equal(repeated.pattern.method, "repeated block");

const phrase = estimator.estimatePassword("correct-horse-battery-staple");
assert.ok(phrase.signals.includes("4-word phrase"));

const generated = estimator.estimatePassword("m7Q!v2K@p9R#x4Tz");
assert.equal(generated.label, "Very strong");
assert.equal(generated.grover.queryBits, generated.random.guessBits / 2);
assert.match(estimator.formatCountFromBits(generated.random.guessBits), /10\^/);
assert.match(estimator.formatDuration(32, 1_000_000), /(second|minute|hour|day|year)/);
assert.throws(() => estimator.formatDuration(32, 0));

console.log(JSON.stringify({
  status: "pass",
  assertions: 11,
  claim_boundary: "Pure estimator contract only; no browser credential input was used."
}));
