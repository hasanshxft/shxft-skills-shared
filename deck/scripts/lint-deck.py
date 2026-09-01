#!/usr/bin/env python3
"""
Deck linter — catches AI-template tells and rule violations before delivery.

Usage:
    python3 lint-deck.py /path/to/index.html
    python3 lint-deck.py /path/to/index.html --strict   # exits 1 on warnings too

Checks:
    1. Banned filler words (leverage, elevate, seamlessly, unlock, craft, ...)
    2. Banned vibe-coded phrases (scroll-stopping, level up, next-level, ...)
    3. Em dashes / en dashes / double-dashes in client-facing copy
    4. "Kiosk" used in client-facing context (FRXME is a display, never a kiosk)
    5. Decorative emoji on stat/data tiles (functional emoji on journey/step lists are fine)
    6. Generic AI-template tells (placeholder logos, lorem ipsum, fake stat formats)
    7. Meta-tag content (<title>, og:*, twitter:*) — banned words + em dashes
       (these ship in WhatsApp/iMessage/LinkedIn previews, invisible to body checks)

The linter inspects only client-visible copy: <script> and <style> blocks are stripped.
"""

import re
import sys
from pathlib import Path

BANNED_FILLER = [
    "leverage", "elevate", "seamlessly", "unlock", "craft",
    "tapestry", "landscape", "harness", "ecosystem",
]
BANNED_VIBE = [
    "scroll-stopping", "share-worthy", "built to convert", "level up",
    "next-level", "reimagine", "redefine", "revolutionize",
    "supercharge", "built with intention", "designed with care",
    "game-changer", "game-changing", "master it", "built for impact",
    "sound familiar", "where x becomes y",
]
# "transform" / "immersive" only flagged when not in obvious AR/VR context
SOFT_FLAGS = ["transform", "immersive"]
# "kiosk" hard-banned for FRXME
HARD_BAN = ["kiosk"]

# Decorative emoji that show up on stat tiles and read AI-generic
DECORATIVE_EMOJI_CONTEXT = [
    "tile-icon", "stat-icon", "data-icon", "metric-icon",
]

EMOJI_RANGES = (
    (0x1F600, 0x1F64F), (0x1F300, 0x1F5FF), (0x1F680, 0x1F6FF),
    (0x1F700, 0x1F77F), (0x1F780, 0x1F7FF), (0x1F800, 0x1F8FF),
    (0x1F900, 0x1F9FF), (0x1FA00, 0x1FA6F), (0x1FA70, 0x1FAFF),
    (0x2600, 0x26FF), (0x2700, 0x27BF),
)

PLACEHOLDER_TELLS = [
    "lorem ipsum", "your brand here", "client logo here",
    "[client]", "[brand]", "tbd", "todo:", "fixme",
]

# Known Lucide source paths — copy-pasted Lucide icons in inline SVG. These
# became an AI tell in 2024-25 because every shadcn/v0 template ships them.
# Match a snippet of each path's `d=` attribute.
LUCIDE_PATH_TELLS = {
    "M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z": "eye",
    "M23 19a2 2 0 0[01]-2 2H3a2 2 0 0[01]-2-2V8": "camera",
    "M12 2L2 7l10 5 10-5-10-5z": "layers",
    "M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10": "globe",
    "M12 22s8-4 8-10V5l-8-3-8 3v7": "shield",
    "M21 12a9 9 0 0[01]-9 9m9-9a9 9 0 00-9-9": "refresh-cw",
    "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8": "file-text",
    "M6 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2": "user",
    "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2": "users",
    "M8 14s1.5 2 4 2 4-2 4-2": "smile",
}


def is_emoji(c: str) -> bool:
    cp = ord(c)
    return any(lo <= cp <= hi for lo, hi in EMOJI_RANGES)


def strip_html(html: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text)
    return text


def visible_text(html: str) -> str:
    """Return only the text users will read (no tags, no script/style)."""
    text = strip_html(html)
    return re.sub(r"<[^>]+>", " ", text)


def extract_meta_text(html: str) -> dict[str, str]:
    """
    Extract text content from <title>, <meta name=description>, og:*, twitter:*
    These ship to clients via WhatsApp / iMessage / LinkedIn link previews and
    search snippets — they're invisible to body-text checks but very visible
    to anyone who sees the deck shared. Per memory rule
    feedback_linter_meta_tag_blindspot.md: meta tags need their own scan.

    Returns dict {tag-label: text-content} for use in violation messages.
    """
    out = {}
    title_m = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
    if title_m:
        out["<title>"] = title_m.group(1).strip()
    for m in re.finditer(
        r'<meta\s+(?:name|property)="([^"]+)"\s+content="([^"]*)"',
        html, re.IGNORECASE,
    ):
        name = m.group(1)
        content = m.group(2).strip()
        if not content:
            continue
        # Only scan TEXT-bearing meta tags, not URLs / dimensions / image refs
        if name.lower() in {
            "description", "keywords", "author", "twitter:title",
            "twitter:description", "og:title", "og:description",
            "og:site_name", "twitter:site", "application-name",
        }:
            out[f'<meta {name}>'] = content
    return out


