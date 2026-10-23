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
<rect x="10" y="55" width="55" height="32" rx="4" transform="rotate(-8 10 55)" fill="#F2B134" stroke="#1D2731" stroke-width="3"/>
<circle cx="38" cy="66" r="7" fill="#1D2731"/>
<rect x="55" y="45" width="40" height="26" rx="4" transform="rotate(-8 55 45)" fill="#E4572E" stroke="#1D2731" stroke-width="3"/>
<circle cx="18" cy="30" r="9" fill="#157A72"/>
<circle cx="35" cy="20" r="9" fill="#157A72"/>
</svg>""",
    "jenga": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="30" y="10" width="40" height="14" rx="2" fill="#F2B134" stroke="#1D2731" stroke-width="3"/>
<rect x="30" y="26" width="40" height="14" rx="2" fill="#E4572E" stroke="#1D2731" stroke-width="3"/>
<rect x="30" y="42" width="40" height="14" rx="2" fill="#157A72" stroke="#1D2731" stroke-width="3"/>
<rect x="30" y="58" width="40" height="14" rx="2" fill="#F2B134" stroke="#1D2731" stroke-width="3"/>
<rect x="20" y="74" width="60" height="14" rx="2" fill="#E4572E" stroke="#1D2731" stroke-width="3"/>
</svg>""",
    "beerpong": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M22 35 L30 85 L70 85 L78 35 Z" fill="#F2B134" stroke="#1D2731" stroke-width="3"/>
<ellipse cx="50" cy="35" rx="28" ry="8" fill="#FFF8EC" stroke="#1D2731" stroke-width="3"/>
<circle cx="50" cy="18" r="9" fill="#E4572E" stroke="#1D2731" stroke-width="3"/>
</svg>""",
    "slushie": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="25" y="15" width="50" height="34" rx="6" fill="#FFF8EC" stroke="#1D2731" stroke-width="3"/>
<path d="M30 49 L50 85 L70 49 Z" fill="#157A72" stroke="#1D2731" stroke-width="3"/>
<rect x="43" y="22" width="14" height="20" fill="#E4572E"/>
<circle cx="50" cy="12" r="4" fill="#1D2731"/>
</svg>""",
    "basketball": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="42" r="26" fill="#E4572E" stroke="#1D2731" stroke-width="3"/>
<path d="M50 16 V68 M26 42 H74 M32 24 Q50 42 32 60 M68 24 Q50 42 68 60" stroke="#1D2731" stroke-width="2.5" fill="none"/>
<rect x="42" y="68" width="16" height="22" fill="#157A72" stroke="#1D2731" stroke-width="3"/>
</svg>""",
    "ballpit": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<ellipse cx="50" cy="78" rx="42" ry="12" fill="none" stroke="#1D2731" stroke-width="3"/>
<circle cx="30" cy="55" r="10" fill="#E4572E" stroke="#1D2731" stroke-width="2.5"/>
<circle cx="50" cy="45" r="10" fill="#F2B134" stroke="#1D2731" stroke-width="2.5"/>
<circle cx="70" cy="55" r="10" fill="#157A72" stroke="#1D2731" stroke-width="2.5"/>
<circle cx="40" cy="68" r="10" fill="#157A72" stroke="#1D2731" stroke-width="2.5"/>
<circle cx="62" cy="68" r="10" fill="#E4572E" stroke="#1D2731" stroke-width="2.5"/>
</svg>""",
    "truck": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="10" y="35" width="50" height="30" rx="3" fill="#F2B134" stroke="#1D2731" stroke-width="3"/>
<path d="M60 45 H82 L90 60 V65 H60 Z" fill="#157A72" stroke="#1D2731" stroke-width="3"/>
<circle cx="28" cy="70" r="8" fill="#1D2731"/>
<circle cx="76" cy="70" r="8" fill="#1D2731"/>
</svg>""",
    "phone": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="32" y="12" width="36" height="76" rx="8" fill="#FFF8EC" stroke="#1D2731" stroke-width="3"/>
<path d="M40 70 Q50 60 60 70 Q65 75 60 82 Q50 90 40 82 Q35 75 40 70 Z" fill="#E4572E"/>
<circle cx="50" cy="26" r="3" fill="#1D2731"/>
</svg>""",
    "browse": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="42" cy="42" r="26" fill="none" stroke="#1D2731" stroke-width="4"/>
