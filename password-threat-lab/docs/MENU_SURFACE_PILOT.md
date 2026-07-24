# Menu Surface Pilot

The Password Threat Lab is a static web surface rather than a desktop GUI. Visible actions map to `app.surface.json` as follows:

| Command | Visible surface | Behavior |
|---|---|---|
| `lab.estimate` | Representative password sample input | Computes local estimates as the sample changes |
| `lab.select_profile` | Classical attack scenario selector and custom-rate field | Changes the illustrative classical scenario |
| `lab.clear` | Clear button | Removes the transient sample and result state |
| `app.about` | Method and Sources sections | Explains assumptions, boundaries, and primary sources |

## Primary path

1. Read the privacy boundary.
2. Enter a synthetic representative sample.
3. Select an illustrative classical profile.
4. Compare pattern-aware and random-model results.
5. Read the Grover query boundary.
6. Review Shor/PQC context and primary sources.
7. Clear the sample.

## Surface constraints

- No submit button or form action.
- No server round trip for analysis.
- No hidden command palette.
- No destructive action beyond clearing transient local input.
- Keyboard focus, visible labels, and screen-reader live status are required.
