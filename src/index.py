#!/usr/bin/env python3
"""
dropship-radar — AI product trend monitor for dropshippers
Monitors AliExpress, Temu, TikTok Shop trends and scores products on:
margin potential, trend velocity, competition density, saturation risk
"""
import anthropic
import json
import re
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path


SYSTEM = """You are a dropshipping expert and e-commerce trend analyst with deep knowledge of:
- Product margins and supplier pricing patterns
- Trend velocity on TikTok, Instagram, and Google
- Competition density on Amazon, Shopify, and Etsy
- Seasonal patterns and shelf life of trending products

Analyze the provided product/trend data and score each product.

Return ONLY valid JSON — no markdown, no explanation.

For a list of products to analyze:
{
  "analyzed_at": "ISO timestamp",
  "products": [
    {
      "name": "product name",
      "category": "category",
      "estimated_cogs": number_usd,
      "suggested_retail": number_usd,
      "estimated_margin_pct": number,
      "scores": {
        "trend_velocity": number_0_to_10,
        "margin_potential": number_0_to_10,
        "competition": number_0_to_10,
        "wow_factor": number_0_to_10,
        "overall": number_0_to_100
      },
      "verdict": "hot|warm|cold|saturated",
      "why": "2 sentence explanation of the opportunity",
      "risks": ["risk 1", "risk 2"],
      "target_audience": "description",
      "best_platforms": ["TikTok", "Instagram", "Facebook"],
      "suggested_ad_angle": "one-liner hook for ads",
      "seasonality": "year-round|Q4|summer|spring|...",
      "estimated_saturation_months": number_or_null,
      "aliexpress_search": "suggested AliExpress search term",
      "tiktok_hashtags": ["#hashtag1", "#hashtag2"]
    }
  ],
  "top_pick": "product name",
  "market_notes": "broader trend observations"
}"""


TREND_SOURCES = {
    "tiktok_trending": [
        "LED strip lights bedroom aesthetic",
        "Portable blender smoothie",
        "Posture corrector back support",
        "Mini projector bedroom",
        "Magnetic phone mount car",
        "Electric nail file set",
        "Shower head filter",
        "Portable air purifier car",
        "Silicone food storage bags",
        "Automatic plant watering",
        "Under desk treadmill",
        "Cold plunge portable tub",
        "Book nook kit diorama",
        "Wall art prints aesthetic",
        "Handheld garment steamer",
    ],
    "problem_solvers": [
        "Leak-proof coffee tumbler",
        "Cable management box",
        "Drawer organizer set",
        "Windshield sun shade",
        "Bathroom shelf no drill",
        "Ergonomic laptop stand",
        "Portable charger solar",
        "Pet hair remover laundry",
        "Fabric shaver lint remover",
        "Door draft stopper",
    ],
    "health_wellness": [
        "Red light therapy face mask",
        "Gua sha facial tool set",
        "Resistance bands set",
        "Massage gun mini",
        "Eye mask heated",
        "Posture corrector",
        "Acupressure mat",
        "Water flosser portable",
    ]
}


def analyze_products(products: list[str], niche: str = "general") -> dict:
    """Score a list of product ideas."""
    client = anthropic.Anthropic()

    product_list = "\n".join(f"- {p}" for p in products)
    prompt = f"""Analyze these {len(products)} potential dropshipping products for niche: {niche}

Products to analyze:
{product_list}

Current date: {datetime.now(timezone.utc).strftime('%B %Y')}

For each product, research typical AliExpress pricing, current trend signals,
competition level on major platforms, and profit potential for a dropshipper
charging 3-4x the supplier price."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'\s*```$', '', raw, flags=re.MULTILINE)
    return json.loads(raw)


def scan_niche(niche: str, count: int = 10) -> dict:
    """Scan a niche for winning products."""
    client = anthropic.Anthropic()

    prompt = f"""You are a dropshipping product researcher. Find {count} potential winning products in the "{niche}" niche.

Research criteria:
- Products that solve a clear problem or satisfy a desire
- Available on AliExpress for $3-$30
- Can be sold for 3-5x supplier price
- Currently trending or evergreen
- Not yet oversaturated on major platforms

Current date: {datetime.now(timezone.utc).strftime('%B %Y')}

Generate {count} specific product ideas for this niche and score each one."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'\s*```$', '', raw, flags=re.MULTILINE)
    return json.loads(raw)


VERDICT_ICON = {"hot": "🔥", "warm": "✅", "cold": "❄️", "saturated": "💀"}
VERDICT_COLOR = {"hot": "\033[91m", "warm": "\033[92m", "cold": "\033[94m", "saturated": "\033[90m"}
RESET = "\033[0m"

def print_report(result: dict):
    products = result.get("products", [])
    top = result.get("top_pick", "")
    print(f"\n{'═'*60}")
    print(f"  DROPSHIP RADAR — {len(products)} products analyzed")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'═'*60}")

    sorted_products = sorted(products, key=lambda p: p.get("scores", {}).get("overall", 0), reverse=True)

    for p in sorted_products:
        verdict = p.get("verdict", "cold")
        icon = VERDICT_ICON.get(verdict, "•")
        score = p.get("scores", {}).get("overall", 0)
        margin = p.get("estimated_margin_pct", 0)
        cogs = p.get("estimated_cogs", 0)
        retail = p.get("suggested_retail", 0)
        star = " ⭐ TOP PICK" if p.get("name") == top else ""

        print(f"\n  {icon} {p.get('name','?')}{star}")
        print(f"     Score: {score}/100 | Margin: {margin:.0f}% | ${cogs:.0f} → ${retail:.0f}")
        print(f"     {p.get('why','')}")
        scores = p.get("scores", {})
        print(f"     Trend:{scores.get('trend_velocity',0):.0f}/10  Margin:{scores.get('margin_potential',0):.0f}/10  Competition:{scores.get('competition',0):.0f}/10  WOW:{scores.get('wow_factor',0):.0f}/10")
        if p.get("suggested_ad_angle"):
            print(f"     Ad angle: \"{p['suggested_ad_angle']}\"")
        if p.get("risks"):
            print(f"     Risks: {' | '.join(p['risks'][:2])}")

    if result.get("market_notes"):
        print(f"\n{'─'*60}")
        print(f"  Market notes: {result['market_notes']}")
    print(f"\n{'═'*60}\n")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print("Usage:")
        print("  python -m dropship_radar scan <niche> [--count 10]")
        print("  python -m dropship_radar analyze product1 product2 ...")
        print("  python -m dropship_radar trending")
        sys.exit(0)

    cmd = args[0]

    if cmd == "scan":
        niche = args[1] if len(args) > 1 else "home decor"
        count_idx = args.index("--count") if "--count" in args else -1
        count = int(args[count_idx + 1]) if count_idx >= 0 else 10
        result = scan_niche(niche, count)
    elif cmd == "analyze":
        products = args[1:]
        if not products:
            print("Provide product names to analyze")
            sys.exit(1)
        result = analyze_products(products)
    elif cmd == "trending":
        all_products = []
        for category_products in TREND_SOURCES.values():
            all_products.extend(category_products[:5])
        result = analyze_products(all_products[:15], "trending general")
    else:
        # treat as niche scan
        result = scan_niche(" ".join(args))

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_report(result)
