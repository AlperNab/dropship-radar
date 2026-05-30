# Dropship Radar — Standalone Real GUI Implementation

This folder is now its own runnable project app. It does not depend on the root all-project dashboard at runtime.

## Run

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default URL: `http://127.0.0.1:9117`

## What is inside this project folder

- `app/` — FastAPI backend for this project.
- `static/` — elegant browser GUI.
- `plugins/dropship-radar.json` — this project’s own feature/customization/input schema.
- `project_config.json` — readable copy of the same project-specific configuration.
- `data/` — local SQLite jobs, uploads, exports.
- `tests/` — verifies this project has a registered real local engine.

## Project-specific scope

- Domain: `E-commerce / Product Research`
- Target user: `Domain operator, business owner, analyst, or team member who needs this workflow executed reliably.`
- Core job: Niche scan → product opportunity radar
- Suite: `E-commerce Growth Suite`

## Deep features applied

- trend velocity
- margin calculator
- supplier research
- competitor ads
- saturation score
- WOW-factor analysis
- launch queue
- risk filters

## Customization controls

- `execution_mode` — Execution mode (select)
- `target_market` — target market (text)
- `niche` — niche (text)
- `budget` — budget (text)
- `supplier_region` — supplier region (text)
- `shipping_limits` — shipping limits (text)
- `ad_platform` — ad platform (select)
- `banned_categories` — banned categories (text)
- `margin_target` — margin target (text)
- `output_format` — output format (select)
- `language` — language (select)
- `privacy_mode` — privacy mode (select)
- `confidence_threshold` — Confidence threshold (slider)

## Input fields

- `niche_scan` — Niche scan (text) required
- `work_brief` — Work brief / source text / URL / instructions (textarea) required

## External data policy

The local deterministic core is real and executable. Live external systems are not simulated. If Shopify, ATS, ERP, OCR/STT, maps, SERP, market data, medical databases, tax/customs databases, or other live systems are required, this project reports the missing connector/API requirement instead of inventing data.

---

## Final UX/UI Layer

This project now uses the **Growth Command Center** pattern.

**UX workflow:** Research → positioning → content/ads → launch queue → measurement

**Domain components:**
- Product research board
- Margin calculator
- Competition/WOW scorecards
- Supplier evidence panel
- Launch queue

**Quick actions:**
- Score product idea
- Calculate margin
- Check competition risk
- Create launch checklist

**No fake-data policy:** external/live actions require real connectors or API keys. Missing connectors are reported instead of simulated.
