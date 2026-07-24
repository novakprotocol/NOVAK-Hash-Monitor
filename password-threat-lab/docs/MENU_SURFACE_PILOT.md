# Menu Surface Pilot

## Primary surface

`index.html` is the web surface. It exposes four bounded commands from `app.surface.json`:

| Command | Visible control or section | Effect |
|---|---|---|
| `lab.estimate` | Representative sample field | Updates local estimate text in the current tab |
| `lab.select_profile` | Classical attack scenario selector | Changes the local illustrative rate |
| `lab.clear` | Clear button | Removes the transient sample and resets results |
| `app.about` | Method and Sources sections | Presents read-only assumptions and primary sources |

## Accessibility behavior

- keyboard-visible focus treatment;
- skip link to the analyzer;
- native labels and controls;
- password input masked by default;
- show/hide state expressed with `aria-pressed`;
- result changes announced through a polite status region;
- native progress element for the five-level heuristic label;
- reduced-motion support;
- responsive one-column mobile layout.

## Launcher boundary

The manifest advertises a launcher surface for future N-Suite integration. This scoped patch does not modify N-Suite, a parent navigation menu, or the root GitHub Pages page. Any launcher or parent navigation addition requires a separate routed change.
