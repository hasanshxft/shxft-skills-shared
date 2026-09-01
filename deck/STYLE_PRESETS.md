# Style Presets Reference

Curated visual styles for Deck presentations. Each preset has specific design DNA — no generic "AI slop" aesthetics. **Abstract shapes only — no illustrations.**

**Viewport CSS:** For mandatory base styles, see [viewport-base.css](viewport-base.css). Include in every presentation.

---

## Custom Styles

### 1. FRXME Dark

**Vibe:** Tech-forward, premium, immersive — the FRXME platform aesthetic

**Layout:** Content on dark background. Glassmorphism cards for key content. Grid/dot pattern backgrounds for depth.

**Typography:**
- Display: `Inter` (700/800)
- Body: `Inter` (400/500)
- Mono: `Geist Mono` or `JetBrains Mono` (400)

**Colors:**
```css
:root {
    --bg-primary: #09090b;
    --bg-surface: #18181b;
    --bg-muted: #27272a;
    --border: #27272a;
    --text-primary: #fafafa;
    --text-secondary: #a1a1aa;
    --text-muted: #71717a;
    --brand: #06b6d4;
    --brand-dark: #0891b2;
    --brand-light: #22d3ee;
    --brand-glow: rgba(6, 182, 212, 0.25);
    --brand-glow-strong: rgba(6, 182, 212, 0.4);
}
```

**Signature Elements:**
- Glassmorphism cards: `background: rgba(24, 24, 27, 0.8); backdrop-filter: blur(12px); border: 1px solid rgba(6, 182, 212, 0.15);`
- Glow pulse on key elements: `box-shadow: 0 0 20px var(--brand-glow);`
- Dot grid background pattern (subtle, 1px dots at ~40px intervals)
- Teal/cyan accent for headings, links, highlights, and borders
- Monospace labels in brackets: `[ PRODUCT ]`, `[ OVERVIEW ]`
- Staggered entrance animations with 150ms timing
- Radial gradient ambient glow behind hero content

**Card Pattern:**
```css
.glass-card {
    background: rgba(24, 24, 27, 0.8);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(6, 182, 212, 0.15);
    border-radius: 16px;
    padding: clamp(1.5rem, 3vw, 2.5rem);
    transition: all 0.15s ease;
}
.glass-card:hover {
    border-color: rgba(6, 182, 212, 0.3);
    box-shadow: 0 0 30px rgba(6, 182, 212, 0.15);
}
```

**Background Pattern:**
```css
.dot-grid {
    background-image: radial-gradient(circle, rgba(6, 182, 212, 0.15) 1px, transparent 1px);
    background-size: 40px 40px;
}
```

**Logo Assets** (located at `~/.claude/skills/deck/assets/frxme/logos/`):
- `frxme-logo-dark.png` — White text + teal frame → use on **dark** backgrounds
- `frxme-logo-light.png` — Black text + teal frame → use on **light** backgrounds

Place logo bottom-left or top-left, sized ~120-180px wide.

**FRXME Dark Brand Rules (follow these exactly):**
1. **Title/cover slide**: Use `frxme-logo-dark.png` as the hero element — centered, large. Do NOT type "FRXME" as text. No small logo on the title slide.
2. **All other slides**: Place `frxme-logo-light.png` bottom-left, small (~100-150px wide), at ~60% opacity.
3. **Monospace labels**: Use `[ SECTION NAME ]` labels in uppercase monospace (Geist Mono / JetBrains Mono) above each section heading.
4. **Glass cards**: Feature content in glassmorphism cards with teal border glow on hover.
5. **Dot grid**: Use the dot-grid background pattern on title and CTA slides. Other slides can use plain dark bg.
6. **Glow effects**: Apply teal glow (`box-shadow` / `text-shadow`) sparingly on key stats, CTAs, or hero elements.
7. **Staggered reveals**: All slide content should animate in with staggered delays (100-150ms between children).

---

### FRXME Dark — Battle-Tested Component Patterns

These patterns were refined building the FRXME product deck (product.frxme.co). Use these as the canonical implementations.

#### Section Divider Slides

High-energy divider slides with layered ambient effects. Use for section breaks ("THIS IS FRXME", "CASE STUDIES", etc.).

**Structure:** Centered massive text with 4 ambient layers behind it.

```css
/* 1. Glow Orb — radial gradient pulsing behind title */
.divider-glow-orb {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: clamp(250px, 40vw, 600px); height: clamp(250px, 40vw, 600px);
    background: radial-gradient(circle, rgba(6,182,212,0.15) 0%, rgba(6,182,212,0.05) 40%, transparent 70%);
    border-radius: 50%;
    animation: dividerGlowPulse 4s ease-in-out infinite;
    pointer-events: none;
}
@keyframes dividerGlowPulse {
    0%, 100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1); }
    50% { opacity: 1; transform: translate(-50%, -50%) scale(1.15); }
}

/* 2. Floating Particles — CSS custom properties for unique motion per particle */
.divider-particles { position: absolute; inset: 0; pointer-events: none; overflow: hidden; }
.d-particle {
    position: absolute;
    width: var(--d-size); height: var(--d-size);
    background: var(--brand); border-radius: 50%;
    box-shadow: 0 0 6px var(--brand-glow);
    animation: dParticleFloat var(--d-dur) var(--d-delay) ease-in-out infinite;
    opacity: 0;
}
@keyframes dParticleFloat {
    0% { opacity: 0; transform: translate(0, 0); }
    20% { opacity: 0.7; }
    80% { opacity: 0.5; }
    100% { opacity: 0; transform: translate(var(--d-dx), var(--d-dy)); }
}

/* 3. Scanline — horizontal line sweeping top to bottom */
.divider-scanline {
    position: absolute; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(6,182,212,0.4) 20%, rgba(6,182,212,0.6) 50%, rgba(6,182,212,0.4) 80%, transparent 100%);
    animation: scanlineMove 6s ease-in-out infinite;
    pointer-events: none; opacity: 0.5;
}
@keyframes scanlineMove {
    0% { top: 15%; opacity: 0; }
    10% { opacity: 0.5; }
    90% { opacity: 0.5; }
    100% { top: 85%; opacity: 0; }
}

/* 4. Title text — gradient fill with breathing glow */
.divider-title-glow {
    filter: drop-shadow(0 0 40px rgba(6,182,212,0.3));
    animation: titleGlowBreath 3s ease-in-out infinite;
}
@keyframes titleGlowBreath {
    0%, 100% { filter: drop-shadow(0 0 30px rgba(6,182,212,0.2)); }
    50% { filter: drop-shadow(0 0 60px rgba(6,182,212,0.45)); }
}
```

