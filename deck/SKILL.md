---
name: deck
description: Create animation-rich HTML slide presentations, client proposals, convert PowerPoint/Google Slides decks, or enhance existing presentations. Triggers on /deck, proposals, pitches, and client deck requests.
---

# Deck — Animation-Rich HTML Presentations & Client Proposals

Create stunning, self-contained HTML presentations with zero dependencies. Single file, inline CSS/JS, production-quality output. Includes a dedicated **Proposal Mode** for generating co-branded client pitches.

## Phase 0 — Detect Task Type

Read the user's request and determine the path:

| Signal | Path |
|--------|------|
| User mentions a **prospect**, **brand**, **proposal**, **pitch for [client]**, or "create a FRXME proposal" | → **Proposal** (Phase 1P → Phase 1R → Phase 3P → Phase 5) |
| User provides `.pptx` file or Google Slides link | → **Convert** (Phase 4 → Phase 2 → Phase 3) |
| User provides existing `.html` presentation | → **Enhance** (Phase 3 with existing file) |
| Everything else | → **New** (Phase 1 → Phase 2 → Phase 3) |

---

## Phase 1P — Proposal Intake (Proposal mode only)

### Pre-flight Step 0: Pending-outcome gate (returning clients only)

If the client has prior brain entries, run the gate before any intake:

```bash
bash "$HOME/.claude/skills/cs/scripts/check-pending-outcomes.sh" --client SLUG
```

If the script flags `pending no-outcome-ever` or `pending stale-status`, do
NOT start new deck work. Surface the prompt to Hasan and log the outcome
first via `log-outcome.sh`. This is what turns the OS feedback layer from
empty into compounding intelligence over time.

Skip for first-touch clients (script returns `no pending`).

---

### Pre-flight: Read the Brain (MANDATORY)

The deck skill shares a brain with `/cs` — three sources of compounding knowledge that MUST be queried before asking any intake questions or drafting any concept. Skipping this step is how we end up making the same mistake twice and shipping a deck that feels generic.

The four sources, in this order:

**1. Brief templates** — Read [brief-templates.md](brief-templates.md). If the user's opening message matches a template (event activation, strategy pitch, retail deployment), pre-fill the defaults and only ask the remaining 3-4 fields. Tell the user: "This sounds like a [type]. I've pre-filled the usual defaults. Just need a few things from you:"

