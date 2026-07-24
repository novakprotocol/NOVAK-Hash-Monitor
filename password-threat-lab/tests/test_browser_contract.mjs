import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const estimator = require("../assets/estimator.js");

const common = estimator.estimatePassword("password");
assert.equal(common.pattern.method, "common-password match");
assert.equal(common.label, "Very weak");

const suffix = estimator.estimatePassword("Password1!");
assert.equal(suffix.pattern.method, "word with predictable suffix");
assert.equal(suffix.label, "Very weak");

const repeated = estimator.estimatePassword("abcabcabc");
assert.equal(repeated.pattern.method, "repeated block");

const phrase = estimator.estimatePassword("correct-horse-battery-staple");
assert.ok(phrase.signals.includes("4-word phrase"));

const strong = estimator.estimatePassword("m7Q!v2K@p9R#x4Tz");
assert.equal(strong.label, "Very strong");
assert.equal(strong.grover.queryBits, strong.random.guessBits / 2);

const long = estimator.estimatePassword("Ab9!".repeat(64));
assert.ok(Number.isFinite(long.random.guessBits));
assert.equal(long.length, 256);

assert.throws(() => estimator.estimatePassword(""), /cannot be empty/);
assert.throws(() => estimator.formatDuration(32, 0), /positive finite/);

process.stdout.write(`${JSON.stringify({ status: "pass", assertions: 12 })}\n`);