<line x1="61" y1="61" x2="86" y2="86" stroke="#1D2731" stroke-width="5" stroke-linecap="round"/>
<circle cx="42" cy="42" r="12" fill="#F2B134"/>
</svg>""",
    "calendar": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="14" y="22" width="72" height="64" rx="6" fill="#FFF8EC" stroke="#1D2731" stroke-width="3"/>
<rect x="14" y="22" width="72" height="18" fill="#E4572E"/>
<line x1="30" y1="14" x2="30" y2="30" stroke="#1D2731" stroke-width="4" stroke-linecap="round"/>
<line x1="70" y1="14" x2="70" y2="30" stroke="#1D2731" stroke-width="4" stroke-linecap="round"/>
<circle cx="34" cy="58" r="5" fill="#157A72"/>
<circle cx="50" cy="58" r="5" fill="#157A72"/>
<circle cx="66" cy="58" r="5" fill="#F2B134"/>
</svg>""",
    "house": """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 48 L50 16 L88 48" stroke="#1D2731" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="24" y="48" width="52" height="38" fill="#F2B134" stroke="#1D2731" stroke-width="3"/>
<rect x="44" y="62" width="12" height="24" fill="#E4572E"/>
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
# Blog — Allie Intelligence (B1–B4)
# Two authorship streams: "human" posts are written by Allie; "ai" posts are
# written by the Allie Intelligence desk and ship only with a named human
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
        "stream": "human",  # "human" (Allie) or "ai" (Allie Intelligence)
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
        "modified": None,
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
            "The permit closes your street; it doesn't furnish it. The games, the tables, the <a href=\"/rentals/slushie-machine-rental-brooklyn.html\">slushie machine</a> — that part is ours to deliver, set up, and pick up, and <a href=\"/faq.html\">the permit itself stays the organizer's responsibility</a>. File the paperwork, then tell us what the block wants on it — <a href=\"/rentals/\">the full catalog is one trip away</a>.",
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
    pages += [{"path": post_path(p), "lastmod": p["date"]} for p in published_posts()]
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
    <a class="logo" href="/">Block<span class="dot">Party</span></a>
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
        <div class="footer-brand">BlockParty</div>
        <p>{TAGLINE}. Brooklyn-based party-equipment rentals — we deliver, we pick up, and we call you first.</p>
        <p>Brooklyn only. <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="/rentals/">Packages &amp; Catalog</a></li>
          <li><a href="/blog/">Allie Intelligence</a></li>
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
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
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
        "@id": f"{DOMAIN}/blog/#allie-intelligence",
        "name": "Allie Intelligence",
        "description": "The AI-written trends desk of the BlockParty blog. Every post it publishes is reviewed and approved by Allie Esslinger before it ships.",
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
        "name": "Allie Intelligence",
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
    <p>So here's the pitch: <strong>you don't need to purchase everything and store it for the year. Rent from us, and figure out what works for the people on your block. Let the party evolve with your neighbors. Try new stuff. Build traditions. Just don't be left figuring out what to do with the stuff all year.</strong></p>
    <p>We're Brooklyn-based, we deliver and pick up everything ourselves, and before your date we get on the phone with you to make sure the truck shows up at the right time, to the right spot, with the right stuff. No self-service pickup, no guessing &mdash; just a straightforward way to make your block's day better. We're your source for Brooklyn block party fun.</p>
    <div class="section-links">
      <a href="/how-it-works.html">How It Works &rarr;</a>
      <a href="/rentals/">Browse Packages &amp; Rentals &rarr;</a>
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
      <div class="icon-wrap">{ICONS[item['icon']]}</div>
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
        <h3>More from Allie is on the way</h3>
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
    <h1>Allie Intelligence</h1>
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
      <h2>More from Allie</h2>
    </div>
    {second}
  </div>
</section>

{series_block}

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
        title="Allie Intelligence — The BlockParty Blog",
        description="The BlockParty blog: Allie Esslinger on why block parties matter, plus AI-written Brooklyn trend scans — reviewed and approved by Allie before they ship.",
        path=BLOG_PATH,
        body=body,
        json_ld_objects=[
            breadcrumb_jsonld([("Home", "/"), ("Allie Intelligence", BLOG_PATH)]),
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
        byline = f'<div class="blog-byline">{stream_badge("human")} By <strong>Allie Esslinger</strong>, Founder</div>'
        disclosure = ""
    else:
        byline = f'<div class="blog-byline">{stream_badge("ai")} By <strong>Allie Intelligence</strong></div>'
        disclosure = f'<p class="blog-disclosure">AI-written &middot; reviewed and approved by {post.get("reviewed_by") or "review pending"}</p>'

    body = f"""
