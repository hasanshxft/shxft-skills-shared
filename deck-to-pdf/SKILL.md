---
name: deck-to-pdf
description: Convert HTML slide decks into polished, shareable PDF documents with pixel-perfect slides, retina quality, and clickable hyperlinks. Use when the user wants a PDF version of a deck for email, WhatsApp, or client sharing — especially when the live URL is blocked by corporate email filters (FortiMail, Mimecast, Proofpoint).
---

# Deck to PDF — HTML Deck → Shareable PDF

Turn any single-file HTML deck into a polished PDF that passes corporate email filters, renders identically to the live deck, and keeps its CTAs clickable.

## Trigger

`/deck-to-pdf`, "convert this deck to PDF", "make a PDF version", "I need a PDF to share", "client can't open the link" (email filter issue → PDF is the workaround).

## The Pipeline (proven — use this, do not improvise)

**DO NOT use `chrome --print-to-pdf`.** It silently clips slides that are taller than the page, ignores `@page size` CSS without the right flags, and produces different output on different Chrome versions. On the Boggi Milano deck (2026-04-23) this approach cost an hour and produced a broken PDF. The reliable pipeline is screenshot-per-slide.

### Step 1 — Serve the deck locally

```bash
cd /path/to/deck-folder && python3 -m http.server 8770 &
```

Leave running in the background until all captures are done. Kill at the end.

### Step 2 — Capture each slide as a PNG via Puppeteer

**Puppeteer must run under Node, not Bun.** Bun's ESM/CJS interop breaks Puppeteer's `debug` dependency. Install Puppeteer in a throwaway directory:

```bash
mkdir -p /tmp/pup && cd /tmp/pup
npm init -y > /dev/null 2>&1
npm install puppeteer@latest --silent
```

Then write and run this capture script (`/tmp/pup/capture.mjs`):

```javascript
import puppeteer from "puppeteer";
import fs from "node:fs";
import path from "node:path";

const URL = "http://localhost:8770/index.html";
const OUT_DIR = "/tmp/deck-slides";
const WIDTH = 1440;
const HEIGHT = 900;

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.readdirSync(OUT_DIR).forEach((f) => fs.unlinkSync(path.join(OUT_DIR, f)));

const browser = await puppeteer.launch({
  headless: "new",
  args: ["--no-sandbox", "--disable-gpu"],
});
const page = await browser.newPage();
await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 2 });
await page.goto(URL, { waitUntil: "networkidle0", timeout: 30000 });

// Strip anything that would pollute a static PDF
await page.evaluate(() => {
  document.getElementById("desktopBanner")?.remove();
  document.querySelectorAll(".nav-dots, .progress-bar").forEach((el) => el.remove());
  const style = document.createElement("style");
  style.innerHTML = `
    html, body { scroll-snap-type: none !important; scroll-behavior: auto !important; }
    .slide { scroll-snap-align: none !important; }
    .reveal, .reveal.d1, .reveal.d2, .reveal.d3, .reveal.d4 {
      opacity: 1 !important; transform: none !important; animation: none !important;
    }
  `;
  document.head.appendChild(style);
});
await new Promise((r) => setTimeout(r, 800)); // fonts + lazy bits

const count = await page.$$eval(".slide", (els) => els.length);

for (let i = 0; i < count; i++) {
  await page.evaluate((y) => window.scrollTo({ top: y, left: 0, behavior: "instant" }), i * HEIGHT);
  await new Promise((r) => setTimeout(r, 500));

  // CRITICAL: clip uses PAGE coordinates (not viewport). Use actual scrollY, not 0.
  const actualY = await page.evaluate(() => window.scrollY);
  await page.screenshot({
    path: path.join(OUT_DIR, `slide-${String(i + 1).padStart(2, "0")}.png`),
    clip: { x: 0, y: actualY, width: WIDTH, height: HEIGHT },
    type: "png",
  });
  console.log(`slide ${i + 1}: scrollY=${actualY}`);
}

await browser.close();
```

Run: `cd /tmp/pup && node capture.mjs`

**The non-obvious bug (solved):** Puppeteer's `page.screenshot({ clip })` uses PAGE coordinates, not viewport. If you pass `clip: { y: 0 }`, it always screenshots the document top regardless of scroll position. File sizes will come out suspiciously similar (near-identical PNG sizes). Use the current `scrollY` as `clip.y`.

### Step 3 — Stitch PNGs into a PDF with PIL

```python
from PIL import Image
import glob

pages = sorted(glob.glob('/tmp/deck-slides/slide-*.png'))
imgs = [Image.open(p).convert('RGB') for p in pages]
imgs[0].save(
    '/path/to/Deck Output.pdf',
    save_all=True,
    append_images=imgs[1:],
    resolution=144.0,
    quality=92,
)
```

At 144 DPI, a 2880×1800 pixel image = 1440×900 points in the PDF. This 1:1 mapping makes link annotation math trivial in Step 4.

### Step 4 — Overlay clickable link annotations with pymupdf

This is the reason screenshots-based PDFs feel like images: they're flat, no links. Fix with pymupdf.

