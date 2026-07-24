(function () {
  "use strict";
  const estimator = globalThis.PasswordThreatEstimator;
  if (!estimator) {
    document.documentElement.dataset.appError = "estimator-unavailable";
    return;
  }
  const FALLBACK_CONFIG = Object.freeze({
    profiles: [
      { id: "online_rate_limited", label: "Online login — rate limited", guesses_per_second: 5,
        description: "Illustrative endpoint protected by throttling, lockouts, or bot controls." },
      { id: "offline_memory_hard", label: "Offline memory-hard password hash", guesses_per_second: 500,
        description: "Illustrative Argon2id or scrypt-style scenario. Real throughput depends on parameters and hardware." },
      { id: "offline_slow_kdf", label: "Offline slower password KDF", guesses_per_second: 100000,
        description: "Illustrative bcrypt or PBKDF2-style scenario. This is not a benchmark." },
      { id: "offline_fast_hash", label: "Offline fast hash — one accelerator", guesses_per_second: 10000000000,
        description: "Illustrative 10 billion guesses per second for a fast hash." },
      { id: "offline_fast_cluster", label: "Offline fast hash — GPU cluster", guesses_per_second: 100000000000,
        description: "Illustrative 100 billion guesses per second. Hash choice and hardware determine real rates." }
    ],
    default_profile_id: "offline_fast_hash",
    limits: { maximum_password_characters: 256, maximum_custom_guesses_per_second: 1e18 }
  });
  const dom = {
    password: document.getElementById("passwordInput"), toggle: document.getElementById("toggleVisibility"),
    clear: document.getElementById("clearInput"), count: document.getElementById("characterCount"),
    profile: document.getElementById("attackProfile"), profileDescription: document.getElementById("profileDescription"),
    customGroup: document.getElementById("customRateGroup"), customRate: document.getElementById("customRate"),
    analyzeStatus: document.getElementById("analysisStatus"), emptyState: document.getElementById("emptyState"),
    resultState: document.getElementById("resultState"), strengthLabel: document.getElementById("strengthLabel"),
    strengthMeter: document.getElementById("strengthMeter"), method: document.getElementById("patternMethod"),
    explanation: document.getElementById("patternExplanation"), patternBits: document.getElementById("patternBits"),
    patternGuesses: document.getElementById("patternGuesses"), patternTime: document.getElementById("patternTime"),
    randomBits: document.getElementById("randomBits"), randomGuesses: document.getElementById("randomGuesses"),
    randomTime: document.getElementById("randomTime"), groverBits: document.getElementById("groverBits"),
    groverQueries: document.getElementById("groverQueries"), selectedRate: document.getElementById("selectedRate"),
    signals: document.getElementById("patternSignals"), suggestions: document.getElementById("suggestions"),
    configStatus: document.getElementById("configStatus")
  };
  let config = FALLBACK_CONFIG;
  let profilesById = new Map();

  function validateConfig(candidate) {
    if (!candidate || !Array.isArray(candidate.profiles) || candidate.profiles.length === 0) throw new Error("profiles missing");
    for (const profile of candidate.profiles) {
      if (typeof profile.id !== "string" || typeof profile.label !== "string" || typeof profile.description !== "string" ||
          !Number.isFinite(profile.guesses_per_second) || profile.guesses_per_second <= 0) throw new Error("invalid profile");
    }
  }
  function populateProfiles() {
    profilesById = new Map(config.profiles.map((profile) => [profile.id, profile]));
    dom.profile.replaceChildren();
    for (const profile of config.profiles) {
      const option = document.createElement("option");
      option.value = profile.id;
      option.textContent = profile.label;
      dom.profile.append(option);
    }
    const custom = document.createElement("option");
    custom.value = "custom";
    custom.textContent = "Custom illustrative rate";
    dom.profile.append(custom);
    dom.profile.value = profilesById.has(config.default_profile_id) ? config.default_profile_id : config.profiles[0].id;
    updateProfileDescription();
  }
  async function loadConfig() {
    try {
      const response = await fetch("data/attack-profiles.json", { cache: "no-store", credentials: "same-origin" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const candidate = await response.json();
      validateConfig(candidate);
      config = candidate;
      dom.configStatus.textContent = "Assumptions loaded from local JSON.";
    } catch (_error) {
      config = FALLBACK_CONFIG;
      dom.configStatus.textContent = "Using built-in assumptions; local JSON was unavailable.";
    }
    populateProfiles();
    render();
  }
  function selectedScenario() {
    if (dom.profile.value === "custom") {
      const maximum = config.limits?.maximum_custom_guesses_per_second || 1e18;
      const parsed = Number(dom.customRate.value);
      return { id: "custom", label: "Custom illustrative rate",
        guesses_per_second: Number.isFinite(parsed) && parsed > 0 ? Math.min(parsed, maximum) : 1,
        description: "User-supplied educational assumption. It is not validated against a hardware benchmark." };
    }
    return profilesById.get(dom.profile.value) || config.profiles[0];
  }
  function updateProfileDescription() {
    dom.customGroup.hidden = dom.profile.value !== "custom";
    dom.profileDescription.textContent = selectedScenario().description;
  }
  function fillList(element, items, emptyText) {
    element.replaceChildren();
    for (const value of items.length ? items : [emptyText]) {
      const item = document.createElement("li");
      item.textContent = value;
      element.append(item);
    }
  }
  function render() {
    const password = dom.password.value;
    dom.count.textContent = `${Array.from(password).length} / ${dom.password.maxLength}`;
    if (!password) {
      dom.emptyState.hidden = false;
      dom.resultState.hidden = true;
      dom.analyzeStatus.textContent = "No sample is being analyzed.";
      return;
    }
    const scenario = selectedScenario();
    const result = estimator.estimatePassword(password);
    const rate = scenario.guesses_per_second;
    dom.emptyState.hidden = true;
    dom.resultState.hidden = false;
    dom.strengthLabel.textContent = result.label;
    dom.strengthMeter.value = result.score + 1;
    dom.method.textContent = result.pattern.method;
    dom.explanation.textContent = result.pattern.explanation;
    dom.patternBits.textContent = `${result.pattern.guessBits.toFixed(1)} bits`;
    dom.patternGuesses.textContent = estimator.formatCountFromBits(result.pattern.guessBits);
    dom.patternTime.textContent = estimator.formatDuration(result.pattern.guessBits, rate);
    dom.randomBits.textContent = `${result.random.guessBits.toFixed(1)} bits`;
    dom.randomGuesses.textContent = estimator.formatCountFromBits(result.random.guessBits);
    dom.randomTime.textContent = estimator.formatDuration(result.random.guessBits, rate);
    dom.groverBits.textContent = `${result.grover.queryBits.toFixed(1)} query bits`;
    dom.groverQueries.textContent = estimator.formatCountFromBits(result.grover.queryBits);
    dom.selectedRate.textContent = `${scenario.label}: ${estimator.formatRate(rate)}`;
    fillList(dom.signals, result.signals, "No bundled shortcut pattern was detected.");
    fillList(dom.suggestions, result.suggestions, "Use a unique generated password and phishing-resistant MFA.");
    dom.analyzeStatus.textContent = `Analysis updated: ${result.label}; ${result.pattern.method}.`;
  }
  function toggleVisibility() {
    const showing = dom.password.type === "text";
    dom.password.type = showing ? "password" : "text";
    dom.toggle.textContent = showing ? "Show" : "Hide";
    dom.toggle.setAttribute("aria-pressed", String(!showing));
    dom.password.focus({ preventScroll: true });
  }
  function clearPassword() {
    dom.password.value = "";
    dom.password.type = "password";
    dom.toggle.textContent = "Show";
    dom.toggle.setAttribute("aria-pressed", "false");
    render();
    dom.password.focus({ preventScroll: true });
  }
  dom.password.addEventListener("input", render);
  dom.toggle.addEventListener("click", toggleVisibility);
  dom.clear.addEventListener("click", clearPassword);
  dom.profile.addEventListener("change", function () { updateProfileDescription(); render(); });
  dom.customRate.addEventListener("input", render);
  window.addEventListener("pagehide", function () { dom.password.value = ""; dom.customRate.value = "1000000"; });
  populateProfiles();
  render();
  loadConfig().finally(function () { document.documentElement.dataset.ready = "true"; });
})();
