#!/usr/bin/env python3
"""
lint-copy.py — the CNQR/SHXFT copy linter.

Reads text/HTML/markdown and flags:
  1. HARD BANS (exit 1) — lexical, structural, formatting from ai-tells-hard-bans.md
  2. SOFT FLAGS (exit 0 with warnings) — patterns from ai-tells-soft-flags.md that read AI in aggregate

Usage:
  python3 lint-copy.py path/to/file.html
  python3 lint-copy.py path/to/file.md
  echo "some text" | python3 lint-copy.py -

Called by:
  - /copy skill (standalone lint)
  - /deck skill (extends lint-deck.py at push time)
  - /cs skill (foundation drafting sanity check)

Exit codes:
  0 = clean or soft-flags-only
  1 = hard bans present
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple

# ─── HARD BANS ────────────────────────────────────────────────────────────

# Lexical filler / puff words (case-insensitive, word boundary)
HARD_BAN_WORDS = [
    "unlock", "elevate", "leverage", "seamless", "seamlessly",
    "empower", "empowerment", "harness", "tapestry",
    "revolutionize", "revolutionary", "supercharge", "turbocharge",
    "curate", "curated", "foster", "embark", "delve",
    "robust", "cutting-edge", "best-in-class", "holistic",
    "synergy", "synergies",
    "industry-leading", "premium quality", "end-to-end",
    "thought leadership", "paradigm shift",
    "game-changer", "game-changing",
    "disrupt", "disruption", "disruptive",
    "circle back", "at the end of the day", "that being said",
    "needless to say", "simply put",
    "passionate about",
]

# Context-dependent words permitted in narrow cases (linter flags them but they can be overridden)
CONTEXT_DEPENDENT_WORDS = [
    "transform", "transformation",  # permitted for literal XR/AR/body-tracking
    "journey",                       # permitted for literal physical journeys
    "landscape",                     # near-universally puff
    "solutions",                     # near-universally puff
    "navigate",                      # near-universally puff
    "in short",
]

# Banned openers (start of paragraph or sentence)
HARD_BAN_OPENERS = [
    r"^\s*Introducing\b",
    r"^\s*Discover\b",
    r"^\s*Experience the\b",
    r"^\s*Welcome to a new era\b",
    r"^\s*In today's\b.{0,30}landscape",
    r"^\s*In a world where\b",
    r"^\s*Picture this\b",
    r"^\s*Imagine this\b",
    r"^\s*Ever notice how\b",
    r"^\s*Sound familiar\b",
    r"^\s*Let's dive\b",
    r"^\s*Now imagine\b",
    r"^\s*Simply put,",
    r"^\s*That being said,",
    r"^\s*Whether you're\b.{0,80}or",
    r"^\s*When it comes to\b",
    r"^\s*Ultimately,",
    r"^\s*Additionally,",
    r"^\s*Moreover,",
    r"^\s*Furthermore,",
]

# Banned closers / rhetorical devices
HARD_BAN_CLOSERS = [
    r"\bThe result\?",
    r"\bThe takeaway\?",
    r"\bThe bottom line\?",
    r"\bSound familiar\?",
    r"\bEnter [A-Z][a-zA-Z]+\.",
    r"is here to change all that\b",
    r"\bBut here's the thing\b",
    r"\bThat's where .{2,40} comes in\b",
]

# Em-dashes and en-dashes
DASH_BANS = [
    ("—", "em-dash (—)"),
    ("–", "en-dash (–)"),
]

# Structural bans (regex-based)
STRUCTURAL_BANS = [
    (
        r";\s*(however|moreover|therefore|furthermore|additionally)\b",
        "adverbial-semicolon coupling (semicolon + however/moreover/etc)",
    ),
    (
        r"\*\*[A-Z][a-zA-Z\s]{1,20}:\*\*\s+\w",
        "bold-header-colon inline list (**Speed:** ...)",
    ),
]

# Vague authority attribution
VAGUE_AUTHORITY = [
    r"\bIndustry reports? suggest\b",
    r"\bExperts argue\b",
    r"\bStudies show\b(?![^.]{0,100}\([12][0-9]{3}\))",  # allow if (YYYY) follows
    r"\bRecent data indicates\b",
    r"\bObservers have noted\b",
    r"\bIt has been said\b",
    r"\bAccording to industry sources\b",
]

# Present-participle closer tags (as sentence-final -ing phrases)
PARTICIPLE_CLOSERS = [
    r",\s+(highlighting|underscoring|marking|positioning|fostering|showcasing|illustrating|demonstrating)\s+[^.]+\.\s",
]

# ─── SOFT FLAGS ───────────────────────────────────────────────────────────

SOFT_FLAG_WORDS = [
    "kind of", "sort of", "a bit",  # hedging fillers
    "essentially", "basically", "actually",  # filler
    "ultimately",  # as opener soft-flagged; hard-banned if actually opener
]

# ─── HELPERS ──────────────────────────────────────────────────────────────

def read_input(path_arg: str) -> str:
    if path_arg == "-":
        return sys.stdin.read()
    p = Path(path_arg)
    if not p.exists():
        print(f"ERROR: file not found: {path_arg}", file=sys.stderr)
        sys.exit(2)
    return p.read_text(encoding="utf-8", errors="replace")


def strip_code_blocks_and_titles(text: str) -> Tuple[str, str]:
    """Return (body_text, meta_text). Meta = <title>/<meta> tags (dashes allowed there per hard-ban exception).

    Preserves line numbers. Replaces stripped ranges with spaces so line offsets
    stay identical between input and body — so line-number diagnostics match
    the raw file.
    """

    def blank(m: re.Match) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))

    # Extract meta/title tags into their own bucket
    meta_pattern = re.compile(r"<(title|meta)[^>]*>([\s\S]*?)</\1>|<meta[^>]*/?>", re.IGNORECASE)
    meta_hits = " ".join(m.group(0) for m in meta_pattern.finditer(text))
    body = meta_pattern.sub(blank, text)

    # Strip <script>, <style>
    body = re.sub(r"<script[\s\S]*?</script>", blank, body, flags=re.IGNORECASE)
    body = re.sub(r"<style[\s\S]*?</style>", blank, body, flags=re.IGNORECASE)

    # Strip HTML comments
    body = re.sub(r"<!--[\s\S]*?-->", blank, body)

    # Strip URL attribute values (href/src/action/data-src) — third-party URLs
    # legitimately contain banned words (e.g. snapchat.com/unlock/). Only the
    # attribute VALUE is blanked; visible link text is still scanned.
    body = re.sub(r"(?:href|src|action|data-src)=(\"[^\"]*\"|'[^']*')",
                  lambda m: m.group(0)[: m.group(0).index("=") + 2] + " " * (len(m.group(0)) - m.group(0).index("=") - 3) + m.group(0)[-1],
                  body)

    # Strip markdown code fences ```...```
    body = re.sub(r"```[\s\S]*?```", blank, body)

    # Strip inline code spans `foo` — legitimate citations of banned words in
    # internal reference docs use backticks. Removing them removes the false
    # positives without touching client-facing prose (which shouldn't use
    # backticks anyway).
    body = re.sub(r"`[^`\n]+`", lambda m: " " * len(m.group(0)), body)

    return body, meta_hits


SKIP_SENTINEL = "linter:skip-file"


def find_all_case_insensitive(pattern: str, text: str) -> List[Tuple[int, str]]:
    """Return list of (line_num, matched_text) for pattern in text."""
    hits = []
    lines = text.split("\n")
    for i, line in enumerate(lines, start=1):
        for m in re.finditer(pattern, line, flags=re.IGNORECASE):
            hits.append((i, m.group(0)))
    return hits


def find_word(word: str, text: str) -> List[Tuple[int, str]]:
    # Word boundary; escape special chars
    esc = re.escape(word)
    pattern = rf"\b{esc}\b"
    return find_all_case_insensitive(pattern, text)


# ─── SOFT FLAG DETECTORS ──────────────────────────────────────────────────

def detect_sentence_length_uniformity(text: str) -> List[str]:
    """Flag paragraphs where sentence lengths cluster (std dev < 40% of mean)."""
    warnings = []
    # Split by blank line = paragraphs
    paragraphs = re.split(r"\n\s*\n", text)
    for p_idx, p in enumerate(paragraphs, start=1):
        clean = re.sub(r"<[^>]+>", " ", p)
        clean = re.sub(r"\s+", " ", clean).strip()
        if len(clean) < 200:
            continue
        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", clean)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 3]
        if len(sentences) < 4:
            continue
        lens = [len(s.split()) for s in sentences]
        if not lens:
            continue
        mean_len = sum(lens) / len(lens)
        if mean_len < 8:
            continue
        variance = sum((l - mean_len) ** 2 for l in lens) / len(lens)
        std_dev = variance ** 0.5
        if std_dev / mean_len < 0.40:
            warnings.append(
                f"paragraph {p_idx}: uniform sentence length "
                f"(mean={mean_len:.1f}w, stdev={std_dev:.1f}w — burstiness low)"
            )
    return warnings


def detect_ascending_tricolons(text: str) -> List[str]:
    """Flag when > 2 ascending three-item lists appear."""
    warnings = []
    # Rough regex: comma-item, comma-item, and item (with item2 > item1 in word count via length heuristic)
    hits = re.findall(
        r"([A-Z][a-z]+(?:\s+[a-z]+)?,\s+[a-z]+(?:\s+[a-z]+)?,\s+and\s+[a-z]+(?:\s+[a-z]+){1,3})",
        text,
    )
    if len(hits) > 2:
        warnings.append(f"ascending-tricolon pattern used {len(hits)}x — pick your best one")
    return warnings


def detect_not_x_its_y(text: str) -> List[str]:
    """Ban when > 1 'not X, it's Y' construction appears."""
    warnings = []
    hits = re.findall(r"\bnot\s+an?\s+\w+[^,.]{0,40},\s+it'?s\s+an?\s+\w+", text, re.IGNORECASE)
    if len(hits) > 1:
        warnings.append(f"'not X, it's Y' used {len(hits)}x — banned after first instance per deck")
    return warnings