**HTML pattern** (use 6-8 particles with varied custom properties):
```html
<section class="slide" style="position: relative; overflow: hidden;">
    <div class="divider-glow-orb"></div>
    <div class="divider-particles">
        <div class="d-particle" style="left:10%;top:20%;--d-size:4px;--d-dur:6s;--d-delay:0s;--d-dx:60px;--d-dy:-80px;"></div>
        <div class="d-particle" style="left:75%;top:25%;--d-size:5px;--d-dur:5s;--d-delay:0.5s;--d-dx:-50px;--d-dy:-70px;"></div>
        <!-- 4-6 more with varied positions/sizes/speeds -->
    </div>
    <div class="divider-scanline"></div>
    <div style="position: relative; z-index: 2; text-align: center;">
        <span class="mono-label reveal">[ SECTION ]</span>
        <h1 class="reveal-scale divider-title-glow" style="font-size: clamp(3rem, 10vw, 8rem); font-weight: 900; letter-spacing: -0.04em; background: linear-gradient(135deg, #fafafa 30%, #06b6d4 70%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            SECTION<br>TITLE.
        </h1>
        <p class="reveal" style="font-family: var(--font-mono); font-size: clamp(0.65rem, 1vw, 0.85rem); color: var(--text-secondary); letter-spacing: 0.15em; text-transform: uppercase;">
            Subtitle text here
        </p>
    </div>
    <!-- Optional: trust markers at bottom -->
    <div class="reveal" style="position: absolute; bottom: clamp(60px, 8vh, 100px); display: flex; gap: clamp(2rem, 4vw, 4rem); opacity: 0.35;">
        <span style="font-family: var(--font-mono); font-size: clamp(0.55rem, 0.8vw, 0.7rem); letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-muted);">CLIENT ONE</span>
        <span>CLIENT TWO</span>
        <span>CLIENT THREE</span>
    </div>
</section>
```

**Tip:** Vary the glow orb gradient color per section. Case studies can use `rgba(168,85,247,0.06)` (purple tint). Give some particles alternate colors (`background:#a855f7`) for visual interest.

#### Video Card Labels

Persistent labels on video/image cards with gradient overlay. Used on case study slides.

```css
.video-card { position: relative; overflow: hidden; border-radius: 12px; }
.video-label {
    position: absolute; bottom: 0; left: 0; right: 0;
    padding: 6px 10px;
    background: linear-gradient(0deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 60%, transparent 100%);
    font-family: var(--font-mono);
    font-size: clamp(0.5rem, 0.9vw, 0.65rem);
    letter-spacing: 0.1em; text-transform: uppercase;
    color: rgba(255,255,255,0.8);
    border-radius: 0 0 12px 12px;
    pointer-events: none;
}
```

#### Case Study Slide Layout

Text on left, two video/image cards on right (staggered offset). Content area uses a 2-column grid.

```css
.case-study-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: clamp(2rem, 4vw, 4rem);
    align-items: center;
}
.case-study-images {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
}
/* Stagger second card down for visual depth */
.video-card:nth-child(2) { transform: translateY(1rem); }
/* Note: translateY offset prevents CSS hover scale — this is intentional.
   Left card scales on hover, right card highlights but stays in place. */
```

**Themed ambient backgrounds:** Each case study can have a unique warm ambient effect. For example, golden diagonal rays for a desert theme:
```css
.golden-ray {
    position: absolute; top: -20%; right: -10%;
    width: 60%; height: 140%;
    background: linear-gradient(135deg, transparent 0%, rgba(212,165,116,0.04) 30%, rgba(201,184,150,0.06) 60%, transparent 100%);
    transform: rotate(15deg); pointer-events: none;
    opacity: 0; transition: opacity 1.5s ease 0.3s;
}
.slide.visible .golden-ray { opacity: 1; }
```

#### Analytics / Dashboard Slide

Stat cards in a row + bar chart + donut chart below.

```css
/* Stat cards — 4 across */
.analytics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: clamp(0.5rem, 1.5vw, 1rem);
}
.stat-card {
    /* uses .glass-card base */
    padding: clamp(0.75rem, 1.5vw, 1.25rem);
}
.stat-number {
    font-size: clamp(1.5rem, 3vw, 2.5rem);
    font-weight: 800; color: var(--brand);
    font-variant-numeric: tabular-nums;
}
.stat-metric-label {
    font-family: var(--font-mono);
    font-size: clamp(0.5rem, 0.7vw, 0.6rem);
    color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.1em;
}
.stat-change {
    font-size: clamp(0.5rem, 0.7vw, 0.6rem);
    color: #10b981; /* green for positive */
}

/* Bar chart — pure CSS, no JS needed */
.bar-chart { display: flex; align-items: flex-end; gap: clamp(0.5rem, 1vw, 1rem); height: clamp(100px, 15vh, 180px); }
.bar-group { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 0.5rem; height: 100%; justify-content: flex-end; }
.bar {
    width: 100%; border-radius: 4px 4px 0 0;
    background: linear-gradient(to top, var(--brand-dark), var(--brand));
    height: 4px; /* animates to var(--bar-height) when .slide.visible */
    transition: height 1s var(--ease-out-expo);
}
.slide.visible .bar { height: var(--bar-height); }

/* Donut chart — conic-gradient */
.donut {
    width: clamp(80px, 10vw, 120px); height: clamp(80px, 10vw, 120px);
    border-radius: 50%;
    background: conic-gradient(var(--brand) 0deg 234deg, #8b5cf6 234deg 360deg);
    position: relative;
}
.donut::after {
    content: ''; position: absolute; inset: 25%;
    border-radius: 50%; background: var(--bg-surface);
}
```

#### CTA / Get in Touch Slide

```css
.glow-border {
    border: 1px solid var(--brand);
    animation: glow-pulse 3s ease-in-out infinite;
}
/* Use <a> tag for the button, not <div> */
```

```html
<a href="mailto:hello@example.com" class="glass-card glow-border"
   style="display: inline-block; padding: 0.75rem 2.5rem; cursor: pointer; text-decoration: none; color: inherit;">
    <span style="font-weight: 600; letter-spacing: 0.02em;">Get in Touch →</span>
</a>
```

#### Responsive Design — Battle-Tested Patterns

**CRITICAL: Every deck must be tested on mobile portrait, mobile landscape, and desktop.** These patterns are non-negotiable.

##### Core Principles

1. **Use `clamp()` everywhere** — never hard-code font sizes, padding, or gaps. Every dimension should scale fluidly:
   ```css
   font-size: clamp(min, preferred, max);
   padding: clamp(0.75rem, 2.5vw, 1.5rem);
   gap: clamp(0.5rem, 1.5vw, 1rem);
   ```

2. **Use `dvh` (dynamic viewport height)** — iOS Safari's toolbar changes the viewport. Always declare both:
   ```css
   .slide { height: 100vh; height: 100dvh; }
   ```