def find_banned(text: str, words: list[str]) -> dict[str, int]:
    found = {}
    for word in words:
        # Word boundary so "elevate" doesn't match "elevated platform" parts
        pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            found[word] = len(matches)
    return found


def find_duplicate_section_labels(html: str) -> list[tuple[str, str]]:
    """
    Find slides where the data-title attribute is rendered as a corner label
    (via ::after { content: attr(data-title); }) AND the same section heading
    appears as an in-content <span class*="mono-label*">. The duplicated text
    reads as broken hierarchy.

    Detection strategy:
    1. Confirm the deck CSS includes `content: attr(data-title)` rendering.
    2. For each <section ... data-title="X" ...>, check whether any element with
       a class containing "mono-label" or "section-label" inside that section
       has text content that case-insensitively matches X.

    Returns list of (slide_id_or_index, label_text) tuples flagged.
    """
    flagged = []
    has_corner_render = bool(re.search(r"content:\s*attr\(data-title\)", html))
    if not has_corner_render:
        return flagged

    # Iterate sections with data-title attribute
    section_pattern = re.compile(
        r'<section\b[^>]*?\bdata-title="([^"]+)"[^>]*?>(.*?)</section>',
        re.DOTALL | re.IGNORECASE,
    )
    label_pattern = re.compile(
        r'<(?:span|div|p|h[1-6])[^>]*class="[^"]*(?:mono-label|section-label)[^"]*"[^>]*>'
        r'\s*\[?\s*([^<\[\]]+?)\s*\]?\s*</',
        re.IGNORECASE,
    )
    for m in section_pattern.finditer(html):
        data_title = m.group(1).strip()
        body = m.group(2)
        # Find an id for the slide if any (for clearer error)
        section_open = m.group(0)[: m.group(0).find(">") + 1]
        id_match = re.search(r'\bid="([^"]+)"', section_open)
        slide_id = id_match.group(1) if id_match else "(no-id)"
        for lab in label_pattern.finditer(body):
            label_text = lab.group(1).strip()
            if not label_text:
                continue
            # Case- and bracket-insensitive equality
            norm_a = re.sub(r"[^a-z0-9 ]", "", data_title.lower()).strip()
            norm_b = re.sub(r"[^a-z0-9 ]", "", label_text.lower()).strip()
            if norm_a and norm_a == norm_b:
                flagged.append((slide_id, data_title))
                break  # one flag per slide is enough
    return flagged


def find_ai_tell_card_patterns(html: str) -> list[str]:
    """
    Detect known AI-template card patterns. Today's pattern: a card with
    `border-left: Npx solid var(--brand)` PLUS a numbered tile inside
    (`<div class*="...num*">01</div>` etc). The combo reads as v0/Cursor.

    Returns a list of human-readable warnings.
    """
    warnings = []

    # Pattern A: brand-coloured left bar + numbered tile inside the card class
    # We look for a CSS rule that combines a card class name with both the
    # left border and a child element with "num" in its class.
    # Heuristic: any rule that defines `.X` { ... border-left: Npx solid var(--brand)... }
    # AND another rule `.X .Y-num` or `.X .X-num` exists in the same stylesheet.
    border_rule = re.compile(
        r"\.([a-z][a-z0-9_-]*)\s*\{[^}]*border-left:\s*\d+px\s+solid\s+var\(--brand[^)]*\)[^}]*\}",
        re.IGNORECASE,
    )
    matched_classes = {m.group(1) for m in border_rule.finditer(html)}
    for cls in matched_classes:
        # Check whether the same class hosts a numbered tile child
        num_child = re.compile(
            r"\."
            + re.escape(cls)
            + r"\s+\.[a-z0-9_-]*num[a-z0-9_-]*\s*\{",
            re.IGNORECASE,
        )
        if num_child.search(html):
            warnings.append(
                f"AI CARD PATTERN: '.{cls}' has a brand-coloured left border AND a numbered tile child — "
                "v0/Cursor signature. Lose the bar, let typography carry the hierarchy."
            )

    return warnings


