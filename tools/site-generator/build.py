#!/usr/bin/env python3
"""
BlockParty static site generator.
Builds the full marketing site from the authoritative copy/pricing docs
(art_K7lqnl0A, art_le2BjCpS) into ./dist as static HTML + CSS.
"""
import os
import json
import html
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")

SITE_NAME = "BlockParty"
DOMAIN = "https://blockpartysupply.co"
EMAIL = "reserve@blockpartysupply.co"
TAGLINE = "We bought it so you don't have to"

# Social card image (R4) — generated at build time from assets/badge.png
OG_IMAGE_PATH = "/og-image.png"
OG_IMAGE_URL = f"{DOMAIN}{OG_IMAGE_PATH}"
OG_IMAGE_ALT = f"{SITE_NAME} — {TAGLINE}"

# ---------------------------------------------------------------------------
# Icons (simple inline SVGs, consistent line style, teal/red/yellow palette)
# ---------------------------------------------------------------------------

ICONS = {
    "cornhole": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="10" y="55" width="55" height="32" rx="4" transform="rotate(-8 10 55)" fill="#CB9F5C" stroke="#1D2334" stroke-width="3"/>
<circle cx="38" cy="66" r="7" fill="#1D2334"/>
<rect x="55" y="45" width="40" height="26" rx="4" transform="rotate(-8 55 45)" fill="#AC7044" stroke="#1D2334" stroke-width="3"/>
<circle cx="18" cy="30" r="9" fill="#693F35"/>
<circle cx="35" cy="20" r="9" fill="#693F35"/>
</svg>""",
    "jenga": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="30" y="10" width="40" height="14" rx="2" fill="#CB9F5C" stroke="#1D2334" stroke-width="3"/>
<rect x="30" y="26" width="40" height="14" rx="2" fill="#AC7044" stroke="#1D2334" stroke-width="3"/>
<rect x="30" y="42" width="40" height="14" rx="2" fill="#693F35" stroke="#1D2334" stroke-width="3"/>
<rect x="30" y="58" width="40" height="14" rx="2" fill="#CB9F5C" stroke="#1D2334" stroke-width="3"/>
<rect x="20" y="74" width="60" height="14" rx="2" fill="#AC7044" stroke="#1D2334" stroke-width="3"/>
</svg>""",
    "beerpong": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M22 35 L30 85 L70 85 L78 35 Z" fill="#CB9F5C" stroke="#1D2334" stroke-width="3"/>
<ellipse cx="50" cy="35" rx="28" ry="8" fill="#F7E4C1" stroke="#1D2334" stroke-width="3"/>
<circle cx="50" cy="18" r="9" fill="#AC7044" stroke="#1D2334" stroke-width="3"/>
</svg>""",
    "slushie": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="25" y="15" width="50" height="34" rx="6" fill="#F7E4C1" stroke="#1D2334" stroke-width="3"/>
<path d="M30 49 L50 85 L70 49 Z" fill="#693F35" stroke="#1D2334" stroke-width="3"/>
<rect x="43" y="22" width="14" height="20" fill="#AC7044"/>
<circle cx="50" cy="12" r="4" fill="#1D2334"/>
</svg>""",
    "basketball": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="42" r="26" fill="#AC7044" stroke="#1D2334" stroke-width="3"/>
<path d="M50 16 V68 M26 42 H74 M32 24 Q50 42 32 60 M68 24 Q50 42 68 60" stroke="#1D2334" stroke-width="2.5" fill="none"/>
<rect x="42" y="68" width="16" height="22" fill="#693F35" stroke="#1D2334" stroke-width="3"/>
</svg>""",
    "ballpit": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<ellipse cx="50" cy="78" rx="42" ry="12" fill="none" stroke="#1D2334" stroke-width="3"/>
<circle cx="30" cy="55" r="10" fill="#AC7044" stroke="#1D2334" stroke-width="2.5"/>
<circle cx="50" cy="45" r="10" fill="#CB9F5C" stroke="#1D2334" stroke-width="2.5"/>
<circle cx="70" cy="55" r="10" fill="#693F35" stroke="#1D2334" stroke-width="2.5"/>
<circle cx="40" cy="68" r="10" fill="#693F35" stroke="#1D2334" stroke-width="2.5"/>
<circle cx="62" cy="68" r="10" fill="#AC7044" stroke="#1D2334" stroke-width="2.5"/>
</svg>""",
    "truck": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="10" y="35" width="50" height="30" rx="3" fill="#CB9F5C" stroke="#1D2334" stroke-width="3"/>
<path d="M60 45 H82 L90 60 V65 H60 Z" fill="#693F35" stroke="#1D2334" stroke-width="3"/>
<circle cx="28" cy="70" r="8" fill="#1D2334"/>
<circle cx="76" cy="70" r="8" fill="#1D2334"/>
</svg>""",
    "phone": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="32" y="12" width="36" height="76" rx="8" fill="#F7E4C1" stroke="#1D2334" stroke-width="3"/>
<path d="M40 70 Q50 60 60 70 Q65 75 60 82 Q50 90 40 82 Q35 75 40 70 Z" fill="#AC7044"/>
<circle cx="50" cy="26" r="3" fill="#1D2334"/>
</svg>""",
    "sparkles": """<svg viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M28 14 C30 26 32 28 44 30 C32 33 30 35 28 46 C26 35 24 33 13 30 C24 28 26 26 28 14 Z" fill="#CB9F5C"/>
<path d="M78 34 C80 44 82 46 92 48 C82 50 80 52 78 62 C76 52 74 50 64 48 C74 46 76 44 78 34 Z" fill="none" stroke="#1D2334" stroke-width="3" stroke-linejoin="round"/>
<path d="M44 66 C46 74 48 76 56 78 C48 80 46 82 44 90 C42 82 40 80 32 78 C40 76 42 74 44 66 Z" fill="none" stroke="#1D2334" stroke-width="3" stroke-linejoin="round"/>
<path d="M92 84 L92 96 M86 90 L98 90" stroke="#1D2334" stroke-width="3" stroke-linecap="round"/>
<circle cx="14" cy="98" r="3.5" fill="#AC7044"/>
<circle cx="106" cy="18" r="3.5" fill="#1D2334"/>
</svg>""",
    "arrow_doodle": """<svg viewBox="0 0 90 60" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M8 12 C 28 40, 50 44, 74 38" stroke="#1D2334" stroke-width="3.5" stroke-linecap="round"/>
<path d="M64 28 L 76 38 L 61 45" stroke="#1D2334" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",
    "browse": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="42" cy="42" r="26" fill="none" stroke="#1D2334" stroke-width="4"/>
<line x1="61" y1="61" x2="86" y2="86" stroke="#1D2334" stroke-width="5" stroke-linecap="round"/>
<circle cx="42" cy="42" r="12" fill="#CB9F5C"/>
</svg>""",
    "calendar": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="14" y="22" width="72" height="64" rx="6" fill="#F7E4C1" stroke="#1D2334" stroke-width="3"/>
<rect x="14" y="22" width="72" height="18" fill="#AC7044"/>
<line x1="30" y1="14" x2="30" y2="30" stroke="#1D2334" stroke-width="4" stroke-linecap="round"/>
<line x1="70" y1="14" x2="70" y2="30" stroke="#1D2334" stroke-width="4" stroke-linecap="round"/>
<circle cx="34" cy="58" r="5" fill="#693F35"/>
<circle cx="50" cy="58" r="5" fill="#693F35"/>
<circle cx="66" cy="58" r="5" fill="#CB9F5C"/>
</svg>""",
    "house": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 48 L50 16 L88 48" stroke="#1D2334" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="24" y="48" width="52" height="38" fill="#CB9F5C" stroke="#1D2334" stroke-width="3"/>
<rect x="44" y="62" width="12" height="24" fill="#AC7044"/>
</svg>""",
}

def icon(key, css_class="icon"):
    return f'<div class="{css_class}">{ICONS[key]}</div>'

# ---------------------------------------------------------------------------
# Catalog data — sourced verbatim from art_le2BjCpS / art_K7lqnl0A
# ---------------------------------------------------------------------------

# Packages: `price_label` is the display string; `price` is the structured
# numeric price JSON-LD must never drift from.
PACKAGES = [
    {
        "name": "Classic Block Party Package",
        "price_label": "$185",
        "price": 185,
        "subtitle": "Cornhole, Giant Jenga, and Giant/Human-Sized Beer Pong, delivered and picked up in one trip.",
        "group_size": "~10–25 people",
        "desc": "For blocks of about 10–25 people who want a few solid lawn games without extra setup. One delivery run covers all three games, which is why the package runs below the combined à la carte price. Includes delivery, pickup, and a pre-event confirmation call.",
        "includes": ["Cornhole Set", "Giant Jenga", "Giant/Human-Sized Beer Pong"],
        "featured": False,
    },
    {
        "name": "Full Block Party Package",
        "price_label": "$420",
        "price": 420,
        "subtitle": "Everything in the Classic package, plus a single-flavor slushie or frozen-cocktail machine.",
        "group_size": "~25–50 people",
        "desc": "Built for bigger blocks (roughly 25–50 people) who want a drink station alongside the games. Includes delivery, pickup, and a pre-event confirmation call.",
        "includes": ["Cornhole Set", "Giant Jenga", "Giant/Human-Sized Beer Pong", "Single-Flavor Slushie Machine"],
        "featured": True,
    },
    {
        "name": "Deluxe Block Party Package",
        "price_label": "$675",
        "price": 675,
        "subtitle": "Everything in the Full package, plus a ball pit.",
        "group_size": "~40–75 people",
        "desc": "The flagship package for larger, family-heavy blocks (roughly 40–75 people). Like every other BlockParty rental, it's drop-off service — no on-site attendant required for any item in this package. Includes delivery, pickup, and a pre-event confirmation call.",
        "includes": ["Cornhole Set", "Giant Jenga", "Giant/Human-Sized Beer Pong", "Single-Flavor Slushie Machine", "Ball Pit"],
        "featured": False,
    },
]

# Each catalog item: slug drives /rentals/<slug>.html
# `offers` carries the structured numeric prices (R9) that JSON-LD renders;
# `price_label` is display-only and may hold two prices for one item.
CATALOG = [
    {
        "slug": "cornhole-rental-brooklyn",
        "icon": "cornhole",
        "photo": "/images/social-square-cornhole.png",
        "photo_alt": "Vintage BlockParty illustration of a cornhole tournament on a block-party street, a beanbag mid-air between two boards",
        "photo_w": 1024,
        "photo_h": 1024,
        "name": "Cornhole Set Rental",
        "price_label": "$65/day bundled",
        "offers": [{"price": 65}],
        "solo_note": "$150 solo-order minimum",
        "short": "Regulation 2-board cornhole set with bags, delivered and picked up.",
        "who": "Works for groups of any size — most blocks run 2–4 boards' worth of players at once.",
        "pairs": "Pairs naturally with Giant Jenga and Giant Beer Pong in the Classic package.",
        "answer": "BlockParty rents a regulation cornhole set for Brooklyn block parties and backyard events, delivered and picked up, for $65/day bundled or a $150 solo-order minimum.",
        "facts": [("What it is", "Regulation 2-board cornhole set with bags"), ("Who it's for", "Groups of any size — 2–4 boards' worth of players at once"), ("What's included", "Delivery, pickup, set-up on your block"), ("Price", "$65/day bundled"), ("Delivery note", "$150 solo-order minimum, or bundle with another item")],
        "item_faq": [
            ("How many people can play cornhole at once?", "A regulation 2-board set plays 2–4 at a time, but most blocks rotate through many more players over the course of the day."),
            ("Can I rent cornhole on its own?", "Yes — standalone cornhole orders carry the $150 solo-order minimum that covers a dedicated Brooklyn delivery-and-pickup trip. Adding it to a package or bundling it with another item clears that minimum automatically."),
        ],
    },
    {
        "slug": "giant-jenga-rental-brooklyn",
        "icon": "jenga",
        "name": "Giant Jenga Rental",
        "price_label": "$65/day bundled",
        "offers": [{"price": 65}],
        "solo_note": "$150 solo-order minimum",
        "short": "Oversized stacking-block game, 3–5 feet tall fully built.",
        "who": "A low-effort, all-ages game that works on pavement, sidewalk, or a closed street.",
        "pairs": "Included in every package tier.",
        "answer": "BlockParty rents Giant Jenga — an oversized stacking-block game that stands 3–5 feet tall fully built — for Brooklyn block parties and backyard events, delivered and picked up, for $65/day bundled or a $150 solo-order minimum.",
        "facts": [("What it is", "Oversized stacking blocks, 3–5 ft tall fully built"), ("Who it's for", "All ages — low-effort, high-replay-value game"), ("What's included", "Delivery, pickup, set-up on your block"), ("Price", "$65/day bundled"), ("Delivery note", "$150 solo-order minimum, or bundle with another item")],
        "item_faq": [
            ("What surface does Giant Jenga need?", "It works on pavement, sidewalk, or a closed street — no grass or level lawn required."),
            ("Is Giant Jenga included in the packages?", "Yes — it's included in the Classic, Full, and Deluxe Block Party packages, and also available on its own."),
        ],
    },
    {
        "slug": "human-beer-pong-rental-brooklyn",
        "icon": "beerpong",
        "name": "Giant / Human-Sized Beer Pong Rental",
        "price_label": "$75/day bundled",
        "offers": [{"price": 75}],
        "solo_note": "$150 solo-order minimum",
        "short": "Oversized buckets and balls, scaled up for a block-party crowd.",
        "who": "Not a kids' version — plays with water or any drink of your choice.",
        "pairs": "Included in every package tier.",
        "answer": "BlockParty rents Giant/Human-Sized Beer Pong — oversized buckets and balls scaled up for a block-party crowd — for Brooklyn block parties and backyard events, delivered and picked up, for $75/day bundled or a $150 solo-order minimum.",
        "facts": [("What it is", "Oversized buckets + oversized balls, human-scale version"), ("Who it's for", "Teens and adults — plays with water or any drink"), ("What's included", "Delivery, pickup, set-up on your block"), ("Price", "$75/day bundled"), ("Delivery note", "$150 solo-order minimum, or bundle with another item")],
        "item_faq": [
            ("Is this an alcohol game?", "It plays with water or any drink of your choice — it's not alcohol-specific, and it's scaled up for a block-party crowd rather than a dorm-room table."),
            ("Is Giant Beer Pong included in the packages?", "Yes — it's included in the Classic, Full, and Deluxe Block Party packages, and also available on its own."),
        ],
    },
    {
        "slug": "slushie-machine-rental-brooklyn",
        "icon": "slushie",
        "photo": "/images/social-wide-frozen-drinks.png",
        "photo_alt": "Vintage BlockParty illustration of a frozen-drink station: a slushie machine and dispensers on a folding table under a white canopy, with a hand-painted sign reading frozen drinks and slushies",
        "photo_w": 1376,
        "photo_h": 768,
        "name": "Slushie & Frozen Cocktail Machine Rental",
        "price_label": "$275/day single-flavor, $375/day double-flavor",
        "offers": [
            {"price": 275, "variant": "single-flavor"},
            {"price": 375, "variant": "double-flavor"},
        ],
        "solo_note": "Clears the solo-order minimum on its own",
        "short": "A real commercial frozen-drink machine, delivered, set up, and picked up after your event.",
        "who": "Single-flavor for one crowd-pleasing mix, double-flavor for two options running side by side.",
        "pairs": "Included starting in the Full package.",
        "answer": "BlockParty rents a commercial slushie and frozen cocktail machine for Brooklyn block parties and backyard events, delivered, set up, and picked up, for $275/day single-flavor or $375/day double-flavor — no self-pickup option.",
        "facts": [("What it is", "Commercial frozen-drink machine (single- or double-flavor)"), ("Who it's for", "Blocks of ~25+ wanting a drink station alongside the games"), ("What's included", "Delivery, full setup, pickup — no self-service pickup"), ("Price", "$275/day single-flavor, $375/day double-flavor"), ("Delivery note", "Clears the solo-order minimum on its own")],
        "item_faq": [
            ("Can I choose any flavor?", "The machine supports a kids' slushie flavor or an adult frozen-cocktail mix — the double-flavor unit runs two options side by side, e.g., one of each."),
            ("Do I need to pick it up myself?", "No — there is no self-pickup option for the machine. We deliver, set it up, and come back for pickup after your event."),
        ],
    },
    {
        "slug": "basketball-hoop-rental-brooklyn",
        "icon": "basketball",
        "name": "Portable Basketball Hoop Rental",
        "price_label": "$85/day bundled",
        "offers": [{"price": 85}],
        "solo_note": "$150 solo-order minimum",
        "short": "A real portable hoop system, not a toy-tier set.",
        "who": "Works on a closed street or driveway.",
        "pairs": "No power or water hookup needed.",
        "answer": "BlockParty rents a real portable basketball hoop system — not a toy-tier set — for Brooklyn block parties and backyard events, delivered and picked up, for $85/day bundled or a $150 solo-order minimum.",
        "facts": [("What it is", "Portable hoop system, regulation-style, not a toy tier"), ("Who it's for", "Blocks with a closed street or driveway to use"), ("What's included", "Delivery, pickup, set-up on your block"), ("Price", "$85/day bundled"), ("Delivery note", "$150 solo-order minimum, or bundle with another item")],
        "item_faq": [
            ("Does the hoop need power or water?", "No — it's a freestanding portable system, no hookups needed."),
            ("Can I rent just the hoop?", "Yes, as a standalone rental it carries the $150 solo-order minimum that covers a dedicated delivery-and-pickup trip, or bundle it with another item to clear that automatically."),
        ],
    },
    {
        "slug": "ball-pit-rental-brooklyn",
        "icon": "ballpit",
        "name": "Ball Pit Rental",
        "price_label": "$325/day",
        "offers": [{"price": 325}],
        "solo_note": "Clears the solo-order minimum on its own",
        "short": "6x6 to 8x8 ball pit with balls included, delivered and set up.",
        "who": "A good fit for blocks with younger kids.",
        "pairs": "Included in the Deluxe package.",
        "answer": "BlockParty rents a 6x6 to 8x8 ball pit with balls included for Brooklyn block parties and backyard events, delivered and set up, for $325/day.",
        "facts": [("What it is", "6x6 to 8x8 ball pit, balls included"), ("Who it's for", "Blocks with younger kids"), ("What's included", "Delivery, setup, pickup"), ("Price", "$325/day"), ("Delivery note", "Clears the solo-order minimum on its own")],
        "item_faq": [
            ("Is supervision required?", "Yes — supervision is required during use, and an unattended-use waiver applies."),
            ("Is the ball pit included in a package?", "Yes — it's included in the Deluxe Block Party package, and also available on its own."),
        ],
    },
]

