#!/usr/bin/env python3
"""
BlockParty build validator (R11).

Checks the generated site in dist/ — the artifacts crawlers and AI engines
actually consume — and exits non-zero on any failure, listing every problem,
so a broken tree cannot merge (R12 gates CI on this script).

Checks:
  1. Per-page head: exactly one rel=canonical (absolute HTTPS, matching the
     page's own URL and the sitemap); single <title> and meta description with
     length warnings; og:image + twitter:image present and absolute (with
     alts, summary_large_image card, and the image file itself resolvable);
     fonts.gstatic.com preconnect present.
  2. Every application/ld+json block parses as JSON with @context/@type.
  3. sitemap.xml: one URL per built indexable page in BOTH directions,
     unique, absolute HTTPS on the canonical host, ISO lastmod.
  4. Every internal href/src on every built page resolves to a built file.
  5. robots.txt and llms.txt exist at the dist root and reference the sitemap.

Standalone by design: it validates the emitted artifacts rather than the
generator source, so drift between the two is caught instead of inherited.
Constants below must track build.py.
"""
import html as html_lib
import json
import os
import posixpath
import re
import sys
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")

DOMAIN = "https://blockpartysupply.co"
SITEMAP_NAME = "sitemap.xml"
SITEMAP_URL = f"{DOMAIN}/{SITEMAP_NAME}"

# 404.html is a built utility page: served but never indexed, so it is
# deliberately absent from the sitemap. It still gets every head/link check.
NON_INDEXABLE = {"404.html"}

TITLE_MAX = 60
DESCRIPTION_MAX = 160

OUR_HOSTS = {"blockpartysupply.co", "www.blockpartysupply.co"}
SKIP_SCHEMES = {"mailto", "tel", "data", "javascript"}

FAILURES = []
WARNINGS = []


def fail(check, where, msg):
    FAILURES.append(f"[{check}] {where}: {msg}")


def warn(check, where, msg):
    WARNINGS.append(f"[{check}] {where}: {msg}")


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

ATTR_RE = re.compile(r'([a-zA-Z_:][-\w:.]*)\s*=\s*"([^"]*)"')
LD_SCRIPT_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.S | re.I,
)
HREF_RE = re.compile(r'''\shref\s*=\s*["\']([^"\']+)["\']''', re.I)
SRC_RE = re.compile(r'''\ssrc\s*=\s*["\']([^"\']+)["\']''', re.I)
ISO_LASTMOD_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?)?$"
)


def parse_tags(page_html, tag):
    """All <tag ...> occurrences as (raw, attribute-dict) pairs."""
    out = []
    for m in re.finditer(rf"<{tag}\b([^>]*)/?>", page_html, re.I):
        out.append((m.group(0), dict(ATTR_RE.findall(m.group(1)))))
    return out


def file_to_site_path(rel_file):
    """dist-relative file -> site path (rentals/index.html -> /rentals/)."""
    p = "/" + rel_file
    if p.endswith("/index.html"):
        return p[: -len("index.html")]
    return p


def site_path_to_file(site_path):
    """Site path -> expected dist-relative file (/rentals/ -> rentals/index.html)."""
    path = site_path.split("#", 1)[0].split("?", 1)[0]
    if not path or path == "/":
        return "index.html"
    if path.endswith("/"):
        return path.lstrip("/") + "index.html"
    return path.lstrip("/")


