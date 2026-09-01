# Animation Patterns Reference

Use this reference when generating presentations. Match animations to the intended feeling.

## Effect-to-Feeling Guide

| Feeling | Animations | Visual Cues |
|---------|-----------|-------------|
| **Dramatic / Cinematic** | Slow fade-ins (1-1.5s), large scale transitions (0.9 to 1), parallax scrolling | Dark backgrounds, spotlight effects, full-bleed images |
| **Techy / Futuristic** | Neon glow (box-shadow), glitch/scramble text, grid reveals | Particle systems (canvas), grid patterns, monospace accents, cyan/magenta/electric blue |
| **Playful / Friendly** | Bouncy easing (spring physics), floating/bobbing | Rounded corners, pastel/bright colors, hand-drawn elements |
| **Professional / Corporate** | Subtle fast animations (200-300ms), clean slides | Navy/slate/charcoal, precise spacing, data visualization focus |
| **Calm / Minimal** | Very slow subtle motion, gentle fades | High whitespace, muted palette, serif typography, generous padding |
| **Editorial / Magazine** | Staggered text reveals, image-text interplay | Strong type hierarchy, pull quotes, grid-breaking layouts, serif headlines + sans body |

## Entrance Animations

```css
/* Fade + Slide Up (most versatile) */
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s var(--ease-out-expo),
                transform 0.6s var(--ease-out-expo);
}
.visible .reveal {
    opacity: 1;
    transform: translateY(0);
}

/* Scale In */
.reveal-scale {
    opacity: 0;
    transform: scale(0.9);
    transition: opacity 0.6s, transform 0.6s var(--ease-out-expo);
}

/* Slide from Left */
.reveal-left {
    opacity: 0;
    transform: translateX(-50px);
    transition: opacity 0.6s, transform 0.6s var(--ease-out-expo);
}

/* Blur In */
.reveal-blur {
    opacity: 0;
    filter: blur(10px);
    transition: opacity 0.8s, filter 0.8s var(--ease-out-expo);
}
```

## Stagger Pattern

```css
/* Stagger children for sequential reveal */
.reveal:nth-child(1) { transition-delay: 0.1s; }
.reveal:nth-child(2) { transition-delay: 0.2s; }
.reveal:nth-child(3) { transition-delay: 0.3s; }
.reveal:nth-child(4) { transition-delay: 0.4s; }
.reveal:nth-child(5) { transition-delay: 0.5s; }
.reveal:nth-child(6) { transition-delay: 0.6s; }
```

## Background Effects

```css
/* Gradient Mesh — layered radial gradients for depth */
.gradient-bg {
    background:
        radial-gradient(ellipse at 20% 80%, rgba(120, 0, 255, 0.3) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(0, 255, 200, 0.2) 0%, transparent 50%),
        var(--bg-primary);
}

/* Noise Texture — inline SVG for grain */
.noise-bg::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
}

/* Grid Pattern — subtle structural lines */
.grid-bg {
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
}

/* Dot Grid — for FRXME style */
.dot-grid {
    background-image: radial-gradient(circle, rgba(6, 182, 212, 0.15) 1px, transparent 1px);
    background-size: 40px 40px;
}
```

## Section Divider Effects (FRXME Dark)

Layered ambient effects for high-energy section dividers. Combine all 4 layers for maximum impact. Full CSS and HTML in [STYLE_PRESETS.md](STYLE_PRESETS.md) under "FRXME Dark — Battle-Tested Component Patterns".

| Layer | Effect | Animation |
|-------|--------|-----------|
| Glow Orb | Radial gradient behind title, centered | Pulse scale 1→1.15 (4s loop) |
| Particles | 6-8 small circles with CSS custom properties (`--d-size`, `--d-dur`, `--d-delay`, `--d-dx`, `--d-dy`) | Float upward and outward, fade in/out |
| Scanline | Horizontal 1px gradient line | Sweeps top (15%) to bottom (85%) over 6s |
| Title Glow | `drop-shadow` on gradient text | Breathing glow 30px↔60px (3s loop) |

**Key technique:** Each `.d-particle` uses CSS custom properties for unique motion, so you can place 6-8 particles with different sizes/speeds/directions without writing separate keyframes for each.

---

## Glow Effects (FRXME / Neon Cyber)

```css
/* Glow Pulse — for brand accent elements */
@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 20px var(--brand-glow); }
    50% { box-shadow: 0 0 40px var(--brand-glow-strong, var(--brand-glow)); }
}

.glow {
    animation: glow-pulse 3s ease-in-out infinite;
}

/* Text Glow */
.text-glow {
    text-shadow: 0 0 20px var(--brand-glow),
                 0 0 40px var(--brand-glow);
}

/* Border Glow */
.border-glow {
    border: 1px solid var(--brand);
    box-shadow: 0 0 15px var(--brand-glow),
                inset 0 0 15px var(--brand-glow);
}
```

## Interactive Effects

```javascript
/* 3D Tilt on Hover — adds depth to cards/panels */
class TiltEffect {
    constructor(element) {
        this.element = element;
        this.element.style.transformStyle = 'preserve-3d';
        this.element.style.perspective = '1000px';

        this.element.addEventListener('mousemove', (e) => {
            const rect = this.element.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            this.element.style.transform = `rotateY(${x * 10}deg) rotateX(${-y * 10}deg)`;
        });

        this.element.addEventListener('mouseleave', () => {
            this.element.style.transform = 'rotateY(0) rotateX(0)';
        });
    }
}
```

## 3D Scroll-Linked Rotation

Inspired by the FRXME product showcase on shxftweb.vercel.app. The product/image rotates in 3D space as the user scrolls through the slide.

**When to use:** Product showcase slides, hero slides with a key visual, tech demo slides.

### CSS Setup