**2. Local knowledge base** — Check [knowledge/_index.md](knowledge/_index.md) for:
- Past proposals for the same client (build continuity, don't re-pitch same concepts)
- Past proposals in the same industry (reference what worked, evolve successful patterns)
- If a match exists, read the full `knowledge/[slug].md` file for brand research, approved concepts, corrections from past sessions, and feedback

**3. Strategy foundation docs from /cs** — Check `~/Documents/CLAUDE PROJECTS/STRATEGIES/[slug]/` for any `*-foundation.md` files. If `/cs` has already done strategic thinking for this client (tension, insight, platform line, creative territories, references, FRXME proprietary numbers, cultural moment), READ THE LATEST ONE FIRST and build the deck around that foundation. Do not regenerate strategy work that already exists.

**4. CNQR OS ProposalFeedback API** — Pull every past learning logged for this client / vertical / market:

```bash
bash "$HOME/.claude/skills/cs/tools/fetch-feedback.sh" \
  --client "CLIENT_NAME" \
  --tags "vertical:VERTICAL,market:MARKET" \
  --limit 50
```

The CNQR OS `ProposalFeedback` table compounds across proposals — every win-reason, loss-reason, client quote, internal post-mortem the team has logged. This is how /deck and /cs share institutional memory beyond what's in this conversation. If `API_SECRET_KEY` isn't set in `~/.claude/skills/cs/.env`, flag the gap to the user but proceed.

**5. Persistent feedback memories** — Read [`~/.claude/projects/-Users-hasanshah-Documents-CLAUDE-PROJECTS/memory/MEMORY.md`](~/.claude/projects/-Users-hasanshah-Documents-CLAUDE-PROJECTS/memory/MEMORY.md) and pull any `feedback_*` entry that mentions decks, proposals, vibe-coded tells, video compression, or the specific client. These are durable rules learned across all conversations — they apply to every deck build.

**STALE-CHECK GATE for memories and per-client knowledge:**

Memory entries and per-client knowledge files have a `freshness:` field in their frontmatter:

- `freshness: durable` — universal rule, doesn't decay (em-dashes, OG image required, video compression, content protection script). Apply directly.
- `freshness: market-watch` — claim about a specific client's brand state, recent palette decisions, current competitive landscape, or anything tied to live circumstance. **Stale after 60 days.** Quick verify before applying.

When a `market-watch` knowledge entry is older than 60 days:
1. Quote the relevant fact: "knowledge/[slug].md says [X] (date: [Y])"
2. Confirm with one quick check (re-read the live deck, re-WebFetch the client site, or ask the user)
3. Apply if still true; update the knowledge file with new dated section if not

Without this gate, the brain accumulates outdated assumptions silently. With it, today's decision uses today's truth.

**Surface the brain back to the user before intake.** When relevant past learnings exist, show them as a short list:

> "Before we start — pulling from past brain:
> - QM brief similar to past Mathaf Snap × QM activation (knowledge/qatar-museums.md). Notable: Baraa is in Sheikha Al Mayassa's office — not a vendor pitch.
> - Foundation doc exists at STRATEGIES/qatar-museums/2026-04-26-foundation.md — using its tension and platform line.
> - 2 OS feedback entries from past museum proposals: clients flagged 'AR for AR's sake' as a common turn-off; lead with mechanic not tech.
> - Persistent rules to apply: never decorate concept slides with HTML/CSS animations without asking, lint-deck must pass before any push.
> Want me to apply all this and proceed with the standard intake?"

This makes the compounding visible. Hasan sees the deck getting smarter; the team sees the institutional memory working.

If no template matches AND no knowledge exists for the client/vertical/market, proceed with the full intake below — but say so explicitly: "No prior brain for this client / vertical — first deck in the lineage. We'll build it fresh and capture lessons at the end."

---

Before generating anything, collect all ten. Ask naturally, not as a form — but don't skip any.

**The basics:**
1. **Brand name** — the prospect
2. **Website URL** — will be scraped for brand research
3. **Industry / vertical** — open-ended, no fixed list
4. **Budget tier** — Starter (~$15K), Growth (~$35K), Enterprise (~$75K+), or "Not sure yet"
5. **Key pain points / challenges** — what the brand is struggling with

**Context & history:**
6. **Brain dump** — Ask open-ended: "Tell me everything you know — meeting notes, client goals, audience, vibes, random thoughts, what they said, what the mood was. Brain dump it all, I'll organize it." This is critical because team members may not know what's relevant. Accept raw meeting recaps, voice-note transcripts, bullet points, or rambling paragraphs — Claude structures the chaos. Save the parsed brief to project memory (`project_CLIENT_brief.md`) so it persists across sessions.
7. **Client history** — "Have we worked with this client before? Any previous proposals, activations, or briefs?" If yes, reference those — build continuity ("Building on X...") and avoid re-pitching things they've seen. Check project memory for past proposals. Store client history in project memory for future use.

**Creative direction:**
8. **Platform type** — "Is this Web AR, Snapchat, TikTok, a FRXME screen activation, or a mix?" This narrows the idea space significantly: Snapchat = **Snapchat Face Lens** (face-tracked) or **Snapchat World Lens** (environment/full-body) — always use the correct lens type, never just "Snapchat AR". TikTok = **TikTok Branded Effect** — always use this exact term, never "TikTok AR effect" or "TikTok filter". FRXME = full-body interactive screen experiences. Web AR = browser-based marker/markerless. Physical = installations/OOH. Ask follow-up if "mixed" — which platforms specifically?
9. **Top-line ideas** — "Do you have any ideas or directions you're already exploring? Even rough ones." If yes, Claude builds on and elevates them — at least 1-2 ideas should be extensions of what the user gave. Then complement with 1-2 fresh concepts. If none, Claude ideates from scratch based on brand research + platform type.

**Presentation scope:**
10. **Include pricing / scoping?** — "Should we include pricing or a 'what's included' scoping slide, or is this purely about getting them excited about the ideas first?" Three options:
    - **No pricing, no scoping** (default for first-touch / proactive proposals) — skip the Investment slide entirely. The deck ends with Why Now → Next Steps. The goal is idea approval first; scoping comes in the follow-up conversation.
    - **Scoping only** — include a "What's Included" slide (deliverables, analytics, support) but no dollar amounts. Good for when they need to understand the offering but pricing is premature.
    - **Full pricing** — show the recommended package with dollar amounts and ROI anchors per the pricing guide. Only for later-stage proposals where budget has been discussed.

**Do not proceed until you have all ten.**

---

## Handover decks (intermediary-route rule, added 2026-07-18)

When the deck reaches the decision maker via an intermediary (a family member, a champion forwarding on WhatsApp, a gatekeeper passing it upward), the deck must sell with NOBODY in the room:

1. **Zero-voiceover test:** every slide must be self-explanatory read cold on a phone. If a slide needs a presenter sentence to land, rewrite the slide.
2. **Demo before claims:** any live/tryable artifact (web demo link, QR) goes in the first third of the deck, before proof slides. The intermediary's strongest move is handing over a working thing, not an argument.
3. **Arm the intermediary:** alongside the deck, give the carrier a 2-3 line pocket answer for the questions the decision maker will ask out loud (usually price and "who are these people"), so momentum never routes to a stalled channel.

First applied: Dr Joy Clinics (2026-07-18, daughter-to-founder route).

---

## Phase 1I — Ideation (Proposal mode only)

After collecting inputs and completing brand research (Phase 1R), generate 3-4 concept ideas before building the deck.

**Ideation rules:**
- Ideas MUST be platform-specific. Snapchat = **Snapchat Face Lens** (face-tracked effects, filters) or **Snapchat World Lens** (environment/full-body/markerless) — use the correct lens type for each concept. TikTok = **TikTok Branded Effect** — always this term, never "TikTok AR effect" or "TikTok filter". FRXME screen = full-body interactive experiences (AR overlays, gesture games, photo moments). Web AR = marker-based or markerless browser experiences. Mixed = combine platforms into a cohesive campaign.
- If the user provided directions (question 9), at least 1-2 ideas should build on their input — elevate, refine, or extend their thinking. Don't ignore what they gave you.
- If a brief exists (question 6), every idea must clearly address the brief's objectives and KPIs.
- If there's client history (question 7), reference what worked before and evolve it — don't repeat the same pitch.
- Each concept needs: a name, a one-line hook, 3-4 sentence description of the experience, and which platform(s) it uses.

**Present the concepts to the user for feedback before proceeding to deck generation.** They may want to adjust, swap, or add. This is collaborative — the user's input makes the ideas stronger.

**Save approved concepts to project memory** (`project_CLIENT_brief.md`) alongside the original brief context. This means future conversations can reference what was proposed, what was approved, and what the client's reaction was — building institutional knowledge across the team.

### Goal Threading

**Every client goal identified in the brief (question 5/6) must be woven throughout the entire deck — not mentioned once and forgotten.**

This is critical. If the client's goal is "drive app subscribers", that goal should surface in:
- **Idea slides** — each concept's description should explain how it converts to the goal (not just "cool AR experience" but "every interaction funnels to app subscription")
- **How It Works steps** — the final step of every concept should end with the conversion action tied to the goal
- **Tag pills** — include goal-relevant tags where natural (e.g. "Foot Traffic → App", "Subscriber Funnel")
- **Investment slide** — frame ROI in terms of the client's goal metric (cost-per-subscriber, not just impressions)
- **Why Now slide** — at least one urgency point should tie timing to the goal ("this is when subscription intent peaks")

**Rules:**
- Never dedicate a whole slide to the goal — that feels like we're teaching them their own business
- Instead, make it impossible to miss: the goal should be the throughline connecting every concept
- Use the client's own language for the goal — mirror how they described it in the brief
- Every concept should feel like it was designed with the goal as its north star (because it was)
- In the "How It Works" steps, the final step should always connect the experience to the client's KPI — that's the money shot

---

## Phase 1R — Brand Research (Proposal mode only)

### HARD RULE — never inherit a previous deck's chassis. Build from THIS client's brand, every time.

Before any styling, palette decision, slide-class structure, or CSS choice, you MUST run a brand assessment for the current client and answer the questions below in writing (in conversation or a brain note). **No exceptions, no shortcuts, no "the previous deck looked like this so let's just adapt."** Inheriting the previous client's palette is the #1 way decks end up feeling like *our* deck about the client instead of *their* deck.

The brand assessment must include:

1. **Primary visual identity colour** — the colour the client *lives in*. Pull from their actual website hero, marketing collateral, physical-environment photos, branded packaging — not just the logo. The colour someone would describe their brand as.
2. **Secondary surface colour** — the typical background colour they sit on. Clinical white? Warm cream? Off-black? Saturated brand background?
3. **Accent colour(s)** — the colour they use to highlight, but never dominantly.
4. **Light or dark dominant identity?** — does their world feel light (cream, white, off-white) or dark (navy, charcoal, deep brand colour)?
5. **What would *their* deck look like if they made it themselves?** — squint test. If the answer is "the previous client's deck with their logo dropped in," start over.
6. **Banned colours from prior decks** — if the previous deck had warm cream, gold, burgundy, etc, write down explicitly: *"Drop these — don't survive into this deck without an explicit reason rooted in THIS client's identity."*

Then, and only then, build CSS root variables from the answers. **Don't reuse `slide-cream` / `slide-sand` / etc class names from previous decks** — rename per client (`slide-clinical`, `slide-warm`, etc) so the chassis itself doesn't carry forward palette assumptions.

**The squint test (mandatory before deck handoff):** zoom out, blur your eyes. Does the deck visually feel like the client's website + their brand environment? Or does it feel like the previous deck with their logo dropped in? If the answer is the second one, palette is wrong, restart the CSS root.

**For physical-product 3D models (FRXME, etc):** match the actual hardware colour the client received or would receive (white, navy, etc). Don't tint to the previous client's brand.

Why this rule exists: KCH 2026-05-04 incident. The DGDA-cream chassis bled into the KCH deck (warm cream backgrounds, heritage gold accents, tan-toned 3D body) when KCH's actual brand is clinical navy + white. The deck shipped feeling like a heritage proposal with a hospital logo dropped in. Hasan's call: *"There is NO King's vibe across this deck, this should be in the deck skill."* See `feedback_no_cream_default_chassis.md` durable memory for the full ruleset.

---

Fetch the prospect's website using WebFetch and extract:

- **Brand colors** — from CSS custom properties, meta tags, hero sections, buttons
- **Brand voice/tone** — headlines, about page, taglines, how they talk to their audience
- **Key messaging and positioning** — what they sell, how they differentiate
- **Market context** — who they serve, their competitive landscape

If the site is inaccessible, ask the user to provide: brand colors (hex), tagline, and a short description.

### Client Logo Sourcing (Critical)

**Never assume, generate, or approximate a client logo.** The logo is the single most important brand element. If you cannot source it from the client's website during Phase 1R:
1. Tell the user: "I couldn't pull the logo from their site. Can you drop the file here? I need it for the title slide, cobrand bar, and 3D model."
2. Wait for the file before generating any slides that use the logo.
3. Do not use text-based logo recreations, SVG approximations, or placeholder text styled to look like a logo. A wrong logo is worse than no logo.
4. If the user provides multiple variants (color, white, black), save all to `assets/` and use the correct variant per context (dark bg → white/light logo, light bg → dark logo).

Store the extracted brand profile mentally — it drives everything in Phase 3P.

### Brand Element Sourcing (Required)

During Phase 1R, actively source **brand-specific visual assets** that can be used as animated floating elements throughout the deck. These are NOT just product photos — they are signature brand marks, patterns, and iconography:

- **Signature brand marks** — e.g. Nike swoosh, Adidas three stripes, Apple silhouette. These are the most powerful floating elements because they're instantly recognisable.
- **Product cutouts** — transparent PNGs of hero products (jerseys, sneakers, devices, packaging). Source from the client's e-commerce or press pages.
- **Campaign imagery** — current campaign hero shots, lifestyle photography.
- **Pattern elements** — if the brand has signature patterns (e.g. Burberry check, Louis Vuitton monogram), extract and use subtly.

Save all sourced assets to `assets/` with descriptive names (e.g. `adidas-three-stripes.png`, `adidas-jersey-home.png`). If you cannot find suitable transparent PNGs or high-quality assets from the client's public channels, ask the user: "I need brand imagery for the floating elements. Can you provide product shots, logo marks, or campaign visuals?"

These assets feed directly into the **Animated Brand Elements** section — they fly into slides, drift in corners, and reinforce brand identity at a subconscious level. A proposal without brand elements feels generic. A proposal with three stripes animating in from the corner feels like Adidas.

**Brand element fallback hierarchy (strict order):**
1. **Real brand assets** (best) — transparent PNGs/SVGs sourced from the client's website, social media, press kits. Product shots, logo marks, campaign visuals. Always try this first during Phase 1R.
2. **Contextual inline SVGs** (good fallback) — if real assets can't be sourced, use simple inline SVG illustrations that are contextually relevant to the brand's industry. A football for a sportswear brand, a speaker for an audio brand, a building silhouette for real estate. Keep them minimal: thin strokes, low opacity (`rgba(255,255,255,0.1-0.15)`), subtle. These should feel like atmospheric texture, not clip art.
3. **Nothing** — if neither option works, skip floating elements on that slide. An empty slide is better than bad decoration.
4. **NEVER abstract CSS shapes** — divs, borders, rectangles, or any CSS-only shapes pretending to be brand marks. A few coloured rectangles do NOT look like the Adidas three stripes. They look like random decorations and cheapen the deck.

When in doubt, ask the user for assets.

---

## Phase 1 — Gather Content (New standard presentations only)

Ask these questions **one message at a time**, not all at once:

1. **Purpose & audience** — "What is this presentation about, and who will see it?"
2. **Slide count** — "Roughly how many slides? (5–10 is typical, 15+ is long)"
3. **Content** — "Do you have an outline, bullet points, or should I draft the content?"
4. **Images** — "Will you provide images, or should I skip imagery and use abstract shapes only?"
5. **Inline editing** — "Do you want an edit button so you can tweak text directly in the browser? (Yes/No)"

Move to Phase 2 once you have enough context.

---

## Phase 2 — Style Selection (Show, Don't Tell)

**Never ask the user to describe their preferred style in words.** Instead:

1. Read [STYLE_PRESETS.md](STYLE_PRESETS.md) for the full style catalog
2. Based on the presentation's mood/purpose, pick **3 candidate styles**
3. For each candidate, generate a **single-slide HTML preview** (title slide only) and save it
4. Present the 3 options with filenames so the user can open and compare
5. User picks one (or asks for adjustments)

### Style Matching Guide

| Presentation Type | Suggested Styles |
|---|---|
| FRXME product pitch / tech demo | FRXME Dark, FRXME Light |
| SHXFT agency intro / capabilities | SHXFT Sketch |
| High-impact client pitch | Bold Signal, FRXME Dark |
| Elegant / premium | Dark Botanical |
| Clean / precise / corporate | Swiss Modern |
| Futuristic / innovation | Neon Cyber, FRXME Dark |
| General / versatile | Any — show 3 diverse options |

---

## Phase 3 — Generate Presentation

### Load references before generating:
- [STYLE_PRESETS.md](STYLE_PRESETS.md) — chosen style's full spec
- [html-template.md](html-template.md) — required HTML structure
- [viewport-base.css](viewport-base.css) — mandatory base styles (paste into `<style>`)
- [animation-patterns.md](animation-patterns.md) — animation library

### Critical Rules

**Viewport fitting — the #1 rule:**
- Every slide = exactly `100vh`. No internal scrolling. Ever.
- All text uses `clamp()` — never fixed pixel sizes
- Images cap at `max-height: min(50vh, 400px)`
- If content overflows → split across multiple slides, don't cram

**Content density limits per slide:**
- Title slide: 1 heading + 1 subtitle (max)
- Content slide: heading + 4–6 bullets OR heading + 2 short paragraphs
- Image slide: 1 image + 1 heading + 1 caption
- Section divider: 1–3 words, massive type

**If the user opted for 3D effects**, read the "3D Scroll-Linked Rotation" section in [animation-patterns.md](animation-patterns.md) and apply it to product showcase slides.

### Output format
- Single `.html` file, all CSS/JS inline
- If images exist: create `assets/` folder alongside
- Comments in the code explaining each section

---

## Phase 3P — Generate Proposal (Proposal mode only)

### Brand-assessment gate — DO NOT skip

Before writing a single line of CSS in Phase 3P, confirm the Phase 1R brand-assessment is done in writing for THIS client:
- Primary visual identity colour (their world, not their logo) ✓
- Secondary surface colour ✓
- Accent colour(s) ✓
- Light or dark dominant identity ✓
- Banned colours from prior decks (cream, gold, etc — call them out explicitly so they don't sneak in) ✓

If any of those boxes is unchecked, return to Phase 1R. **No CSS without the brand assessment.** This prevents the failure mode where the previous deck's chassis (DGDA cream + heritage gold, etc) bleeds into the new build and the deck ships feeling like the previous client's deck with a different logo dropped in.

### Co-Branding Design System

This is critical — proposal decks should feel like the client's own internal presentation that happens to pitch FRXME/SHXFT ideas. **Note:** This theme flexibility applies ONLY to client proposals. The core FRXME Dark / FRXME Light style presets (used for product decks, capability decks, etc.) retain their own fixed identity.

- **Match the client's PRIMARY theme.** Research their website. If their home/primary visual identity is light (white backgrounds), build a light deck. If dark, build dark. Do NOT default to dark — match THEIR world.
- **Client's brand colors dominate.** Extract their actual CSS values (backgrounds, surfaces, borders, text colors) and use them as the deck's custom properties. The client's accent color is `--brand`.
- **Parent brand selection — SHXFT vs FRXME:** Determine which brand anchors the proposal:
  - **FRXME** — when the proposal is purely about FRXME screen-based / AR activations
  - **SHXFT** — when the proposal covers a mix of FRXME screens + broader experiential activations, or when pitching SHXFT's full capabilities
  - This choice affects the title slide, cobrand bars, and closing slide
- **Title slide — client logo as hero.** The client's logo is the star, centered and prominent. No `Client × FRXME` lockup on title. Below the logo: a divider, then at the bottom a "POWERED BY" label + the parent brand wordmark logo (SHXFT or FRXME). The wordmark sits at ~45% opacity and glows on hover (`filter: drop-shadow()`), gated behind `@media (hover: hover)`.
- **Cobrand bar on content slides:** Every content slide has a persistent bottom-left `[Client Logo] × [Parent Brand wordmark]` bar at ~60% opacity. Uses the correct logo variants for the deck's background (dark logos on light bg, light logos on dark bg).
- **Typography:** Premium display font — bold, editorial (Syne, Clash Display, Cabinet Grotesk, etc.). Clean sans-serif body. Monospace for labels. **Never** Inter/Arial/Roboto.
- **Layout:** Cinematic. Asymmetric. Generous whitespace. No cookie-cutter grids.
- **Motion:** Smooth slide transitions, subtle fade-ins. Refined, not flashy.
- **Atmosphere:** Premium, immersive. The deck should pass the "squint test" — squinting, it looks like the client's website, not ours.

#### Light vs Dark Theme Adjustments

| Element | Dark Deck | Light Deck |
|---------|-----------|------------|
| `--bg-primary` | Client's dark bg (e.g. `#141414`) | Client's light bg (e.g. `#ffffff`) |
| `--text-primary` | `#ffffff` or client's light text | `#1a1a1a` or client's dark text |
| Gradient text | `#FAFAFA` → brand color | `#1a1a1a` → brand color |
| Glass cards | `rgba(255,255,255,0.04)` bg, white borders | Surface color bg, border color borders, subtle shadow |
| Ambient orbs | 10-18% opacity brand glow | 5-10% opacity brand glow (softer on white) |
| Scanlines | 30-50% opacity | 15-25% opacity |
| Particles | Normal glow | Stronger glow (`--brand-glow-strong`) so visible on white |
| Nav dots | `rgba(255,255,255,0.25)` border | `rgba(0,0,0,0.2)` border |
| Lockup × symbol | `rgba(255,255,255,0.35)` | `rgba(0,0,0,0.3)` |
| CTA button hover | Brand bg, dark text | Brand bg, white text |
| Parent brand logo | `frxme-logo-light.png` / `shxft-wordmark-white.png` | `frxme-logo-dark.png` / `shxft-wordmark-black.png` |

### SHXFT Brand Colors (reference)

| Token | Value |
|-------|-------|
| Primary Black | `#0A0A0A` |
| Pure White | `#FFFFFF` |
| Accent Electric (cyan) | `#00F0FF` |
| Accent Warm (orange-red) | `#FF3D00` |
| Mid Gray | `#1A1A1A` |
| Text Gray | `#888888` |

### Slide Structure — The Narrative Arc

This is NOT a product brochure. It's a story. A marketing director should feel understood before they ever see the product.

**Slide 1 — Title**
Client logo centered as the hero element. `[ proposal ]` mono-label above. Divider below the logo. At the bottom: "POWERED BY" label + parent brand wordmark (SHXFT or FRXME — see parent brand selection rule above). Date at the very bottom. Background uses client's brand color as subtle ambient glow.

**Slide 2 — "Your World"**
Show you understand their brand. Reference their actual positioning, messaging, market. Pull phrases from their website. Make them feel seen.

**Slide 3 — "The Challenge"**
Surface the tension. Connect their specific pain points to broader industry trends (diminishing returns on traditional activations, audience expectations shifting, competitors investing in experiential, gap between digital and physical). Frame as industry shift, not criticism.

**Slide 4 — "The Shift"**
Transitional moment. "What if your physical spaces could become as dynamic as your digital presence?" Build anticipation without revealing the product yet. **Viewport discipline:** This is a section divider — the headline should be large and cinematic but MUST fit comfortably within `100vh` on desktop AND mobile. Use `clamp()` with a sensible max (e.g. `clamp(2rem, 6vw, 4rem)` for the headline). Test at 375px width — if the text wraps more than 3 lines or clips, the font size is too large. Less is more on divider slides.

**Slide 5 — "Enter FRXME"**
Now introduce FRXME. Two-column layout: left = interactive 3D model viewer (Three.js), right = features tailored to the client. Frame every feature as a benefit for THEIR specific use case, not generic specs.

**3D Product Viewer requirements:**
- Load `frxme_low_poly.glb` + `studio_small_09_1k.hdr` (copy to project `assets/`)
- Three.js v0.162.0 via CDN importmap — use ONLY this in `<head>`, nothing else:
  ```html
  <script type="importmap">
  { "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.162.0/build/three.module.js", "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.162.0/examples/jsm/" } }
  </script>
  ```
  **NEVER add `es-module-shims`.** It conflicts with native importmap support on modern browsers and breaks the 3D viewer completely. Modern Chrome/Safari handle CDN ES module imports natively — no shim needed.
- **3D requires a local server to preview.** Chrome 115+ blocks XHR to local files from `file://` — this breaks GLB and HDR loading. The model will be invisible when opened directly. Always preview via HTTP. Tell the user to run: `cd "FRXME PROPOSALS" && python3 -m http.server 8080` then open `http://localhost:8080/filename.html`. On Cloudflare Pages this is never an issue.
- **Brand-tint the lighting**: replace default teal with client's `--brand` color on fill light, rim light, screen glow, ground glow, light bar emissive, and all screen dashboard elements
- **Client logo on device (`logo_plane` / `m_logo` mesh) — MANDATORY on every proposal with a 3D viewer.** This is not optional. The FRXME display in the 3D model must show the client's logo, not a blank or default texture. Adapt for deck theme: dark deck → use a white/light version of the logo; light deck → use the dark version. If you only have one variant, apply `MeshBasicMaterial` with appropriate settings to ensure visibility against the device's screen surface. Generate a 1024×1024 transparent PNG: render SVG via `qlmanage -t -s 2048`, extract non-white pixels to white-on-transparent (threshold: R,G,B all >245 = transparent, else solid white 255 alpha), crop to bbox, scale to ~85% canvas width maintaining aspect ratio, center on 1024×1024. Save as `CLIENT_MODEL_LOGO.png`. Apply as clean material swap: `TextureLoader().load()`, `MeshBasicMaterial({ map, transparent: true, side: DoubleSide })`, `toneMapped = false`. **DO NOT blindly flip UVs or set flipY.** The `frxme_low_poly.glb` mesh uses standard GLB UV conventions where `flipY = false` is correct for `TextureLoader` textures applied to GLB meshes. **Always set `logoTexture.flipY = false`** — the default `true` from TextureLoader will flip the logo upside-down on GLB meshes. Never use `repeat.set(1,-1)` + `offset.set(0,1)` either. Start with `flipY = false`, no UV manipulation, and visually verify.
- Dark canvas container with rounded corners + brand-tinted border/shadow (looks great on both light and dark decks)
- Slow idle auto-rotation (`model.rotation.y += 0.003` per frame when user not dragging) + drag-to-rotate with OrbitControls
- Animated screen texture (dashboard with metrics, line graph, bar chart) in brand colors
- "Drag to rotate" hint appears after 2s, hides on first interaction
- See [animation-patterns.md](animation-patterns.md) "3D Scroll-Linked Rotation" for the base pattern

**Slides 6–8 (or 6–9) — Idea Deep-Dives**
Each approved concept from Phase 1I gets its own full slide. This is where the proposal earns its fee — fleshed-out, vivid, exciting ideas that make the client say "yes."

**Content slide visual differentiation (mandatory):** Idea slides MUST look and feel distinct from the narrative slides (slides 1–4). The viewer should immediately sense they've entered the "ideas" section. Techniques:
- Shift the background: use the client's brand gradient, a darker/lighter variant of the base bg, or a subtle brand-tinted overlay. Don't use the same `--bg-primary` as the narrative slides.
- Alternate between slides: if concept 1 uses a brand gradient bg, concept 2 can return to base with a different treatment, concept 3 shifts again. Variety keeps attention.
- Use the `.slide-immersive` pattern on at least some idea slides — brand gradient background, flipped text colors, adjusted UI elements.
- The goal: when someone scrolls from "The Shift" into the first idea, there should be a visible "we're in the ideas now" moment.

Layout is a two-column split:
- **LEFT (~55%):** `[ concept 01 ]` mono-label, concept name as gradient h2, 2-3 sentence description painting the picture vividly, "How It Works" section with 3-4 numbered steps walking through the experience, tag pills at the bottom (platform, duration, shareability, etc.)
- **RIGHT (~45%):** Reference video or placeholder, **always in 9:16 portrait format** (`.ref-video-wrap` or `.media-placeholder` with `aspect-ratio: 9/16`). Never use landscape or square aspect ratios for concept slide media — all reference content is portrait phone-captured. When a reference file is provided, embed as protected autoplay video. When no file is provided yet, use the styled placeholder with play button SVG.

**Reference media — always prompt before building concept slides.** Do not generate concept slides with empty placeholders. For each approved concept, ask: "Do you have a reference video or image for [concept name]? Drop the file here." Wait for the file before generating that slide. If the user doesn't have one yet, they can say "skip for now" — only then use the placeholder and note it needs a reference added. Never silently leave placeholders without first asking.

**Reference caption text:** Once a file is provided, attempt to read/analyse it to understand what it shows. If the content is clear (e.g. a recognisable activation, a branded effect, an obvious campaign), infer the caption and confirm it. If the content is ambiguous or cannot be fully deciphered, ask: "What should the caption say for this reference? (e.g. 'Reference: [Brand] World Lens activation')" — do not guess and leave a wrong caption on the slide.

Use `.idea-slide-layout`, `.idea-content`, `.idea-steps`, `.idea-tags`, `.media-placeholder` CSS classes (see Reusable Proposal Components below).

**Slide 10 — "Investment" (OPTIONAL — based on question 10)**
Only include if the user chose "scoping only" or "full pricing". For scoping: show deliverables, analytics, support without dollar amounts. For full pricing: show recommended package with ROI anchors per [proposal-pricing.md](proposal-pricing.md). **Skip entirely for first-touch proposals** — the deck should end with ideas → Why Now → Next Steps. Don't push scoping before they've bought into the vision.

**Slide 10 or 11 — "Why Now"**
Create urgency. First-mover advantage, upcoming activations, limited slots, cost of waiting.

**Slide 12 — "Next Steps"** (was 9)
Keep this slide clean and confident — the big headline does the work. Structure:
- Large gradient headline (the emotional close, e.g. "Let's make April unforgettable.")
- "Let's get started" button — on tap, fills the screen with brand-colored confetti (canvas-based, uses client brand palette). No mailto, no scheduling link — keep it light, not salesy.
- Contact email below: hello@shxft.studio
- SHXFT.STUDIO wordmark at bottom

**WhatsApp CTA button (ask every time):**
Before building the final slide, always ask:
1. "Should we add a WhatsApp button so the client can message directly from their phone? (Yes/No)"
2. If yes: "What's the WhatsApp number to link to?" (include country code, e.g. +971 50 000 0000)

If yes, add a WhatsApp button directly below "Let's get started":
```html
<a href="https://wa.me/[number_no_plus_or_spaces]" target="_blank" rel="noopener" class="whatsapp-btn">
  <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  WhatsApp us
</a>
```
**WhatsApp button style — small pill, consistent across ALL proposals.** This is a secondary CTA, not a hero button. It should be subtle and native-feeling. Use this exact pattern (reference: Yango proposal):
```css
.whatsapp-btn {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 0.35rem 0.85rem; border-radius: 20px;
    background: #25D366; color: #ffffff;
    font-family: var(--font-body); font-size: 0.7rem; font-weight: 500;
    text-decoration: none; letter-spacing: 0.01em;
    transition: all 0.3s ease;
    box-shadow: 0 1px 4px rgba(37, 211, 102, 0.25);
}
.whatsapp-btn:hover { background: #1ebe5c; transform: scale(1.05); box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4); }
.whatsapp-btn svg { width: 14px; height: 14px; fill: currentColor; }
```
Small green pill, tiny WhatsApp icon on the left. Sits below the confetti "Let's get started" button with a small gap. NOT a large hero button — keep it secondary. This is the most important CTA on mobile since the deck is shared via WhatsApp in the MENA region.

### SHXFT Logo on Dark Decks — Use the White PNG Directly

**NEVER use `filter: brightness(0) invert(1)` on the SHXFT logo.** The X in SHXFT has internal detail/lines that get destroyed by CSS inversion, making it look like a solid white blob. Instead, use the dedicated white version of the logo which preserves all detail.

- **Dark decks**: Use `shxft-wordmark-white.png` (or `SHXFTWHITE.png`) directly. No CSS filter needed. Set `opacity: 0.45-0.85` as appropriate.
- **Light decks**: Use `shxft-wordmark-black.png` (or `SHXFTBLACK.png`) as-is. No filter.
- **Available in skill assets**: `assets/shxft/logos/shxft-wordmark-white.png` (for dark bg), `assets/shxft/logos/shxft-wordmark-black.png` (for light bg)
- On hover (gated behind `@media (hover: hover)`): add `filter: drop-shadow(0 0 12px rgba(var(--brand-rgb), 0.4))`
- **Always link SHXFT logos and wordmarks to `https://shxft.studio`** (target="_blank", rel="noopener"). This applies to: the "POWERED BY" section on the title slide, the "SHXFT.STUDIO" text on the closing slide, and any standalone SHXFT branding. Every touchpoint is a click opportunity. Keep styling subtle (opacity, no underline).

**No** "30 minutes", **no** "schedule a walkthrough", **no** friction copy. The proposal already made the case — this slide is the celebration moment. The confetti is the payoff.

### Visual Richness Requirements

Proposals must NOT be text documents with nice fonts. Every slide needs visual weight.

- **Slide 2 (Your World):** Include a hero image from the client's website/social as a subtle background — product shot, lifestyle imagery, or campaign visual. Use CSS gradient overlay for text legibility (`.slide-hero-bg` pattern).
- **Slide 3 (The Challenge):** Use brand imagery as card backgrounds or as an atmospheric backdrop behind the grid. Consider client's product photography with desaturated/blurred treatment.
- **Idea slides (6-8/9):** Media placeholder on right is MANDATORY. Left side can include a small reference thumbnail if available.
- **Slide 10 (Investment — if included):** Subtle product silhouette or brand image as background element.
- **Throughout:** Every slide should have visual texture — ambient orbs, particles, dot grids, and at minimum one photographic or media element where possible.

**Brand-immersive content slides:** Idea slides (6–9) and other content-heavy slides should adopt the client's own visual language — not just their accent color, but their gradients, background treatments, and color palette. During Phase 1R, extract:
- Primary and secondary brand gradients (e.g. a purple-to-blue gradient from their hero section)
- Background color palette (dark mode tones, card colors, section dividers)
- Any signature visual patterns (glass effects, mesh gradients, grain overlays)

Apply these as slide backgrounds, section dividers, or card treatments on content slides. The goal: when the client sees the idea slides, it should feel like their own internal deck — familiar, on-brand, immersive. Store extracted gradients/palettes as CSS custom properties (e.g. `--brand-gradient`, `--brand-bg-dark`) so they're easy to swap per client.

**Image sourcing during Phase 1R:** While researching the client's brand, actively collect product images, hero banners, lifestyle photography, campaign visuals, social content. Save URLs or download to `assets/`. These feed directly into the slides.

**Image treatments for background use:**
```css
/* Gradient overlay — light deck */
background: linear-gradient(to right, var(--bg-primary) 0%, rgba(255,255,255,0.9) 40%, rgba(255,255,255,0.7) 100%), url('image.jpg');
/* Gradient overlay — dark deck */
background: linear-gradient(to right, var(--bg-primary) 0%, rgba(0,0,0,0.85) 40%, rgba(0,0,0,0.6) 100%), url('image.jpg');
/* Or subtle atmospheric texture */
opacity: 0.12; filter: blur(2px) saturate(0.6);
```

### Brand-Relevant Atmospheric Effects

Every proposal should explore **animated background effects that connect to what the client's product actually does**. These are subtle, ambient animations layered behind content that reinforce the brand's identity at a subconscious level.

**Process (during Phase 1R):**
1. Identify the client's core product/service category
2. Brainstorm visual metaphors: What does this product *feel* like? What motions or patterns relate to it?
3. Choose 1-2 effects that are subtle enough not to distract but atmospheric enough to set mood
4. Apply to content/idea slides using `.slide-immersive` pattern

**Examples by category:**
| Industry | Effect | Implementation |
|----------|--------|---------------|
| Audio / smart speakers | Expanding sound wave rings + equalizer bars | CSS `border-radius: 50%` rings with `scale()` animation, thin bars with `scaleY()` pulse |
| Fitness / sports | Pulse/heartbeat line + particle trails | SVG path animation, CSS dot particles with staggered drift |
| Food / beverage | Rising steam/bubbles + warm color shift | Circles with `translateY` float + fade, warm gradient overlay |
| Fashion / beauty | Shimmer/sparkle particles + fabric wave | Small rotating squares with opacity flicker, sine-wave SVG distortion |
| Tech / SaaS | Data flow lines + grid pulse | Thin horizontal lines with `translateX` scroll, dot grid with `opacity` pulse |
| Automotive | Speed lines + lens flare | Diagonal streaks with `translateX`, radial gradient bloom |
| Real estate / architecture | Blueprint grid + floating floor plans | Dashed grid lines with low opacity, subtle parallax on geometric shapes |

**Rules:**
- Effects must be **extremely subtle** — opacity between 0.03–0.10 for most elements
- Use `pointer-events: none` on all atmospheric layers
- Keep to CSS animations where possible (no heavy JS) — `@keyframes` with `transform` and `opacity` only
- Position behind content with `z-index: 0`, content at `z-index: 2`
- Must not impact readability — if text becomes hard to read, reduce opacity or reposition
- Test at mobile: hide complex effects below 768px if they cause clutter
- Store as reusable CSS classes (`.sound-waves`, `.pulse-lines`, `.shimmer-particles`) so they're easy to drop into any slide

**Immersive slide pattern (`.slide-immersive`):**
When applying brand gradient + atmospheric effects to content slides:
- Override background with `--brand-gradient-dark`
- Flip text colors to light (white headings, `rgba(255,255,255,0.8)` body)
- Adjust tag pills, step numbers, captions to use light variants of brand accent
- Invert cobrand bar logos to white: `.slide-immersive .cobrand-bar img { filter: brightness(0) invert(1); }`
- Media placeholder keeps its dark style (already dark) — just adjust border/shadow to match brand accent

### Reusable Proposal Components

**Idea Slide Layout:**
```css
.idea-slide-layout {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: clamp(1.5rem, 3vw, 3rem);
    align-items: center;
    width: 100%;
}
@media (max-width: 768px) {
    .idea-slide-layout { grid-template-columns: 1fr; }
}
.idea-content { display: flex; flex-direction: column; gap: clamp(0.5rem, 1vw, 0.75rem); }
.idea-content h2 {
    font-size: clamp(1.5rem, 3.5vw, 2.5rem);
    background: linear-gradient(135deg, var(--text-primary) 30%, var(--brand) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.idea-steps { display: flex; flex-direction: column; gap: clamp(0.4rem, 0.8vw, 0.6rem); margin-top: 0.75rem; }
.idea-step { display: flex; align-items: flex-start; gap: 0.75rem; }
.step-num { font-family: var(--font-mono); font-size: 0.7rem; color: var(--brand); font-weight: 600; flex-shrink: 0; margin-top: 0.15em; }
.idea-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem; }
.idea-tag {
    font-family: var(--font-mono); font-size: 0.58rem; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 0.25rem 0.6rem; border: 1px solid var(--border); border-radius: 20px; color: var(--text-muted);
}
```

**Media Placeholder (9:16 vertical — reference videos are always portrait format):**
```css
.media-placeholder {
    position: relative; height: min(60vh, 500px); aspect-ratio: 9 / 16; width: auto; max-width: 100%;
    background: radial-gradient(ellipse at center, #1a1f2e 0%, #0f1218 100%);
    border-radius: 16px; overflow: hidden;
    border: 1px solid rgba(var(--brand-rgb), 0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.15), 0 0 60px rgba(var(--brand-rgb), 0.06);
    display: flex; align-items: center; justify-content: center;
}
.media-placeholder:hover { border-color: rgba(var(--brand-rgb), 0.35); }
.play-btn {
    width: 64px; height: 64px; background: rgba(255,255,255,0.08); backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.15); border-radius: 50%;
    display: flex; align-items: center; justify-content: center; transition: all 0.3s ease;
}
.play-btn svg { width: 24px; height: 24px; fill: rgba(255,255,255,0.8); margin-left: 3px; }
.media-caption {
    font-family: var(--font-mono); font-size: 0.6rem; color: var(--text-muted);
    letter-spacing: 0.08em; margin-top: 0.6rem; text-align: center;
}
```

**Hero Background Image:**
```css
.slide-hero-bg {
    position: absolute; inset: 0; z-index: 0; pointer-events: none;
}
.slide-hero-bg img {
    width: 100%; height: 100%; object-fit: cover; opacity: 0.12; filter: blur(2px) saturate(0.6);
}
.slide-hero-bg::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(to right, var(--bg-primary) 0%, rgba(255,255,255,0.9) 40%, rgba(255,255,255,0.7) 100%);
}
```

### Responsive Rules — Mobile Is Critical

⚠️ **Decks are frequently shared via WhatsApp and viewed on phones in the Middle East.** Mobile portrait AND landscape MUST be airtight. This is not optional polish — it's a core delivery requirement.

🔒 **MANDATORY — keyboard navigation on EVERY deck.** Arrows, up/down, PageUp/PageDown, space, Home and End must all move the deck. Presenters drive with the keyboard and a deck that ignores it reads as broken in front of a client. Hasan has raised this repeatedly. Copy the handler from [references/scroll-3d-mechanic.md](references/scroll-3d-mechanic.md) section 1b, and derive the current slide from viewport position rather than a counter.

🔒 **MANDATORY — scroll + 3D mechanic: copy [references/scroll-3d-mechanic.md](references/scroll-3d-mechanic.md) verbatim from the SquatWolf deck. Do NOT re-derive it.** Every slide-scroll deck and every 3D-viewer deck uses that exact CSS/JS. The Dr Joy deck (2026-07-19) cost hours of client-facing back-and-forth (stuck scroll, frozen 3D, cramped mobile layout) purely because it diverged on small details — 768 vs 820 breakpoint, `overflow-y`/`-webkit-overflow-scrolling` on html, disabling OrbitControls on touch, inline grid overrides that block mobile collapse, a full-screen 3D that traps the swipe. All of those are pre-solved in the reference. Read it before writing any scroll or 3D code.

**⚠️ CRITICAL — Never combine `max-width` with `max-height` in mobile media queries:**
```css
/* ❌ WRONG — breaks when desktop browser is narrowed to simulate mobile */
@media (max-width: 768px) and (max-height: 900px) { ... }

/* ✅ CORRECT — width-only detection */
@media (max-width: 768px) { ... }
```
The `and (max-height: Npx)` condition fails when a user narrows their desktop browser window to test mobile (the window height stays ~900px+). It also silently fails on tall phones (iPhone 15 Pro Max is 956px tall). **Mobile layout must be detected by width alone.**

**Mobile strategy (applied in [viewport-base.css](viewport-base.css)):**
- **Desktop (>768px wide, >600px tall):** Scroll-snap, full-viewport slides, nav dots = "deck" experience
- **Mobile portrait (≤768px wide):** Free-scrolling long page, single-column cards, no nav dots = premium site experience
- **Landscape phone (≤500px tall):** Free-scrolling, 2-col grids kept but tighter, compact typography, no nav dots

**Nav dots:**
- Hide on mobile portrait (≤768px) and landscape (≤600px height) — too many slides, dots clutter the screen
- Auto-fade labels after appearing: `animation: labelFadeOut 2.5s ease forwards`
- Hide labels entirely below 900px: `@media (max-width: 900px) { .nav-dot-label { display: none; } }`

**Scroll-snap:**
- Disable at `≤768px` width OR `≤600px` height via `html { scroll-snap-type: none; }`
- When disabled, slides become `height: auto; min-height: 100dvh; overflow: visible; overflow-x: clip;`
- MUST use `overflow-x: clip` (not `overflow: hidden`) — clip prevents pseudo-element bleed without creating a scroll container that blocks vertical scroll
- Also add `overflow-x: hidden` on `html` and `body` as safety net

**Horizontal overflow prevention:**
- Any pseudo-element using negative positioning (e.g. `.perspective-grid::after { left: -20%; right: -20%; }`) WILL cause horizontal scroll on mobile
- MUST use `overflow-x: clip` on `.slide` to contain these
- Always verify: `document.body.scrollWidth === window.innerWidth` at every viewport

**Card grids on mobile:**
- `.card-grid` (2-column) → `1fr` on mobile portrait, kept 2-col in landscape
- `.card-grid-3` (3-column) → `1fr` on mobile portrait, kept 3-col in landscape (with tighter padding)
- Never use 3+ columns at <768px width — causes orphan rows (2+1)

**3D viewers:**
- Heavy (Three.js + GLB + HDRI) — consider impact on mobile performance
- **CRITICAL — mobile scroll traps (Dr Joy 2026-07-19 incident). The known-good reference is the SquatWolf deck; copy its scroll setup exactly.** Two independent bugs bit this deck vs SquatWolf:
  - **(a) Scroll-snap breakpoint gap → first-swipe "snap back" stick.** SquatWolf disables scroll-snap at `@media (max-width: 820px)`; Dr Joy used 768px. Large phones / iPads in portrait are 810-834px wide, so they fell through the 768 gap, kept `scroll-snap-type: y mandatory`, and the first gentle swipe snapped back to slide 1. **FIX (better than a pixel breakpoint): disable scroll-snap on ANY touch device by capability, in JS, on load:** `if (window.matchMedia('(hover: none), (pointer: coarse)').matches) { document.documentElement.style.scrollSnapType='none'; document.querySelectorAll('.slide').forEach(s=>{s.style.scrollSnapAlign='none';s.style.height='auto';s.style.minHeight='100dvh';}); }`. Keep the CSS `@media (max-width: 820px)` override too (use 820, never 768, for the snap/layout breakpoint).
  - **(b) OrbitControls forces `touch-action: none` on its canvas → traps the swipe on the 3D slide.** SquatWolf does NOT add `touch-action: none` in CSS. Never add it. On touch devices set `controls.enabled = false` (model still auto-rotates as a showpiece) + `canvas.style.touchAction = 'pan-y'` (AFTER OrbitControls construction) + hide the drag hint. Desktop keeps full drag.
  - Never ship a 3D deck without testing vertical scroll AND first-swipe-off-slide-1 at ~810px width (the tablet-portrait gap), not just 375px.
- **Model centering is critical** — proptech/architecture decks demand precision. Camera target MUST be `[0, 0, 0]` (model geometric center). Camera position centered on X axis `[0, Y, Z]` — never offset laterally
- `cloneAndPrepare()` centers model at origin via bounding box — camera target must match. **Always re-compute bounding box AFTER scaling**, then center: `model.scale.setScalar(s)` → `new Box3().setFromObject(model)` → `model.position.sub(newCenter)`. Centering before scale causes the model to drift off-center.
- **Model scale**: use `targetScale = 3` (not 4) — gives breathing room in the container. With FOV 40 and camera Z ~6, the model sits comfortably centered with margin on all sides
- **Camera FOV**: use 40 (not 35) — wider FOV ensures the full model is visible even in constrained landscape containers. Camera Y MUST be 0 for true vertical centering
- **OrbitControls polar angle**: `maxPolarAngle` must be `Math.PI / 2` (horizontal). Values like `PI/2.2` clamp the camera above horizontal and silently push the model to the top of the frame — this is the #1 cause of "model not centered" bugs
- **Landscape container sizing**: use `max-width: min(Npx, Nvh)` so width scales proportionally with viewport height. Prevents stretched/distorted containers. E.g. `max-width: min(500px, 75vh)` for pipeline, `min(400px, 60vh)` for demo
- Constrain height: `max-height: 50vh` in landscape, `aspect-ratio: 4/3` on mobile portrait
- **Never float CTAs over 3D viewers** — looks messy. Keep buttons in normal flow; make layout compact enough by hiding description text and tightening gaps
- Add responsive FOV in ResizeObserver: increase FOV slightly when container aspect > 1.6 in landscape
- Pause render loop when off-screen (IntersectionObserver)
- `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` — cap at 2x

**Touch navigation:**
- Disable programmatic touch swipe nav on mobile/landscape — let native scroll handle it
- Detection: `if (window.innerWidth <= 768 || window.innerHeight <= 600) return;` in touch handler
- IntersectionObserver threshold: `0.15` on mobile (vs `0.5` desktop) — taller slides need lower threshold

**Two-column layouts:**
- Collapse to single column at 768px: `grid-template-columns: 1fr`
- Keep 2-col in landscape (width > 768px but height ≤ 500px)
- Media placeholders: `max-height: 250px` on mobile portrait

**General:**
- All `font-size` and `padding`/`gap` MUST use `clamp()` — never fixed px
- Test every slide at 375×812 (portrait) and 812×375 (landscape) minimum
- Progress bar stays on all viewports (thin, non-intrusive) — **must always use the client's most recognisable/dominant brand color as a gradient**. If the brand has a signature gradient (e.g. Yango's purple `#5510FF → #BE9BFF`), use that — not a secondary accent. `background: linear-gradient(90deg, [primary], [light])`. Never default to `var(--brand)` blindly if the client's hero identity is a different colour.

### Mobile "Best on Desktop" Banner

Every deck with interactive or scroll-snap features should include a **dismissible banner on mobile** nudging users to open on desktop for the full experience. This is not a blocker, just a gentle hint.

**Implementation:**
```html
<div class="desktop-banner" id="desktopBanner" role="note">
    <span class="desktop-banner-icon">[BRAND ICON]</span>
    <span class="desktop-banner-copy">For the full experience, open on desktop.</span>
    <button class="desktop-banner-dismiss" id="desktopBannerDismiss" aria-label="Dismiss">✕</button>
</div>
```

**Rules:**
- Only shows at `≤820px` width (mobile/tablet)
- Dismissible with `sessionStorage` persistence (doesn't reappear after closing in same session)
- Adds `padding-top: 42px` to body when visible so content doesn't hide behind it
- **Icon and colour must match the deck's brand accent** — not a generic star or generic colour. If the deck is for Lefties (gold star), use a gold star. If it's BOTOX (purple), use a purple element. Match the `--brand` variable.
- Mono font, uppercase, small (0.62rem), centred text
- Dark background (`--bg-primary` or brand dark), light text
- Reference: Lefties Trio Hunt deck

### Mobile Validation Checklist

**Run this checklist on EVERY deck before delivery.** Use the preview tool to resize to each viewport.

**1. Portrait phone (375×812):**
- [ ] No horizontal scroll (`body.scrollWidth === window.innerWidth`)
- [ ] All text readable without zooming (minimum effective ~14px)
- [ ] No content clipped at edges — check right edge especially
- [ ] Cards stack single-column (no orphan 2+1 rows)
- [ ] Nav dots hidden
- [ ] Scroll-snap disabled — free vertical scroll works
- [ ] All slides reachable by scrolling
- [ ] 3D viewers (if any) render and don't block scroll
- [ ] CTA button/link tappable (min 44×44px touch target)
- [ ] Title slide logo fits within viewport

**2. Landscape phone (812×375):**
- [ ] No horizontal scroll
- [ ] Scroll-snap disabled — free scroll works
- [ ] Nav dots hidden
- [ ] 2-column grids fit (no clipping on right edge)
- [ ] 3-card grids: either fit 3 across or gracefully stack
- [ ] 3D viewers don't consume entire viewport (max-height capped)
- [ ] Headings readable (not too large, not too small)
- [ ] "Powered by" / footer text visible or gracefully hidden

**3. Per-deck assessment:**
- Decks with **3D viewers**: heavier — disable touch swipe nav, lower observer threshold, cap viewer heights
- Decks with **many slides (10+)**: hide nav dots on all mobile — too many dots
- Decks with **video**: lazy-load, compress to <5MB, verify autoplay with `muted playsinline`
- **Standard text/card decks** (≤8 slides, no 3D): nav dots can stay on tablet (768px+), simpler responsive needed
- Decks with **background pseudo-elements** extending beyond viewport: MUST use `overflow-x: clip` on slides

### Animated Brand Elements

Every deck should include **animated product/brand imagery** that flies into slides as they become visible. This brings slides to life and reinforces brand presence throughout the presentation.

**CSS classes:**
- `.brand-float` — base class: `position: absolute; pointer-events: none; z-index: 1; opacity: 0;` with transition on opacity + transform
- `.from-right` — flies in from the right with slight rotation
- `.from-left` — flies in from the left with slight rotation
- `.from-bottom` — rises up from below with scale
- `.hover-drift` — after appearing, gently bobs with `@keyframes brand-drift` (4s infinite alternate, translateY -12px)
- `.delay-1` / `.delay-2` / `.delay-3` — stagger entrance timing (0.3s / 0.6s / 0.9s)
- `.hide-mobile` — hide on viewports below 768px to prevent clutter

**Rules:**
- Use `drop-shadow` on images for depth, tinted to the client's brand accent
- Position floating elements in corners/edges so they don't overlap text content
- Use `clamp()` for width sizing so elements scale between viewports
- During Phase 1R brand research, actively source product cutout images (transparent PNG) — product shots, app icons, device renders
- Never repeat the same image on adjacent slides — alternate between product variants or angles
- Max 1-2 floating elements per slide — don't overload
- All floating elements trigger on `.slide.visible` (IntersectionObserver), same as `.reveal`

**Where to use:**
- Slide 2 (Your World) — client's hero product, fly from right
- Slide 3 (Challenge) — product variant or contextual image, from left or bottom
- Slide 4 (The Shift) — product accent, from bottom
- Idea slides — optional if media placeholder already provides visual weight
- Investment / CTA slides — optional small accent

### Quality Bar

The final proposal must:
- Feel like a **$10K agency deliverable**
- Show deep understanding of the prospect's brand
- Build emotional momentum through the narrative
- Make FRXME feel inevitable, not optional
- Be visually rich — brand imagery, media placeholders, atmospheric texture on every slide
- Match the client's own visual identity (light or dark)
- Work as a standalone shareable piece
- Be fully responsive across mobile, tablet, and desktop (see Responsive Rules above)

After generating, proceed to Phase 5 (Deliver).

### Brand Integrity Checklist

**Every proposal must pass these checks before delivery. Brand elements are the client's identity — getting them wrong destroys credibility instantly.**

**Logos & brand marks:**
- Verify every logo renders correctly — not flipped, stretched, cropped, or distorted
- Open the deck and visually confirm each logo at every location it appears (title slide, cobrand bar, 3D model)
- If a logo appears on a 3D model, do NOT apply UV flips (`repeat.set(1,-1)`) by default — test first, only flip if the GLB's UVs are proven inverted for that specific mesh
- Client logos must use the exact asset they provide or that's sourced from their official channels — never approximate or recreate

**Colors:**
- Extract exact hex/RGB values from the client's website — don't eyeball or approximate
- Test brand colors against both light and dark backgrounds to ensure contrast
- Brand accent color should be consistent across: CSS variables, 3D lighting, screen dashboard, ambient orbs, tag pills, gradient overlays

**Typography & naming:**
- Spell the client/product name exactly as they do (capitalization, spaces, special characters)
- Double-check every instance — title slide, cobrand bar, slide content, 3D model logo, meta tags
- **Never use em dashes (—) or hyphens as punctuation in client-facing content.** They are a dead giveaway of AI-generated copy. Instead of `"X - Y"` or `"X — Y"`, rephrase: use a period for a hard break, a comma for a soft join, a colon to introduce a list or explanation, or restructure the sentence entirely. Think like an agency copywriter. The only acceptable hyphen is in `<title>` / `og:title` as a brand separator (e.g. `"SHXFT Studio - Client Proposal"`). Code comments are exempt.

**Vibe-coded tells — hard bans vs conditionals:**

Hasan can instantly spot AI-generated work. But the signal isn't structure — it's authenticity and execution. Distinguish hard bans (always bad) from conditionals (fine if executed with real content).

**HARD BANS (always bad, no exceptions):**

*Copy:*
- Banned words (extend the filler list): scroll-stopping, share-worthy, built to convert, level up, next-level, reimagine, redefine, revolutionize, supercharge, harness, built with intention, designed with care, game-changer, master it
- "Sound familiar?" rhetorical opener
- "Where X becomes Y" hollow headline formula
- "Built for Impact / Built for X" hollow positioning
- Selling "AI" as the feature instead of selling the outcome
- "transform" / "immersive" when not actually XR/VR
- "Made with ❤️ / 💚 for [community]" forced emotional footer

*Visuals:*
- **Lucide icons (any form)** — the #1 visual AI tell in 2025-26. Don't reference `lucide.min.js`, don't use `data-lucide=`, don't copy-paste Lucide source `<path d="...">` snippets into inline SVG. Every shadcn/v0/Cursor template uses Lucide. Recognisable instantly. Use **custom hand-drawn SVG in brand accent color** instead — they take 10-30 lines, no dependency, fully on-brand. The deck linter (`scripts/lint-deck.py`) catches both the library and known Lucide paths. (Lucide is fine on internal tools like CNQR OS — it's a tell only on client-facing decks/sites.)
- **Emoji on stat / data / metric tiles** — instant AI-template tell. Custom monoline SVG icons in the brand accent color cost nothing and read premium. Reserved for: data tiles, KPI cards, stat boxes, "what you get" grids.
- **Emoji as decorative section dividers / random sprinkles** — nope. If it's not functional, cut it.
- **Functional emoji on step / journey lists IS OK** — when an emoji genuinely helps the reader scan a multi-step process (📷 capture, 📱 share, ✉ email), it's earning its place. But: pick emoji that fit the brand tone. Heritage / luxury / B2B-finance briefs prefer monoline SVG even on journey lists. Playful / consumer / hospitality briefs can lean on emoji.
- Broken placeholder logos (`![Ref 1]`, grey squares)
- "Trusted by" grids with brands you haven't worked with
- Initials-only testimonials ("A", "M", "G") with identical 5-star formatting
- Raw shadcn/Tailwind defaults unchanged — default violet/indigo on black, stock Lucide icons, stock cards, untouched mesh/aurora backgrounds

**CONDITIONAL (fine if executed with real content + brand specificity):**

These are NOT inherently vibe-coded — they're standard patterns that work when the execution is authentic.

| Pattern | Vibe-coded | Good |
|---------|-----------|------|
| Stat boxes | "100+ Projects, 20+ Countries, 4K Resolution" | "55K+ interactions at Soundstorm 2025" |
| Numbered cards 01-06 | Identical grey card + h3 + p | Editorial type, asymmetric sizes (FRXME deck) |
| "How It Works" | 3 generic circles, vague 3-word steps | Brand voice, specifics, or renamed |
| Hero pill + 2 CTAs | Generic pill + motivational headline | Specific pill + specific headline |
| Testimonials | Initials, 5 stars, identical | Real name + role + company + quoted outcome |
| Free/Pro/Max pricing | Generic with "Popular" ribbon | Fine if matches actual product structure |
| Glassmorphism + dark + accent | Default tailwind violet on black | Brand palette (CNQR blue, FRXME teal) |
| Logo grid | Google/Meta/Amazon you haven't served | Only real clients (CNQR site has 21 real partners) |

**The real signal (what separates good from vibe-coded):**
1. **Content authenticity** — real logos, real names, real numbers, real voice
2. **Visual specificity** — custom icons (not emoji, not raw Lucide), unique type pairings, brand palette
3. **Editorial intention** — asymmetry, hierarchy, breathing room (not perfect grids)
4. **Copy voice** — specific > abstract ("Dubai-native sports agency" beats "empowering brands")

**Reference sites NOT to ship:** discoverin360.com, groundedlabs.io, scorper.ai, groundedlabs.io/products.
**Reference sites that use similar patterns well:** cnqrmedia.com build (real partners, editorial asymmetry), FRXME Decks (real case study metrics, custom 3D).

Full master checklist in memory: `feedback_vibe_coded_sites.md`.

**Product language:**
- **NEVER call FRXME a "kiosk" in client-facing content.** Always use "interactive display", "FRXME display", or just "FRXME". "Kiosk" sounds generic and cheap — the product is premium. This applies to: deck slide copy, meta descriptions, OG tags, email copy, everything a client sees. "Kiosk" is acceptable only in internal notes and CLAUDE.md.

**3D model brand elements:**
- The `logo_plane` / `m_logo` mesh in the GLB uses the logo texture — always visually verify after applying the material
- The screen dashboard texture must use brand colors, not leftover defaults from a previous proposal
- Camera position must show the device centered and fully visible (no cutoff at edges/bottom)
- When scroll-snap is used, initialize the renderer with fallback dimensions (`canvas.clientWidth || 500`) because the canvas may be off-screen at load time — and use an IntersectionObserver to force resize when the slide scrolls into view

**Product imagery:**
- Floating brand elements must use real product images, correctly oriented
- Verify downloaded images are the right format (CDNs sometimes serve `.webp` with wrong extension — check with `file` command)
- Large images (>2MB) must be resized before use

**Pre-delivery visual sweep:**
- Scroll through every slide in the browser and visually confirm all brand elements
- Check the 3D model from multiple angles (wait for auto-rotation or drag)
- Verify on both desktop and mobile viewports

---

## Phase 4 — Convert Existing Deck

For `.pptx` files:
1. Run the extraction script: `python ~/.claude/skills/deck/scripts/extract-pptx.py input.pptx [output_dir]`
2. This produces `extracted-slides.json` + extracted images in `assets/`
3. Review the JSON, map content to slides
4. Proceed to Phase 2 (style selection) → Phase 3 (generation)

For Google Slides links:
1. Ask the user to export as `.pptx` (File → Download → .pptx), OR
2. View the published slides in browser and extract content manually
3. Proceed to Phase 2 → Phase 3

**Important:** When converting, preserve the original content structure but upgrade the visual design. Don't lose information.

---

## Phase 5A — Hard Linter Gate (MANDATORY before any push)

Before `git add` / `git commit` / `git push` of ANY proposal deck, run **both** linters and confirm exit code 0 on each:

```bash
python3 ~/.claude/skills/deck/scripts/lint-deck.py /full/path/to/index.html
python3 ~/.claude/skills/copy/scripts/lint-copy.py /full/path/to/index.html
```

`lint-deck.py` catches deck-structural and visual AI tells. `lint-copy.py` (from the `/copy` skill) catches copy-level AI tells and house-voice drift. Both must exit 0. If either non-zero, do NOT push. Read every flagged line, fix the issue, re-run both. Repeat until clean.

`lint-deck.py` catches things memory rules can't reliably catch:
- Banned filler words and vibe-coded copy
- Em-dashes and double-dashes (Hasan's hard ban)
- "Kiosk" used in any client-facing context (FRXME is a display, never a kiosk)
- Decorative emoji on stat / data tiles
- Lucide path tells (copy-pasted shadcn icons)
- Duplicate section labels (data-title attr matching the in-content mono-label)
- Known AI-tell card patterns (e.g. `border-left: 3px solid var(--brand)` + numbered tile)
- Missing OG image, missing favicon, "kiosk" in copy, gitignored video files

`lint-copy.py` catches things the deck linter can't see:
- The full ban lexicon from `~/.claude/skills/copy/references/ai-tells-hard-bans.md` (unlock, elevate, leverage, seamless, foster, robust, cutting-edge, best-in-class, holistic, tapestry, revolutionize, curate, harness, embark, delve, and 30+ more)
- Structural AI tells: adverbial-semicolon coupling, bold-header-colon inline lists, present-participle closer tags, vague-authority attribution ("industry reports suggest," "studies show")
- Banned openers: "Introducing," "Discover," "Experience the," "In today's landscape," "Picture this," "Now imagine," "Simply put," "Whether you're X or Y," "Additionally / Moreover / Furthermore" as sentence-openers
- Banned closers: "The result?" "The takeaway?" "Sound familiar?" "Enter [product]," "That's where [product] comes in"
- Soft flags (surface, don't block): uniform sentence length (low burstiness), ascending-tricolon overuse, "not X, it's Y" used more than once per deck, hedge stacks

**Third pass — impeccable design detectors (added 2026-07-18):** after both linters exit 0, run the `/impeccable` skill's deterministic detector CLI against the built HTML (no-LLM, one command; see `~/.claude/skills/impeccable/` for invocation). It catches visual AI-design tells the deck linter misses (icon-tile-above-heading, gray-on-color text, cards-in-cards, purple-gradient defaults). Fix hard hits; treat style-preference flags with judgment since decks follow the CLIENT's locked brand, not the detector's taste.

**Both linters are the last guard between a sloppy deck and the client.** Past sessions have shipped broken patterns because either linter wasn't run. Don't repeat that.

If a flagged item is intentional and shouldn't be flagged in future, propose adding an exception to the relevant linter (Phase 5B Step 3). Don't silently override.

---

## Phase 5 — Deliver

### OG Meta Tags (Required on all proposals)

**MANDATORY: OG image and metadata must be generated and committed as part of every proposal build. Never defer to "later" or offer to skip.** Proposals are shared via WhatsApp and LinkedIn in the MENA region. A link without a clean preview thumbnail looks unprofessional and kills click-through. Generate the OG image immediately after the deck HTML is complete, before the first push.

Every proposal HTML file must include these in `<head>` for clean WhatsApp/Twitter/iMessage link previews:

```html
<meta property="og:type" content="website" />
<meta property="og:title" content="[Brand] — [Client] Proposal" />
<!-- e.g. "SHXFT Studio — Yango Yasmina Proposal" or "FRXME — King's College Hospital Proposal" -->
<meta property="og:description" content="[One-line summary of what's being proposed]" />
<!-- e.g. "A full-spectrum experiential strategy for Yango Yasmina's Dubai launch." -->
<meta property="og:url" content="https://proposal.[domain]/[slug]" />
<meta property="og:image" content="https://proposal.[domain]/[slug]/og-image.jpg" />
<meta name="twitter:card" content="summary_large_image" />
```

**OG image (`og-image.jpg`):**
- Size: 1200×630px
- **NOT a screenshot of the live deck.** The OG image must be a clean title card with zero deck UI — no progress bar, no nav dots, no scroll indicators, no loading spinners. Just the core title slide content on the deck's background gradient.
- **How to create:** Build a standalone `og-capture.html` (gitignored) sized exactly 1200×630 with only: `[ PROPOSAL ]` label, client logo, divider, "POWERED BY" + parent brand wordmark, date. Subtle decorative particles are fine. Match the deck's background gradient and typography exactly.
- **Capture at 1x:** Use headless Chrome at 1x (do NOT use `--force-device-scale-factor=2`, it creates a white bar artifact). Capture as PNG, then crop to exact 1200×630 with PIL and convert to JPG at quality 92.
- **Default: clean framing with no bar.** A clean 1200×630 capture with no artifacts is the goal — this works on most projects.
- **BACKUP ONLY — accent bar hack:** If Chrome headless produces a visible white strip at the bottom (known rendering artifact on some setups), paint a 5px brand gradient bar at the very bottom using PIL to turn the artifact into an intentional design element. Use the client's brand gradient, or fall back to `#5510FF → #018ad2 → #5bbce6`. This is a last resort, not the default.
- Command: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --screenshot=og-raw.png --window-size=1200,630 --hide-scrollbars --virtual-time-budget=5000 --run-all-compositor-stages-before-draw "http://localhost:PORT/og-capture.html"` then use PIL to crop to 1200×630, optionally paint accent bar, save as JPEG quality 92.
- Clean up: delete `og-raw.png` after. The `og-capture.html` stays gitignored for future re-captures.
- If skipped for now: use a simple branded fallback — just omit `og:image` line rather than point to a broken URL.

**Title format rules:**
- SHXFT proposals: `"SHXFT Studio - [Client] Proposal"`
- FRXME proposals: `"FRXME - [Client] Proposal"`
- SCXPE proposals: `"SCXPE - [Client] Proposal"`

### Favicon + Apple Touch Icon (Required on all proposals)

Every proposal must include the correct brand favicon as both a standard favicon and an Apple touch icon. Add these in `<head>`:

```html
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="favicon.png">
```

**Favicon per brand domain:**
- `proposal.shxft.studio` → SHXFT X icon (`SHXFT_Favicon.png`, 512×512)
- `proposal.frxme.co` → FRXME icon (use existing `frxme-favicon.png`)
- `proposal.scxpe.co` → SCXPE icon (use existing SCXPE favicon)

**Setup:** Copy the correct brand favicon into the proposal folder as `favicon.png`. Also keep a copy at the repo root so it serves as the default for any path that doesn't have its own. The apple-touch-icon ensures the favicon shows correctly when saved to home screen on iOS.

1. Save the final `.html` file
2. **Run the linter — MANDATORY before showing the deck to the user.** Catches AI-template tells (em dashes, banned filler/vibe words, "kiosk", decorative emoji on stat tiles, placeholders left in copy):
   ```bash
   python3 ~/.claude/skills/deck/scripts/lint-deck.py /path/to/index.html
   ```
   - **Errors (✗)** are blocking. Fix every one before delivery — em dashes, banned filler, "kiosk", placeholders left in copy.
   - **Warnings (⚠)** are review-required. Decorative emoji on stat tiles (replace with custom monoline SVGs in brand color), soft flags ("transform"/"immersive" outside literal AR/VR contexts).
   - Only after the linter prints `✓ Clean` (or all warnings have been deliberately accepted) should you tell the user the deck is ready.
3. Tell the user the filename and how to open it (`open filename.html` in terminal)
4. Capture `og-image.jpg` (see OG image rules above) and place it in the same folder
5. Offer to make adjustments:
   - "Want me to tweak any slides?"
   - "Should I adjust the color scheme or typography?"
   - "Need a different animation style?"
6. **Ship it**: Once the user is happy, deploy directly:
   1. Ask: "What slug do you want for the URL? (e.g. `botox-hk` → `proposal.shxft.studio/botox-hk`)"
   2. **Slug must be lowercase, hyphenated, ASCII only.** Cloudflare Pages serves URLs case-sensitively, and the OG/canonical meta tags assume lowercase. A folder named `DGDA` produces a 404 at `/dgda/` and only resolves at `/DGDA/` — fragile, ugly to share, and breaks the OG image preview. If the user types an uppercase or mixed-case slug, silently lowercase it before creating the folder. Hyphens not underscores. No spaces. No accents.
   3. Ensure the folder is named with that lowercased slug under the correct brand directory:
      - SHXFT proposals: `~/Documents/CLAUDE PROJECTS/PROPOSALS/SHXFT/[slug]/`
      - FRXME proposals: `~/Documents/CLAUDE PROJECTS/PROPOSALS/FRXME/[slug]/`
      - SCXPE proposals: `~/Documents/CLAUDE PROJECTS/PROPOSALS/SCXPE/[slug]/`
   4. Run: `cd [brand folder] && git add [slug]/ && git commit -m "feat: [client] proposal" && git push`
   5. Cloudflare Pages auto-deploys in 30-60 seconds
   6. Confirm to user: "Live at `proposal.[domain]/[slug]`"
   7. No separate `/ship` skill needed — this is the deploy workflow.
   8. **Ask about OS sync**: "Want me to add this as a proposal in CNQR OS? That way you can track views, link it to a deal/contact, and manage status." If yes, POST to `https://os.cnqrmedia.com/api/proposals` with Bearer token `API_SECRET_KEY` from `.env`:
      ```json
      {
        "title": "[Client] × [Product]: [Concept]",
        "workspaceId": "[the CNQR Media workspace id, look up or ask once]",
        "url": "https://proposal.[domain]/[slug]",
        "deckType": "SHXFT" | "FRXME" | "SCXPE",
        "htmlPath": "[slug]"
      }
      ```
      This creates a DRAFT proposal. User can then open OS to enrich with deal/contact, change status to SENT when they've sent it, and track views. If the user says no, skip silently.

---

## Mid-build — Capture Corrections in Real Time

Do NOT wait until end-of-deck to remember what the user corrected. Lessons captured later get lost or watered down. The moment a correction lands, decide whether it's a durable rule.

**Trigger phrases — when the user says any of these, pause and log:**
- "no, don't" / "stop doing X" / "remove X" / "I don't like X"
- "you didn't ask me before doing that" / "did you run this by me?"
- "X is bad / not nice / so bad"
- "didn't I tell you this before?" / "this happened last time"
- "actually" / "wait, no" / "scratch that"
- "yes exactly / perfect / keep doing that" (positive — capture validated approaches too)

**For each correction, classify it:**

| Class | Where it lives | Example |
|---|---|---|
| Universal rule | New `feedback_*.md` memory in `~/.claude/projects/-Users-hasanshah-Documents-CLAUDE-PROJECTS/memory/` + index in `MEMORY.md` | "Never add CSS animations to placeholders without asking" |
| Per-client lesson | Append to `knowledge/[slug].md` under "Corrections" | "QM specifically: contemporary brand colours dominate, treat their bright primary palette as the hero" |
| Skill rule | Add to relevant section of this SKILL.md + log in [changelog.md](changelog.md) | "Video pre-flight checklist before any embed" |
| Linter rule | Add a check to `scripts/lint-deck.py` so it's machine-enforced not memory-enforced | "Flag `border-left: 3px solid var(--brand)` + numbered card combo as AI vibe-coded tell" |

**Do not log silently.** Surface the proposed entry to the user in one line and confirm:

> "Logging: 'Always re-encode user-provided videos with silent audio track even if size is fine — surprise sound on a deck = bad meeting.' Save to memory + skill?"

If yes, write it. If no, drop it. Either way: keep moving on the deck.

The longer you wait to capture a correction, the lower the chance it survives compaction or context-rotation. Real-time logging > end-of-session reflection.

---

## Phase 5B — Post-Delivery Reflection (Self-Learning, MANDATORY)

After every deck push (live URL deployed, user satisfied), perform these steps. This is not optional. Skipping Phase 5B is the #1 reason the skill fails to compound.

### Step 1 — Write/update `knowledge/[slug].md`

Mandatory contents:
- **Client meta:** name, industry, deck type, live URL, date built, who attended the call (if known)
- **Brief summary** parsed from intake — the actual ask, in 2-3 sentences
- **Concepts pitched + status:** name, one-liner, kept/dropped/replaced (and why)
- **Strategic foundation:** if a `/cs` strategy doc was used, link to its path and quote its tension + insight + platform line
- **Visual decisions:** palette, font choices, photography direction, anything decided mid-build
- **Mid-build corrections:** every correction logged via the Mid-build process above, copied verbatim into a "Corrections from this session" subsection
- **OS feedback merged in:** if `fetch-feedback.sh` returned ProposalFeedback entries, summarise them at the bottom under "Past OS feedback applied"
- **Open questions for follow-up:** anything Hasan flagged as "address tomorrow" or "we'll revisit"
- **Outcome (if known yet):** sent / viewed / accepted / declined + any client quotes

### Step 2 — Update `knowledge/_index.md`

Add a row: `| slug | Client | Industry | Deck Type | Status | Date | Concepts |`. Status starts as `BUILT` (or `SENT` if `/ship` was used). Updates to `VIEWED` / `ACCEPTED` / `DECLINED` as the proposal-tracker Worker reports back.

### Step 3 — Propose new universal rules

Review the conversation:
1. Scan for trigger phrases (see Mid-build section above) you may have missed in real-time
2. Scan for approaches the user explicitly validated ("perfect", "yes exactly", "that's the move")
3. For each, classify universal-rule / client-specific / skill-rule / linter-rule

Surface the proposals as a numbered list:

> "End-of-build review — 3 proposed rule additions:
> 1. Memory: 'Never reuse mockup illustrations across decks — each client's concept slots either get a real video reference or stay as empty `.media-placeholder`.' (universal)
> 2. SKILL.md Phase 1P: 'When a logo file is dropped into assets/, generate the white/dark variants needed for 3D model + dark slides BEFORE asking next question.' (skill rule)
> 3. lint-deck.py: 'Flag any `<rect class*=mockup-block>` SVG inside a concept slide as an illustrated placeholder.' (linter rule)
> Save which?"

Wait for the user's confirmation. Never add rules silently.

### Step 4 — Sync to CNQR OS ProposalFeedback

If the user can articulate a win-or-loss reason for this proposal yet, log it via the OS API so future `/cs` and `/deck` runs can pull it. Tags MUST include `vertical:X`, `market:Y`, plus optional `client:Z`. The OS feedback is the cross-skill compounding layer — both /cs and /deck read from it at brief intake.

If the proposal is too fresh to know, set a follow-up reminder for 7-14 days out.

### Step 5 — Record outcome when known

When the user later reports outcome (accepted, declined, ghosted, ROI numbers):
1. Update `knowledge/[slug].md` outcome section + any client quotes verbatim
2. Update `knowledge/_index.md` status column
3. Push the win/loss reason to CNQR OS ProposalFeedback API (Step 4 above)
4. If a `/cs` strategy foundation was used, update `STRATEGIES/[slug]/` with the outcome too

Over time, this builds a win/loss database that informs every future proposal across both skills. **The skill gets smarter automatically — but only if Phase 5B actually runs.**

---

## Video Handling — Compression & Mobile Loading

**CRITICAL: Videos MUST be committed to git.** Never gitignore video files (`*.mp4`, `*.mov`, etc.) in proposal repos. If `.gitignore` blocks video files, remove those rules immediately. Videos that aren't in git won't deploy to Cloudflare Pages and the live site will show broken/empty video containers. Before pushing any proposal with videos, always verify: `git ls-files "folder/*.mp4"` returns the files. If it returns nothing, the videos aren't tracked — fix the `.gitignore` and `git add` them.

When a deck includes video content, follow these rules to ensure reliable playback on all devices including iOS Safari.

### Video Pre-flight Check — RUN ON EVERY VIDEO BEFORE EMBED

**Mandatory.** When the user drops a video into an assets folder for use in a deck, you MUST verify it matches the deck-video standard BEFORE wiring it into any slide. Surprise audio, non-baseline profiles, fractional fps, missing faststart, odd dimensions — all silently break autoplay or playback on iOS Safari, embedded webviews, or low-end Android. The deck looks broken and the client thinks the studio is sloppy.

**Step 1 — probe with ffprobe:**

```bash
/opt/homebrew/bin/ffprobe -v error -show_entries stream=codec_name,profile,width,height,r_frame_rate,pix_fmt,channels:format=duration,size -of default=noprint_wrappers=0 PATH/TO/VIDEO.mp4
```

**Step 2 — pass/fail checklist:**

| Check | Required | Re-encode if not |
|---|---|---|
| Video codec | `h264` | Yes |
| Profile | `Baseline` or `Constrained Baseline` (NOT High, NOT Main) | Yes |
| Pixel format | `yuv420p` | Yes |
| Frame rate | exactly `30/1` (force normalised — NOT 29.97, 24, 60, etc) | Yes |
| Width × Height | both even (mod 2 = 0) | Yes |
| Audio | **silent** stereo AAC track (NEVER live audio on a deck reference video) | Yes |
| Faststart | moov atom at start (test with `ffprobe -show_format ... \| grep -i moov_at_start` if uncertain — easier: just always re-encode with `+faststart`) | Yes |
| File size | <5 MB ideally, <8 MB acceptable | Re-encode at higher CRF |

**Step 3 — canonical re-encode (handles every failure case at once):**

```bash
/opt/homebrew/bin/ffmpeg -y -hide_banner -loglevel error \
  -i input.mp4 \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -map 0:v:0 -map 1:a:0 \
  -c:v libx264 -profile:v baseline -level 3.0 -pix_fmt yuv420p -r 30 \
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
  -crf 23 -preset slow -movflags +faststart \
  -c:a aac -b:a 64k -shortest \
  output_web.mp4
```

What each piece does:
- `-f lavfi -i anullsrc...` + `-map 1:a:0` — generates a silent stereo audio track and uses it INSTEAD of the source audio. Source audio is dropped entirely. Required because (a) browsers throttle/block autoplay if audio policy is uncertain, (b) sound from a deck video during a meeting is jarring.
- `-profile:v baseline -level 3.0` — maximum decoder compatibility. iOS Safari, Android stock browsers, Chromium webviews all decode baseline reliably. High/Main profiles can stutter or fail on older devices.
- `-r 30` — forces exactly 30fps. Phones recorded at 29.97 or 60 will be normalised. Variable framerate sources will be made constant.
- `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"` — rounds both dimensions to even numbers. h264 requires even dims; odd-pixel sources fail the encode otherwise.
- `-crf 23 -preset slow` — sweet spot for quality/size on portrait phone clips. Bump to `-crf 26` if file lands over 8MB.
- `-movflags +faststart` — moov atom at the start. Without this, the browser must download the whole file before playback begins.
- `-shortest` — caps audio length to the video length (the silent anullsrc would otherwise be infinite).

**Step 4 — verify the re-encode:**

```bash
/opt/homebrew/bin/ffprobe -v error -show_entries stream=codec_name,profile,r_frame_rate,pix_fmt,channels:format=duration,size -of default=noprint_wrappers=0 output_web.mp4
```

Confirm: profile=Baseline (or Constrained Baseline), r_frame_rate=30/1, pix_fmt=yuv420p, channels=2 (silent), size sane.

**Step 5 — overwrite the original.** Move the re-encoded file into the original filename (`mv output_web.mp4 original_name.mp4`) so the deck markup keeps a clean asset path. Don't ship a `_web` suffix in production.

**Failure mode to guard against:** stream-copy or remux (`-c copy`) does NOT fix any of these issues. It just re-wraps the container. ALWAYS re-encode in full when any check fails. Flagged as a hard rule in `feedback_video_compression.md`.

### Video Compression — Bulk Compression for Reference Footage

If the source video is fine on the pre-flight checklist but oversized (>8MB), use the lighter compression command:

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset slow -vf "scale='min(1080,iw)':-2" -an -movflags +faststart -y output_mobile.mp4
```

- `-crf 28` balances quality and size (24-30 is the sweet spot)
- `-an` strips audio (use this only when source already passed the pre-flight; otherwise use the canonical re-encode in Step 3 above which handles silent-audio insertion explicitly)
- `-movflags +faststart` moves metadata to the front so playback can begin before full download

### Video HTML Attributes

Every `<video>` element must include:
```html
<video muted loop playsinline webkit-playsinline preload="none" data-src="video_mobile.mp4"></video>
```
- `muted` — required for autoplay on iOS
- `playsinline` + `webkit-playsinline` — prevents iOS fullscreen takeover
- `preload="none"` — don't load until needed (lazy loading via JS)
- `data-src` instead of `src` — JS copies it to `src` when the slide is visible

### Reference Videos on Concept Slides — Protected Embed Pattern

**Never use `controls` on reference videos.** No fullscreen button, no unmute option, no scrubber — videos autoplay silently and loop only. Use the `.ref-video-wrap` class for the container to get the hover glow effect:

```css
.ref-video-wrap {
    position: relative; border-radius: 16px; overflow: hidden;
    height: min(60vh, 500px); aspect-ratio: 9/16; max-width: 100%;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease;
}
.ref-video-wrap:hover {
    transform: scale(1.03);
    box-shadow: 0 8px 40px rgba(var(--brand-rgb), 0.28), 0 0 30px rgba(var(--brand-rgb), 0.14);
}
```

```css
.video-label {
    position: absolute; bottom: 0; left: 0; right: 0;
    padding: 6px 10px;
    background: linear-gradient(0deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 60%, transparent 100%);
    font-family: var(--font-mono); font-size: clamp(0.5rem, 0.9vw, 0.65rem);
    letter-spacing: 0.1em; text-transform: uppercase;
    color: rgba(255,255,255,0.8); border-radius: 0 0 16px 16px;
    pointer-events: none;
}
```

```html
<div class="ref-video-wrap">
    <video src="FILENAME.mp4" autoplay muted loop playsinline webkit-playsinline disablePictureInPicture disableRemotePlayback
        style="width: 100%; height: 100%; object-fit: cover; display: block; pointer-events: none;"></video>
    <div style="position: absolute; inset: 0;"></div>
    <div class="video-label">Caption text here</div>
</div>
```

- Label sits inside the wrap — fades up from the bottom over the video, exactly like FRXME deck `.video-label` style. Never as a `<p>` below the video.
- Hover: slight scale-up (`1.03`) + brand-colored glow behind the video — matches the FRXME deck `.video-card:hover` style
- `pointer-events: none` on both the video and the label — no interaction
- Transparent `inset: 0` overlay — captures right-click, blocking "Save Video As" and hiding file names
- `disablePictureInPicture` + `disableRemotePlayback` — removes those browser UI options
- No `controls` attribute — ever

### Content Protection — Required on ALL Decks (All Presets)

**This is not optional.** Every deck, every preset (FRXME, SHXFT, SCXPE, proposals, enhances, converts) must include this as the last `<script>` before `</body>`. It protects logos, reference videos, brand assets, and file names from casual download or inspection:

### Favicon rule — CANONICAL SHXFT FAVICON FOR ALL `proposal.shxft.studio` DECKS

Every proposal under `proposal.shxft.studio/*` MUST use the canonical SHXFT favicon. There is exactly one correct file: `~/Documents/CLAUDE PROJECTS/SHXFT DECKS/SHXFT_Favicon.png` (37,950 bytes). Always copy this verbatim into each new proposal's root as `favicon.png`. Do not generate a custom favicon, do not use a brand-tinted variant, do not improvise. Reason: the favicon is a brand-consistency surface across the 20+ live proposals — divergent favicons read as not-quite-our-house.

```bash
cp "$HOME/Documents/CLAUDE PROJECTS/SHXFT DECKS/SHXFT_Favicon.png" \
   "$HOME/Documents/CLAUDE PROJECTS/PROPOSALS/SHXFT/[slug]/favicon.png"
```

The deck linter checks the favicon byte-size against the canonical (37,950 bytes) and flags any mismatch. If you genuinely need a custom favicon for a specific brand reason, override with `<!-- linter:allow-custom-favicon -->` near the favicon link tag and document the reason. Otherwise: copy the canonical file, don't think about it.

This rule is repeated from `feedback_shxft_favicon_consistency.md` memory because it has been violated three times to date (Halabi, Peace Homes, DGDA — the latter caught by Hasan post-deploy 2026-04-29). Mechanical enforcement in the linter, not just a memory rule.



```html
<script>
    document.addEventListener('contextmenu', e => e.preventDefault());
    document.addEventListener('dragstart', e => e.preventDefault());
    document.addEventListener('selectstart', e => e.preventDefault());
</script>
```

What each line does:
- `contextmenu` — blocks right-click everywhere: no "Save As", no "Inspect Element", no visible file names in the context menu
- `dragstart` — prevents drag-to-desktop of images, videos, and assets
- `selectstart` — blocks text selection (prevents copying slide copy or spotting asset paths)

### Lazy Loading Pattern (iOS-safe)

iOS Safari with `scroll-snap-type: y mandatory` often skips `IntersectionObserver` events. Use this multi-layer approach:

1. **IntersectionObserver** with very low threshold (`0.01`) and generous `rootMargin` (`50% 0px`)
2. **Scroll-settle fallback** — on scroll stop (debounced 100ms), manually check `getBoundingClientRect()` for all video slides
3. **Touchend fallback** — iOS sometimes doesn't fire scroll events with snap; check visibility 300ms after touchend
4. **Initial load** — on `DOMContentLoaded` + 500ms delay, load videos on the first visible slide
5. **Adjacent preload** — when a slide gets `.visible` class, preload videos on prev/next slides via `MutationObserver`

Key implementation detail: use `v.getAttribute('src')` not `v.src` to check if src is set — on iOS, `.src` returns the page base URL even when no `src` attribute exists.

### Loading Indicators

Add a CSS spinner to video containers that fades out on `canplay`:
```css
.video-card::after {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 28px; height: 28px;
    margin: -14px 0 0 -14px;
    border: 2px solid rgba(6, 182, 212, 0.2);
    border-top-color: rgba(6, 182, 212, 0.8);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    transition: opacity 0.3s;
}
.video-card.video-loaded::after { opacity: 0; }
```
Add `.video-loaded` class via JS when the video fires `canplay`.

---

## Form Security (Contact / Lead Capture Forms)

When any deck, landing page, or website includes a contact or lead capture form, apply ALL of these measures:

1. **Honeypot field** — hidden `website` input (position: absolute, off-screen). If filled, return fake success silently.
2. **Timing check** — record first field focus timestamp. If submitted in under 2 seconds, return fake success (bot detection).
3. **Client-side rate limit** — 30 seconds between submissions.
4. **Server-side rate limit** — 3 requests per minute per IP.
5. **Input sanitization** — strip HTML tags on both client and server: `str.replace(/<[^>]*>/g, '').trim()`
6. **Email regex** — `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` on both sides.
7. **Max lengths** — name: 100, email: 200, company: 200, message: 2000.
8. **CORS** — lock origin to the specific site domain.
9. **API keys** — env vars only, never in client code.
10. **Source tracking** — every form POST includes a `source` field (e.g. `SHXFT_SITE`, `FRXME_SITE`) for CNQR OS lead attribution.

**CNQR OS leads endpoint:** `/api/proposals/leads` (NOT `/api/leads`). Bearer token auth via `API_SECRET_KEY`. Env vars on site side: `CNQR_API_URL` (`https://os.cnqrmedia.com/api/proposals/leads`), `CNQR_API_KEY` (must match `API_SECRET_KEY`), `CNQR_WORKSPACE_ID`.

Reference implementation: `SHXFT SITE/components/ContactForm.tsx` + `SHXFT SITE/api/contact.js`

---

## Quick Reference

| What | Where |
|------|-------|
| Style definitions | [STYLE_PRESETS.md](STYLE_PRESETS.md) |
| Animation library | [animation-patterns.md](animation-patterns.md) |
| HTML skeleton | [html-template.md](html-template.md) |
| Viewport CSS | [viewport-base.css](viewport-base.css) |
| **Scroll + 3D mechanic (COPY VERBATIM)** | **[references/scroll-3d-mechanic.md](references/scroll-3d-mechanic.md)** |
| PPTX extractor | [scripts/extract-pptx.py](scripts/extract-pptx.py) |
| Proposal pricing & ROI | [proposal-pricing.md](proposal-pricing.md) |
| Brief templates | [brief-templates.md](brief-templates.md) |
| Knowledge base index | [knowledge/_index.md](knowledge/_index.md) |
| Skill changelog | [changelog.md](changelog.md) |
| Deploy & register | `/ship` command |