3. **Breakpoint strategy** — use both `max-width` AND `max-height` to catch landscape phones:
   - `max-width: 768px` — tablets and phones (portrait)
   - `max-width: 768px` + `max-height: 900px` — mobile portrait specifically (avoids tablets in landscape)
   - `max-height: 500px` — landscape phones (very short viewport)
   - `max-width: 400px` + `max-height: 750px` — extra small phones (iPhone SE, etc.)

##### Breakpoint 1: Mobile Portrait (`max-width: 768px` + `max-height: 900px`)

```css
@media (max-width: 768px) and (max-height: 900px) {
    .slide { padding: clamp(0.75rem, 2.5vw, 1.5rem); }
    .slide-content { gap: clamp(0.5rem, 1.5vw, 1rem); }
    h2 { font-size: clamp(1.3rem, 5vw, 2rem); }
    p { font-size: clamp(0.78rem, 2.2vw, 0.9rem) !important; line-height: 1.45 !important; }
    .mono-label { font-size: clamp(0.55rem, 1.5vw, 0.7rem); }

    /* Title slide — scale up content to fill portrait space */
    #slide-title .slide-content { gap: clamp(1rem, 3vh, 2rem); }
    #slide-title .reveal-scale { width: clamp(200px, 55vw, 340px) !important; }
    #slide-title .stat-row { flex-wrap: wrap; gap: 0.5rem 1.5rem !important; }

    /* Grids → single column */
    .case-study-layout { grid-template-columns: 1fr !important; gap: 0.5rem !important; }
    .case-study-images { grid-template-columns: 1fr 1fr !important; gap: 0.5rem; }
    .video-card { max-height: clamp(160px, 30vh, 260px); }
    .video-card[style*="translateY"] { transform: none !important; }
    .analytics-grid { grid-template-columns: repeat(2, 1fr); }

    /* Trim case study text to give videos more room */
    .case-study-layout > div:first-child p {
        font-size: clamp(0.72rem, 2vw, 0.85rem) !important;
        line-height: 1.4 !important; margin-bottom: 0.25rem !important;
    }

    /* Glass cards — tighter */
    .glass-card { padding: 0.75rem; }
    .glass-card h3 { font-size: 0.85rem; }
    .glass-card p { font-size: 0.72rem !important; }
}
```

##### Breakpoint 2: Extra Small Phones (`max-width: 400px` + `max-height: 750px`)

```css
@media (max-width: 400px) and (max-height: 750px) {
    .slide-content { gap: clamp(0.35rem, 1.2vw, 0.75rem); }
    h2 { font-size: clamp(1.1rem, 4.5vw, 1.6rem); }
    .video-card { max-height: clamp(100px, 18vh, 140px); }
    .glass-card { padding: 0.5rem; }
}
```

##### Breakpoint 3: Landscape Mobile (`max-height: 500px`)

```css
@media (max-height: 500px) {
    .slide { padding: 0.5rem 1.5rem; }
    .slide-content { gap: 0.4rem; }
    h2 { font-size: clamp(1rem, 3.5vw, 1.5rem); }
    p { font-size: clamp(0.7rem, 1.8vw, 0.82rem) !important; }

    /* Case studies — text + videos side by side */
    .case-study-layout {
        grid-template-columns: 1fr 1fr !important;
        gap: 0.75rem !important; align-items: start;
    }
    .case-study-images {
        grid-template-columns: 1fr 1fr !important;
        gap: 0.35rem; justify-items: center;
    }
    /* Constrain video width so they don't float apart */
    .video-card { max-height: clamp(80px, 35vh, 170px); max-width: 120px; width: 100%; }
    .video-card[style*="translateY"] { transform: none !important; }

    /* Shrink ambient effects */
    .divider-glow-orb { width: clamp(150px, 30vw, 300px); height: clamp(150px, 30vw, 300px); }
}
```

##### Video Lazy Loading (mandatory for mobile)

Mobile Safari limits concurrent video streams. **Never use `autoplay` + `src` on multiple videos.** Instead, lazy-load via IntersectionObserver:

```html
<!-- HTML: use data-src, NOT src. No autoplay attribute. -->
<video class="case-video" muted loop playsinline webkit-playsinline preload="none" data-src="video.mp4"></video>
```

```javascript
/* JS: Load video when slide becomes visible, pause when off-screen */
const videoObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        const videos = entry.target.querySelectorAll('video[data-src]');
        if (entry.isIntersecting) {
            videos.forEach(v => {
                if (!v.src) { v.src = v.dataset.src; v.load(); }
                v.play().catch(() => {});
            });
        } else {
            entry.target.querySelectorAll('video').forEach(v => {
                if (!v.paused) v.pause();
            });
        }
    });
}, { threshold: 0.15 });

document.querySelectorAll('.slide').forEach(slide => {
    if (slide.querySelector('video')) videoObserver.observe(slide);
});
```

**Key requirements:**
- `playsinline` + `webkit-playsinline` — required for iOS inline playback
- `muted` — required for autoplay on mobile
- `preload="none"` — prevents mobile from downloading all videos at page load
- Pause off-screen videos — frees memory and network bandwidth
- `.play().catch(() => {})` — silent catch for browsers that reject autoplay

##### Common Mobile Gotchas

1. **Nav dots overflow** — hide connecting lines on mobile: `@media (max-width: 768px) { .nav-dot::before { display: none; } }`
2. **Hover effects** — mobile has no hover. Use `@media (hover: hover)` to gate hover-only styles
3. **Video aspect ratio** — `aspect-ratio: 9/16` on `.video-card` + `object-fit: cover` on `<video>` ensures consistent sizing
4. **`translateY` offset on 2nd video card** — disable on mobile with `transform: none !important` (it prevents proper stacking)
5. **Stat rows** — add `flex-wrap: wrap` on mobile so stats don't overflow
6. **3D model canvas** — override height on mobile: `#slide-meet-frxme canvas { height: clamp(200px, 35vh, 300px) !important; }`

---

### 2. FRXME Light

**Vibe:** Clean, modern, tech — light mode variant of the FRXME platform

**Layout:** Same structure as FRXME Dark but inverted for bright environments/projectors.

**Typography:** Same as FRXME Dark (Inter + Geist Mono)

**Colors:**
```css
:root {
    --bg-primary: #ffffff;
    --bg-surface: #f4f4f5;
    --bg-muted: #e4e4e7;
    --border: #e4e4e7;
    --text-primary: #09090b;
    --text-secondary: #52525b;
    --text-muted: #a1a1aa;
    --brand: #0891b2;
    --brand-dark: #0e7490;
    --brand-light: #06b6d4;
    --brand-glow: rgba(8, 145, 178, 0.15);
}
```

