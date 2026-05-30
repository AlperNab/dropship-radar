# Dropship Radar

This folder has been upgraded into a **standalone real GUI project**.

Run the project GUI:

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default local URL: `http://127.0.0.1:9117`

This project includes its own FastAPI backend, browser GUI, provider settings, local/cloud LLM routing, encrypted API-key storage, file uploads, job history, exports, and a project-specific plugin configuration.

See `PROJECT_IMPLEMENTATION.md` and `project_config.json` for the applied project-specific features and customization controls.

---

## Original README

# dropship-radar

> **AI product trend monitor for dropshippers.** Scans trending products across niches, scores each on margin potential, trend velocity, competition density and WOW factor. Know what to sell before it peaks.

[![PyPI](https://img.shields.io/pypi/v/dropship-radar?style=flat)](https://pypi.org/project/dropship-radar/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quickstart

```bash
pip install dropship-radar

# Scan a niche for winning products
python -m dropship_radar scan "home office"

# Analyze specific product ideas
python -m dropship_radar analyze "LED desk lamp" "ergonomic mouse pad" "cable organizer"

# Scan current trending products
python -m dropship_radar trending
```

## Example output

```
🔥 Portable Blender ⭐ TOP PICK
   Score: 87/100 | Margin: 71% | $8 → $28
   High TikTok virality with UGC content driving organic traffic.
   Low competition on Etsy and emerging on Shopify stores.
   Trend:9/10  Margin:8/10  Competition:7/10  WOW:8/10
   Ad angle: "Smoothies anywhere — gym, office, travel"

✅ Under-Desk Treadmill
   Score: 74/100 | Margin: 65% | $45 → $129
```

## Scoring dimensions

| Dimension | What it measures |
|-----------|-----------------|
| Trend velocity | TikTok/Instagram/Google momentum right now |
| Margin potential | Typical AliExpress cost vs achievable retail price |
| Competition | Saturation on Amazon, Shopify, Etsy |
| WOW factor | Shareability, gifting appeal, impulse buy strength |

## License
MIT © [Alper Nabil Gabra Zakher](https://github.com/AlperNab)