FAQS = [
    ("What areas does BlockParty serve?", "BlockParty currently serves Brooklyn only. We don't deliver to other boroughs at this time."),
    ("How does delivery and pickup work?", "Delivery and pickup are included with every booking. After you book, we schedule a confirmation call to set your exact delivery window, drop-off location on your block, and pickup time. Our team delivers the equipment, sets it up, and returns for pickup — you don't need a vehicle, and you don't store anything afterward."),
    ("What is the confirmation call, and why does every booking include one?", "The confirmation call is a short conversation we have with every customer after booking and before the event. It confirms timing, exact placement (curb, sidewalk, or a specific spot on your block), and any street-specific logistics like permit windows or closures. It's part of every booking, not an optional upsell."),
    ("How far in advance do I need to book?", "Book at least 2 weeks ahead of your event date. This gives us time to confirm delivery logistics with you and make sure your equipment is available."),
    ("Is there a minimum order?", "Standalone single-item rentals carry a $150 minimum order value, or a flat $75 delivery/pickup fee on items priced under $150 — this covers the cost of a dedicated delivery-and-pickup trip. Ordering a package or combining multiple items in one booking clears this automatically."),
    ("Do I need a street permit to have a block party in Brooklyn?", "Yes. NYC block parties require a permit from your local Community Board, generally filed around 60 days before the event, per NYC's Street Activity Permit Office (SAPO) rules. BlockParty provides the equipment; the street permit itself is the organizer's responsibility."),
    ("What can I rent for a Brooklyn block party?", "Lawn games (cornhole, giant Jenga, giant/human-sized beer pong), a slushie or frozen-cocktail machine, a portable basketball hoop, and a ball pit — individually or bundled into the Classic, Full, or Deluxe Block Party packages."),
    ("Is BlockParty only for block parties, or can I rent for a backyard party too?", "Block parties on Brooklyn streets are our main focus, but the same equipment works for backyard parties, birthdays, and other private Brooklyn events. Delivery and the confirmation call work the same way either way."),
    ("Do you sell equipment, or only rent it?", "Rental only. The idea is you don't have to buy and store gear you'll only use once or twice a year — rent what your block wants this year, and try something different next year."),
    ("Does BlockParty offer bounce houses?", "Not currently. This isn't part of the v1 catalog."),
    ("Is BlockParty available yet? Have you done events before?", "We're brand new — your source for Brooklyn block party fun, booking now for the current season. We don't have a history of past events to point to yet, but we're ready to deliver, set up, and pick up for your block starting today. Reach out at reserve@blockpartysupply.co to book."),
]

NAV_ITEMS = [
    ("Rentals", "/rentals/"),
    ("Blog", "/blog/"),
    ("Guides", "/guides/"),
    ("How It Works", "/how-it-works.html"),
    ("About", "/about.html"),
    ("FAQ", "/faq.html"),
]

# ---------------------------------------------------------------------------
# Page registry — the single source of truth for every indexable URL (R1).
# The sitemap is generated from this registry, so it cannot drift from the
# pages the build emits. Bump `lastmod` when a page's copy or structured
# data meaningfully changes; it is an honest date, not a build stamp.
# ---------------------------------------------------------------------------

DEFAULT_LASTMOD = "2026-10-23"

CORE_PAGES = [
    {"path": "/", "lastmod": "2026-10-23"},
    {"path": "/about.html", "lastmod": "2026-10-23"},
    {"path": "/how-it-works.html", "lastmod": "2026-10-23"},
    {"path": "/faq.html", "lastmod": "2026-10-23"},
    {"path": "/rentals/", "lastmod": "2026-10-23"},
]

# ---------------------------------------------------------------------------
# Blog — The Block Party Playbook (B1–B4)
# Two authorship streams: "human" posts are written by Allie; "ai" posts are
# written by the BlockParty Trends Desk and ship only with a named human
# reviewer (publish gate, enforced by check_publish_gate). The B4 seed
# content lands as DRAFTS: "published": False keeps every post out of the
# live build — not rendered, not in the sitemap, not in llms.txt, absent
# from the hub — until Allie reviews and the flags flip. AI posts
# additionally require a named "reviewed_by" before they can ship.
# Body items are paragraph strings, ("h2"/"h3", text) headings, or
# ("html", raw) pre-built blocks.
# ---------------------------------------------------------------------------

POSTS = [
    {
        "slug": "why-we-throw-the-party",
        "stream": "human",  # "human" (Allie) or "ai" (Trends Desk)
        "title": "Why we throw the party",
        "subhead": "Block parties are how a block becomes a neighborhood — a note on what BlockParty is really for.",
        "date": "2026-10-23",   # datePublished (ISO)
        "modified": None,        # dateModified; None = never edited since publish
        "series": None,          # (key, label) or None
        "reviewed_by": None,     # AI posts only: name of the human reviewer
        "published": False,      # B4 gate: draft — ships only after Allie's sign-off
        "note": "Draft for Allie to edit — every word is hers to change before publish.",
        "body": [
            "You know the scene. The folding chairs come out at ten, somebody's uncle is judging the Jenga stack by noon, and the kids have claimed the hydrant spray like it's a water park they own. Nobody hands out trophies for any of this — and yet, every summer, the same handful of people make it happen again.",
            ("h2", "The quiet tax on the fun part"),
            "Here's what nobody sees when the party's good: the group chat that took four months to get an answer, the permit paperwork, the tables borrowed from three different stoops, the garage slowly turning into storage for games that come out twice a year. Block parties run on emotional labor, and it's usually the same neighbor paying the tax every year.",
            "BlockParty started with a simple wish: the party should be exciting for the kids tearing around the hydrant spray and for the parents trying to have one conversation that isn't about logistics. Not another thing to manage. A thing that just happens, and is good.",
            ("h2", "Why we rent instead of sell"),
            "So here's the pitch: you don't need to purchase everything and store it for the year. Rent from us, and figure out what works for the people on your block. Let the party evolve with your neighbors. Try new stuff. Build traditions. Just don't be left figuring out what to do with the stuff all year.",
            "That's the whole idea behind the company — <a href=\"/rentals/\">cornhole, giant Jenga, a slushie machine, a ball pit</a> that shows up on your block and leaves again, with delivery, pickup, and a confirmation call included either way.",
            ("h2", "What this blog is for"),
            "This is where we'll keep the notes: what Brooklyn blocks book, what they add late, what actually got played, and how the traditions got built. Some of it will be practical — permit timelines, tournament brackets, what to serve — and some of it will just be about why the block party might be the best thing a city ever invented.",
            "Written by me, Allie — founder, Brooklynite, and the person who answers reserve@blockpartysupply.co. If your block is planning its day, <a href=\"mailto:reserve@blockpartysupply.co\">email me</a> and we'll figure it out together.",
        ],
    },
    {
        "slug": "the-lifestyle-business-i-started-now",
        "stream": "human",
        "title": "A lifestyle business, started mid-life",
        "subhead": "Why BlockParty exists as a rental company, why now, and why a share of the profits flows back to the PTAs and PTOs of the blocks we serve.",
        "date": "2026-10-23",
        "modified": None,
        "series": None,
        "reviewed_by": None,
        "published": False,      # B4 gate: draft — ships only after Allie's sign-off
        "note": "Draft for Allie to edit. The bracketed paragraph needs the real profit-share terms before publish.",
        "body": [
            "The classic startup story is twenty-somethings in a garage. Mine is a woman in her forties looking at a folding table and thinking: this city's best tradition runs on borrowed stuff and burnout. There has to be a better way to throw a block party — and maybe a better way to build a business while I'm at it.",
            ("h2", "What a lifestyle business means here"),
            "BlockParty is a lifestyle business on purpose. It's built small and deliberate: Brooklyn only — no other boroughs, no exceptions. Rentals, never sales. Delivery, pickup, and a confirmation call on every booking. It's a company sized to the life around it, not the other way around — starting at this stage of life means I'm not chasing scale for its own sake, I'm building the thing I actually want to run.",
            "The idea itself is simple: the fun stuff — <a href=\"/rentals/cornhole-rental-brooklyn.html\">cornhole</a>, <a href=\"/rentals/giant-jenga-rental-brooklyn.html\">giant Jenga</a>, a <a href=\"/rentals/slushie-machine-rental-brooklyn.html\">slushie machine</a> — shouldn't require a storage unit or a standing yearly commitment. Rent what your block wants this year. Skip it next year if the block's into something else.",
            ("h2", "The profit-sharing part"),
            "Here's the piece I care about most. Block parties don't happen in a vacuum — they happen around schools. The PTAs and PTOs are the ones running the bake sales, organizing the fairs, showing up for their blocks all year long. So BlockParty is built mission-first: a share of the company's profits goes back to the PTAs and PTOs of the communities we serve. When the blocks we rent to thrive, the schools inside them should feel it too.",
            "[Allie: this is the paragraph to finish — the exact profit-share terms, the percentage or mechanism, and how schools get nominated. It ships with real numbers or not at all.]",
            ("h2", "Why now"),
            "Because the timing argument cuts both ways. I know what people say about starting over mid-life — that it's risky, that it's late. But the skills are real, the community is real, and the second act is allowed to be the good one. The garage full of games nobody uses is somebody else's business model; mine is making sure it never has to be yours.",
            "If your block is planning its party, <a href=\"/how-it-works.html\">here's how it works</a> — and if you want the founder directly, that's <a href=\"mailto:reserve@blockpartysupply.co\">reserve@blockpartysupply.co</a>.",
        ],
    },
    {
        "slug": "brooklyn-block-party-permits",
        "stream": "ai",
        "title": "Block party permits: the 60-day rule",
        "subhead": "Brooklyn block-party permits are due 60 days before your event — the CECM/SAPO timeline, the $25 fee, and when to book the fun stuff.",
        "date": "2026-10-23",
        "modified": "2026-10-27",   # added link to the definitive /guides/ permit walkthrough
        "series": ("brooklyn-trends", "Brooklyn Trends"),
        "reviewed_by": "Allie Esslinger",   # approved via review card 2026-10-23
        "published": True,       # approved for publish by Allie
        "note": "Approved by Allie Esslinger, 2026-10-23.",
        "body": [
            "File your block-party permit application at least 60 days before your event date. In New York City, block parties are permitted through the Street Activity Permit Office (SAPO) — now part of the Mayor's Office of Citywide Event Coordination and Management (CECM) — and the application carries a $25 processing fee that is not refunded if you withdraw or are denied.",
            "Every summer, Brooklyn's block-party calendar fills through this exact process. On the public permit rolls you'll find parties like Tiffany Place between Degraw Street and Kane Street (Community Board 6, 76th precinct) or 17th Street between Prospect Park West and 10th Avenue (Community Board 7, 72nd precinct) — real blocks, real closures, all filed through the same system.",
            ("h2", "How the application actually works"),
            "Block parties are single-block street closures for a single day — exactly what the SAPO rules define as a community-sponsored street event — so the application is about your specific block, your date, and your community board. You apply online through CECM's permitting system, and your community board reviews the application and weighs in before final approval. Tell your board early, not just the form.",
            "One wrinkle: some community boards ask organizers to file even earlier than the citywide deadline — Brooklyn Community Board 2's own guidance, for example, tells block parties to submit 90 days out. Treat 60 days as the floor, not a guarantee, and check your own board's page first.",
            ("h2", "A timeline that works backwards"),
            "Here's the sequence most Brooklyn organizers actually run:",
            ("html", '<table class="bracket-table"><thead><tr><th>When</th><th>What</th><th>Why</th></tr></thead><tbody><tr><td>60+ days out</td><td>File the CECM/SAPO application</td><td>Citywide block-party deadline; some community boards want earlier</td></tr><tr><td>45&ndash;30 days out</td><td>Confirm with your community board</td><td>The board reviews and recommends before SAPO decides</td></tr><tr><td>2+ weeks out</td><td>Book equipment and lock logistics</td><td>BlockParty asks for at least 2 weeks&rsquo; lead to confirm delivery windows</td></tr><tr><td>Week of</td><td>Confirmation call</td><td>Every booking includes a call to lock timing, placement, and street specifics</td></tr></tbody></table>'),
            "The order matters because the permit is the long pole. Equipment can move fast — <a href=\"/how-it-works.html\">a call and a delivery window</a> is genuinely all it takes — but the permit clock is fixed, and it runs on city time.",
            ("h2", "What the permit doesn't cover"),
            "The permit closes your street; it doesn't furnish it. The games, the tables, the <a href=\"/rentals/slushie-machine-rental-brooklyn.html\">slushie machine</a> — that part is ours to deliver, set up, and pick up, and <a href=\"/faq.html\">the permit itself stays the organizer's responsibility</a>. File the paperwork, then tell us what the block wants on it — <a href=\"/rentals/\">the full catalog is one trip away</a>. For the whole process in order — eligibility, E-Apply, the fee, and the extras that trip people up — <a href=\"/guides/nyc-block-party-permit-guide.html\">the full permit guide walks it step by step</a>.",
        ],
    },
    {
        "slug": "cornhole-tournament-brackets",
        "stream": "ai",
        "title": "Cornhole brackets that actually work",
        "subhead": "The 8-team, single-elimination cornhole bracket Brooklyn blocks actually finish — timing, rules, board placement, and the bracket to print.",
        "date": "2026-10-23",
        "modified": None,
        "series": ("brooklyn-trends", "Brooklyn Trends"),
        "reviewed_by": "Allie Esslinger",   # approved via review card 2026-10-23
        "published": True,       # approved for publish by Allie
        "note": "Approved by Allie Esslinger, 2026-10-23.",
        "body": [
            "The cornhole tournament that works on a Brooklyn block is an 8-team, single-elimination bracket with a 21-point or 15-minute cap per game, run on two boards with a losers' game alongside. Sixteen teams sounds inclusive; it turns your afternoon into a bracket-management job. Eight teams, run well, plays everyone and still ends before the slushie melts.",
            ("h2", "Why 8 teams is the sweet spot"),
            "Eight teams of two is sixteen players — about what one regulation board set can keep fed in an afternoon, since most blocks rotate 2–4 boards' worth of players over a full day. A tournament should be a highlight, not the whole schedule. Sign-ups happen at the folding table by the grill: team name, a number drawn from a coffee can, done.",
            ("h2", "The bracket to tape to the folding table"),
            "Print this, fill in the winners, keep it moving:",
            ("html", '<table class="bracket-table"><thead><tr><th>Round</th><th>Matchup</th><th>Played</th><th>Winner</th></tr></thead><tbody><tr><td>Quarterfinal 1</td><td>Team 1 vs Team 2</td><td>Board A</td><td>&mdash;</td></tr><tr><td>Quarterfinal 2</td><td>Team 3 vs Team 4</td><td>Board B</td><td>&mdash;</td></tr><tr><td>Quarterfinal 3</td><td>Team 5 vs Team 6</td><td>Board A</td><td>&mdash;</td></tr><tr><td>Quarterfinal 4</td><td>Team 7 vs Team 8</td><td>Board B</td><td>&mdash;</td></tr><tr><td>Semifinal 1</td><td>Winner QF1 vs Winner QF2</td><td>Board A</td><td>&mdash;</td></tr><tr><td>Semifinal 2</td><td>Winner QF3 vs Winner QF4</td><td>Board B</td><td>&mdash;</td></tr><tr><td>Third place</td><td>Semifinal losers</td><td>Board A</td><td>&mdash;</td></tr><tr><td>Final</td><td>Semifinal winners</td><td>Board B</td><td>&mdash;</td></tr></tbody></table>'),
            "The empty Winner column is the point — a bracket everyone can see is a bracket nobody argues with.",
            ("h2", "The three rules that keep it moving"),
            "First: games go to 21 points or 15 minutes, whichever comes first — the cap is what guarantees the bracket finishes. Second: the losing team works — it resets the boards, keeps score for the next match, and keeps the line moving. Third: nobody's afternoon ends on one bad game — the two semifinal losers meet in a third-place match, and losing teams seed the running jokes that outlast the trophy.",
            "Between the semifinals and the final, run a kids' exhibition round — shorter boards, sillier rules, no bracket. It's the breather that keeps the adults honest about the final.",
            ("h2", "Where the boards go on your block"),
            "Set the two boards facing each other on the flattest stretch of closed street you've got, away from the food table and well away from the <a href=\"/rentals/slushie-machine-rental-brooklyn.html\">slushie machine line</a>. Brooklyn pavement plays faster than grass — sweep the landing zone first and enjoy the speed.",
            "BlockParty rents a regulation 2-board cornhole set — <a href=\"/rentals/cornhole-rental-brooklyn.html\">$65/day bundled, delivered and picked up</a> — and it comes standard in every package tier: <a href=\"/rentals/\">Classic, Full, and Deluxe</a>. Add <a href=\"/rentals/giant-jenga-rental-brooklyn.html\">giant Jenga</a> beside the boards and the non-tournament players have a reason to stay too.",
        ],
    },
    {
        "slug": "frozen-drink-station-trends",
        "stream": "ai",
        "title": "Block party food & frozen-drink trends",
        "subhead": "Frozen-drink stations are becoming the anchor of Brooklyn block-party menus — single- vs double-flavor machines, and food that survives a sidewalk.",
        "date": "2026-10-23",
        "modified": None,
        "series": ("brooklyn-trends", "Brooklyn Trends"),
        "reviewed_by": "Allie Esslinger",   # approved via review card 2026-10-23
        "published": True,       # approved for publish by Allie
        "note": "Approved by Allie Esslinger, 2026-10-23.",
        "body": [
            "The trend Brooklyn hosts are planning around this season: the frozen-drink station as the anchor of the block-party menu. One commercial slushie machine — a kids' flavor on one side, an adult frozen-cocktail mix on the other — does the work a cooler full of melting ice used to do, and it makes sense to plan the food around it instead of the other way around.",
            ("h2", "Single flavor or double flavor?"),
            "The machine comes two ways. Single-flavor ($275/day) runs one mix — one crowd-pleaser for the whole block, the simplest setup on the sidewalk. Double-flavor ($375/day) runs two mixes side by side, which is the configuration that ends the biggest planning argument before it starts: a kids' slushie flavor on the left, an adult frozen cocktail on the right, one line, no drama.",
            "Either way it's a real commercial frozen-drink machine — delivered, set up, and picked up by us, with no self-pickup option, because a machine that heavy shouldn't ride home in anyone's SUV.",
            ("h2", "Food that survives a sidewalk"),
            "The menu pattern that works on a closed street is low-lift by design: one signature dish per household rather than a dozen side dishes nobody coordinated, make-ahead mains that hold at street temperature, and a shade tarp over anything dairy. A block party is not a catered dinner — the food that works is the food that forgives.",
            "Hydration rides beside every drink station: a water pitcher within reach of the kids' line, especially on hydrant-spray days when nobody realizes how much sun they're getting.",
            ("h2", "How it fits your order"),
            "The slushie machine clears BlockParty's $150 solo-order minimum on its own, so it works as a standalone rental. It's also included, single-flavor, starting in the $420 <a href=\"/rentals/\">Full Block Party package</a> — and the $675 Deluxe adds a <a href=\"/rentals/ball-pit-rental-brooklyn.html\">ball pit</a> for the under-10 crowd while the machine holds the grown-ups' attention.",
            "Full specs, flavors, and booking details live on the <a href=\"/rentals/slushie-machine-rental-brooklyn.html\">slushie &amp; frozen cocktail machine rental page</a> — and if you're building the whole day, <a href=\"/how-it-works.html\">here's how delivery and pickup work</a>.",
        ],
    },


]