**Signature Elements:**
- Clean white cards with subtle border: `border: 1px solid #e4e4e7;`
- Teal accent for headings and interactive elements
- Light dot grid: `radial-gradient(circle, rgba(8, 145, 178, 0.1) 1px, transparent 1px)`
- Same monospace label convention as dark variant
- Softer shadows instead of glow: `box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);`

---

### 3. SHXFT Sketch

**Vibe:** Bold, raw, creative energy — hand-drawn meets high-impact typography

**Layout:** White canvas with hand-drawn decorative elements. Content left-aligned or centered. Large type section dividers.

**Typography:**
- Display: `Onest` (800/900) — bold, all uppercase headlines
- Body: `Onest` (400/500) — clean, readable body text
- All weights from one family: 300 (light), 400 (regular), 500 (medium), 600 (semibold), 700 (bold), 800 (extrabold), 900 (black)

**Colors:**
```css
:root {
    --bg-primary: #ffffff;
    --text-primary: #000000;
    --text-secondary: #333333;
    --highlight-bg: #000000;
    --highlight-text: #ffffff;
    --sketch-stroke: #333333;
    --sketch-fill: none;
}
```

**Signature Elements:**

- **Hand-drawn sketch PNG elements** — actual hand-drawn assets (NOT generated SVGs):

**Asset files** (located at `~/.claude/skills/deck/assets/shxft/`):
| File | Description | Background | CSS Note |
|------|-------------|-----------|----------|
| `sketch-elements/sketch-arrow.png` | Pencil arrow pointing up-right | White/transparent | Use directly on white slides |
| `sketch-elements/corner-bracket.png` | L-shaped bracket frame corner | White/transparent | Use directly; rotate/flip via CSS for all 4 corners |
| `sketch-elements/pattern-tile.png` | Repeating pattern: X's, arrows, circles, dashes | **Black** | Apply `filter: invert(1)` on white slides |
| `sketch-elements/shapes-group.png` | Circle + arrow + X composition | **Black** | Apply `filter: invert(1)` on white slides |
| `sketch-elements/flowing-arrows.png` | Sweeping curved arrow lines | **Black** | Apply `filter: invert(1)` on white slides |
| `logos/shxft-wordmark-black.png` | Full SHXFT wordmark | Transparent | For light backgrounds |
| `logos/shxft-icon-black.png` | SHXFT X icon mark | Transparent | For light backgrounds |

**CSS for black-background assets on white slides:**
```css
.sketch-element.invert {
    filter: invert(1);
    opacity: 0.12;
}
```

**Sketch element placement pattern:**
```css
.sketch-element {
    position: absolute;
    pointer-events: none;
    opacity: 0.1;
    z-index: 0;
}
/* Corner placements */
.sketch-tl { top: 5%; left: 5%; width: clamp(60px, 8vw, 120px); }
.sketch-tr { top: 5%; right: 5%; width: clamp(60px, 8vw, 120px); transform: scaleX(-1); }
.sketch-bl { bottom: 5%; left: 5%; width: clamp(60px, 8vw, 120px); transform: scaleY(-1); }
.sketch-br { bottom: 5%; right: 5%; width: clamp(60px, 8vw, 120px); transform: scale(-1); }
/* Animated entrance */
.slide.visible .sketch-element {
    animation: sketch-fade 1s ease forwards;
}
@keyframes sketch-fade {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 0.1; transform: translateY(0); }
}
```

- **Inverted text highlights** on key words:
```css
.highlight {
    background: #000;
    color: #fff;
    padding: 0.05em 0.2em;
    display: inline;
    box-decoration-break: clone;
}
```
- **Sketch bracket frames** using corner-bracket.png rotated for each corner, or CSS fallback:
```css
.bracket-frame {
    border: 2px solid #333;
    border-radius: 0;
    transform: rotate(-0.5deg);
    padding: clamp(1rem, 2vw, 2rem);
}
```
- **Section dividers**: Massive bold text filling 60-80% of viewport width
- **Tilted photo cards** for case studies:
```css
.photo-card {
    transform: rotate(-2deg);
    border: 3px solid #333;
    box-shadow: 4px 4px 0 #333;
}
.photo-card:nth-child(2) { transform: rotate(1.5deg); }
```
- Logo placement: SHXFT wordmark bottom-left corner, small
- No gradients, no shadows (except on photo cards), no color — strictly monochrome

**IMPORTANT:** Always use the actual PNG sketch elements from the assets directory. Never generate inline SVG approximations — the hand-drawn PNGs are the brand's visual identity.