def find_decorative_emoji(html: str) -> list[tuple[str, str]]:
    """
    Find emoji used inside elements with class names that suggest decorative
    icon use (tile-icon, stat-icon, etc). These read as generic AI-template.

    Returns list of (emoji_char, surrounding_class_context).
    """
    flagged = []
    # Match: class="...DECORATIVE_EMOJI_CONTEXT..."> ... emoji ... <
    # Be lenient — just look for tile-icon-like spans containing emoji
    for ctx in DECORATIVE_EMOJI_CONTEXT:
        # Match opening tag with class containing ctx, then capture content up to closing tag
        pattern = re.compile(
            r'<(?:span|div|i)[^>]*class="[^"]*' + re.escape(ctx) + r'[^"]*"[^>]*>([^<]+)<',
            re.IGNORECASE,
        )
        for m in pattern.finditer(html):
            content = m.group(1).strip()
            # Decode common HTML entities to detect emoji
            decoded = content
            decoded = re.sub(
                r"&#(\d+);",
                lambda x: chr(int(x.group(1))),
                decoded,
            )
            decoded = re.sub(
                r"&#x([0-9a-fA-F]+);",
                lambda x: chr(int(x.group(1), 16)),
                decoded,
            )
            for char in decoded:
                if is_emoji(char):
                    flagged.append((char, ctx))
                    break
    return flagged


def count_overrides(html: str, word: str) -> int:
    """
    Count per-word override comments. Authors can suppress a specific banned-word
    flag for a deliberate, context-appropriate usage by placing this comment
    anywhere in the HTML:

        <!-- linter:allow-word:WORD -->

    Each override comment subtracts 1 from the flagged count for that word.
    If the override count >= the flag count, no error fires.

    This is a deliberate-override mechanism, not a wholesale exemption. The
    override must be documented inline so future readers see why the usage
    survived the linter.
    """
    # Comment opens with `<!-- linter:allow-word:WORD`, optionally followed by
    # an inline note (e.g. "(Hasan-approved 2026-05-12: 'craft' is fine here)"),
    # then closes with `-->`. Word boundary prevents `craft` from matching
    # `craftsmanship` etc.
    pattern = re.compile(
        r"<!--\s*linter:allow-word:" + re.escape(word) + r"\b[\s\S]*?-->",
        re.IGNORECASE,
    )
    return len(pattern.findall(html))


def apply_overrides(html: str, found: dict[str, int]) -> dict[str, int]:
    """
    Subtract per-word overrides from a find_banned() result dict. Returns a
    dict of words that still have positive counts after overrides are applied.
    """
    out = {}
    for word, count in found.items():
        override = count_overrides(html, word)
        effective = count - override
        if effective > 0:
            out[word] = effective
    return out