BLOG_PATH = "/blog/"

def post_path(post):
    return f"{BLOG_PATH}{post['slug']}.html"

def post_image_path(post):
    """Host-relative URL for HTML/CSS references (img src, backgrounds) —
    works on any host serving dist, including the non-canonical preview."""
    return f"{BLOG_PATH}images/{post['slug']}.png"

def post_image_url(post):
    """Absolute canonical URL for machine-facing metadata (BlogPosting image)."""
    return f"{DOMAIN}{BLOG_PATH}images/{post['slug']}.png"

def published_posts():
    """POSTS that ship. Drafts (published=False — the B4 review gate) stay out
    of every public artifact: not rendered, not in the sitemap, not in
    llms.txt, absent from the hub. The flag defaults to True so a post
    without one behaves as before."""
    return [p for p in POSTS if p.get("published", True)]

# The hub changes whenever a post lands, so its lastmod tracks the newest post.
BLOG_LASTMOD = max((p["date"] for p in published_posts()), default=DEFAULT_LASTMOD)

# ---------------------------------------------------------------------------
# Guides — practical reference pages at /guides/ (G1). These are business
# reference content (like how-it-works/faq), not editorial blog posts, so
# they don't run through the B2 blog publish gate; they ship through PR
# review. NYC permit facts cite the nyc.gov pages they came from; anything
# not verifiable from city sources is phrased as guidance-to-confirm.
# Body items follow the POSTS convention: strings are paragraphs,
# ("h2"/"h3", text) headings, ("html", raw) pre-built blocks.
# ---------------------------------------------------------------------------

GUIDES_PATH = "/guides/"
GUIDES_LASTMOD = "2026-10-27"