```css
.product-showcase {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    overflow: hidden;
    perspective: 1200px;
}

.product-3d {
    transform-style: preserve-3d;
    transition: transform 0.1s ease-out;
    will-change: transform;
}

.product-3d img {
    max-height: min(70vh, 500px);
    width: auto;
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

/* Spec table that appears alongside */
.spec-table {
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
    font-size: clamp(0.7rem, 1vw, 0.9rem);
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.spec-row {
    display: flex;
    justify-content: space-between;
    padding: clamp(0.5rem, 1vh, 1rem) 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    opacity: 0;
    transform: translateX(20px);
    transition: opacity 0.4s ease, transform 0.4s ease;
}

.spec-row.visible {
    opacity: 1;
    transform: translateX(0);
}

.spec-label { color: var(--text-muted, #71717a); }
.spec-value { color: var(--text-primary, #fafafa); font-weight: 600; }
```

### JavaScript Controller

```javascript
class Product3DShowcase {
    constructor(slideElement) {
        this.slide = slideElement;
        this.product = slideElement.querySelector('.product-3d');
        this.specRows = slideElement.querySelectorAll('.spec-row');

        // Rotation range: 0deg (front) to -45deg (three-quarter view)
        this.maxRotation = -45;
        this.currentRotation = 0;

        this.setupScrollListener();
    }

    setupScrollListener() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    window.addEventListener('scroll', this.handleScroll.bind(this));
                    this.revealSpecs();
                } else {
                    window.removeEventListener('scroll', this.handleScroll.bind(this));
                }
            });
        }, { threshold: 0.1 });

        observer.observe(this.slide);
    }

    handleScroll() {
        const rect = this.slide.getBoundingClientRect();
        const slideHeight = rect.height;
        const scrollProgress = Math.max(0, Math.min(1,
            (window.innerHeight - rect.top) / (window.innerHeight + slideHeight)
        ));

        // Map scroll progress to rotation
        this.currentRotation = scrollProgress * this.maxRotation;
        this.product.style.transform = `rotateY(${this.currentRotation}deg)`;
    }

    revealSpecs() {
        this.specRows.forEach((row, i) => {
            setTimeout(() => row.classList.add('visible'), 300 + (i * 150));
        });
    }
}
```

### HTML Structure

```html
<section class="slide product-showcase">
    <div class="showcase-layout">
        <div class="product-3d">
            <img src="assets/product.png" alt="FRXME Display">
        </div>
        <div class="spec-panel">
            <span class="mono-label">[ SPECIFICATIONS ]</span>
            <div class="spec-table">
                <div class="spec-row">
                    <span class="spec-label">DISPLAY</span>
                    <span class="spec-value">55" 4K Multi-Touch</span>
                </div>
                <div class="spec-row">
                    <span class="spec-label">TRACKING</span>
                    <span class="spec-value">Full-Body AR @ 60fps</span>
                </div>
                <!-- more rows -->
            </div>
        </div>
    </div>
</section>
```

---

## Responsive Animation Patterns

Animations must degrade gracefully across devices. Never assume desktop.

### Reduce Motion on Mobile

Heavy ambient effects (particles, beam sway, floating elements) hurt mobile performance. Scale them down or remove:

```css
@media (max-width: 768px) and (max-height: 900px) {
    /* Fewer particles — hide every other one */
    .d-particle:nth-child(odd) { display: none; }
    /* Smaller glow orbs */
    .divider-glow-orb { width: clamp(150px, 30vw, 300px); height: clamp(150px, 30vw, 300px); }
    /* Simpler reveal — reduce distance */
    .reveal { transform: translateY(15px); } /* down from 25px */
}

@media (max-height: 500px) {
    /* Landscape: minimal ambient, just keep scanline */
    .divider-particles { display: none; }
    .divider-glow-orb { opacity: 0.3; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

### Touch-Friendly Interactions

Desktop hover effects don't work on mobile. Gate them properly:

```css
/* Only apply hover effects when device actually supports hover */
@media (hover: hover) {
    .glass-card:hover {
        border-color: rgba(6, 182, 212, 0.3);
        box-shadow: 0 0 30px rgba(6, 182, 212, 0.15);
        transform: translateY(-2px);
    }
    .video-card:hover { transform: scale(1.03); }
}
```

### Canvas/3D on Mobile

Three.js or canvas-based effects must resize responsively:

```css
@media (max-width: 768px) and (max-height: 900px) {
    #slide-meet-frxme canvas { height: clamp(200px, 35vh, 300px) !important; }
}
@media (max-height: 500px) {
    #slide-meet-frxme canvas { height: clamp(150px, 40vh, 250px) !important; }
}
```

Also limit `devicePixelRatio` to 2 for canvas renderers:
```javascript
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Fonts not loading | Check Fontshare/Google Fonts URL; ensure font names match in CSS |
| Animations not triggering | Verify Intersection Observer is running; check `.visible` class is being added |
| Scroll snap not working | Ensure `scroll-snap-type: y mandatory` on html; each slide needs `scroll-snap-align: start` |
| 3D rotation jittery | Throttle scroll handler; use `will-change: transform` on product element |
| Videos not playing on mobile | Must have `playsinline`, `muted`, `webkit-playsinline`. Use lazy loading via IntersectionObserver — never load all videos at once |
| Videos too far apart in landscape | Constrain `max-width` on `.video-card` in landscape breakpoint |
| Title slide feels empty on mobile | Scale up hero elements with `vw` units (e.g. `width: 55vw`), add `flex-wrap` to stat rows |
| `dvh` not working | Always double-declare: `height: 100vh; height: 100dvh;` |
| Performance issues | Use `will-change` sparingly; prefer `transform`/`opacity` animations; throttle scroll handlers; pause off-screen videos |