<section class="hero" style="padding-bottom:0;">
  <div class="container hero-inner" style="text-align:left; max-width:820px;">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/blog/">Allie Intelligence</a> &rsaquo; {html.escape(post['title'])}</div>
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
        <a class="btn btn-secondary" href="/blog/">&larr; Back to Allie Intelligence</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(
        title=f"{post['title']} — Allie Intelligence",
        description=post["subhead"],
        path=post_path(post),
        body=body,
        json_ld_objects=[
            breadcrumb_jsonld([
                ("Home", "/"),
                ("Allie Intelligence", BLOG_PATH),
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
    lines += ["", "## Allie Intelligence (blog)", ""]
    lines += [
        f"- [Allie Intelligence]({DOMAIN}/blog/): the BlockParty blog — Allie Esslinger on block-party life, plus AI-written trend scans (every AI post is reviewed and approved by Allie before it ships)."
    ]
    lines += [
        f"- [{p['title']}]({DOMAIN}/blog/{p['slug']}.html): {p['subhead']}"
        + (
            " By Allie Esslinger, Founder."
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
CREAM = (255, 248, 236)   # #FFF8EC — site cream
NAVY = (29, 39, 49)       # #1D2731 — site navy
RUST = (228, 87, 46)      # #E4572E — site rust

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

def make_favicons(dist_dir):
    """Rasterize favicon.svg to PNG fallbacks: 32/16 + apple-touch 180 (R7)."""
    sizes = [(32, "favicon-32.png"), (16, "favicon-16.png"), (180, "apple-touch-icon.png")]
    try:
        import cairosvg
    except (ImportError, OSError):
        # Documented fallback: derive the PNGs from the badge raster with PIL.
        # OSError covers cairosvg present but its native cairo lib missing.
        from PIL import Image
        badge = Image.open(BADGE_PATH).convert("RGBA")
        side = min(badge.size)
        square = badge.crop((
            (badge.width - side) // 2,
            (badge.height - side) // 2,
            (badge.width + side) // 2,
            (badge.height + side) // 2,
        ))
        for size, name in sizes:
            square.resize((size, size), Image.LANCZOS).save(os.path.join(dist_dir, name), "PNG")
        return
    svg = os.path.join(ROOT, "favicon.svg")
    for size, name in sizes:
        cairosvg.svg2png(
            url=svg,
            write_to=os.path.join(dist_dir, name),
            output_width=size,
            output_height=size,
        )

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
    flags = [(228, 87, 46), (242, 177, 52), (255, 248, 236), (21, 122, 114)]
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

    shutil.copyfile(os.path.join(ROOT, "style.css"), os.path.join(DIST, "style.css"))
    shutil.copyfile(os.path.join(ROOT, "favicon.svg"), os.path.join(DIST, "favicon.svg"))
    shutil.copyfile(os.path.join(ROOT, "CNAME"), os.path.join(DIST, "CNAME"))

    write("sitemap.xml", sitemap_xml())
    write("robots.txt", robots_txt())
    write("llms.txt", llms_txt())
    make_og_image(os.path.join(DIST, "og-image.png"))
    make_favicons(DIST)
    make_post_images(DIST)

    print("Build complete ->", DIST)

if __name__ == "__main__":
    main()