def internal_target(ref, page_dir):
    """dist-relative file an internal ref points at, or None to skip.

    Internal = root-relative, page-relative, or an absolute URL on the
    canonical host. Fragments, queries-only, mailto/tel/data, and foreign
    hosts are skipped.
    """
    parts = urlsplit(ref)
    scheme = parts.scheme.lower()
    if parts.scheme:
        if scheme in SKIP_SCHEMES:
            return None
        if scheme not in ("http", "https"):
            return None
        if parts.netloc.lower() not in OUR_HOSTS:
            return None
        path = parts.path
    elif parts.netloc:  # protocol-relative URL to a foreign host
        return None
    else:
        path = parts.path

    if not path:  # pure fragment or query-only ref
        return None
    if not path.startswith("/"):
        path = posixpath.normpath(posixpath.join(page_dir, path))
    return site_path_to_file(path)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_head(rel_file, page_html, sitemap_urls):
    """Head completeness for one built page. sitemap_urls of None means the
    sitemap itself failed to load — skip membership checks to avoid cascades."""
    site_path = file_to_site_path(rel_file)
    indexable = rel_file not in NON_INDEXABLE
    page_url = DOMAIN + site_path

    canonicals = [
        attrs
        for _raw, attrs in parse_tags(page_html, "link")
        if attrs.get("rel", "").lower() == "canonical"
    ]
    if len(canonicals) != 1:
        fail("head.canonical", rel_file,
             f"expected exactly 1 rel=canonical link, found {len(canonicals)}")
    else:
        href = canonicals[0].get("href", "")
        if not href.startswith("https://"):
            fail("head.canonical", rel_file, f"canonical is not absolute HTTPS: {href!r}")
        else:
            if href != page_url:
                fail("head.canonical", rel_file,
                     f"canonical {href!r} does not match the page's own URL {page_url!r}")
            if indexable and sitemap_urls is not None and href not in sitemap_urls:
                fail("head.canonical", rel_file,
                     f"canonical {href!r} is not listed in sitemap.xml")

    titles = re.findall(r"<title>(.*?)</title>", page_html, re.S | re.I)
    if len(titles) != 1:
        fail("head.title", rel_file, f"expected exactly 1 <title>, found {len(titles)}")
    else:
        text = html_lib.unescape(titles[0]).strip()
        if not text:
            fail("head.title", rel_file, "empty <title>")
        elif len(text) > TITLE_MAX:
            warn("head.title", rel_file,
                 f"title is {len(text)} chars (target <= {TITLE_MAX}): {text!r}")

    descriptions = [
        attrs.get("content", "")
        for _raw, attrs in parse_tags(page_html, "meta")
        if attrs.get("name", "").lower() == "description"
    ]
    if len(descriptions) != 1:
        fail("head.description", rel_file,
             f"expected exactly 1 meta description, found {len(descriptions)}")
    else:
        text = html_lib.unescape(descriptions[0]).strip()
        if not text:
            fail("head.description", rel_file, "empty meta description")
        elif len(text) > DESCRIPTION_MAX:
            warn("head.description", rel_file,
                 f"description is {len(text)} chars (target <= {DESCRIPTION_MAX})")

    metas = parse_tags(page_html, "meta")

    def meta_content(key):
        return [
            attrs.get("content", "")
            for _raw, attrs in metas
            if attrs.get("property") == key or attrs.get("name") == key
        ]

    def check_image(key, alt_key, check):
        contents = meta_content(key)
        if len(contents) != 1:
            fail(check, rel_file,
                 f"expected exactly 1 <meta {key}>, found {len(contents)}")
            return
        url = contents[0]
        if not url.startswith("https://"):
            fail(check, rel_file, f"{key} is not absolute HTTPS: {url!r}")
            return
        parts = urlsplit(url)
        if parts.netloc.lower() in OUR_HOSTS:
            target = site_path_to_file(parts.path)
            if not os.path.isfile(os.path.join(DIST, target)):
                fail(check, rel_file,
                     f"{key} target does not exist in dist: {parts.path!r}")
        if not meta_content(alt_key):
            fail(check, rel_file, f"missing <meta {alt_key}>")

    check_image("og:image", "og:image:alt", "head.og_image")
    check_image("twitter:image", "twitter:image:alt", "head.twitter")

    cards = meta_content("twitter:card")
    if len(cards) != 1 or cards[0] != "summary_large_image":
        fail("head.twitter", rel_file,
             f"twitter:card must be summary_large_image, found {cards!r}")

    preconnects = [
        (raw, attrs)
        for raw, attrs in parse_tags(page_html, "link")
        if attrs.get("rel", "").lower() == "preconnect"
    ]
    if not any(
        attrs.get("href") == "https://fonts.gstatic.com" and "crossorigin" in raw
        for raw, attrs in preconnects
    ):
        fail("head.preconnect", rel_file,
             "missing <link rel=preconnect href=\"https://fonts.gstatic.com\" crossorigin>")


def check_jsonld(rel_file, page_html):
    """Every ld+json block must be valid JSON with @context and @type."""
    count = 0
    for i, m in enumerate(LD_SCRIPT_RE.finditer(page_html), start=1):
        count += 1
        where = f"JSON-LD block #{i}"
        try:
            obj = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            fail("jsonld", rel_file, f"{where} is not valid JSON ({e.msg} at line {e.lineno})")
            continue
        if not isinstance(obj, dict):
            fail("jsonld", rel_file, f"{where} is not a JSON object")
            continue
        missing = [k for k in ("@context", "@type") if not obj.get(k)]
        if missing:
            fail("jsonld", rel_file, f"{where} is missing {', '.join(missing)}")
    return count


def check_links(rel_file, page_html):
    """Every internal href/src on the page must resolve to a built file."""
    page_dir = posixpath.dirname(rel_file)
    refs = [(m.group(1), "href") for m in HREF_RE.finditer(page_html)]
    refs += [(m.group(1), "src") for m in SRC_RE.finditer(page_html)]
    resolved = 0
    seen = set()
    for ref, kind in refs:
        if (ref, kind) in seen:
            continue
        seen.add((ref, kind))
        target = internal_target(ref, page_dir)
        if target is None:
            continue
        resolved += 1
        if not os.path.isfile(os.path.join(DIST, target)):
            fail("links", rel_file,
                 f"internal {kind}={ref!r} does not resolve to a built file "
                 f"(expected {target!r})")
    return resolved