def lint(html_path: Path, strict: bool = False) -> int:
    if not html_path.exists():
        print(f"[error] File not found: {html_path}")
        return 2

    html = html_path.read_text(encoding="utf-8")
    text = visible_text(html)

    errors = []
    warnings = []

    # 1. Hard-banned terms (kiosk)
    hb = apply_overrides(html, find_banned(text, HARD_BAN))
    if hb:
        for w, c in hb.items():
            errors.append(f"HARD BAN: '{w}' appears {c}x — never use 'kiosk' in client-facing copy. Use 'FRXME display' or 'interactive display'.")

    # 2. Banned filler words
    bf = apply_overrides(html, find_banned(text, BANNED_FILLER))
    if bf:
        for w, c in bf.items():
            errors.append(f"AI FILLER: '{w}' appears {c}x — agency-speak / generic. Rewrite or remove.")

    # 3. Banned vibe-coded phrases
    bv = apply_overrides(html, find_banned(text, BANNED_VIBE))
    if bv:
        for w, c in bv.items():
            errors.append(f"VIBE-CODED: '{w}' appears {c}x — instant AI tell. Rewrite.")

    # 4. Em dash / en dash / double-dash in visible text
    em = text.count("—")
    en = text.count("–")
    dd = text.count("--")
    if em:
        errors.append(f"EM DASH: — appears {em}x in visible copy — banned. Use period, comma, colon, or restructure.")
    if en:
        errors.append(f"EN DASH: – appears {en}x — banned. Use period, comma, or colon.")
    if dd:
        warnings.append(f"DOUBLE-DASH: '--' appears {dd}x — usually a typo for em dash. Check.")

    # 5. Soft flags (transform / immersive) — only warn
    sf = find_banned(text, SOFT_FLAGS)
    if sf:
        for w, c in sf.items():
            warnings.append(f"SOFT FLAG: '{w}' appears {c}x — fine if literal AR/VR, otherwise rewrite.")

    # 6. Decorative emoji on stat/data tiles
    de = find_decorative_emoji(html)
    if de:
        chars = ", ".join(set(c for c, _ in de))
        contexts = ", ".join(set(ctx for _, ctx in de))
        warnings.append(
            f"DECORATIVE EMOJI: {len(de)} emoji ({chars}) on stat/data tiles ({contexts}) — "
            f"reads as AI-template. Replace with custom monoline SVGs in brand color. "
            f"(Functional emoji on journey/step lists are fine.)"
        )

    # 7. Placeholder tells
    placeholders = find_banned(text, PLACEHOLDER_TELLS)
    if placeholders:
        for w, c in placeholders.items():
            errors.append(f"PLACEHOLDER LEFT: '{w}' appears {c}x — replace with real content.")

    # 8. Lucide icon library use — error (library is the strongest AI tell)
    if re.search(r'(?:src|href)="[^"]*lucide(?:\.min)?\.js', html, re.IGNORECASE):
        errors.append("LUCIDE LIBRARY: Lucide CDN/script reference — pure AI-template tell. Replace with custom inline SVG icons in brand color.")
    if re.search(r'data-lucide=', html):
        errors.append("LUCIDE LIBRARY: data-lucide attributes — reads as AI-template. Replace with custom inline SVG icons.")
    if re.search(r'lucide\.(?:createIcons|icons)\b', html):
        errors.append("LUCIDE LIBRARY: lucide.createIcons() / lucide.icons — replace with custom inline SVG icons.")

    # 9. Lucide source paths copy-pasted into inline SVG — warning per match
    lucide_hits = []
    for path_re, name in LUCIDE_PATH_TELLS.items():
        if re.search(path_re, html):
            lucide_hits.append(name)
    if lucide_hits:
        names = ", ".join(lucide_hits)
        warnings.append(
            f"LUCIDE PATH SVGs: {len(lucide_hits)} known Lucide icon path(s) inline ({names}) — "
            f"the visual signature reads as v0/Cursor/AI-built. Replace with custom hand-drawn SVG in brand accent."
        )

    # 10a. Duplicate section labels (data-title corner render + in-content mono-label)
    dup_labels = find_duplicate_section_labels(html)
    if dup_labels:
        for slide_id, label in dup_labels:
            errors.append(
                f"DUPLICATE LABEL: slide '{slide_id}' renders '{label}' twice — "
                f"once as data-title corner label and once as in-content mono-label. "
                f"Remove the data-title corner render OR change the in-content label."
            )

    # 10b. Known AI-tell card patterns (brand left-bar + numbered tile)
    card_warnings = find_ai_tell_card_patterns(html)
    for w in card_warnings:
        warnings.append(w)

    # 11. OG image + favicon — MUST exist as actual files in deck folder.
    # WhatsApp / iMessage / LinkedIn link previews break silently without them.
    deck_dir = html_path.parent

    # Find og:image meta and confirm the referenced file exists locally
    og_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html, re.IGNORECASE)
    if og_match:
        og_url = og_match.group(1)
        # Extract filename (last segment of URL path)
        og_filename = og_url.rstrip("/").split("/")[-1]
        og_path = deck_dir / og_filename
        if not og_path.exists():
            errors.append(
                f"OG IMAGE MISSING: meta tag references '{og_filename}' but file not found in {deck_dir.name}/. "
                f"WhatsApp / iMessage / LinkedIn link previews will be broken. Generate the OG image (1200x630 PNG) before delivery."
            )
    else:
        # No og:image at all — block
        errors.append(
            "OG IMAGE META MISSING: no <meta property=\"og:image\"> tag found. "
            "Required for WhatsApp / iMessage / LinkedIn link previews. Add the full OG meta block."
        )

    # Find favicon link and confirm file exists
    fav_match = re.search(r'<link\s+rel="(?:icon|shortcut icon)"[^>]*href="([^"]+)"', html, re.IGNORECASE)
    if fav_match:
        fav_url = fav_match.group(1)
        # Skip if external URL (data: or http://)
        if not fav_url.startswith(("data:", "http://", "https://")):
            fav_filename = fav_url.lstrip("/").split("/")[-1]
            fav_path = deck_dir / fav_filename
            assets_fav_path = deck_dir / "assets" / fav_filename
            actual_path = fav_path if fav_path.exists() else (assets_fav_path if assets_fav_path.exists() else None)
            if not actual_path:
                warnings.append(
                    f"FAVICON MISSING: meta tag references '{fav_filename}' but file not found in {deck_dir.name}/. "
                    f"Browser tab will show the default Cloudflare/Vercel favicon."
                )
            else:
                # CANONICAL SHXFT FAVICON BYTE-CHECK for proposal.shxft.studio decks.
                # Every SHXFT proposal must use the canonical favicon (37,950 bytes,
                # ~/Documents/CLAUDE PROJECTS/SHXFT DECKS/SHXFT_Favicon.png) unless
                # explicitly opted out via <!-- linter:allow-custom-favicon -->.
                # See feedback_shxft_favicon_consistency.md.
                deck_str = str(deck_dir.resolve())
                is_shxft_proposal = "/PROPOSALS/SHXFT/" in deck_str
                opt_out = bool(re.search(r"linter:allow-custom-favicon", html))
                CANONICAL_BYTES = 37950
                if is_shxft_proposal and not opt_out:
                    actual_size = actual_path.stat().st_size
                    if actual_size != CANONICAL_BYTES:
                        errors.append(
                            f"NON-CANONICAL FAVICON: '{fav_filename}' is {actual_size} bytes; "
                            f"canonical SHXFT favicon is {CANONICAL_BYTES} bytes. "
                            f"All proposal.shxft.studio decks must use the canonical favicon. "
                            f"Run: cp ~/Documents/CLAUDE\\ PROJECTS/SHXFT\\ DECKS/SHXFT_Favicon.png "
                            f"{deck_dir}/favicon.png — or add <!-- linter:allow-custom-favicon --> "
                            f"and document the brand reason."
                        )
    else:
        warnings.append(
            "FAVICON META MISSING: no <link rel=\"icon\"> tag. Browser tab gets the default favicon."
        )

    # 12. Meta-tag text content scan (per feedback_linter_meta_tag_blindspot.md).
    # <title>, <meta name=description>, og:*, twitter:* ship to clients via
    # WhatsApp / iMessage / LinkedIn link previews and search snippets — they
    # bypass the body-text checks above. Run the same banned-word + em-dash +
    # banned-phrase rules against them.
    meta_text_map = extract_meta_text(html)
    for tag_label, content in meta_text_map.items():
        # Hard ban (kiosk)
        for w, c in find_banned(content, HARD_BAN).items():
            errors.append(
                f"META {tag_label}: HARD BAN '{w}' in '{content}' — never use 'kiosk' in client-facing copy."
            )
        # Banned filler
        for w, c in find_banned(content, BANNED_FILLER).items():
            errors.append(
                f"META {tag_label}: AI FILLER '{w}' in '{content}' — agency-speak, rewrite."
            )
        # Banned vibe-coded phrases
        for w, c in find_banned(content, BANNED_VIBE).items():
            errors.append(
                f"META {tag_label}: VIBE-CODED '{w}' in '{content}' — instant AI tell, rewrite."
            )
        # Em / en / double dash
        if "—" in content:
            errors.append(
                f"META {tag_label}: EM DASH in '{content}' — banned. Use middot, period, colon, or restructure. "
                f"(Ships in WhatsApp/iMessage/LinkedIn previews.)"
            )
        if "–" in content:
            errors.append(
                f"META {tag_label}: EN DASH in '{content}' — banned. Use period, comma, or colon."
            )
        if "--" in content:
            warnings.append(
                f"META {tag_label}: DOUBLE-DASH in '{content}' — usually a typo for em dash."
            )
        # Soft flags (warn only)
        for w, c in find_banned(content, SOFT_FLAGS).items():
            warnings.append(
                f"META {tag_label}: SOFT FLAG '{w}' in '{content}' — fine if literal AR/VR, otherwise rewrite."
            )

    # Output
    if errors:
        print(f"\n✗ {len(errors)} ERROR(S):")
        for e in errors:
            print(f"  ✗ {e}")
    if warnings:
        print(f"\n⚠  {len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"  ⚠  {w}")

    if not errors and not warnings:
        print("✓ Clean. No banned words, em dashes, kiosk, or decorative emoji.")
        return 0

    if errors:
        print(f"\n✗ Deck has {len(errors)} blocking issue(s). Fix before delivery.")
        return 1

    if strict and warnings:
        print(f"\n⚠  Strict mode: {len(warnings)} warning(s) treated as failures.")
        return 1

    print(f"\n⚠  {len(warnings)} warning(s). Review before delivery.")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 lint-deck.py /path/to/index.html [--strict]")
        sys.exit(2)
    strict = "--strict" in args
    paths = [a for a in args if not a.startswith("--")]
    rc = 0
    for path_str in paths:
        path = Path(path_str)
        print(f"\n=== Linting {path.name} ===")
        rc = max(rc, lint(path, strict=strict))
    sys.exit(rc)
