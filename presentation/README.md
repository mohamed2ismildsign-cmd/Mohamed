# Designed to Be Made — presentation

A 10-minute animated presentation: 17 slides styled as an engineering drawing sheet.

**To present:** open one of the two versions in Chrome or Edge. Each is a single file with every image
and font built in, so it works offline from a USB stick. The slides and wording are the same in both:

- `dist/Mohamed-Ismail-Presentation-Blueprint.html`: dark blueprint drawing sheet
- `dist/Mohamed-Ismail-Presentation-Light.html`: light dot-grid wall, black type, framed prints

| Key | Action |
| --- | --- |
| → / Space / clicker | Next slide |
| ← | Previous slide |
| F | Full screen |
| P | Presenter view in a second window: current and next slide, a 10:00 timer, pace check |
| B | Blank the screen (press again to return) |
| T | Small timer in the corner |
| O | Index of all slides and shortcuts |

For presenter view on a projector: set the display to *extend*, press **P**, drag the presenter window
to your laptop screen, then click the main window and press **F** on the projector.
If the browser blocks the pop-up, allow pop-ups for the file and press **P** again.

**To edit:** change `src/deck.html` (text and layout) or swap images in `src/assets/`, then run
`python3 build.py` to rebuild both files in `dist/`. The light theme's styles live in `src/theme-light.css`.