GUIDES = [
    {
        "slug": "nyc-block-party-permit-guide",
        "title": "NYC Block Party Permit Guide",
        "label": "NYC block party permit, step by step",
        "blurb": "Eligibility, E-Apply steps, the 60-day rule, the $25 fee, and what happens after you file.",
        "description": "How to get an NYC block party permit: eligibility, the E-Apply application, the 60-day deadline, the $25 fee, community board review, and what happens next.",
        "updated": "2026-10-27",
        "body": [
            "Short version: a block party on a closed Brooklyn street runs on a Street Activity Permit, filed through the city's E-Apply system at least 60 days before your date, with a $25 non-refundable fee. The permit itself is the organizer's job — <a href=\"/faq.html\">that's been the deal since day one</a> — and this page walks the whole process in order.",
            ("h2", "What counts as a block party (to the city)"),
            "New York City defines a block party as a community-sponsored, public event — one block, one day, no sale of goods or services, no fundraising, generally limited to nine consecutive hours (<a href=\"https://www.nyc.gov/site/cecm/permitting/permit-types/block-parties.page\" rel=\"nofollow\">CECM's block party rules</a>). That \"no sales\" line is the hinge: the moment money changes hands on the street, you're describing a street festival, which is a different permit with different requirements — including insurance and Health Department clearances.",
            ("h2", "Before you apply: two checks that prevent rejections"),
            "First, your community board. The citywide rule is 60 days, but boards run their own calendars on top of it — Brooklyn Community Board 2's guidance, for example, asks block parties to submit 90 days out, and Brooklyn CB9 set July 14 as the last day to apply for a summer 2026 party (<a href=\"https://www.nyc.gov/site/brooklyncb9/resources/block-parties-and-street-activities.page\" rel=\"nofollow\">CB9's block party page</a>). Check your own board's page for its deadline and any extra paperwork.",
            "Second, your police precinct. Some precincts keep lists of blocks that can't close and dates that are already spoken for — Brooklyn CB4, for instance, tells organizers to check the 83rd Precinct's street-closing denial and blocked-off date lists before applying (<a href=\"https://www.nyc.gov/site/brooklyncb4/resources/block-parties-and-street-fairs.page\" rel=\"nofollow\">CB4's process</a>). One look at that list can save you $25 and a summer of waiting.",
            ("h2", "The application, step by step"),
            ("html", "<ol><li><strong>Create an E-Apply account.</strong> Block party permits are filed online through the city's E-Apply system at nyc.gov — and if you've held a permit from SAPO or another city agency, you may already have the account.</li><li><strong>Choose \"Block Party\" as the event type,</strong> then enter your date and the sponsor contact. If a community organization is sponsoring, the contact should be a person in that organization, not \"whoever answers the group chat fastest.\"</li><li><strong>Enter the location:</strong> the specific block you're closing.</li><li><strong>Fill out the questionnaire.</strong> Describe the event and list everything that will occupy the street, sidewalk, or curb lane — tables, games, the drink station. Honesty here is what keeps the agencies from surprises later.</li><li><strong>Upload what your board asks for.</strong> Some boards want resident signatures, a site plan, or an event schedule.</li><li><strong>Pay the $25 processing fee</strong> by credit or debit card. It's non-refundable — denied or withdrawn, it stays with the city (<a href=\"https://home4.nyc.gov/site/cecm/permitting/fees.page\" rel=\"nofollow\">CECM's fee schedule</a>).</li></ol>"),
            "From there the application routes to SAPO — the Street Activity Permit Office, now part of the Mayor's Office of Citywide Event Coordination and Management — along with the NYPD and your community board.",
            ("h2", "After you file: the review"),
            "Your community board reviews the application and weighs in before final approval, and SAPO coordinates with the NYPD and other city agencies. Answer document requests fast — a slow email thread is how August dates get lost. Approval isn't real until you're holding it.",
            ("h2", "The extras that trip people up"),
            "Amplified sound needs a separate NYPD sound permit, and sound permits generally expire at 7:00 p.m. — plan the speeches accordingly. Rides and some inflatables trigger insurance and clearance requirements. Food for the general public runs on its own Health Department track (<a href=\"/guides/block-party-food-bbq-rules-insurance.html\">covered here</a>), and a tent or temporary structure over 10 feet tall can pull in the Department of Buildings. None of these are reasons to skip the party; they're just not on the main form.",
            ("h2", "Approved. Now what?"),
            "Download the permit from E-Apply, print it, and keep it on the block on party day — it's the document that answers \"who said this was okay?\" before anyone has to ask it twice.",
            ("html", "<table class=\"bracket-table\"><thead><tr><th>When</th><th>What</th><th>Why</th></tr></thead><tbody><tr><td>90 days out</td><td>Check your community board's own deadline</td><td>Some boards want more than the citywide 60 days</td></tr><tr><td>60 days out</td><td>File the E-Apply application and pay the $25 fee</td><td>Citywide floor for block party applications</td></tr><tr><td>45&ndash;30 days out</td><td>Follow up with your board; answer document requests</td><td>The board reviews and recommends before approval</td></tr><tr><td>30 days out</td><td>Coordinate food with DOHMH if the public is eating</td><td>Temporary food service permits take their own track</td></tr><tr><td>2+ weeks out</td><td>Book the equipment</td><td><a href=\"/guides/when-to-book-block-party-rentals.html\">BlockParty's minimum lead is 2 weeks</a></td></tr><tr><td>Week of</td><td>Confirmation call</td><td>Delivery window, placement, and pickup get locked</td></tr></tbody></table>"),
            "The permit is the long pole; the equipment is the easy part. When the paperwork's in, <a href=\"/rentals/\">browse the catalog</a> or <a href=\"mailto:reserve@blockpartysupply.co\">email us</a> — the street's closed either way, so it might as well be fun.",
        ],
        "faq": [
            ("How far in advance do I need to apply for an NYC block party permit?", "At least 60 days before your event, through the city's E-Apply system. Treat 60 days as the floor — some community boards ask for earlier filing on top of that."),
            ("How much does a block party permit cost in NYC?", "A $25 non-refundable processing fee, paid online when you apply. The fee is not returned if your application is denied or withdrawn."),
            ("Can I sell food at an NYC block party?", "Not under a standard block party permit — block parties are community events with no sales of goods or services. Events with vendors or food sales are a different permit type with Health Department requirements."),
            ("Do I need a separate permit for amplified sound at a block party?", "Yes — amplified sound needs its own NYPD sound permit, separate from the street activity permit, and sound permits generally expire at 7:00 p.m."),
        ],
    },
    {
        "slug": "block-party-street-closure-logistics",
        "title": "Block Party Street Closure Logistics",
        "label": "Street closure logistics",
        "blurb": "Barricades, the emergency lane, closure hours, hydrant spray caps, and the no-list.",
        "description": "What a closed Brooklyn street involves: barricades, the emergency lane, closure hours, hydrant spray caps, generators, and the rules that keep it clean.",
        "updated": "2026-10-27",
        "body": [
            "The permit closes your street on paper. Logistics close it in real life — and \"logistics\" here means one planning conversation with your precinct, a lane for ambulances, and a short list of rules that all boil down to the same idea: the street comes back by night.",
            ("h2", "Know your hours before you plan anything"),
            "Block party permits run for one day, generally no more than nine consecutive hours. Community board rules commonly let you close as early as 9:00 a.m. and require the street fully reopened by 9:00 p.m. — tables, chairs, and games out of the roadway — and your precinct can require an earlier reopening (<a href=\"https://www.nyc.gov/site/queenscb10/resources/block-party-procedure.page\" rel=\"nofollow\">an example of the 9 p.m. rule, from Queens CB10</a>). Build your schedule backwards from reopening, not forwards from the first coffee.",
            ("h2", "Barricades and the emergency lane"),
            "No city crew arrives to dress your block. Current guidance puts arranging the closure on the organizer, coordinated with the local precinct — so ask your precinct directly what they require at each end of the block. What's non-negotiable everywhere: a clear emergency lane all day, and no blocking of intersections, hydrants, or building entrances (<a href=\"https://www.nyc.gov/html/dot/html/pedestrians/openstreets.shtml\" rel=\"nofollow\">the same access rule DOT applies to Open Streets</a>).",
            ("h2", "Hydrants: spray caps or nothing"),
            "An opened hydrant without a spray cap is illegal, dangerous, and the fastest way to end a good party — the pressure turns the gutter into a river and the Fire Department turns it off. The legal version: the FDNY installs spray caps, so arrange it before your date, and keep the hydrant visible and unblocked either way (<a href=\"https://www.nyc.gov/site/fdny/education/fire-and-life-safety/block-parties.page\" rel=\"nofollow\">FDNY's block party safety page</a>).",
            ("h2", "Power, generators, and cooking"),
            "Generators at permitted street events need an FDNY certificate. Cooking is its own question: the city's 2026 event permitting guide says permitted street events may not barbecue on location (<a href=\"/guides/block-party-food-bbq-rules-insurance.html\">the food page has the details</a>). The games in our catalog were chosen in part because none of them need power, water, or an open flame: <a href=\"/rentals/cornhole-rental-brooklyn.html\">cornhole</a>, <a href=\"/rentals/giant-jenga-rental-brooklyn.html\">giant Jenga</a>, and <a href=\"/rentals/human-beer-pong-rental-brooklyn.html\">giant beer pong</a> work anywhere on a closed block. The <a href=\"/rentals/slushie-machine-rental-brooklyn.html\">slushie machine</a> we deliver, set up, and pick up — talk placement with us on the confirmation call.",
            ("h2", "The no-list"),
            "Alcohol is prohibited on the street and sidewalk at permitted block parties, along with vendors, commercial branding, and admission charges. Fireworks are illegal, full stop. Yes, some blocks bend these rules every summer; also yes, one call from one neighbor can end the whole afternoon early. The list is short. Keep all of it.",
            "One practical translation for the games: the <a href=\"/rentals/human-beer-pong-rental-brooklyn.html\">human beer pong</a> buckets play with water or any drink of your choice — and on a closed street, the drink is water. The street version of the game is about the toss, not the tab.",
            "Your permit and your precinct decide the shape of the day; we bring what goes in the middle of it. <a href=\"/rentals/\">See the full catalog</a> — everything on it was picked for closed-pavement Brooklyn blocks.",
        ],
        "faq": [
            ("Who sets up barricades for an NYC block party?", "The organizer arranges the closure with the local NYPD precinct — city guidance doesn't have DOT or NYPD routinely supplying barricades for block parties. Ask your precinct what they require, and keep an emergency lane clear all day."),
            ("What time does a block party street have to reopen?", "Community board rules commonly require the street fully reopened — tables, chairs, and games out of the roadway — by 9:00 p.m., and your precinct can require an earlier time. Plan backwards from reopening."),
            ("Can we open the fire hydrant during the party?", "Only with an FDNY-approved spray cap, arranged before your event. Uncapped hydrants are illegal and dangerous, and they wreck water pressure for the whole block."),
        ],
    },
    {
        "slug": "block-party-food-bbq-rules-insurance",
        "title": "Block Party Food, BBQ & Insurance",
        "label": "Food, BBQ & insurance rules",
        "blurb": "The BBQ rule, Health Department permits for public food, and when insurance applies.",
        "description": "Can you grill at an NYC block party, when does food need a permit, and does a block party need insurance? What the city's rules say, and what to confirm.",
        "updated": "2026-10-27",
        "body": [
            "Food is where block parties get ambitious and permits get technical. The rules split three ways — cooking on the street, serving the public, and who's liable if something goes wrong — so here's each, straight.",
            ("h2", "The BBQ question"),
            "The city's Comprehensive Event Permitting Guide for 2026 is blunt: at permitted street and sidewalk events, the permittee must not barbecue on location, and there are no sit-down catered meals on public streets (<a href=\"https://www.nyc.gov/assets/cecm/downloads/pdf/CECM-Comprehensive-Event-Permitting-Guide-2026.pdf\" rel=\"nofollow\">CECM guide, PDF</a>). Plenty of blocks run grills anyway; that's the \"one neighbor's phone call\" category from our <a href=\"/guides/block-party-street-closure-logistics.html\">closure logistics page</a>. If a grill is central to your plan, get written confirmation from your community board and SAPO before you count on it — don't assume practice equals permission.",
            "The menu shape that works with the rules instead of against them: one signature dish per household, made ahead, served from folding tables. That's not a compromise — it's how the best block parties already eat.",
            ("h2", "If the public is eating, that's a different lane"),
            "Handing plates to your neighbors is the normal block-party shape. Serving food to the general public at a temporary event — a booth, a stand — runs on Health Department rules: vendors typically need a Temporary Food Service Establishment permit, and organizers should coordinate with DOHMH about 30 days out (<a href=\"https://www.nyc.gov/site/doh/business/food-operators/temporary-food-service-establishments.page\" rel=\"nofollow\">DOHMH's temporary food page</a>, <a href=\"https://portal.311.nyc.gov/article/?kanumber=KA-01825\" rel=\"nofollow\">311's plain-English version</a>). And selling food or anything else is off the table under a block party permit — vendor events are a different permit type entirely.",
            ("h2", "Insurance: probably not — but confirm your classification"),
            "A standard block party doesn't automatically trigger the city's $1 million commercial liability requirement. That requirement attaches to street festivals, commercial and promotional events, and block parties with rides — typically a certificate of liability naming New York City as an additional insured (<a href=\"https://www.nyc.gov/site/cecm/support/frequently-asked-questions.page\" rel=\"nofollow\">CECM's permit FAQ</a>). Which side your event lands on depends on its classification, so ask SAPO what your event counts as before you apply. If you need a certificate, that's a question for your insurer or broker — the city names what it requires; who you buy it from is your call. And keep the division of labor straight: the street permit — and anything the city requires alongside it — belongs to the organizer; <a href=\"/how-it-works.html\">the equipment logistics are ours</a>.",
            ("h2", "A menu that survives a sidewalk"),
            "Whatever the permit situation, the food that works on a closed street is the food that forgives: made-ahead mains that hold at street temperature, shade over anything dairy, and a water pitcher within reach of the kids' line. For the cold stuff, the <a href=\"/rentals/slushie-machine-rental-brooklyn.html\">slushie machine</a> does the work a cooler full of melting ice used to (<a href=\"/blog/frozen-drink-station-trends.html\">more on that here</a>) — and it clears our $150 solo-order minimum on its own.",
            "Rules change; check the city pages linked above when you plan, and ask your community board the specific questions early. Then <a href=\"/rentals/\">let us handle the not-food part</a>.",
        ],
        "faq": [
            ("Can you barbecue at an NYC block party?", "The city's 2026 event permitting guide says permitted street and sidewalk events may not barbecue on location. If a grill is central to your plan, get written confirmation from your community board and SAPO before you commit — don't assume practice equals permission."),
            ("Do I need a permit to give out food at a block party?", "Food for your neighbors is the normal block-party case. Serving the general public at a temporary event is Health Department territory — vendors typically need a Temporary Food Service Establishment permit, and organizers should coordinate with DOHMH about 30 days ahead."),
            ("Does a NYC block party need insurance?", "Usually not for a standard block party. The city's insurance requirements attach to street festivals, commercial events, and block parties with rides — typically a $1 million certificate of liability naming the City as an additional insured. Confirm your event's classification with SAPO before applying."),
        ],
    },
    {
        "slug": "block-party-planning-timeline",
        "title": "Block Party Planning Timeline",
        "label": "Planning timeline & checklist",
        "blurb": "90/60/30/14 — the whole timeline backwards from party day, plus the checklist.",
        "description": "A Brooklyn block party timeline that works backwards from the fun: the 60-day permit clock, board follow-up, food notices, and when to book equipment.",
        "updated": "2026-10-27",
        "body": [
            "A block party has one immovable object — the city's permit clock — and a dozen movable parts around it. Plan backwards from party day and the whole thing stays calm. Here's the sequence that works, with the two dates nobody should have to learn twice: the permit application goes in 60 days out, minimum, and equipment gets booked at least 2 weeks out.",
            ("html", "<table class=\"bracket-table\"><thead><tr><th>When</th><th>What</th><th>Why</th></tr></thead><tbody><tr><td>90 days out</td><td>Check your community board's own rules and deadline</td><td>Some boards want more than the citywide 60 days</td></tr><tr><td>60 days out</td><td>File the E-Apply permit application, pay the $25 fee</td><td>The citywide floor — the long pole starts here</td></tr><tr><td>45&ndash;30 days out</td><td>Follow up with your board; answer document requests fast</td><td>The board reviews and recommends before approval</td></tr><tr><td>30 days out</td><td>If the public is eating, coordinate with DOHMH</td><td>Temporary food permits run their own track</td></tr><tr><td>2+ weeks out</td><td>Book the equipment &mdash; <a href=\"mailto:reserve@blockpartysupply.co\">email us</a></td><td>BlockParty's minimum lead for delivery windows and availability</td></tr><tr><td>Week of</td><td>Confirmation call</td><td>Delivery window, placement on the block, and pickup get locked</td></tr><tr><td>Day before</td><td>Whatever your precinct asked for &mdash; notices, signage &mdash; happens now</td><td>Not on party morning, when half the block is inflating pools</td></tr><tr><td>Party day</td><td>Setup, then the fun</td><td>Keep the emergency lane clear; hydrant stays capped or closed</td></tr><tr><td>9 p.m.</td><td>Street reopened, roadway clear</td><td>Community board rules commonly require it; the precinct can want earlier</td></tr></tbody></table>"),
            ("h2", "The checklist version"),
            ("html", "<ul><li>Permit filed on E-Apply (60 days out, $25 fee)</li><li>Community board's own deadline checked — and met</li><li>Precinct's denied-block and blocked-date lists checked</li><li>Sound permit filed if anything's amplified</li><li>Food plan set — DOHMH coordinated if the public is eating</li><li>Spray cap requested from the FDNY if the hydrant's in the plan</li><li>Equipment booked (2+ weeks out)</li><li>Rain plan agreed (<a href=\"/guides/block-party-rain-plan.html\">there's a page for that</a> — the city doesn't do rain dates)</li><li>Budget collected (<a href=\"/guides/block-party-budget-planner.html\">the planner</a> helps)</li><li>Confirmation call done</li></ul>"),
            "Notice what's not on the list: anything about games, tables, or the drink station after the 2-week mark. That's deliberate — <a href=\"/guides/when-to-book-block-party-rentals.html\">the equipment is the easy part</a>, and it stays easy right up until the confirmation call makes it certain.",
            "Want the long version of the permit steps? <a href=\"/guides/nyc-block-party-permit-guide.html\">Start here</a> — then hand this page to whoever inherits the group chat next year.",
        ],
        "faq": [
            ("What is the most common block party planning mistake?", "Treating the 60-day permit filing as the only deadline. Community boards can want more notice, food for the public adds a 30-day Health Department track, and precinct requirements vary. File early, then work the checklist backwards from party day."),
            ("When should I book rentals for a block party?", "At least 2 weeks before your date — BlockParty's minimum lead — but book as soon as your permit filing is in. The permit is the long pole; early booking locks your equipment while it's still available."),
        ],
    },
    {
        "slug": "block-party-budget-planner",
        "title": "Block Party Budget Planner",
        "label": "Budget planner",
        "blurb": "Real rental prices, the city's $25 fee, and where packages beat à la carte.",
        "description": "What a Brooklyn block party costs: real rental prices from $65/day, the $25 permit fee, the line items to price locally, and where packages beat à la carte.",
        "updated": "2026-10-27",
        "body": [
            "Here's the honest math. A block party has one small fixed city cost and one big equipment line, and everything else is food and folding chairs you price out locally. We'll give you our actual numbers — the same ones on our <a href=\"/rentals/\">catalog pages</a> — and mark clearly what we're not the source for.",
            ("h2", "The fixed city cost"),
            "The street activity permit runs $25, non-refundable even if you're denied or withdraw. If anything's amplified, there's a separate sound permit. That's the city's share of the budget — the permit fee is not where block party money goes.",
            ("h2", "The equipment math (our real prices)"),
            ("html", "<table class=\"bracket-table\"><thead><tr><th>Option</th><th>Price</th><th>Sized for</th></tr></thead><tbody><tr><td>Classic Block Party Package</td><td>$185</td><td>~10&ndash;25 people: cornhole, giant Jenga, giant beer pong</td></tr><tr><td>Full Block Party Package</td><td>$420</td><td>~25&ndash;50 people: everything in Classic plus a single-flavor slushie machine</td></tr><tr><td>Deluxe Block Party Package</td><td>$675</td><td>~40&ndash;75 people: everything in Full plus a ball pit</td></tr><tr><td>Cornhole set</td><td>$65/day bundled</td><td>2&ndash;4 players at a time, all-day rotation</td></tr><tr><td>Giant Jenga</td><td>$65/day bundled</td><td>All ages, any pavement</td></tr><tr><td>Giant/human beer pong</td><td>$75/day bundled</td><td>Teens and adults</td></tr><tr><td>Portable basketball hoop</td><td>$85/day bundled</td><td>Closed street or driveway</td></tr><tr><td>Slushie machine</td><td>$275/day single-flavor, $375/day double-flavor</td><td>Drink-station anchor for ~25+</td></tr><tr><td>Ball pit</td><td>$325/day</td><td>Blocks with younger kids (supervision required)</td></tr></tbody></table>"),
            "Every price above includes delivery, pickup, and the pre-event confirmation call. Standalone single-item orders carry a $150 minimum order value — or a flat $75 delivery/pickup fee on items priced under $150 — and bundling with any other item clears that automatically.",
            "And the packages earn their keep: the Classic trio books à la carte for $65 + $65 + $75 = $205, and the package is $185. Full is $420 against $460 for Classic-plus-slushie. Deluxe is $675 against $745 for Full-plus-ball-pit. Same equipment, same service, less money — that's the whole trick.",
            ("h2", "The line items we're not the source for"),
            "Food and drinks, tables and chairs, ice, cups, a canopy, trash bags, a banner for the corner — we don't rent any of it (rentals only, we don't sell equipment), so price those with local vendors. Budget honest numbers for the crowd you actually expect; the <a href=\"/guides/what-to-rent-for-crowd-size.html\">crowd-size guide</a> keeps the equipment side from bloating.",
            ("h2", "Splitting it fairly"),
            "The budget conversation is the group chat's final boss. What works: one post with the real total, small asks split the way the block splits everything, and collection finished before the week of — not on party morning. Keep the ask modest: for most blocks, the equipment is the cheapest memorable thing on the budget.",
            "When the numbers look right, <a href=\"mailto:reserve@blockpartysupply.co\">email us</a> — the confirmation call is where the plan gets locked.",
        ],
        "faq": [
            ("How much does a block party cost in Brooklyn?", "The city's share is small — a $25 permit fee. Equipment is the main line item: BlockParty packages run $185 (Classic), $420 (Full), and $675 (Deluxe), with à la carte games from $65/day. Food, tables, and supplies are separate line items to price locally."),
            ("Does BlockParty charge for delivery?", "Delivery, pickup, and the confirmation call are included with every booking. Standalone single-item orders carry a $150 minimum order value, or a flat $75 delivery/pickup fee on items priced under $150 — cleared automatically by bundling or a package."),
        ],
    },
    {
        "slug": "block-party-rain-plan",
        "title": "Rain Plan for a Brooklyn Block Party",
        "label": "Rain contingency plan",
        "blurb": "No rain dates in NYC — here's the wet-weather plan instead.",
        "description": "NYC doesn't do rain dates for block parties — build a wet-weather plan instead: the go/no-go call, what moves under cover, and how the rental fits in.",
        "updated": "2026-10-27",
        "body": [
            "First, the fact that shapes everything: New York City doesn't accept rain-date applications for block parties. Your permit is for one specific date — there's no \"and if it rains, the following Saturday\" box on the form. Check the forecast like it owes you money, and build the plan that works in both weathers.",
            ("h2", "The go/no-go call"),
            "Pick a decision time — morning of, early — and a decider: one person, not a committee of the whole group chat. Summer rain in Brooklyn is usually a passing shower, not an event-killer; the plan that works is \"start late\" or \"shorten the day\" more often than \"cancel.\"",
            ("h2", "What moves, what stays"),
            "Under cover goes anything with a plug or a pour: the drink station first. Give the <a href=\"/rentals/slushie-machine-rental-brooklyn.html\">slushie machine</a> the most covered spot on the block — shade is good practice on a sunny day anyway (<a href=\"/blog/frozen-drink-station-trends.html\">more on drink-station setup here</a>). The lawn games shake off a drizzle; pause play when the bags soak through or the Jenga stack goes slippery — nobody's proud moment happens with wet gear.",
            ("h2", "Canopies and the 10-foot line"),
            "A pop-up canopy keeps the food table usable and the adults upright. The rule to know: a temporary structure over 10 feet tall can pull in a Department of Buildings permit — so keep the setup modest and weighted, and your rain plan simple.",
            ("h2", "How the rental fits in"),
            "The confirmation call every booking includes is exactly where this gets settled: delivery window, placement, pickup — matched to what the day actually needs. If the forecast turns ugly before your date, <a href=\"mailto:reserve@blockpartysupply.co\">email us</a> and we'll talk through it. Rescheduling terms are a booking detail we confirm with you directly — ask at booking, get a straight answer, no fine print.",
            "And when the sky does cooperate: <a href=\"/rentals/\">the catalog</a> is built for exactly one kind of day — the kind where the street is closed and the block is out.",
        ],
        "faq": [
            ("Does NYC give rain dates for block parties?", "No — the city doesn't accept rain-date or make-up-date applications for block parties. Your permit covers one specific date, so build a wet-weather plan instead of banking on a do-over."),
            ("What happens if it rains on my block party?", "Light rain: cover the drink station and electronics, pause the lawn games, keep going. Steady rain: make the morning-of go/no-go call with your neighbors. If the forecast turns before your date, email us — the confirmation call is where delivery, setup, and pickup get matched to what the day actually needs."),
        ],
    },
    {
        "slug": "what-to-rent-for-crowd-size",
        "title": "What to Rent for Your Crowd Size",
        "label": "What to rent for your crowd size",
        "blurb": "Packages sized for 10–75 people, and the à la carte calls that change a party.",
        "description": "Matching block party rentals to your headcount: packages sized for 10–75 people, à la carte games from $65/day, and when a slushie machine or ball pit fits.",
        "updated": "2026-10-27",
        "body": [
            "Rent for the crowd you have, not the one you're picturing at peak. Here's the sizing we use when blocks ask us — and it's the same sizing our packages were built around.",
            ("h2", "The quick answer"),
            ("html", "<table class=\"bracket-table\"><thead><tr><th>Your crowd</th><th>Rent</th><th>Why it works</th></tr></thead><tbody><tr><td>~10&ndash;25 people (small block, backyard-scale)</td><td><strong>Classic package — $185</strong>: cornhole, giant Jenga, giant beer pong</td><td>Three games cover a crowd this size with rotation</td></tr><tr><td>~25&ndash;50 people (a full block out)</td><td><strong>Full package — $420</strong>: Classic plus a single-flavor slushie machine</td><td>The drink station earns its spot at this scale</td></tr><tr><td>~40&ndash;75 people (family-heavy, multiple generations)</td><td><strong>Deluxe package — $675</strong>: Full plus a ball pit</td><td>The under-10s get their own anchor</td></tr></tbody></table>"),
            ("h2", "Why packages beat picking items one by one"),
            "Arithmetic, mostly: the Classic trio books à la carte for $65 + $65 + $75 = $205, and the package is $185 with the same delivery, pickup, and confirmation call. Packages are also sized by the people who deliver the stuff — they're what we'll recommend on the call if they fit.",
            ("h2", "The à la carte calls that change a party"),
            "Hot day or long party: the <a href=\"/rentals/slushie-machine-rental-brooklyn.html\">slushie machine</a> ($275/day single-flavor, $375/day double-flavor — one kids' flavor and one adult mix side by side). Blocks with a lot of under-10s: the <a href=\"/rentals/ball-pit-rental-brooklyn.html\">ball pit</a> ($325/day, supervision required). A block with teenagers: the <a href=\"/rentals/basketball-hoop-rental-brooklyn.html\">portable hoop</a> ($85/day) buys you four quiet hours. Every item works on closed pavement; each <a href=\"/rentals/\">item page</a> notes what it needs.",
            ("h2", "Two placement rules that matter more than quantity"),
            "First: two or three well-placed games beat five scattered ones — players rotate, and nobody wonders where the crowd is. Second: keep the games where people can see them from the food table. A game nobody can see from the food table is a game that plays twice all day.",
            "Measure the block, count the kids, <a href=\"/rentals/\">pick the tier</a> — or <a href=\"mailto:reserve@blockpartysupply.co\">email us</a> and we'll size it with you on the confirmation call.",
        ],
        "faq": [
            ("What should I rent for 30 people at a block party?", "The Full Block Party package ($420) is sized for roughly 25–50 people: cornhole, giant Jenga, giant beer pong, and a single-flavor slushie machine, delivered and picked up. Skew young? Add the ball pit. A teenager-heavy block? Add the portable basketball hoop."),
            ("How many games does a block party need?", "Fewer than you think: two or three well-placed games rotate players all day. A regulation two-board cornhole set plays 2–4 at a time, and a game nobody can see from the food table plays twice all day."),
        ],
    },
    {
        "slug": "when-to-book-block-party-rentals",
        "title": "When to Book Block Party Rentals",
        "label": "When to book rentals",
        "blurb": "The city's 60-day clock, our 2-week lead, and why you book the same week you file.",
        "description": "The deadline math for a block party: the city's 60-day permit clock, our 2-week minimum lead, and why you book equipment the same week you file the permit.",
        "updated": "2026-10-27",
        "body": [
            "Two clocks run your block party: the city's and ours. One takes 60 days and doesn't bend; the other takes 2 weeks and a phone call. Here's how to make them line up.",
            ("h2", "The city's clock: 60 days, minimum"),
            "Block party permit applications go in at least 60 days before your date through the city's E-Apply system. That's the citywide floor — some community boards ask for more (Brooklyn Community Board 2's guidance says 90 days), and summer calendars can have hard cutoffs. The full sequence lives in our <a href=\"/guides/nyc-block-party-permit-guide.html\">permit guide</a>.",
            ("h2", "Our clock: 2 weeks, and it's a minimum, not a target"),
            "BlockParty asks for at least 2 weeks' lead before your event. That's what it takes to confirm your delivery window, your setup spot, and your pickup with you — the confirmation call is part of every booking, not an upsell. But 2 weeks is the minimum we ask for, not a promise that your first-choice setup is still sitting free. Book the week your permit filing goes in and the question never comes up.",
            ("h2", "The move: same-week booking"),
            "The permit application and the rental email can go out the same afternoon. One of them starts 60 days of city time; the other starts two weeks of, honestly, pretty light logistics. Organizer note: whoever fills out the E-Apply form should <a href=\"mailto:reserve@blockpartysupply.co\">send us the email</a> before closing the laptop.",
            ("h2", "What booking late actually costs"),
            "File at 60 days and book at 13, and the street still closes — with nothing on it. A closed block with no games is just a very public parking complaint. The fix costs nothing: book when you file.",
            "Your date's real the moment the application's in. <a href=\"/rentals/\">Pick the package</a>, send the email, and get back to the group chat — you've done the hard parts.",
        ],
        "faq": [
            ("How far in advance should I book block party rentals?", "BlockParty asks for at least 2 weeks' lead to confirm delivery windows and equipment availability. Book the same week you file your permit application — the permit is the long pole at 60 days, and early booking locks your equipment."),
            ("Is two weeks really enough lead time?", "It's the minimum, not the target. Two weeks covers the logistics on our side; the 60-day permit clock and your community board's own deadlines are what actually pace the planning. Book as early as your date is real."),
        ],
    },
]

