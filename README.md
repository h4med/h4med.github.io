# hdavandeh.ir — career timeline deck

A personal resume as an animated, right-to-left (RTL) timeline. Twenty-two steps show one
career as four parallel branches (electronics, industrial automation, artificial intelligence,
software) that join under one umbrella: systems engineering.

Live site: <https://hdavandeh.ir>

## What it is

- One self-contained HTML file. The build embeds both Vazirmatn fonts as base64, so the page
  makes no external requests.
- Twenty-two steps. Each step thickens one branch and shows that step's label inside the branch
  lane. Labels do not accumulate.
- A grey time axis prints the Hijri-Shamsi year of each step.
- Navigation: click, Space, or the arrow keys. The "صفحه اول" button returns to the cover.
- Responsive. The phone layout stacks the four branches and moves the year to its own line.

## Files

| File | Purpose |
|---|---|
| `index.html` | The built deck. **Generated file — do not edit it by hand.** |
| `build_timeline.py` | The build script. It writes `index.html`. |
| `timeline_data.py` | All content. Edit this file to change the deck. |
| `timeline.js` | Deck behavior: step switching, lane build, chip placement, year, phone scroll. |
| `verify_layout.py` | Optional layout check with Playwright. |
| `fonts/` | Vazirmatn Regular and Bold (SIL OFL 1.1), plus the license text. |
| `CNAME` | Custom domain for GitHub Pages. |

## Build

Requirements: Python 3.9 or later. No third-party Python packages.

```
python3 build_timeline.py
```

The script writes `index.html` next to itself and prints the byte count, the step count, and the
lane count. The fonts come from `./fonts`. To use fonts from another directory, set `FONT_DIR`:

```
FONT_DIR=/path/to/fonts python3 build_timeline.py
```

## Edit the content

Open `timeline_data.py`. It has three parts.

`LANES` — the four branches. Each entry has a `key` (name), a `sub` (subtitle), and a `color`.

`OWNER` — the cover identity: `name`, `kick` (role), `lead` (headline), `last_edit`, `linkedin`.

`STEPS` — the twenty-two pages, in order. Each page is one `dict`:

| Field | Meaning |
|---|---|
| `cap` | Caption at the top of the page. |
| `h` | Cumulative thickness of each branch, as four numbers from 0 to 9. A value never decreases. |
| `grow` | Index list of the branches that thicken on this step. |
| `ev` | Event labels for this step only, as `[(branch_index, text), ...]`. |
| `yr` | Year text on the grey axis, in Persian digits. Omit it to show no year. |
| `hero`, `end` | Mark the cover page and the closing page. |
| `combo` | Marks the step that joins several branches. |
| `think` | Dims the deck for the "why systems engineering" question. |
| `umbrella` | Shows the umbrella overlay. |
| `pg` | Full-page product card: `title`, `tag`, `points`, `role`. |

Technical terms stay in Latin script (`Firmware`, `Modbus/TCP`, `Confluence`). Persian digits
stay in Persian script.

## Check the layout

`verify_layout.py` opens the deck in headless Chromium and measures geometry. It checks these
items at each step and at each viewport size:

- the caption does not touch the home button or the first branch name,
- branch names share one left edge on desktop,
- a label stays inside its own lane and never touches another lane's label,
- labels do not touch the counter, the year line, or the screen edge.

```
pip install playwright && playwright install chromium
python3 verify_layout.py
```

The script exits with a non-zero code when a check fails.

## Deploy

The site is a GitHub Pages user site:

1. Commit `index.html` to the `main` branch.
2. In repository Settings, set Pages source to `main` and `/ (root)`.
3. Keep `CNAME` in place. It points the site to `hdavandeh.ir`.

## Contributing

The repository is public. Only the owner can push to `main`. Other people can fork the
repository, change the source files, and open a pull request. Please change `timeline_data.py`
or `timeline.js`, then run the build. Do not send a pull request that edits `index.html` only,
because the next build overwrites that file.

## License

- Code (`build_timeline.py`, `timeline.js`, `timeline_data.py`, `verify_layout.py`): MIT. See `LICENSE`.
- Personal content (name, career history, dates, and all Persian text about the owner): copyright
  Hamed Davandeh. You may read it, but you may not republish it as your own.
- Fonts: Vazirmatn, SIL Open Font License 1.1. See `fonts/OFL.txt`.