def detect_hedge_stack(text: str) -> List[str]:
    """3+ hedge words in a 100-word window."""
    warnings = []
    hedges = ["typically", "generally", "often", "may", "might", "some argue", "tends to", "usually"]
    hedge_pattern = r"\b(" + "|".join(re.escape(h) for h in hedges) + r")\b"
    total = len(re.findall(hedge_pattern, text, re.IGNORECASE))
    words = len(text.split())
    if words > 0 and total / (words / 100) > 3:
        warnings.append(
            f"hedge stack: {total} hedges across ~{words} words ({total/(words/100):.1f} per 100w)"
        )
    return warnings


# ─── MAIN ─────────────────────────────────────────────────────────────────

def lint(text: str) -> Tuple[List[str], List[str]]:
    body, meta = strip_code_blocks_and_titles(text)
    hard_errors: List[str] = []
    soft_warnings: List[str] = []

    # Dashes (banned in body, allowed in meta with override comment)
    for char, name in DASH_BANS:
        for i, line in enumerate(body.split("\n"), start=1):
            if char in line and "linter:allow-dash" not in line:
                hard_errors.append(f"line {i}: {name} in body — use period/colon/comma/middot")
                break

    # Word bans
    for w in HARD_BAN_WORDS:
        hits = find_word(w, body)
        for line, match in hits:
            hard_errors.append(f"line {line}: banned word '{match}'")

    # Context-dependent words (flag with note)
    for w in CONTEXT_DEPENDENT_WORDS:
        hits = find_word(w, body)
        for line, match in hits:
            soft_warnings.append(
                f"line {line}: context-dependent word '{match}' — permitted only in narrow cases (see ai-tells-hard-bans.md)"
            )

    # Openers
    for pat in HARD_BAN_OPENERS:
        # Match at start of any line (approximates paragraph opener in HTML)
        for i, line in enumerate(body.split("\n"), start=1):
            # Strip tags for opener check
            clean = re.sub(r"<[^>]+>", " ", line).strip()
            if re.match(pat, clean, re.IGNORECASE):
                hard_errors.append(f"line {i}: banned opener matching /{pat}/")

    # Closers
    for pat in HARD_BAN_CLOSERS:
        hits = find_all_case_insensitive(pat, body)
        for line, match in hits:
            hard_errors.append(f"line {line}: banned closer/rhetorical device '{match}'")

    # Structural
    for pat, name in STRUCTURAL_BANS:
        hits = find_all_case_insensitive(pat, body)
        for line, match in hits:
            hard_errors.append(f"line {line}: {name} — '{match}'")

    # Vague authority
    for pat in VAGUE_AUTHORITY:
        hits = find_all_case_insensitive(pat, body)
        for line, match in hits:
            hard_errors.append(f"line {line}: vague-authority attribution '{match}' — cite the source or drop the claim")

    # Participle closers
    for pat in PARTICIPLE_CLOSERS:
        hits = find_all_case_insensitive(pat, body)
        for line, match in hits:
            hard_errors.append(f"line {line}: present-participle closer tag ({match.strip()})")

    # Soft flags
    for w in SOFT_FLAG_WORDS:
        hits = find_word(w, body)
        for line, match in hits:
            soft_warnings.append(f"line {line}: soft-flag filler '{match}'")

    soft_warnings.extend(detect_sentence_length_uniformity(body))
    soft_warnings.extend(detect_ascending_tricolons(body))
    soft_warnings.extend(detect_not_x_its_y(body))
    soft_warnings.extend(detect_hedge_stack(body))

    return hard_errors, soft_warnings


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: lint-copy.py path/to/file  (or - for stdin)", file=sys.stderr)
        return 2

    text = read_input(sys.argv[1])

    # Per-file opt-out: reference docs, internal notes, prompt files that
    # legitimately cite banned words. Sentinel must appear in first 30 lines.
    head = "\n".join(text.splitlines()[:30])
    if SKIP_SENTINEL in head:
        print(f"\x1b[36mskipped ({SKIP_SENTINEL} present) — internal reference doc\x1b[0m")
        return 0

    hard, soft = lint(text)

    if hard:
        print(f"\n\x1b[31mHARD BANS ({len(hard)}):\x1b[0m")
        for e in hard:
            print(f"  ✗ {e}")

    if soft:
        print(f"\n\x1b[33mSOFT FLAGS ({len(soft)}) — review, don't reflexively fix:\x1b[0m")
        for w in soft:
            print(f"  ⚠ {w}")

    if not hard and not soft:
        print("\x1b[32m✓ copy clean — no hard bans, no soft flags\x1b[0m")

    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