def guide_path(guide):
    return f"{GUIDES_PATH}{guide['slug']}.html"

def build_guides_hub():
    """Hub at /guides/: hero, one tile per guide, cross-link band."""
    tiles = "".join(
        f"""
        <a class="tile-link" href="{guide_path(g)}">
        <div class="tile">
          <h3>{html.escape(g['label'])}</h3>
          <p>{html.escape(g['blurb'])}</p>
        </div>
        </a>"""
        for g in GUIDES
    )
    body = f"""
<section class="hero" style="padding-bottom:24px;">
  <div class="container hero-inner" style="text-align:left; max-width:820px;">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; Block Party Guides</div>
    <h1>Block party guides for Brooklyn organizers</h1>
    <p class="hero-sub" style="margin:0;">The practical side of throwing the party: permits, street closures, food rules, budgets, rain plans, and what to rent &mdash; written by the company that delivers, sets up, and picks up the fun.</p>
  </div>
</section>
<section style="padding-top:24px;">
  <div class="container">
    <div class="icon-grid">
        {tiles}
    </div>
  </div>
</section>
<section class="section-alt">
  <div class="container">
    <div class="cta-band">
      <h2>Reading is step one</h2>
      <p>When you're ready for the equipment, the catalog's one click away &mdash; delivery, pickup, and a confirmation call included.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/rentals/">Browse rentals</a>
        <a class="btn btn-secondary" href="/blog/">The Block Party Playbook</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        title="Block Party Guides — BlockParty Brooklyn",
        description="Guides for Brooklyn block-party organizers: permits, street closures, food and insurance rules, budgets, rain plans, and what to rent for your crowd.",
        path=GUIDES_PATH,
        body=body,
        json_ld_objects=[
            breadcrumb_jsonld([("Home", "/"), ("Block Party Guides", GUIDES_PATH)]),
        ],
    )

def build_guide_page(guide):
    """Guide template: hero with updated badge, body, optional FAQ, CTA band."""
    paragraphs = render_post_body(guide)
    faq_section = ""
    faq_ld = []
    if guide.get("faq"):
        qa_pairs = guide["faq"]
        items = "".join(
            f'<div class="faq-item"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></div>'
            for q, a in qa_pairs
        )
        faq_section = (
            '<section class="section-alt"><div class="container">'
            '<div class="section-head" style="text-align:left; margin-bottom:24px;"><h2>Frequently asked</h2></div>'
            f'<div class="faq-list">{items}</div>'
            "</div></section>"
        )
        faq_ld = [faqpage_jsonld(qa_pairs)]
    body = f"""
<section class="hero" style="padding-bottom:0;">
  <div class="container hero-inner" style="text-align:left; max-width:820px;">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/guides/">Block Party Guides</a> &rsaquo; {html.escape(guide['title'])}</div>
    <h1>{html.escape(guide['title'])}</h1>
    <p class="hero-sub" style="margin:0;">{html.escape(guide['description'])}</p>
    <div class="blog-post-meta"><span class="blog-date-badge">Updated {format_date(guide['updated'])}</span></div>
  </div>
</section>
<section style="padding-top:24px;">
  <div class="container narrative">
    {paragraphs}
  </div>
</section>
{faq_section}
<section>
  <div class="container">
    <div class="cta-band">
      <h2>Planning your block's party?</h2>
      <p>Browse the packages or the full catalog &mdash; delivery, pickup, and a confirmation call are included either way.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/rentals/">Browse rentals</a>
        <a class="btn btn-secondary" href="/guides/">&larr; All block party guides</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        title=f"{guide['title']} — BlockParty Brooklyn",
        description=guide["description"],
        path=guide_path(guide),
        body=body,
        json_ld_objects=[
            breadcrumb_jsonld([
                ("Home", "/"),
                ("Block Party Guides", GUIDES_PATH),
                (guide["title"], guide_path(guide)),
            ]),
            *faq_ld,
        ],
    )

MONTHS = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]

def format_date(iso_date):
    """ISO date -> 'October 23, 2026' for display."""
    year, month, day = (int(part) for part in iso_date.split("-"))
    return f"{MONTHS[month - 1]} {day}, {year}"

def check_publish_gate():
    """B2 publish gate: an AI-written post ships only with a named reviewer.

    Runs before any output is written, so an unreviewed post fails the build
    instead of quietly rendering.
    """
    problems = []
    for post in POSTS:
        if post["stream"] not in ("human", "ai"):
            problems.append(
                f"{post_path(post)}: unknown stream {post['stream']!r} (use 'human' or 'ai')"
            )
            continue
        if not post.get("published", True):
            continue  # drafts ship nowhere, so they cannot violate the gate
        if post["stream"] == "ai" and not (post.get("reviewed_by") or "").strip():
            problems.append(
                f"{post_path(post)}: AI-written post has no 'reviewed_by' — "
                "it cannot ship until Allie (or a named human) has reviewed it"
            )
    if problems:
        print("Publish gate failed — unreviewed post(s) blocked:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

def page_registry():
    """Core pages, one entry per catalog item page, and the blog (B1):
    hub plus one entry per post. Every indexable URL lives here (R1)."""
    pages = [dict(p) for p in CORE_PAGES]
    pages += [
        {"path": f"/rentals/{item['slug']}.html", "lastmod": DEFAULT_LASTMOD}
        for item in CATALOG
    ]
    pages += [{"path": BLOG_PATH, "lastmod": BLOG_LASTMOD}]
    pages += [{"path": post_path(p), "lastmod": p.get("modified") or p["date"]} for p in published_posts()]
    pages += [{"path": GUIDES_PATH, "lastmod": GUIDES_LASTMOD}]
    pages += [{"path": guide_path(g), "lastmod": g["updated"]} for g in GUIDES]
    return pages

# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def offer_variant_name(variant):
    """Human label distinguishing multi-variant offers (slushie single/double)."""
    return f"{variant.capitalize()} day rental"

def nav_html(active=""):
    links = "\n".join(
        f'<li><a href="{href}">{html.escape(label)}</a></li>'
        for label, href in NAV_ITEMS
    )
    return f"""
<header class="site-header">
  <div class="nav-wrap">
    <a class="logo" href="/" aria-label="BlockParty — home">
      <img src="/images/wordmark-transparent.png" alt="BlockParty" width="2444" height="616">
    </a>
    <nav>
      <ul class="nav-links" id="navLinks">
        {links}
        <li><a class="nav-cta" href="mailto:{EMAIL}">Book a planning call</a></li>
      </ul>
    </nav>
    <button class="nav-toggle" id="navToggle" aria-label="Toggle menu">&#9776;</button>
  </div>
</header>
"""

def footer_html():
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="footer-wordmark" href="/" aria-label="BlockParty — home">
          <img src="/images/wordmark-transparent.png" alt="BlockParty" width="2444" height="616">
        </a>
        <p>{TAGLINE}. Brooklyn-based party-equipment rentals — we deliver, we pick up, and we call you first.</p>
        <p>Brooklyn only. <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="/rentals/">Packages &amp; Catalog</a></li>
          <li><a href="/blog/">The Block Party Playbook</a></li>
          <li><a href="/guides/">Block Party Guides</a></li>
          <li><a href="/how-it-works.html">How It Works</a></li>
          <li><a href="/about.html">Our Story</a></li>
          <li><a href="/faq.html">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4>Popular Rentals</h4>
        <ul>
          <li><a href="/rentals/cornhole-rental-brooklyn.html">Cornhole Rental</a></li>
          <li><a href="/rentals/slushie-machine-rental-brooklyn.html">Slushie Machine Rental</a></li>
          <li><a href="/rentals/ball-pit-rental-brooklyn.html">Ball Pit Rental</a></li>
        </ul>
      </div>
    </div>
    <p class="photo-credits">Photography: <a href="https://commons.wikimedia.org/wiki/File:BLOCK_PARTY_ON_EAST_35TH_STREET_BETWEEN_LEXINGTON_AND_MADISON_AVENUES._STREET_WAS_CLOSED_TO_MOTOR_TRAFFIC_AND_GIVEN..._-_NARA_-_551687.jpg">Block party on East 35th Street, NYC, 1973</a> by Suzanne Sz&aacute;sz, EPA DOCUMERICA, U.S. National Archives (public domain) &middot; <a href="https://unsplash.com/photos/houses-near-trees-RSILUMwabqc">Brownstone row</a> by Avi Werde (Unsplash) &middot; <a href="https://www.pexels.com/photo/vibrant-community-cornhole-game-outdoors-30388540/">Cornhole</a> &amp; <a href="https://www.pexels.com/photo/joyful-dance-party-in-sunlit-street-28424057/">street dance</a> photos via Pexels. Illustrations by BlockParty.</p>
    <div class="footer-bottom">
      <span>&copy; 2026 BlockParty. Brooklyn, NY.</span>
      <span>Rentals only — we don't sell equipment.</span>
    </div>
  </div>
</footer>
<script>
  var navToggle = document.getElementById('navToggle');
  var navLinks = document.getElementById('navLinks');
  if (navToggle) {{
    navToggle.addEventListener('click', function () {{
      navLinks.classList.toggle('open');
    }});
  }}
</script>
"""

def page(title, description, path, body, json_ld_objects=None, extra_head=""):
    canonical = DOMAIN + path
    ld_scripts = ""
    if json_ld_objects:
        for obj in json_ld_objects:
            ld_scripts += f'<script type="application/ld+json">{json.dumps(obj, indent=2)}</script>\n'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{OG_IMAGE_URL}">
<meta property="og:image:alt" content="{OG_IMAGE_ALT}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{OG_IMAGE_URL}">
<meta name="twitter:image:alt" content="{OG_IMAGE_ALT}">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon-64.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
{extra_head}
{ld_scripts}</head>
<body>
{nav_html()}
{body}
{footer_html()}
</body>
</html>
"""

def local_business_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": f"{DOMAIN}/#business",
        "name": "BlockParty",
        "description": "Brooklyn-based party-equipment rental company. We deliver and pick up cornhole, giant Jenga, giant/human-sized beer pong, slushie and frozen cocktail machines, portable basketball hoops, and ball pits for block parties and private events.",
        "url": DOMAIN,
        "email": EMAIL,
        # Brand assets emitted by the build (R8). logo is the square badge
        # raster; image is the 1200x630 social card. No NAP beyond what is
        # real: no telephone, openingHours, sameAs, or geo (locked decision).
        "logo": f"{DOMAIN}/apple-touch-icon.png",
        "image": OG_IMAGE_URL,
        "areaServed": {
            "@type": "City",
            "name": "Brooklyn, NY"
        },
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Brooklyn",
            "addressRegion": "NY",
            "addressCountry": "US"
        },
        "priceRange": "$65-$675",
        # Derived from PACKAGES so schema prices can never drift from the
        # prices the pages display (same rule as R9).
        "makesOffer": [
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": p["name"],
                    "description": p["subtitle"],
                },
                "price": str(p["price"]),
                "priceCurrency": "USD",
            }
            for p in PACKAGES
        ],
    }