def check_sitemap(built_urls):
    """sitemap.xml must mirror the built indexable pages in both directions."""
    path = os.path.join(DIST, SITEMAP_NAME)
    if not os.path.isfile(path):
        fail("sitemap", SITEMAP_NAME, "missing at dist root — build.py did not emit it")
        return None
    with open(path, encoding="utf-8") as f:
        content = f.read()

    entries = []
    seen_urls = set()
    for i, block in enumerate(re.findall(r"<url>(.*?)</url>", content, re.S), start=1):
        loc = re.search(r"<loc>(.*?)</loc>", block)
        lastmod = re.search(r"<lastmod>(.*?)</lastmod>", block)
        if not loc:
            fail("sitemap", SITEMAP_NAME, f"entry #{i} has no <loc>")
            continue
        url = loc.group(1).strip()
        if not url.startswith(f"{DOMAIN}/") or not url.startswith("https://"):
            fail("sitemap", SITEMAP_NAME,
                 f"{url!r} is not an absolute HTTPS URL on {DOMAIN}")
        elif url in seen_urls:
            fail("sitemap", SITEMAP_NAME, f"duplicate <loc>: {url!r}")
        seen_urls.add(url)
        mod = lastmod.group(1).strip() if lastmod else ""
        if not mod or not ISO_LASTMOD_RE.match(mod):
            fail("sitemap", SITEMAP_NAME,
                 f"{url or f'entry #{i}'}: lastmod {mod!r} is not an ISO 8601 date")
        entries.append(url)

    sitemap_urls = set(entries)
    for url in sorted(sitemap_urls - built_urls):
        fail("sitemap", SITEMAP_NAME,
             f"orphan URL {url!r} — sitemap lists it but no built page emits it")
    for url in sorted(built_urls - sitemap_urls):
        fail("sitemap", SITEMAP_NAME,
             f"built indexable page {url!r} is missing from the sitemap")
    return sitemap_urls


def check_root_artifacts():
    """robots.txt and llms.txt must exist at the dist root and point at the sitemap."""
    robots = os.path.join(DIST, "robots.txt")
    if not os.path.isfile(robots):
        fail("root.artifacts", "robots.txt", "missing at dist root")
    else:
        with open(robots, encoding="utf-8") as f:
            content = f.read()
        if not re.search(rf"(?mi)^\s*Sitemap:\s*{re.escape(SITEMAP_URL)}\s*$", content):
            fail("root.artifacts", "robots.txt",
                 f"does not reference the sitemap (expected a 'Sitemap: {SITEMAP_URL}' line)")

    llms = os.path.join(DIST, "llms.txt")
    if not os.path.isfile(llms):
        fail("root.artifacts", "llms.txt", "missing at dist root")
    else:
        with open(llms, encoding="utf-8") as f:
            content = f.read()
        if SITEMAP_URL not in content:
            fail("root.artifacts", "llms.txt",
                 f"does not reference the sitemap ({SITEMAP_URL})")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def built_pages():
    pages = []
    for dirpath, _dirs, filenames in os.walk(DIST):
        for fn in filenames:
            if fn.endswith(".html"):
                full = os.path.join(dirpath, fn)
                pages.append(os.path.relpath(full, DIST).replace(os.sep, "/"))
    return sorted(pages)


def report(stats):
    for w in WARNINGS:
        print(f"WARNING {w}")
    if FAILURES:
        print(f"\n{len(FAILURES)} failure(s):")
        for f in FAILURES:
            print(f"FAIL {f}")
        return 1
    print(
        f"\nOK: {stats['pages']} pages ({stats['indexable']} indexable), "
        f"{stats['jsonld']} JSON-LD blocks, {stats['sitemap_urls']} sitemap URLs, "
        f"{stats['refs']} internal refs resolved — all checks passed."
    )
    return 0


def main():
    if not os.path.isdir(DIST):
        FAILURES.append("[build] dist/: not found — run build.py first")
        return report({})
    pages = built_pages()
    if not pages:
        FAILURES.append("[build] dist/: no HTML pages found")
        return report({})

    # Sitemap first: head checks cross-reference its URL set.
    indexable = [p for p in pages if p not in NON_INDEXABLE]
    built_urls = {DOMAIN + file_to_site_path(p) for p in indexable}
    sitemap_urls = check_sitemap(built_urls)

    jsonld_count = 0
    ref_count = 0
    for rel in pages:
        with open(os.path.join(DIST, rel), encoding="utf-8") as f:
            page_html = f.read()
        check_head(rel, page_html, sitemap_urls)
        jsonld_count += check_jsonld(rel, page_html)
        ref_count += check_links(rel, page_html)
    check_root_artifacts()

    return report({
        "pages": len(pages),
        "indexable": len(indexable),
        "jsonld": jsonld_count,
        "sitemap_urls": len(sitemap_urls) if sitemap_urls is not None else 0,
        "refs": ref_count,
    })


if __name__ == "__main__":
    sys.exit(main())
