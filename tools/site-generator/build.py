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

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")

SITE_NAME = "BlockParty"
DOMAIN = "https://blockpartysupply.co"
EMAIL = "reserve@blockpartysupply.co"
TAGLINE = "Your Source for Brooklyn Block Party Fun"

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

PACKAGES = [
    {
        "name": "Classic Block Party Package",
        "price": "$185",
        "subtitle": "Cornhole, Giant Jenga, and Giant/Human-Sized Beer Pong, delivered and picked up in one trip.",
        "group_size": "~10–25 people",
        "desc": "For blocks of about 10–25 people who want a few solid lawn games without extra setup. One delivery run covers all three games, which is why the package runs below the combined à la carte price. Includes delivery, pickup, and a pre-event confirmation call.",
        "includes": ["Cornhole Set", "Giant Jenga", "Giant/Human-Sized Beer Pong"],
        "featured": False,
    },
    {
        "name": "Full Block Party Package",
        "price": "$420",
        "subtitle": "Everything in the Classic package, plus a single-flavor slushie or frozen-cocktail machine.",
        "group_size": "~25–50 people",
        "desc": "Built for bigger blocks (roughly 25–50 people) who want a drink station alongside the games. Includes delivery, pickup, and a pre-event confirmation call.",
        "includes": ["Cornhole Set", "Giant Jenga", "Giant/Human-Sized Beer Pong", "Single-Flavor Slushie Machine"],
        "featured": True,
    },
    {
        "name": "Deluxe Block Party Package",
        "price": "$675",
        "subtitle": "Everything in the Full package, plus a ball pit.",
        "group_size": "~40–75 people",
        "desc": "The flagship package for larger, family-heavy blocks (roughly 40–75 people). Like every other BlockParty rental, it's drop-off service — no on-site attendant required for any item in this package. Includes delivery, pickup, and a pre-event confirmation call.",
        "includes": ["Cornhole Set", "Giant Jenga", "Giant/Human-Sized Beer Pong", "Single-Flavor Slushie Machine", "Ball Pit"],
        "featured": False,
    },
]

# Each catalog item: slug drives /rentals/<slug>.html
CATALOG = [
    {
        "slug": "cornhole-rental-brooklyn",
        "icon": "cornhole",
        "name": "Cornhole Set Rental",
        "price_label": "$65/day bundled",
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
    ("How It Works", "/how-it-works.html"),
    ("About", "/about.html"),
    ("FAQ", "/faq.html"),
]

# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

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
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
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
        "makesOffer": [
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Classic Block Party Package",
                    "description": "Cornhole, Giant Jenga, and Giant/Human-Sized Beer Pong, delivered and picked up in one trip.",
                },
                "price": "185",
                "priceCurrency": "USD",
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Full Block Party Package",
                    "description": "Classic package plus a single-flavor slushie or frozen-cocktail machine.",
                },
                "price": "420",
                "priceCurrency": "USD",
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Deluxe Block Party Package",
                    "description": "Full package plus a ball pit.",
                },
                "price": "675",
                "priceCurrency": "USD",
            },
        ],
    }

def service_jsonld(item):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
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
        "offers": {
            "@type": "Offer",
            "price": item["price_label"].split("$")[1].split("/")[0] if "$" in item["price_label"] else None,
            "priceCurrency": "USD",
        },
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
          <span class="price">{p['price']}</span>
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
        json_ld_objects=[local_business_jsonld()],
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
          <div class="price">{p['price']}</div>
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
        json_ld_objects=[{
            "@context": "https://schema.org",
            "@type": "ItemList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "item": {
                        "@type": "Service",
                        "name": item["name"],
                        "url": f"{DOMAIN}/rentals/{item['slug']}.html",
                    },
                }
                for i, item in enumerate(CATALOG)
            ],
        }],
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
        json_ld_objects=[service_jsonld(item), faqpage_jsonld(item["item_faq"])],
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
        json_ld_objects=[faqpage_jsonld(FAQS)],
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
# Write files
# ---------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(DIST, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def main():
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

    shutil.copyfile(os.path.join(ROOT, "style.css"), os.path.join(DIST, "style.css"))
    shutil.copyfile(os.path.join(ROOT, "favicon.svg"), os.path.join(DIST, "favicon.svg"))
    shutil.copyfile(os.path.join(ROOT, "robots.txt"), os.path.join(DIST, "robots.txt"))
    shutil.copyfile(os.path.join(ROOT, "sitemap.xml"), os.path.join(DIST, "sitemap.xml"))
    shutil.copyfile(os.path.join(ROOT, "CNAME"), os.path.join(DIST, "CNAME"))

    print("Build complete ->", DIST)

if __name__ == "__main__":
    main()