def item_offers_jsonld(item):
    """Structured offers for a catalog item (R9).

    Prices come from the item's numeric `offers` data — never parsed from
    the display label, which can hold two prices (e.g. the slushie machine).
    """
    offers = []
    for o in item["offers"]:
        offer = {
            "@type": "Offer",
            "price": str(o["price"]),
            "priceCurrency": "USD",
        }
        if o.get("variant"):
            offer["name"] = offer_variant_name(o["variant"])
        offers.append(offer)
    return offers

def service_jsonld(item):
    page_url = f"{DOMAIN}/rentals/{item['slug']}.html"
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"{page_url}#service",
        "url": page_url,
        "serviceType": item["name"],
        "provider": {
            "@type": "LocalBusiness",
            "name": "BlockParty",
            "@id": f"{DOMAIN}/#business",
        },
        "areaServed": {
            "@type": "City",
            "name": "Brooklyn, NY"
        },
        "description": item["short"],
        "offers": item_offers_jsonld(item),
    }

def faqpage_jsonld(qa_pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a,
                },
            }
            for q, a in qa_pairs
        ],
    }

def website_jsonld():
    """WebSite node for the homepage (R10), joined to the business entity."""
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{DOMAIN}/#website",
        "url": f"{DOMAIN}/",
        "name": SITE_NAME,
        "publisher": {"@id": f"{DOMAIN}/#business"},
    }

def offer_catalog_jsonld():
    """OfferCatalog for the rentals index (R10): packages + à-la-carte items."""
    elements = [
        {
            "@type": "Offer",
            "itemOffered": {
                "@type": "Service",
                "name": p["name"],
                "description": p["subtitle"],
            },
            "price": str(p["price"]),
            "priceCurrency": "USD",
        }
        for p in PACKAGES
    ]
    for item in CATALOG:
        for o in item["offers"]:
            offer = {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": item["name"],
                    "url": f"{DOMAIN}/rentals/{item['slug']}.html",
                },
                "price": str(o["price"]),
                "priceCurrency": "USD",
            }
            if o.get("variant"):
                offer["name"] = offer_variant_name(o["variant"])
            elements.append(offer)
    return {
        "@context": "https://schema.org",
        "@type": "OfferCatalog",
        "@id": f"{DOMAIN}/rentals/#catalog",
        "name": "BlockParty Rentals & Packages",
        "url": f"{DOMAIN}/rentals/",
        "itemListElement": elements,
    }

def breadcrumb_jsonld(trail):
    """BreadcrumbList (R10). trail: (name, path) pairs from Home to this page."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": DOMAIN + path,
            }
            for i, (name, path) in enumerate(trail)
        ],
    }

def blog_author_jsonld(post):
    """Structural authorship for schema (B2/B3): human posts by Allie the
    Person; AI posts by a transparent Organization that says what it is and
    that a human reviews everything it publishes."""
    if post["stream"] == "human":
        return {
            "@type": "Person",
            "@id": f"{DOMAIN}/#allie-esslinger",
            "name": "Allie Esslinger",
            "jobTitle": "Founder",
        }
    return {
        "@type": "Organization",
        "@id": f"{DOMAIN}/blog/#trends-desk",
        "name": "BlockParty Trends Desk",
        "description": "The AI-written trends desk of The Block Party Playbook. Every post it publishes is reviewed and approved by Allie Esslinger before it ships.",
        "parentOrganization": {"@id": f"{DOMAIN}/#business"},
    }

def blogposting_jsonld(post):
    """BlogPosting node for a post page (B3): stable @id, absolute image
    URL, publish/modified dates, and the author per stream."""
    page_url = DOMAIN + post_path(post)
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": f"{page_url}#blogposting",
        "url": page_url,
        "headline": post["title"],
        "description": post["subhead"],
        "image": post_image_url(post),
        "datePublished": post["date"],
        "dateModified": post.get("modified") or post["date"],
        "author": blog_author_jsonld(post),
        "publisher": {"@id": f"{DOMAIN}/#business"},
        "isPartOf": {"@id": f"{DOMAIN}/blog/#blog"},
        "mainEntityOfPage": page_url,
    }

def blog_jsonld():
    """Blog node for the hub (B3), joined to the business entity."""
    return {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": f"{DOMAIN}/blog/#blog",
        "url": f"{DOMAIN}/blog/",
        "name": "The Block Party Playbook",
        "description": "The BlockParty blog: Allie Esslinger on block-party life, plus AI-written trend scans reviewed and approved by Allie before they ship.",
        "publisher": {"@id": f"{DOMAIN}/#business"},
    }

# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def build_home():
    packages_preview = "".join(
        f"""
        <a class="tile-link" href="/rentals/">
        <div class="tile">
          <h3>{p['name']}</h3>
          <p>{p['subtitle']}</p>
          <span class="price">{p['price_label']}</span>
        </div>
        </a>""" for p in PACKAGES
    )

    body = f"""
<section class="hero">
  <div class="container hero-inner">
    <div class="bunting">{''.join('<span></span>' for _ in range(11))}</div>
    <span class="hs hs-left" aria-hidden="true">{ICONS['sparkles']}</span>
    <span class="hs hs-right" aria-hidden="true">{ICONS['sparkles']}</span>
    <span class="eyebrow">Brooklyn Block Party Rentals</span>
    <h1>Your block's party. Our gear. Nobody's garage.</h1>
    <p class="hero-sub">Cornhole, a slushie machine, giant Jenga, a ball pit — whatever your street wants this year. We deliver it, we pick it up, and we call you first to lock down the details. Brooklyn only. Your source for Brooklyn block party fun.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="/rentals/">Browse rentals</a>
      <a class="btn btn-secondary" href="mailto:{EMAIL}">Book a planning call &mdash; {EMAIL}</a>
    </div>
  </div>
</section>

<section>
  <div class="container narrative">
    <p>Every block has that one person who ends up running the party. Permits, borrowed folding tables, a group chat nobody answers, a garage that's slowly turning into storage for games you used twice. By August it's not fun anymore &mdash; it's a second job.</p>
    <p>BlockParty started with a simple wish: block parties in Brooklyn should be exciting for the kids tearing around the hydrant spray and the parents trying to have one conversation that isn't about logistics. Not another thing to manage. A thing that just happens, and is good.</p>
    <div class="notice-arrow" aria-hidden="true">{ICONS['arrow_doodle']}</div>
    <div class="notice">
    <p>So here's the pitch: <strong>you don't need to purchase everything and store it for the year. Rent from us, and figure out what works for the people on your block. Let the party evolve with your neighbors. Try new stuff. Build traditions. Just don't be left figuring out what to do with the stuff all year.</strong></p>
    </div>
    <p>We're Brooklyn-based, we deliver and pick up everything ourselves, and before your date we get on the phone with you to make sure the truck shows up at the right time, to the right spot, with the right stuff. No self-service pickup, no guessing &mdash; just a straightforward way to make your block's day better. We're your source for Brooklyn block party fun.</p>
    <div class="section-links">
      <a href="/how-it-works.html">How It Works &rarr;</a>
      <a href="/rentals/">Browse Packages &amp; Rentals &rarr;</a>
    </div>
  </div>
</section>

<section class="photo-band">
  <div class="container">
    <div class="photo-strip">
      <figure class="photo-frame"><img src="/images/photo-brownstone-row.jpg" alt="Row of Brooklyn brownstones with stoops and street trees" width="1600" height="1067" loading="lazy"></figure>
      <figure class="photo-frame"><img src="/images/photo-cornhole-community.jpg" alt="Neighbors playing cornhole at an outdoor block gathering" width="1066" height="1600" loading="lazy"></figure>
      <figure class="photo-frame"><img src="/images/photo-street-dance.jpg" alt="Neighbors dancing at a sunny street party" width="1600" height="1600" loading="lazy"></figure>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head">
      <h2>Packages built for your block's size</h2>
      <p>Pick a package, or mix and match from the full catalog &mdash; either way, delivery, pickup, and a confirmation call are included.</p>
    </div>
    <div class="icon-grid">
      {packages_preview}
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <h2>How BlockParty works</h2>
    </div>
    <div class="steps">
      <div class="step">{icon('browse')}<h3>1. Browse</h3><p>Look through block-party packages or pick items individually: cornhole, giant Jenga, giant/human-sized beer pong, a slushie or frozen-cocktail machine, a portable basketball hoop, or a ball pit.</p></div>
      <div class="step">{icon('phone')}<h3>2. Book a confirmation call</h3><p>Every booking includes a short call with us before your event to confirm your delivery window, exact setup spot, and pickup time.</p></div>
      <div class="step">{icon('truck')}<h3>3. We deliver and pick up</h3><p>On the day, we bring everything to your block, set it up where you need it, and come back for pickup after your party.</p></div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="cta-band">
      <h2>Ready to plan your block's day?</h2>
      <p>Book at least 2 weeks ahead of your date. Email us and we'll set up your confirmation call.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/rentals/">Browse rentals</a>
        <a class="btn btn-secondary" href="mailto:{EMAIL}">Email {EMAIL}</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        title="BlockParty — Brooklyn Block Party & Backyard Party Rentals",
        description="Brooklyn-only party equipment rentals: cornhole, giant Jenga, giant beer pong, slushie machines, basketball hoops, and ball pits. We deliver, we pick up, and we call you first.",
        path="/",
        body=body,
        json_ld_objects=[local_business_jsonld(), website_jsonld()],
    )


def build_about():
    body = f"""
<section class="hero" style="padding-bottom:0;">
  <div class="container hero-inner" style="text-align:left; max-width:760px;">
    <span class="eyebrow">Our Story</span>
    <h1>Why BlockParty exists</h1>
  </div>
</section>
<section style="padding-top:12px;">
  <div class="container narrative">
    <p>Block party planning carries a quiet tax: emotional labor. Someone has to think of the games, source them, store them, set them up, break them down, and do it again next year &mdash; usually the same someone. That's the part we built BlockParty to take off the table.</p>
    <p>BlockParty is a Brooklyn equipment rental company built around one idea: the fun stuff &mdash; cornhole, giant Jenga, a slushie machine, a ball pit &mdash; shouldn't require a storage unit or a standing yearly commitment. Rent what your block wants this year. Skip it next year if the block's into something else. Nobody's obligated to keep a ball pit in their stairwell until next July.</p>
    <p>You don't need to purchase everything and store it for the year. Rent from us, and figure out what works for the people on your block. Let the party evolve with your neighbors. Try new stuff. Build traditions. Just don't be left figuring out what to do with the stuff all year.</p>
    <p>That's how we think good block-party traditions actually get built &mdash; not by locking in the same order every year because that's what's in the garage, but by neighbors trying things, keeping what works, and letting the party change as the block changes.</p>
    <p>We're a new company, and we're starting with a clear focus: we're your source for Brooklyn block party fun. No other boroughs, no padded r&eacute;sum&eacute; &mdash; just a straightforward rental model built for one neighborhood, starting now.</p>
    <figure class="photo-frame photo-archival">
      <img src="/images/photo-block-party-1973.jpg" alt="A New York street closed to traffic for a block party in June 1973, with sidewalk stalls and neighbors browsing" width="1600" height="1075" loading="lazy">
      <figcaption>East 35th Street, New York, June 1973 &mdash; photograph by Suzanne Sz&aacute;sz, EPA DOCUMERICA, U.S. National Archives (public domain).</figcaption>
    </figure>
  </div>
</section>
<section class="section-alt">
  <div class="container">
    <div class="section-head">
      <h2>What we do (and don't)</h2>
    </div>
    <div class="icon-grid">
      <div class="tile"><h3>Brooklyn only</h3><p>No other boroughs, no exceptions &mdash; it's how we can actually guarantee delivery windows.</p></div>
      <div class="tile"><h3>We deliver, we pick up</h3><p>You never load a van, drive anything, or store anything afterward.</p></div>
      <div class="tile"><h3>Every booking includes a confirmation call</h3><p>A real conversation about timing, placement, and logistics before the truck shows up &mdash; not a phone tree.</p></div>
      <div class="tile"><h3>Rentals, not sales</h3><p>We don't sell equipment. The whole model depends on you not having to own it.</p></div>
    </div>
  </div>
</section>
<section>
  <div class="container">
    <div class="cta-band">
      <h2>Let's plan your block's party</h2>
      <p>Reach out and we'll start with a short planning call.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="mailto:{EMAIL}">Email {EMAIL}</a>
        <a class="btn btn-secondary" href="/rentals/">Browse rentals</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        title="Our Story — BlockParty Brooklyn",
        description="Why BlockParty exists: a Brooklyn-only equipment rental company built so block parties don't require a storage unit or a yearly commitment. Delivery, pickup, and a confirmation call on every booking.",
        path="/about.html",
        body=body,
        json_ld_objects=[breadcrumb_jsonld([("Home", "/"), ("Our Story", "/about.html")])],
    )


def build_how_it_works():
    body = f"""
<section class="hero" style="padding-bottom:0;">
  <div class="container hero-inner" style="text-align:left; max-width:760px;">
    <span class="eyebrow">Process</span>
    <h1>How BlockParty works</h1>
    <p class="hero-sub" style="margin:0;">Three steps, no guesswork. Browse, book a call, and we handle the truck.</p>
  </div>