**Query button coords live** with a one-shot Puppeteer script (`/tmp/pup/extract-links.mjs`). Scroll to the target slide, then `element.getBoundingClientRect()` and add current `scrollY` to get page-absolute coordinates:

```javascript
const rect = (el) => {
  if (!el) return null;
  const r = el.getBoundingClientRect();
  return { x: r.left, y: r.top + window.scrollY, w: r.width, h: r.height };
};
```

Then add link annotations with pymupdf:

```python
import fitz  # pymupdf
SLIDE_HEIGHT = 900  # pt

doc = fitz.open(PDF_PATH)
for link in LINKS:
    page = doc[link["page"]]  # 0-indexed
    # Convert page-absolute y to slide-relative y
    slide_y = link["y"] - link["page"] * SLIDE_HEIGHT
    rect = fitz.Rect(link["x"], slide_y, link["x"] + link["w"], slide_y + link["h"])
    page.insert_link({"kind": fitz.LINK_URI, "from": rect, "uri": link["uri"]})

# pymupdf requires incremental save OR save to a new file:
tmp_path = PDF_PATH + ".tmp"
doc.save(tmp_path, deflate=True, garbage=3)
doc.close()
import os; os.replace(tmp_path, PDF_PATH)
```

**pymupdf uses top-left origin** (unlike raw PDF which uses bottom-left). So page coordinates from `getBoundingClientRect` → pymupdf `Rect(x0, y0, x1, y1)` works directly with the y-flip conversion above.

### Step 5 — Cleanup + deliver

- Stop the local HTTP server (`TaskStop` on the background task)
- Delete `/tmp/deck-slides/*.png` and `/tmp/pup/` (Puppeteer's `node_modules` is heavy)
- Open the PDF: `open "/path/to/Deck Output.pdf"`
- File size target: **under 5MB** for email, **under 10MB** for WhatsApp. The screenshot pipeline typically lands around 2-4MB for a 9-slide deck.

## What to always hyperlink on the final slide

On most SHXFT/FRXME/SCXPE decks the closing slide has:
- **Primary CTA button** (Approve & Begin, Book a call, etc.) → mailto with pre-filled subject + body
- **WhatsApp pill** → `wa.me/<number>` (look up `user_contact.md` memory, never hallucinate)
- **Email fallback** → plain `mailto:hasan@shxft.studio`
- **SHXFT wordmark** in the "POWERED BY" block on the cover → `https://shxft.studio`

Query all four via the extract-links script so the pipeline is repeatable for any deck.

## The ABSOLUTE DON'Ts (from the Boggi autopsy)

- **Don't use `chrome --print-to-pdf`.** Silently clips content taller than 900px. `--prefer-css-page-size` helps sometimes but is unreliable across Chrome versions. Screenshot pipeline is the one that works.
- **Don't trust `page-break-inside: avoid` + `overflow: hidden` to fit content.** Browsers crop silently at page boundaries instead of shrinking content to fit.
- **Don't use Bun for Puppeteer.** `debug` package has an ESM/CJS interop bug that kills the Bun import chain. Node + throwaway `/tmp/pup` is fine.
- **Don't pass `clip: { x:0, y:0 }` in Puppeteer screenshots.** Use current `scrollY` — it's page-relative, not viewport-relative.
- **Don't use `doc.save(SAME_PATH)` with pymupdf.** Raises `save to original must be incremental`. Save to a `.tmp` path and `os.replace`.
- **Don't hallucinate the WhatsApp/email address for hyperlinks.** Read from `user_contact.md` memory or ask.

## Pre-deliver checklist

- [ ] All slides captured (count matches `.slide` elements in HTML)
- [ ] Content-heavy slides (tall mockups, long lists) show fully, not clipped
- [ ] Dark slides (navy backgrounds) render with correct colours
- [ ] Fonts load correctly — Bodoni serif headlines aren't falling back to Georgia
- [ ] Final-slide CTA buttons have clickable link annotations embedded (verify with `doc.get_links()`)
- [ ] File size under 5MB
- [ ] Filename is client-friendly: `"Client Name x Project - SHXFT Proposal.pdf"` (spaces, proper case, no lowercase slug)
- [ ] Test: open the PDF, click Approve / WhatsApp / email — each should launch the right app with pre-filled content

## When this skill gets called

- Client explicitly asks for a PDF
- Corporate email filter blocks the live URL (FortiMail, Mimecast, Proofpoint, Barracuda) — flag this to Hasan immediately; PDF is the workaround
- Client is in a low-connectivity region and wants offline access
- Archiving a delivered proposal
- Sending to a non-technical decision-maker who won't click a link

## Integration with the deck skill

The main `/deck` skill's Phase 5 (Deliver) should offer this as a parallel deliverable when corporate email filtering is a risk — especially for MENA retail conglomerates (Azadea, M.H. Alshaya, Al-Futtaim, Chalhoub), banks, government, and any Emirates / Saudi enterprise where URL filtering is aggressive. If Hasan mentions "they couldn't open the link" or "sending to [enterprise client]", proactively invoke `/deck-to-pdf` after the main deck is approved.