**SHXFT Brand Rules (follow these exactly):**
1. **Title/cover slide**: Use the `shxft-wordmark-black.png` logo image as the hero element — centered, large (~40-60% viewport width). Do NOT type "SHXFT" as text. No logo in the bottom-left on the title slide (it's already the hero).
2. **All other slides**: Place `shxft-wordmark-black.png` bottom-left, small (~80-130px wide), at ~70% opacity.
3. **Sketch elements**: Scatter 2-3 per slide as subtle decorations (opacity 0.1-0.15). Vary which assets you use — don't repeat the same layout on every slide. Use CSS transforms (rotate, flip) to create variety from the same assets.
4. **Typography**: All headlines uppercase. Use Onest 800/900 for display, 400/500 for body.
5. **Color**: Strictly monochrome (black + white + greys). No brand colors, no gradients.
6. **Inverted highlights**: Use `.highlight` (white text on black) on 1-2 key phrases per slide — never overuse.
7. **Slight rotations**: Cards and frames should have subtle rotation (-0.5deg to +0.5deg) for the hand-crafted feel.

---

## Curated Original Styles

### 4. Bold Signal

**Vibe:** Confident, bold, modern, high-impact

**Layout:** Colored card on dark gradient. Number top-left, navigation top-right, title bottom-left.

**Typography:**
- Display: `Archivo Black` (900)
- Body: `Space Grotesk` (400/500)

**Colors:**
```css
:root {
    --bg-primary: #1a1a1a;
    --bg-gradient: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
    --card-bg: #FF5722;
    --text-primary: #ffffff;
    --text-on-card: #1a1a1a;
}
```

**Signature Elements:**
- Bold colored card as focal point (orange, coral, or vibrant accent)
- Large section numbers (01, 02, etc.)
- Navigation breadcrumbs with active/inactive opacity states
- Grid-based layout for precise alignment

---

### 5. Dark Botanical

**Vibe:** Elegant, sophisticated, artistic, premium

**Layout:** Centered content on dark. Abstract soft shapes in corner.

**Typography:**
- Display: `Cormorant` (400/600) — elegant serif
- Body: `IBM Plex Sans` (300/400)

**Colors:**
```css
:root {
    --bg-primary: #0f0f0f;
    --text-primary: #e8e4df;
    --text-secondary: #9a9590;
    --accent-warm: #d4a574;
    --accent-pink: #e8b4b8;
    --accent-gold: #c9b896;
}
```

**Signature Elements:**
- Abstract soft gradient circles (blurred, overlapping)
- Warm color accents (pink, gold, terracotta)
- Thin vertical accent lines
- Italic signature typography
- **No illustrations — only abstract CSS shapes**

---

### 6. Swiss Modern

**Vibe:** Clean, precise, Bauhaus-inspired

**Layout:** Asymmetric grid. Strong vertical/horizontal lines. Content aligned to visible grid.

**Typography:**
- Display: `Archivo` (800)
- Body: `Nunito` (400)

**Colors:**
```css
:root {
    --bg-primary: #ffffff;
    --text-primary: #000000;
    --accent: #ff3300;
    --grid-line: rgba(0, 0, 0, 0.06);
}
```

**Signature Elements:**
- Visible grid lines as design element
- Asymmetric layouts (content shifted off-center)
- Geometric shapes (circles, rectangles) as accent
- Red accent used sparingly for emphasis
- Strong typographic hierarchy with extreme size contrast

---

### 7. Neon Cyber

**Vibe:** Futuristic, techy, confident

**Layout:** Dark background with neon glow accents. Grid patterns. Particle effects optional.

**Typography:**
- Display: `Clash Display` (700) — from Fontshare
- Body: `Satoshi` (400/500) — from Fontshare

**Colors:**
```css
:root {
    --bg-primary: #0a0f1c;
    --bg-secondary: #111827;
    --text-primary: #ffffff;
    --text-secondary: #9ca3af;
    --accent-cyan: #00ffcc;
    --accent-magenta: #ff00aa;
    --accent-glow: rgba(0, 255, 204, 0.3);
}
```

**Signature Elements:**
- Neon glow on text and borders: `text-shadow: 0 0 20px var(--accent-cyan);`
- Grid pattern background
- Particle system (canvas) — optional, for title slides
- Glitch/scramble text effect on headings
- Code-style monospace accents

---

## Font Loading Quick Reference

| Style | Display Font | Body Font | Source |
|-------|-------------|-----------|--------|
| FRXME Dark/Light | Inter | Inter + Geist Mono | Google / Next.js |
| SHXFT Sketch | Onest (800/900) | Onest (400/500) | Google |
| Bold Signal | Archivo Black | Space Grotesk | Google |
| Dark Botanical | Cormorant | IBM Plex Sans | Google |
| Swiss Modern | Archivo | Nunito | Google |
| Neon Cyber | Clash Display | Satoshi | Fontshare |

**Google Fonts URL pattern:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=FONT_NAME:wght@WEIGHTS&display=swap" rel="stylesheet">
```

**Fontshare URL pattern:**
```html
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@700&f[]=satoshi@400;500&display=swap" rel="stylesheet">
```

---

## DO NOT USE (Generic AI Patterns)

**Fonts:** Roboto, Arial, system fonts as display text

**Colors:** `#6366f1` (generic indigo), purple gradients on white

**Layouts:** Everything centered, generic hero sections, identical card grids

**Decorations:** Realistic illustrations, gratuitous glassmorphism without purpose, drop shadows without intent

---

## CSS Gotchas

### Negating CSS Functions

**WRONG — silently ignored by browsers:**
```css
right: -clamp(28px, 3.5vw, 44px);   /* Browser ignores this */
```

**CORRECT — wrap in `calc()`:**
```css
right: calc(-1 * clamp(28px, 3.5vw, 44px));  /* Works */
```

CSS does not allow a leading `-` before function names. Always use `calc(-1 * ...)` to negate CSS function values.

---

### 8. SCXPE Architectural

**Vibe:** High-end architectural studio website. Premium, cinematic, light theme with dark contrast slides. Construction wireframe aesthetic — structural beams, nodes, perspective grids. Feels like browsing an elite interior design or architecture firm's portfolio.

**Layout:** Light backgrounds (`#FAFAFA`) with procedural animated wireframe effects. Glass cards on off-white surfaces. Dark containers (`#111111`) for 3D viewers and contrast/divider slides. Content centered with generous whitespace.

**Typography:**
- Display: `Space Grotesk` (600/700) — geometric, architectural feel. Tight letter-spacing (`-0.03em` on h1, `-0.02em` on h2)
- Body: `Inter` (300-700) — with `-webkit-font-smoothing: antialiased`
- Mono: `JetBrains Mono` (400/500) — for labels, specs, section markers, stage pills
- Line heights: h1 `1.02`, h2 `1.1`, body `1.7`

**Font loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

**Colors:**
```css
:root {
    --bg-primary: #FAFAFA;
    --bg-surface: #F0F0F0;
    --bg-dark: #1A1A1A;
    --bg-darker: #111111;
    --border: #D4D4D4;
    --border-light: #E5E5E5;
    --text-primary: #1A1A1A;
    --text-secondary: #525252;
    --text-muted: #9CA3AF;
    --text-light: #FFFFFF;
    --brand: #2563EB;
    --brand-dark: #1D4ED8;
    --brand-light: #60A5FA;
    --brand-glow: rgba(37, 99, 235, 0.15);
    --brand-glow-strong: rgba(37, 99, 235, 0.3);
    --brand-glow-subtle: rgba(37, 99, 235, 0.06);
}
```

**Animation Timing (Cinematic — slower than other presets):**
```css
:root {
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    --ease-cinematic: cubic-bezier(0.22, 1, 0.36, 1);
    --duration-normal: 1s;     /* longer than standard 0.6s */
    --duration-slow: 1.4s;
}
```

**Signature Elements:**
- 4-layer procedural wireframe backgrounds (no static images) — grid, perspective grid, canvas nodes, structural beams
- Structural beam lines in charcoal/blue that "draw in" on scroll with connection nodes at intersections
- Glass cards on light surfaces with blur backdrop
- Brand blue accent for icons, checkmarks, active states, stat numbers, and stage pills
- Two label styles: `mono-label` (muted brackets `[ SECTION ]`) and `section-heading` (brand blue uppercase)
- Dark containers (`#111111`) for 3D viewers with blue glow border
- Gradient text (charcoal → brand blue) on CTA headlines
- Counter animations for statistics that count up on visibility
- Confetti on CTA button click (brand blue palette)
- Cinematic reveal animations: `reveal` (40px up), `reveal-scale` (0.92→1), `reveal-blur` (16px→0), `reveal-left` (-50px), `reveal-right` (+50px)
- Stagger delays: 0.15s increments (not 0.1s like standard)

**Logo Assets** (in project `logos/` folder):
- `SCXPE_LOGO_DARK.png` — Dark text + network-graph X → use on **light** backgrounds
- `SCXPE_LOGO_LIGHT.png` — White text + network-graph X → use on **dark** backgrounds

**SCXPE Brand Rules:**
1. **Title/cover slide**: Use `SCXPE_LOGO_DARK.png` as hero element — centered, large (`max-width: min(60vw, 500px)`). Do NOT type "SCXPE" as text unless logo fails to load.
2. **Dark slides**: Use `SCXPE_LOGO_LIGHT.png` if logo appears on dark backgrounds.
3. **Powered by**: Show `Powered by SHXFT Studio` at bottom of title and CTA slides at ~35% opacity in mono font. Use `position: absolute; bottom` — do NOT apply `.reveal` class (conflicts with absolute positioning). Use simple opacity transition instead: `opacity: 0; transition: opacity 1s ease 0.8s;` with `.slide.visible .hero-powered { opacity: 0.35 !important; }`.
4. **Monospace labels**: Use `[ SECTION ]` style `mono-label` or brand-blue `section-heading` above headings in JetBrains Mono uppercase, `letter-spacing: 0.2em`.
5. **Glass cards**: Light: `background: rgba(255, 255, 255, 0.65); border: 1px solid #E5E5E5; backdrop-filter: blur(12px);`. Dark variant for dark slides.
6. **Stat numbers**: Use brand blue (`#2563EB`) for statistics, counters, step numbers. `font-family: Space Grotesk; font-weight: 700`.
7. **Buttons**: Pill-shaped (`border-radius: 100px`), brand blue fill, hover lifts `-2px` with glow shadow.
8. **Icons**: SVG stroke icons (not filled), `stroke-width: 1.5`, brand blue color, inside rounded-square containers (`border-radius: 14px`) with `brand-glow-subtle` background.

**Card Pattern:**
```css
.glass-card {
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    padding: clamp(1.5rem, 2.5vw, 2.25rem);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: transform 0.5s var(--ease-cinematic), box-shadow 0.5s var(--ease-cinematic), border-color 0.5s var(--ease-cinematic);
}
@media (hover: hover) {
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.08);
        border-color: rgba(37, 99, 235, 0.15);
    }
}

/* Dark variant (for dark slides) */
.glass-card-dark {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
}
@media (hover: hover) {
    .glass-card-dark:hover {
        border-color: rgba(37, 99, 235, 0.25);
        box-shadow: 0 0 40px rgba(37, 99, 235, 0.08);
    }
}
```

**Comparison Table Pattern:**
Two-column comparison (e.g., "360 Tours vs SCXPE"). Left column muted (`--bg-surface`), right column white with `3px` brand-blue left border. Headers in mono uppercase. Items with inline SVG check/x icons. Wraps to stacked on mobile.

**Browser Chrome 3D Container:**
3D viewer slides use a fake browser chrome bar (traffic light dots: `#FF5F57`, `#FEBC2E`, `#28C840`) above the canvas. Dark background (`#111111`), rounded corners (`16px`), glow border (`rgba(37, 99, 235, 0.08)`).

---

### SCXPE Architectural — Structural Beam Background System

The signature architectural aesthetic uses 4 beam types + vertical columns + connection nodes, all CSS-animated. Each slide gets a unique beam configuration (no two slides should have the same layout). Beams "draw in" when the slide becomes visible via IntersectionObserver.

#### Beam Types

```css
/* I-beam: thick dark charcoal — primary structural element */
.beam-line.ibeam {
    height: 3px;
    background: linear-gradient(90deg, transparent, rgba(60, 60, 60, 0.12) 10%, rgba(60, 60, 60, 0.14) 50%, rgba(60, 60, 60, 0.12) 90%, transparent);
}

/* Structural: medium blue-tinted — brand accent beams */
.beam-line.structural {
    height: 2px;
    background: linear-gradient(90deg, transparent 3%, rgba(37, 99, 235, 0.1) 15%, rgba(37, 99, 235, 0.1) 85%, transparent 97%);
}

/* Cross-brace: thin — diagonal and secondary structure */
.beam-line.brace {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(100, 100, 100, 0.08) 20%, rgba(100, 100, 100, 0.08) 80%, transparent);
}

/* Heavy charcoal: thickest — major structural columns */
.beam-line.heavy {
    height: 4px;
    background: linear-gradient(90deg, transparent, rgba(40, 40, 40, 0.08) 10%, rgba(40, 40, 40, 0.1) 50%, rgba(40, 40, 40, 0.08) 90%, transparent);
}
```

#### Vertical Columns

```css
.beam-vertical {
    position: absolute;
    width: 2px;
    background: linear-gradient(180deg, transparent, rgba(60, 60, 60, 0.1) 15%, rgba(60, 60, 60, 0.1) 85%, transparent);
    opacity: 0;
}
.beam-vertical.thick {
    width: 3px;
    background: linear-gradient(180deg, transparent, rgba(40, 40, 40, 0.12) 10%, rgba(40, 40, 40, 0.12) 90%, transparent);
}
.beam-vertical.drawing {
    animation: beamDrawV 2.5s var(--ease-cinematic) forwards;
}
@keyframes beamDrawV {
    from { height: 0; opacity: 0; }
    to { height: 100%; opacity: 1; }
}
```

#### Connection Nodes

Small circles at beam intersections. Two variants: `.charcoal` (neutral) and `.accent` (brand blue glow).

```css
.beam-node {
    position: absolute;
    width: 6px; height: 6px;
    border-radius: 50%;
    opacity: 0; transform: scale(0);
}
.beam-node.charcoal { background: rgba(60, 60, 60, 0.25); }
.beam-node.accent { background: rgba(37, 99, 235, 0.3); }
.beam-node.visible {
    animation: nodeAppear 0.6s var(--ease-cinematic) forwards;
}
```

#### Grid Nodes (Floating)

Pulsing grid intersection nodes for ambient depth:

```css
.grid-node {
    position: absolute;
    width: 4px; height: 4px;
    background: var(--brand);
    border-radius: 50%;
    opacity: 0;
}
.grid-node.pulse {
    animation: nodePulse 4s ease-in-out infinite;
}
@keyframes nodePulse {
    0%, 100% { opacity: 0.12; transform: scale(1); box-shadow: none; }
    50% { opacity: 0.35; transform: scale(1.5); box-shadow: 0 0 8px var(--brand-glow); }
}
```

#### Dark Slide Beam Variants

On `.slide-dark`, beams switch to white/blue tones:
```css
.slide-dark .beam-line.ibeam,
.slide-dark .beam-line.heavy {
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.06) 10%, rgba(255, 255, 255, 0.08) 50%, rgba(255, 255, 255, 0.06) 90%, transparent);
}
.slide-dark .beam-line.structural {
    background: linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.12) 15%, rgba(37, 99, 235, 0.12) 85%, transparent);
}
.slide-dark .beam-vertical {
    background: linear-gradient(180deg, transparent, rgba(255, 255, 255, 0.06) 15%, rgba(255, 255, 255, 0.06) 85%, transparent);
}
.slide-dark .beam-node.charcoal { background: rgba(255, 255, 255, 0.15); }
```

#### Beam Configurations (JS)

Each slide gets a unique beam layout defined in a `beamConfigs` object keyed by container ID. Beams are generated with:
- `type`: `ibeam`, `structural`, `brace`, or `heavy`
- `top`: vertical position (%, px, or calc())
- `angle`: rotation in degrees (typically -30° to +30°, with more extreme angles for variety)
- `delay`: animation delay for stagger (0.2s increments)

Also supports `verticals` (columns) with `left`, `height`, `thick` boolean, and `delay`. And `nodes` with `top`, `left`, `type` (`charcoal`/`accent`), and `delay`.

Generate 4-8 beams, 1-3 verticals, and 2-4 nodes per slide. Vary configurations dramatically — some slides use mostly horizontal heavy beams, others use diagonal braces, others emphasize verticals.

---

### SCXPE Architectural — Animated Grid Layers (CSS)

#### Layer 1: Breathing Wireframe Grid

```css
.wireframe-grid::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(37, 99, 235, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(37, 99, 235, 0.04) 1px, transparent 1px);
    background-size: 80px 80px;
    pointer-events: none;
    animation: gridBreath 10s ease-in-out infinite;
}
@keyframes gridBreath {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}
.slide-dark .wireframe-grid::before {
    background-image:
        linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
}
```

#### Layer 2: Perspective Vanishing Point Grid

Animates in with `perspectiveExpand` keyframe on slide visibility:

```css
.perspective-grid::after {
    content: '';
    position: absolute;
    bottom: 0; left: -20%; right: -20%;
    height: 60%;
    background-image:
        linear-gradient(rgba(37, 99, 235, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(37, 99, 235, 0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    transform: perspective(500px) rotateX(65deg);
    transform-origin: bottom center;
    pointer-events: none;
    mask-image: linear-gradient(to top, rgba(0,0,0,0.3), transparent 80%);
    -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,0.3), transparent 80%);
    opacity: 0;
}
.slide.visible .perspective-grid::after { opacity: 1; }
```

Use on title and CTA slides for floor-plane depth.

#### Layer 3: Floating Construction Nodes (Canvas)

Full-viewport `position: fixed; inset: 0; pointer-events: none; z-index: 1;` canvas overlay with ~18 nodes. Features:
- Nodes drift with `vx`/`vy` velocities, wrap at screen edges
- Connection lines between nodes within 200px (alpha based on distance)
- Mouse magnetic attraction (250px radius)
- Parallax on scroll: `drawY = (node.y - scrollY * node.depth * 0.05) % height`
- Brand blue at low opacity (0.08-0.12 lines, 0.12-0.15 nodes)
- Glow ring on cursor-proximate nodes
- `requestAnimationFrame` with `document.hidden` check for performance

---

### SCXPE Architectural — 3D Viewer Pattern

For slides with interactive 3D building models. Supports multiple viewers sharing one GLB via a `ModelViewer` class.

**Three.js setup:**
- v0.162.0 via CDN importmap (three, GLTFLoader, OrbitControls, RGBELoader)
- WebGLRenderer: `antialias: true, alpha: true`, pixelRatio `Math.min(devicePixelRatio, 2)`, `ACESFilmicToneMapping`, `toneMappingExposure: 1.4` (or `1.8` for pipeline viewer Final stage)

**Shared ModelViewer Class:**
When using multiple 3D viewers on different slides, use a shared class that:
- Loads GLB once, clones for each viewer instance
- Loads HDRI (`studio_small_09_1k.hdr`) once, shares across all scenes
- Each instance gets its own `WebGLRenderer`, `Scene`, `Camera`, `OrbitControls`
- Render loops are gated by IntersectionObserver (pause when off-screen)

**Lighting (Architectural — warm key, cool fill):**
```javascript
scene.add(new THREE.AmbientLight(0xffffff, 2));
const keyLight = new THREE.DirectionalLight(0xfff5e6, 3);
keyLight.position.set(5, 8, 5);
const fillLight = new THREE.DirectionalLight(0x6090ff, 1.5);
fillLight.position.set(-5, 3, -3);
const rimLight = new THREE.DirectionalLight(0xffffff, 1);
rimLight.position.set(0, -2, -5);
```

**Controls:**
```javascript
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enableZoom = false;
controls.enablePan = false;
controls.autoRotate = true;
controls.autoRotateSpeed = 1.5;
controls.minPolarAngle = Math.PI / 4;
controls.maxPolarAngle = Math.PI / 2.2;
```

**3-Stage Material Transition (Wireframe → Structure → Final):**

On GLB load, traverse meshes, store original materials in `Map`. Create alternatives:

```javascript
const wireframeMat = new THREE.MeshBasicMaterial({
    color: 0x2563EB, wireframe: true, transparent: true, opacity: 0.6
});
const structureMat = new THREE.MeshStandardMaterial({
    color: 0xD4D4D4, metalness: 0.1, roughness: 0.8, flatShading: true
});
// Final stage: original materials with envMapIntensity: 2.0 for premium look
```

`setStage(n)` swaps all mesh materials. Auto-cycle every 3s via `setInterval` when slide visible. Pause auto-cycle on manual stage pill click.

**Stage pills:**
```css
.stage-pill {
    font-family: var(--font-mono);
    font-size: clamp(0.6rem, 0.85vw, 0.72rem);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: clamp(0.4rem, 0.8vw, 0.6rem) clamp(1rem, 1.8vw, 1.4rem);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 100px;
    background: transparent;
    color: rgba(255, 255, 255, 0.4);
    cursor: pointer;
    transition: all 0.4s var(--ease-cinematic);
}
.stage-pill.active {
    background: var(--brand);
    border-color: var(--brand);
    color: white;
    box-shadow: 0 0 24px var(--brand-glow);
}
```

**Viewer containers:**
- Pipeline slide: Full-width wrap with `aspect-ratio: 16/9`, `background: #0a0a0a`, blue glow border and shadow
- Browser chrome viewers: Fake macOS window bar (3 traffic-light dots) above canvas body with `aspect-ratio: 16/10`
- Demo viewer: Centered with `max-width: 750px`
- Drag-to-rotate hint at bottom: mono font, 0.6rem, `rgba(255, 255, 255, 0.25)` with rotating SVG icon

**Performance:**
- Pause render loop when slide not visible (IntersectionObserver)
- ResizeObserver on each canvas wrapper for responsive sizing
- `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))`

---

### SCXPE Architectural — Dark Slide Variant

For contrast/divider slides within the light deck:

```css
.slide-dark {
    background: var(--bg-dark);  /* #1A1A1A */
    color: var(--text-light);
}
.slide-dark h1, .slide-dark h2, .slide-dark h3 { color: var(--text-light); }
.slide-dark p, .slide-dark li { color: rgba(255, 255, 255, 0.65); }
.slide-dark .mono-label { color: rgba(255, 255, 255, 0.35); }
```

Use for:
- Section dividers with large provocative text + glow orb (1-2 max per deck)
- 3D viewer / pipeline slides (`--bg-darker: #111111` for even deeper black)

**Glow orb for divider slides:**
```css
.glow-orb {
    position: absolute;
    width: clamp(200px, 40vw, 500px);
    height: clamp(200px, 40vw, 500px);
    border-radius: 50%;
    background: radial-gradient(circle, var(--brand-glow-strong) 0%, transparent 70%);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    animation: glowPulse 5s ease-in-out infinite;
    pointer-events: none;
}
@keyframes glowPulse {
    0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.4; }
    50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.7; }
}
```

---

### SCXPE Architectural — Responsive

**Mobile strategy:** Desktop = scroll-snap, full-viewport slides, nav dots (deck experience). Mobile (≤768px) = free-scrolling long page, single-column cards, no nav dots (premium site experience, like Apple product pages).

```css
/* Short viewports */
@media (max-height: 700px) {
    .slide { padding: clamp(1rem, 3vw, 2rem); }
    .slide h1 { font-size: clamp(1.5rem, 5vw, 3.5rem); }
}

/* Narrow / mobile */
@media (max-width: 768px) {
    /* Disable scroll-snap — free-scrolling long page */
    html { scroll-snap-type: none; }
    .slide {
        height: auto; min-height: 100dvh;
        overflow: visible; scroll-snap-align: none;
        padding-top: clamp(2.5rem, 6vw, 3.5rem);
        padding-bottom: clamp(2.5rem, 6vw, 3.5rem);
    }
    /* All grids go single-column */
    .two-col, .card-grid, .card-grid-3 { grid-template-columns: 1fr; }
    .process-steps { grid-template-columns: repeat(2, 1fr); }
    .comparison-grid { grid-template-columns: 1fr; }
    .nav-dots { display: none; }
    /* Tighter card padding */
    .glass-card { padding: clamp(1rem, 3vw, 1.5rem); }
    .slide-content { gap: clamp(1rem, 2.5vw, 1.5rem); }
    .slide h2 { font-size: clamp(1.4rem, 6vw, 2rem); }
    .slide p, .slide li { font-size: clamp(0.8rem, 3vw, 0.95rem); line-height: 1.6; }
    /* 3D viewers: constrain height */
    .viewer-3d-body { min-height: 200px; aspect-ratio: 4/3; }
}

/* Landscape phones */
@media (max-height: 500px) {
    .slide { padding: clamp(0.75rem, 2vw, 1.5rem); }
    .glow-orb { display: none; }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.2s !important;
    }
}
```

**Landscape phones (≤500px height):**
- Also disable scroll-snap and free-scroll (same as portrait mobile)
- Use `overflow-x: clip` (NOT `hidden`) on `.slide` — clips perspective grid pseudo-elements without creating a scroll container
- Reduce slide padding: `clamp(1rem, 2.5vw, 1.5rem)` sides
- `.slide-content { max-width: 96vw; }` — use near-full width
- Smaller typography: h2 `clamp(1rem, 3vw, 2rem)`, body `clamp(0.75rem, 1.5vw, 0.9rem)`
- 3-card grids: keep 3 columns but shrink padding/icons
- 2-col grids: keep 2 columns with `gap: 1rem`
- Hide glow orbs and hero-powered text
- 3D viewers: `max-height: 50-55vh`

**CRITICAL — horizontal overflow prevention:**
The `.perspective-grid::after` uses `left: -20%; right: -20%` which extends beyond viewport. MUST use `overflow-x: clip` on `.slide` (not `overflow: hidden` which prevents vertical scroll). Also add `overflow-x: hidden` to `html` and `body` as safety net.

**JS mobile adaptations:**
- Detect mobile as `window.innerWidth <= 768 || window.innerHeight <= 600` (catches landscape phones)
- `IntersectionObserver` threshold: `0.15` on mobile (vs `0.5` on desktop)
- Disable programmatic touch swipe nav on mobile — let native scroll handle it
- Keep keyboard nav for all widths (accessibility)

**⚠️ Mobile is critical — decks are shared via WhatsApp/messaging.** Portrait and landscape must be airtight. Always test at 375×812 (portrait) and 812×375 (landscape) minimum.

---

### SCXPE Architectural — Additional Patterns

**SHXFT Studio Expertise Slide:**
Dark slide variant. Shows SHXFT white wordmark (`logos/shxft-wordmark-white.png`, `max-width: min(30vw, 180px)`, `opacity: 0.7`). Key framing: "founded on 6+ years of hands-on experience" — attribute expertise to the founder/team, NOT the company's age. Stats: `500+` projects delivered by the team, `6+` years AR & immersive expertise. Client roster in "Trusted By" card.

**"Coming Soon" Badge Pattern:**
For features not yet available (e.g., AR capabilities). Inline `<span>` inside `<h3>`:
```css
font-family: var(--font-mono);
font-size: 0.55rem;
letter-spacing: 0.12em;
text-transform: uppercase;
background: var(--brand-glow-subtle);
color: var(--brand);
padding: 3px 10px;
border-radius: 100px;
border: 1px solid rgba(37, 99, 235, 0.12);
vertical-align: middle;
margin-left: 6px;
font-weight: 500;
```

**Card Grid Rules:**
- `.card-grid` (2-column): Use for 4-card layouts. `grid-template-columns: repeat(2, 1fr)` on desktop. Goes `1fr` (single column) on mobile.
- `.card-grid-3` (3-column): Use for exactly 3 cards. Goes `1fr` (single column) on mobile.
- Both grids go single-column on mobile — slides expand vertically with free scroll (no scroll-snap).
- Never use for 5+ cards — causes orphan rows. Split into two slides instead.

**Pricing Slide (Hidden):**
Pricing content is kept HTML-commented (`<!-- PRICING SLIDE — HIDDEN ... END PRICING SLIDE -->`) so it can be re-enabled later. Three tiers: Single Launch / Dual Launch / Enterprise. pricing baseline redacted for the shared copy.

**OG Image:**
1200x630 PNG. Light bg (#F5F5FA), subtle grid lines, centered SCXPE logo (dark variant), tagline below, brand-blue accent line, `scxpe.co` URL at bottom. Generated programmatically via PIL — no external dependencies.

**Domain:** scxpe.co (deployed via Vercel from GitHub `hasanshxft/SCXPE`)