</section>
<section>
  <div class="container">
    <div class="steps">
      <div class="step">
        {icon('browse')}
        <div class="num">1</div>
        <h3>Browse</h3>
        <p>Look through block-party packages or pick items individually: cornhole, giant Jenga, giant/human-sized beer pong, a slushie or frozen-cocktail machine, a portable basketball hoop, or a ball pit.</p>
      </div>
      <div class="step">
        {icon('phone')}
        <div class="num">2</div>
        <h3>Book a confirmation call</h3>
        <p>Every booking includes a short call with us before your event. Reach us at <a href="mailto:{EMAIL}">{EMAIL}</a> to get started. We confirm your exact delivery window, where equipment sets up on your block (curb, sidewalk, or a specific spot), pickup time, and anything about your street that affects logistics &mdash; permit timing, closure hours, tight parking. Nothing gets left to guesswork.</p>
      </div>
      <div class="step">
        {icon('truck')}
        <div class="num">3</div>
        <h3>We deliver and pick up</h3>
        <p>On the day, we bring everything to your block, set it up where you need it, and come back for pickup after your party. You don't drive anything, store anything, or break anything down.</p>
      </div>
    </div>
  </div>
</section>
<section class="section-alt">
  <div class="container">
    <div class="cta-band">
      <h2>Book at least 2 weeks ahead</h2>
      <p>That gives us time to confirm delivery logistics and make sure your equipment is available.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/rentals/">Browse rentals</a>
        <a class="btn btn-secondary" href="mailto:{EMAIL}">Email {EMAIL}</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        title="How It Works — BlockParty Brooklyn Rentals",
        description="Browse rentals, book a confirmation call, and BlockParty delivers and picks up everything for your Brooklyn block party. No self-service pickup, no guesswork.",
        path="/how-it-works.html",
        body=body,
        json_ld_objects=[breadcrumb_jsonld([("Home", "/"), ("How It Works", "/how-it-works.html")])],
    )


def build_catalog_index():
    package_cards = ""
    for p in PACKAGES:
        includes_li = "".join(f"<li>{x}</li>" for x in p["includes"])
        badge = '<span class="badge">Most Popular</span>' if p["featured"] else ""
        featured_cls = " featured" if p["featured"] else ""
        package_cards += f"""
        <div class="package-card{featured_cls}">
          {badge}
          <h3>{p['name']}</h3>
          <div class="price">{p['price_label']}</div>
          <div class="group-size">{p['group_size']}</div>
          <p class="desc">{p['desc']}</p>
          <div class="includes">Includes:</div>
          <ul>{includes_li}</ul>
          <a class="btn btn-primary" href="mailto:{EMAIL}?subject=Booking%20{p['name'].replace(' ', '%20')}">Book this package</a>
        </div>"""

    catalog_items = ""
    for item in CATALOG:
        catalog_items += f"""
        <div class="catalog-item">
          {icon(item['icon'])}
          <div>
            <h3><a href="/rentals/{item['slug']}.html">{item['name']}</a></h3>
            <p>{item['short']} {item['who']}</p>
          </div>
          <div class="cta">
            <span class="price">{item['price_label']}</span>
            <a class="btn btn-secondary" href="/rentals/{item['slug']}.html">Details</a>
          </div>
        </div>"""

    body = f"""
<section class="hero" style="padding-bottom:0;">
  <div class="container hero-inner" style="text-align:left; max-width:820px;">
    <span class="eyebrow">Packages &amp; Catalog</span>
    <h1>Brooklyn block party rentals &amp; packages</h1>
    <p class="hero-sub" style="margin:0;">Bundle into a package for the best price per trip, or build your own order from the full catalog. Delivery, pickup, and a confirmation call are included either way.</p>
  </div>
</section>

<section style="padding-top:0;">
  <div class="container">
    <figure class="photo-frame photo-wide">
      <img src="/images/photo-brownstone-row.jpg" alt="Row of Brooklyn brownstones with stoops and street trees" width="1600" height="1067" loading="lazy">
    </figure>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <h2>Packages</h2>
    </div>
    <div class="packages-grid">
      {package_cards}
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head">
      <h2>&Agrave; la carte catalog</h2>
      <p>Each item below can be rented on its own or added to a package.</p>
    </div>
    <div class="minimum-note">
      <p><strong>Standalone single-item orders carry a $150 minimum order value</strong> (or a flat $75 delivery/pickup fee on items priced under $150) &mdash; this covers the cost of a dedicated Brooklyn delivery-and-pickup trip for one item. Ordering a package or combining items clears this automatically.</p>
    </div>
    <div class="catalog-list">
      {catalog_items}
    </div>
    <div class="not-offered">
      <strong>Not currently offered: Bounce houses.</strong> BlockParty's pricing research recommended against adding bounce houses for initial launch, mainly due to the insurance cost and liability profile of unattended inflatables. This is a final decision for v1.
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="cta-band">
      <h2>Ready to book?</h2>
      <p>Email us your date and we'll set up a confirmation call to lock in delivery.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="mailto:{EMAIL}">Email {EMAIL}</a>
        <a class="btn btn-secondary" href="/how-it-works.html">See how it works</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        title="Packages & Rentals — BlockParty Brooklyn",
        description="Classic ($185), Full ($420), and Deluxe ($675) Block Party packages, plus à la carte cornhole, giant Jenga, giant beer pong, slushie machines, a basketball hoop, and a ball pit. Brooklyn delivery and pickup included.",
        path="/rentals/",
        body=body,
        json_ld_objects=[
            breadcrumb_jsonld([("Home", "/"), ("Packages & Catalog", "/rentals/")]),
            offer_catalog_jsonld(),
        ],
    )


def build_item_page(item):
    facts_html = "".join(
        f'<div class="fact"><div class="label">{html.escape(label)}</div><div class="value">{html.escape(value)}</div></div>'
        for label, value in item["facts"]
    )
    # Items with approved brand art show it in the hero; the rest keep the
    # flat SVG icon (photo keys are optional by design).
    if item.get("photo"):
        hero_visual = (
            f'<img class="item-photo" src="{item["photo"]}" '
            f'alt="{html.escape(item["photo_alt"])}" '
            f'width="{item["photo_w"]}" height="{item["photo_h"]}">'
        )
        wrap_cls = "icon-wrap photo-wrap"
    else:
        hero_visual = ICONS[item["icon"]]
        wrap_cls = "icon-wrap"
    faq_html = "".join(
        f'<div class="faq-item"><h3>{html.escape(q)}</h3><p>{a}</p></div>'
        for q, a in item["item_faq"]
    )
    body = f"""
<section>
  <div class="container">
    <div class="breadcrumb"><a href="/rentals/">Packages &amp; Catalog</a> &rsaquo; {item['name']}</div>
    <div class="item-hero">
      <div>
        <h1>{item['name']}</h1>
        <p class="answer">{item['answer']}</p>
        <div class="item-facts">{facts_html}</div>
        <div class="btn-row">
          <a class="btn btn-primary" href="mailto:{EMAIL}?subject=Booking%20{item['name'].replace(' ', '%20')}">Book this rental</a>
          <a class="btn btn-secondary" href="/rentals/">Back to catalog</a>
        </div>
      </div>
      <div class="{wrap_cls}">{hero_visual}</div>
    </div>
  </div>
</section>
<section class="section-alt">
  <div class="container narrative">
    <h2>Details</h2>
    <p>{item['short']} {item['who']} {item['pairs']}</p>
  </div>
</section>
<section>
  <div class="container">
    <div class="section-head" style="text-align:left; margin-bottom:24px;">
      <h2>Frequently asked</h2>
    </div>
    <div class="faq-list">{faq_html}</div>
  </div>
</section>
"""
    return page(
        title=f"{item['name']} — BlockParty Brooklyn",
        description=item["answer"],
        path=f"/rentals/{item['slug']}.html",
        body=body,
        json_ld_objects=[
            breadcrumb_jsonld([
                ("Home", "/"),
                ("Packages & Catalog", "/rentals/"),
                (item["name"], f"/rentals/{item['slug']}.html"),
            ]),
            service_jsonld(item),
            faqpage_jsonld(item["item_faq"]),
        ],
    )


def build_faq():
    faq_html = "".join(
        f'<div class="faq-item"><h3>{html.escape(q)}</h3><p>{a}</p></div>'
        for q, a in FAQS
    )
    body = f"""
<section class="hero" style="padding-bottom:0;">
  <div class="container hero-inner" style="text-align:left; max-width:760px;">
    <span class="eyebrow">FAQ</span>
    <h1>Frequently asked questions</h1>
    <p class="hero-sub" style="margin:0;">Everything about delivery, booking, minimums, and permits for Brooklyn block parties.</p>
  </div>
</section>
<section>
  <div class="container">
    <div class="faq-list" style="max-width:820px; margin:0 auto;">
      {faq_html}
    </div>
  </div>
</section>
<section class="section-alt">
  <div class="container">
    <div class="cta-band">
      <h2>Still have a question?</h2>
      <p>Email us and we'll answer it on the confirmation call &mdash; or before you even book.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="mailto:{EMAIL}">Email {EMAIL}</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        title="FAQ — BlockParty Brooklyn Block Party Rentals",
        description="Answers on Brooklyn delivery, the confirmation call, booking lead time, order minimums, street permits, and what BlockParty does and doesn't rent.",
        path="/faq.html",
        body=body,
        json_ld_objects=[
            breadcrumb_jsonld([("Home", "/"), ("FAQ", "/faq.html")]),
            faqpage_jsonld(FAQS),
        ],
    )


def stream_badge(stream):
    """Stream badge shown on every blog card and post header (B2)."""
    label = "Allie" if stream == "human" else "AI"
    return f'<span class="blog-badge blog-badge-{stream}">{label}</span>'


def post_card_html(post, variant):
    """Card for the blog rows: date badge, title, stream badge, image background."""
    alt = html.escape(f"Cover art for the post {post['title']}")
    return f"""
      <a class="blog-card blog-card-{variant}" href="{post_path(post)}">
        <img class="blog-card-img" src="{post_image_path(post)}" alt="{alt}">
        <div class="blog-card-body">
          <div class="blog-card-meta">
            {stream_badge(post['stream'])}
            <span class="blog-date-badge">{format_date(post['date'])}</span>
          </div>
          <h3>{html.escape(post['title'])}</h3>
        </div>
      </a>"""


def feature_card_html(post):
    """Full-width feature card for a human post (hero and second feature)."""
    alt = html.escape(f"Cover art for the post {post['title']}")
    return f"""
      <a class="blog-feature" href="{post_path(post)}">
        <img class="blog-feature-img" src="{post_image_path(post)}" alt="{alt}">
        <div class="blog-feature-overlay">
          <div class="blog-card-meta">
            {stream_badge('human')}
            <span class="blog-date-badge">{format_date(post['date'])}</span>
          </div>
          <h2>{html.escape(post['title'])}</h2>
          <p>{html.escape(post['subhead'])}</p>
          <div class="blog-byline">By <strong>Allie Esslinger</strong>, Founder</div>
        </div>
      </a>"""


def build_blog_hub():
    """Hub at /blog/ per Allie's sketch: hero feature, Trends Desk row, a
    second Allie feature, and titled series rows (B1)."""
    posts = published_posts()
    human_posts = sorted(
        (p for p in posts if p["stream"] == "human"),
        key=lambda p: p["date"], reverse=True,
    )
    ai_posts = sorted(
        (p for p in posts if p["stream"] == "ai"),
        key=lambda p: p["date"], reverse=True,
    )

    # Sketch section 1: hero — the most recent Allie-written post.
    hero = feature_card_html(human_posts[0]) if human_posts else ""

    # Sketch section 2: The Trends Desk — scrollable row of AI-post cards.
    trends_cards = "".join(post_card_html(p, "trend") for p in ai_posts)
    trends_section = f"""
  <div class="container">
    <div class="section-head">
      <h2>The Trends Desk</h2>
      <p>AI-written scans of Brooklyn block-party trends &mdash; every post reviewed and approved by Allie Esslinger before it ships.</p>
    </div>
    <div class="blog-row" id="trendsRow">{trends_cards}</div>
    <div class="blog-row-nav">
      <button class="blog-nav-btn" id="trendsPrev" aria-label="Scroll the trends row back">&larr;</button>
      <button class="blog-nav-btn" id="trendsNext" aria-label="Scroll the trends row forward">&rarr;</button>
    </div>
  </div>"""

    # Sketch section 3: a second Allie-written feature. When only one human
    # post exists yet, render an honest coming-soon state instead of a card.
    if len(human_posts) > 1:
        second = feature_card_html(human_posts[1])
    else:
        second = """
      <div class="blog-soon">
        <h3>From the Stoop is on the way</h3>
        <p>Her next piece is being written &mdash; it lands here when it's ready.</p>
      </div>"""

    # Sketch section 4: titled series rows, built from post data. Standalone
    # series/tag index pages stay unmade until a series holds 3+ posts
    # (thin-page rule, B1) — the hub section itself is the only surface.
    groups = {}
    for post in published_posts():
        if post.get("series"):
            groups.setdefault(post["series"], []).append(post)
    series_rows = ""
    for (_key, label), series_posts in groups.items():
        cards = "".join(
            post_card_html(p, "tall")
            for p in sorted(series_posts, key=lambda p: p["date"], reverse=True)
        )
        series_rows += f"""
  <div class="blog-series">
    <div class="section-head"><h2>{html.escape(label)}</h2></div>
    <div class="blog-row">{cards}</div>
  </div>"""
    series_block = f'<section class="section-alt">{series_rows}</section>' if series_rows else ""

    body = f"""
<section class="hero" style="padding-bottom:32px;">
  <div class="container hero-inner">
    <div class="bunting">{''.join('<span></span>' for _ in range(11))}</div>
    <span class="eyebrow">The BlockParty Blog</span>
    <h1>The Block Party Playbook</h1>
    <p class="hero-sub">Field notes from Allie Esslinger on why block parties matter &mdash; plus trend scans from the AI desk she reviews before anything ships.</p>
    <img class="blog-hero-img" src="/blog/images/hub-hero.png" alt="Illustration of a Brooklyn block party outside cream and rust brownstones, with bunting flags overhead" width="1344" height="750">
  </div>
</section>

<section style="padding-top:12px;">
  <div class="container">
    {hero}
  </div>
</section>

<section class="section-alt">{trends_section}</section>

<section>
  <div class="container">
    <div class="section-head">
      <h2>From the Stoop</h2>
    </div>
    {second}
  </div>
</section>

{series_block}

<section>
  <div class="container">
    <figure class="photo-frame photo-archival">
      <img src="/images/photo-block-party-1973.jpg" alt="A New York street closed to traffic for a block party in June 1973, with sidewalk stalls and neighbors browsing" width="1600" height="1075" loading="lazy">
      <figcaption>East 35th Street, New York, June 1973 &mdash; photograph by Suzanne Sz&aacute;sz, EPA DOCUMERICA, U.S. National Archives (public domain).</figcaption>
    </figure>
  </div>
</section>

<script>
  (function () {{
    var row = document.getElementById('trendsRow');
    var prev = document.getElementById('trendsPrev');
    var next = document.getElementById('trendsNext');
    if (!row || !prev || !next) return;
    function stepSize() {{ return Math.max(Math.round(row.clientWidth * 0.8), 300); }}
    prev.addEventListener('click', function () {{ row.scrollBy({{ left: -stepSize(), behavior: 'smooth' }}); }});
    next.addEventListener('click', function () {{ row.scrollBy({{ left: stepSize(), behavior: 'smooth' }}); }});
    function updateArrows() {{
      var overflow = row.scrollWidth > row.clientWidth + 1;
      prev.style.display = overflow ? '' : 'none';
      next.style.display = overflow ? '' : 'none';
    }}
    updateArrows();
    window.addEventListener('resize', updateArrows);
  }})();
</script>
"""
    return page(
        title="The Block Party Playbook — The BlockParty Blog",
        description="The BlockParty blog: Allie Esslinger on why block parties matter, plus AI-written Brooklyn trend scans — reviewed and approved by Allie before they ship.",
        path=BLOG_PATH,
        body=body,
        json_ld_objects=[
            breadcrumb_jsonld([("Home", "/"), ("The Block Party Playbook", BLOG_PATH)]),
            blog_jsonld(),
        ],
    )


def render_post_body(post):
    """B4 body renderer: strings are paragraphs, ("h2"/"h3", text) are
    headings, ("html", raw) is a pre-built block (tables, lists). Unknown
    shapes fail the build loudly instead of flattening into prose."""
    out = []
    for block in post["body"]:
        if isinstance(block, str):
            out.append(f"<p>{block}</p>")
        elif isinstance(block, tuple) and len(block) == 2:
            kind, text = block
            if kind in ("h2", "h3"):
                out.append(f"<{kind}>{text}</{kind}>")
            elif kind == "html":
                out.append(text)
            else:
                raise ValueError(f"{post['slug']}: unknown body block kind {kind!r}")
        else:
            raise ValueError(f"{post['slug']}: bad body block {block!r}")
    return "".join(out)

def build_post_page(post):
    """Post template: structural, visible authorship (B2) with breadcrumbs (B3)."""
    paragraphs = render_post_body(post)
    draft_note = ""
    if not post.get("published", True):
        extra = post.get("note") or ""
        draft_note = (
            '<p class="blog-placeholder-note"><strong>Draft &mdash; not published.</strong> '
            "This post stays out of the live site until Allie reviews it and the "
            "published flag flips. "
            + (f"<em>{extra}</em>" if extra else "")
            + "</p>"
        )
    if post["stream"] == "human":
        byline = f'<div class="blog-byline">{stream_badge("human")} From the Stoop &middot; By <strong>Allie Esslinger</strong>, Founder</div>'
        disclosure = ""
    else:
        byline = f'<div class="blog-byline">{stream_badge("ai")} By <strong>BlockParty Trends Desk</strong></div>'
        disclosure = f'<p class="blog-disclosure">AI-written &middot; reviewed and approved by {post.get("reviewed_by") or "review pending"}</p>'

    body = f"""
<section class="hero" style="padding-bottom:0;">
  <div class="container hero-inner" style="text-align:left; max-width:820px;">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/blog/">The Block Party Playbook</a> &rsaquo; {html.escape(post['title'])}</div>
    {byline}
    <h1>{html.escape(post['title'])}</h1>
    <p class="hero-sub" style="margin:0;">{html.escape(post['subhead'])}</p>
    <div class="blog-post-meta"><span class="blog-date-badge">{format_date(post['date'])}</span></div>
    {disclosure}
  </div>
</section>
<section style="padding-top:24px;">
  <div class="container" style="max-width:820px;">
    <img class="blog-post-img" src="{post_image_path(post)}" alt="Cover art for the post {html.escape(post['title'])}">
  </div>
</section>
<section style="padding-top:12px;">
  <div class="container narrative">
    {draft_note}
    {paragraphs}
  </div>
</section>
<section class="section-alt">
  <div class="container">
    <div class="cta-band">
      <h2>Planning your block's party?</h2>
      <p>Browse the packages or the full catalog &mdash; delivery, pickup, and a confirmation call are included either way.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/rentals/">Browse rentals</a>
        <a class="btn btn-secondary" href="/blog/">&larr; Back to The Block Party Playbook</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        title=f"{post['title']} — The Block Party Playbook",
        description=post["subhead"],
        path=post_path(post),
        body=body,
        json_ld_objects=[
            breadcrumb_jsonld([
                ("Home", "/"),
                ("The Block Party Playbook", BLOG_PATH),
                (post["title"], post_path(post)),
            ]),
            blogposting_jsonld(post),
        ],
    )


def build_404():
    body = f"""
<section class="hero">
  <div class="container hero-inner">
    <span class="eyebrow">404</span>
    <h1>This block doesn't exist (yet).</h1>
    <p class="hero-sub">The page you're looking for moved or never existed. Try the catalog or head home.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="/">Back home</a>
      <a class="btn btn-secondary" href="/rentals/">Browse rentals</a>
    </div>
  </div>
</section>
"""
    return page(
        title="Page Not Found — BlockParty",
        description="This page could not be found.",
        path="/404.html",
        body=body,
    )

# ---------------------------------------------------------------------------
# Crawl artifacts — generated from the registry and site data (R1–R3).
# Nothing crawl-related stays hand-maintained: these render from the same
# data that renders the pages.
# ---------------------------------------------------------------------------

def sitemap_xml():
    """One <url> per indexable page with per-URL lastmod (R1).

    changefreq/priority are omitted — Google ignores them.
    """
    urls = "".join(
        f"  <url><loc>{DOMAIN}{p['path']}</loc><lastmod>{p['lastmod']}</lastmod></url>\n"
        for p in page_registry()
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n"
    )

# AI retrieval bots surface the site in answer engines; training bots are a
# separate, reversible visibility-first choice (locked for v1). Explicit
# per-bot entries document the policy even where the default already allows.
RETRIEVAL_BOTS = ["OAI-SearchBot", "PerplexityBot", "Claude-SearchBot"]
TRAINING_BOTS = ["GPTBot", "ClaudeBot", "CCBot", "Google-Extended"]

def robots_txt():
    """Explicit AI-crawler policy plus the sitemap pointer (R2)."""
    lines = ["User-agent: *", "Allow: /", ""]
    lines += ["# AI answer engines (retrieval) — allowed"]
    for bot in RETRIEVAL_BOTS:
        lines += [f"User-agent: {bot}", "Allow: /", ""]
    lines += ["# AI training crawlers — allowed (visibility-first; revisit any time)"]
    for bot in TRAINING_BOTS:
        lines += [f"User-agent: {bot}", "Allow: /", ""]
    lines += [f"Sitemap: {DOMAIN}/sitemap.xml", ""]
    return "\n".join(lines)

def llms_txt():
    """Curated Markdown for AI answer engines, generated from site data (R3)."""
    pkg_prices = " / ".join(
        f"{p['name'].replace(' Block Party Package', '')} {p['price_label']}"
        for p in PACKAGES
    )
    summary = (
        "BlockParty is a Brooklyn-only party equipment rental company: cornhole, giant Jenga, "
        "giant/human-sized beer pong, a slushie or frozen cocktail machine, a portable basketball "
        "hoop, and a ball pit — delivered to your block, set up, and picked up after the party, "
        "with a confirmation call included in every booking. Packages: "
        f"{pkg_prices}. À la carte rentals are also available; standalone single-item orders "
        "carry a $150 minimum order value. To book, email "
        f"{EMAIL} and we'll set up your confirmation call."
    )
    pages = [
        ("/", "Home", "Brooklyn block party and backyard party rentals — we deliver, we pick up, and we call you first."),
        ("/rentals/", "Packages & Rentals", "Every package and à la carte item, with prices."),
        ("/how-it-works.html", "How It Works", "Browse, book a confirmation call, and we deliver and pick up."),
        ("/about.html", "Our Story", "Why BlockParty exists."),
        ("/faq.html", "FAQ", "Delivery, booking lead time, order minimums, and street permits."),
    ]
    lines = [
        f"# {SITE_NAME}",
        "",
        f"> {summary}",
        "",
        "## Pages",
        "",
    ]
    lines += [f"- [{name}]({DOMAIN}{path}): {blurb}" for path, name, blurb in pages]
    # R11: llms.txt must reference the sitemap so answer engines can find the
    # machine-readable page index too.
    lines += ["", f"- [Sitemap]({DOMAIN}/sitemap.xml): machine-readable index of every page."]
    lines += ["", "## Rentals", ""]
    lines += [
        f"- [{item['name']}]({DOMAIN}/rentals/{item['slug']}.html): {item['short']} {item['price_label']}."
        for item in CATALOG
    ]
    lines += ["", "## Block Party Guides", ""]
    lines += [
        f"- [{g['title']}]({DOMAIN}{guide_path(g)}): {g['description']}"
        for g in GUIDES
    ]
    lines += ["", "## The Block Party Playbook (blog)", ""]
    lines += [
        f"- [The Block Party Playbook]({DOMAIN}/blog/): the BlockParty blog — Allie Esslinger's From the Stoop essays on block-party life, plus AI-written trend scans (every AI post is reviewed and approved by Allie before it ships)."
    ]
    lines += [
        f"- [{p['title']}]({DOMAIN}/blog/{p['slug']}.html): {p['subhead']}"
        + (
            " From the Stoop — by Allie Esslinger, Founder."
            if p["stream"] == "human"
            else f" AI-written, reviewed and approved by {p['reviewed_by']}."
        )
        for p in published_posts()
    ]
    lines.append("")
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Brand image assets (R4, R7)
# ---------------------------------------------------------------------------

BADGE_PATH = os.path.join(ROOT, "assets", "badge.png")
FAVICON_ASSET_DIR = os.path.join(ROOT, "assets", "brand")
CREAM = (247, 228, 193)  # #F7E4C1 — brand Cream
NAVY = (29, 35, 52)      # #1D2334 — brand Ink Navy
RUST = (172, 112, 68)    # #AC7044 — brand Brick Rust

def make_og_image(out_path):
    """Compose the 1200x630 social card: navy ground, script wordmark, tagline."""
    from PIL import Image, ImageDraw, ImageFont

    width, height = 1200, 630
    canvas = Image.new("RGB", (width, height), NAVY)

    badge = Image.open(BADGE_PATH).convert("RGBA")
    badge = badge.crop(badge.getbbox())  # trim any transparent padding
    badge_w = 1000
    badge_h = round(badge.height * badge_w / badge.width)
    badge = badge.resize((badge_w, badge_h), Image.LANCZOS)

    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 40
    )
    gap = 52
    top = (height - badge_h - gap - 44) // 2
    canvas.paste(badge, ((width - badge_w) // 2, top), badge)

    draw = ImageDraw.Draw(canvas)
    tagline_w = draw.textlength(TAGLINE, font=font)
    draw.text(((width - tagline_w) / 2, top + badge_h + gap), TAGLINE, font=font, fill=CREAM)

    canvas.save(out_path, "PNG")

# Approved favicon art: pre-cut brownstone-tile rasters from the brand kit
# (corners cut with transparency outside). Shipped as build inputs and copied
# verbatim so every machine — local or CI — emits byte-identical, art-approved
# favicons with no runtime resampling to drift between environments.
FAVICON_FILES = [
    # (source tile, rendered name)
    ("favicon-16.png", "favicon-16.png"),
    ("favicon-32.png", "favicon-32.png"),
    ("favicon-64.png", "favicon-64.png"),
    ("favicon-180.png", "apple-touch-icon.png"),  # iOS home-screen icon
    ("favicon-192.png", "favicon-192.png"),       # high-density / manifest use
    ("favicon-512.png", "favicon-512.png"),       # PWA-grade master
]

def make_favicons(dist_dir):
    """Emit the approved brand-tile favicons (16/32/64, apple-touch 180,
    192/512), replacing the placeholder favicon.svg pipeline (R7)."""
    for src_name, out_name in FAVICON_FILES:
        src = os.path.join(FAVICON_ASSET_DIR, src_name)
        if not os.path.isfile(src):
            # Fail loudly: a missing approved tile must stop the build, not
            # silently ship a stale or partial icon set.
            raise SystemExit(f"make_favicons: approved brand tile missing: {src}")
        shutil.copyfile(src, os.path.join(dist_dir, out_name))

def make_post_image(post, out_path):
    """Branded cover art for a post: stream-colored ground, bunting strip,
    centered badge. Titles stay in the HTML overlay (they double-read and
    crop badly inside card cutouts); placeholder posts get this generated
    art until real photography ships with the seed content (B4)."""
    from PIL import Image, ImageDraw

    width, height = 1600, 1000
    canvas = Image.new("RGB", (width, height), NAVY if post["stream"] == "human" else RUST)
    draw = ImageDraw.Draw(canvas)

    # Bunting along the top — the site's motif, in brand colors.
    flags = [(172, 112, 68), (203, 159, 92), (247, 228, 193), (105, 63, 53)]
    flag_w, flag_h, gap = 44, 54, 66
    for i in range(width // gap + 1):
        x = 16 + i * gap
        draw.polygon([(x, 0), (x + flag_w, 0), (x + flag_w // 2, flag_h)], fill=flags[i % 4])

    badge = Image.open(BADGE_PATH).convert("RGBA")
    badge = badge.crop(badge.getbbox())
    # 200px height leaves clear margins inside the narrowest card cutout
    # (a 3:4 tall card shows the central 750px of this 1600x1000 image;
    # a 200px badge is ~600px wide and clears both edges).
    badge_h = 200
    badge = badge.resize((round(badge.width * badge_h / badge.height), badge_h), Image.LANCZOS)
    canvas.paste(badge, ((width - badge.width) // 2, (height - badge_h) // 2), badge)

    canvas.save(out_path, "PNG")

def make_post_images(dist_dir):
    """Emit one cover image per post to dist/blog/images/, plus the hub hero.

    Generated brand art (B4) lives in assets/blog/<slug>.png and ships as-is;
    a post without a generated asset falls back to the programmatic art below,
    so the pipeline never breaks on a missing file. Draft posts still get
    their art emitted (unlinked), which keeps preview builds complete."""
    out_dir = os.path.join(dist_dir, "blog", "images")
    os.makedirs(out_dir, exist_ok=True)
    assets_dir = os.path.join(ROOT, "assets", "blog")
    hero = os.path.join(assets_dir, "hub-hero.png")
    if os.path.isfile(hero):
        shutil.copyfile(hero, os.path.join(out_dir, "hub-hero.png"))
    for post in POSTS:
        dest = os.path.join(out_dir, f"{post['slug']}.png")
        asset = os.path.join(assets_dir, f"{post['slug']}.png")
        if os.path.isfile(asset):
            shutil.copyfile(asset, dest)
        else:
            make_post_image(post, dest)

# Site imagery (brand pass): wordmark, page photography, and social-format
# art — approved assets shipped under assets/ and copied verbatim to dist/images/.
SITE_IMAGES = [
    ("brand", "wordmark-transparent.png"),
    ("social", "social-square-cornhole.png"),
    ("social", "social-wide-frozen-drinks.png"),
    ("photos", "photo-brownstone-row.jpg"),
    ("photos", "photo-cornhole-community.jpg"),
    ("photos", "photo-street-dance.jpg"),
    ("photos", "photo-block-party-1973.jpg"),
]

def make_site_images(dist_dir):
    out_dir = os.path.join(dist_dir, "images")
    os.makedirs(out_dir, exist_ok=True)
    for subdir, name in SITE_IMAGES:
        src = os.path.join(ROOT, "assets", subdir, name)
        if not os.path.isfile(src):
            raise SystemExit(f"make_site_images: missing site image: {src}")
        shutil.copyfile(src, os.path.join(out_dir, name))

# ---------------------------------------------------------------------------
# Write files
# ---------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(DIST, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # B2 publish gate first: an unreviewed AI post stops the build before
    # any output is written, so it can never render or deploy.
    check_publish_gate()
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST, exist_ok=True)

    write("index.html", build_home())
    write("about.html", build_about())
    write("how-it-works.html", build_how_it_works())
    write("faq.html", build_faq())
    write("404.html", build_404())
    write("rentals/index.html", build_catalog_index())
    for item in CATALOG:
        write(f"rentals/{item['slug']}.html", build_item_page(item))
    write("blog/index.html", build_blog_hub())
    for post in published_posts():
        write(f"blog/{post['slug']}.html", build_post_page(post))
    write("guides/index.html", build_guides_hub())
    for guide in GUIDES:
        write(f"guides/{guide['slug']}.html", build_guide_page(guide))

    shutil.copyfile(os.path.join(ROOT, "style.css"), os.path.join(DIST, "style.css"))
    shutil.copyfile(os.path.join(ROOT, "CNAME"), os.path.join(DIST, "CNAME"))

    write("sitemap.xml", sitemap_xml())
    write("robots.txt", robots_txt())
    write("llms.txt", llms_txt())
    make_og_image(os.path.join(DIST, "og-image.png"))
    make_favicons(DIST)
    make_post_images(DIST)
    make_site_images(DIST)

    print("Build complete ->", DIST)

if __name__ == "__main__":
    main()
