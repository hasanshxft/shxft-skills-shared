# HTML Presentation Template

Reference architecture for generating slide presentations. Every presentation follows this structure.

## Base HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>

    <!-- Fonts: use Fontshare or Google Fonts — never system fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">

    <style>
        /* ===========================================
           CSS CUSTOM PROPERTIES (THEME)
           Change these to change the whole look
           =========================================== */
        :root {
            /* Colors — from chosen style preset */
            --bg-primary: #0a0f1c;
            --bg-secondary: #111827;
            --text-primary: #ffffff;
            --text-secondary: #9ca3af;
            --accent: #00ffcc;
            --accent-glow: rgba(0, 255, 204, 0.3);

            /* Typography — MUST use clamp() */
            --font-display: 'Clash Display', sans-serif;
            --font-body: 'Satoshi', sans-serif;
            --title-size: clamp(2rem, 6vw, 5rem);
            --subtitle-size: clamp(0.875rem, 2vw, 1.25rem);
            --body-size: clamp(0.75rem, 1.2vw, 1rem);

            /* Spacing — MUST use clamp() */
            --slide-padding: clamp(1.5rem, 4vw, 4rem);
            --content-gap: clamp(1rem, 2vw, 2rem);

            /* Animation */
            --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
            --duration-normal: 0.6s;
        }

        /* ===========================================
           BASE STYLES
           =========================================== */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        /* --- PASTE viewport-base.css CONTENTS HERE --- */

        /* ===========================================
           ANIMATIONS
           Trigger via .visible class (added by JS on scroll)
           =========================================== */
        .reveal {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity var(--duration-normal) var(--ease-out-expo),
                        transform var(--duration-normal) var(--ease-out-expo);
        }

        .slide.visible .reveal {
            opacity: 1;
            transform: translateY(0);
        }

        /* Stagger children for sequential reveal */
        .reveal:nth-child(1) { transition-delay: 0.1s; }
        .reveal:nth-child(2) { transition-delay: 0.2s; }
        .reveal:nth-child(3) { transition-delay: 0.3s; }
        .reveal:nth-child(4) { transition-delay: 0.4s; }

        /* ===========================================
           NAV DOT LABELS
           Shows slide title next to active/hovered dot
           =========================================== */
        .nav-dot-group {
            display: flex;
            align-items: center;
            gap: 8px;
            position: relative;
        }
        .nav-dot-label {
            position: absolute;
            right: 18px;
            font-family: var(--font-mono, monospace);
            font-size: 0.6rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted, #888);
            white-space: nowrap;
            opacity: 0;
            transform: translateX(5px);
            transition: all 0.3s ease;
            pointer-events: none;
        }
        .nav-dot-group.active .nav-dot-label {
            opacity: 1;
            transform: translateX(0);
            animation: labelFadeOut 2.5s ease forwards;
        }
        @media (hover: hover) {
            .nav-dot-group:hover .nav-dot-label {
                opacity: 1;
                transform: translateX(0);
                animation: none;
            }
        }
        @keyframes labelFadeOut {
            0%, 60% { opacity: 1; transform: translateX(0); }
            100% { opacity: 0; transform: translateX(5px); }
        }
        /* Hide labels on small screens — they overlap content */
        @media (max-width: 900px) {
            .nav-dot-label { display: none; }
        }

        /* ===========================================
           ANIMATED BRAND ELEMENTS — Product shots that fly in
           =========================================== */
        .brand-float {
            position: absolute; pointer-events: none; z-index: 1; opacity: 0;
            transition: opacity 1s var(--ease-out-expo), transform 1.2s var(--ease-out-expo);
        }
        .brand-float img {
            max-width: 100%; height: auto;
            filter: drop-shadow(0 8px 32px var(--accent-glow, rgba(0,0,0,0.15)));
        }
        .brand-float.from-right { transform: translateX(80px) rotate(5deg); }
        .slide.visible .brand-float.from-right { opacity: 1; transform: translateX(0) rotate(-2deg); }
        .brand-float.from-left { transform: translateX(-80px) rotate(-5deg); }
        .slide.visible .brand-float.from-left { opacity: 1; transform: translateX(0) rotate(2deg); }
        .brand-float.from-bottom { transform: translateY(60px) scale(0.9); }
        .slide.visible .brand-float.from-bottom { opacity: 1; transform: translateY(0) scale(1); }
        .slide.visible .brand-float.hover-drift {
            animation: brand-drift 4s ease-in-out 1.5s infinite alternate;
        }
        @keyframes brand-drift {
            0% { transform: translateY(0) rotate(-2deg); }
            100% { transform: translateY(-12px) rotate(1deg); }
        }
        .brand-float.delay-1 { transition-delay: 0.3s; }
        .brand-float.delay-2 { transition-delay: 0.6s; }
        .brand-float.delay-3 { transition-delay: 0.9s; }
        @media (max-width: 768px) {
            .brand-float { max-width: 30vw; }
            .brand-float.hide-mobile { display: none; }
        }

        /* ... preset-specific styles ... */
    </style>
</head>
<body>
    <!-- Optional: Progress bar -->
    <div class="progress-bar"></div>

    <!-- Optional: Navigation dots with slide title labels -->
    <nav class="nav-dots" aria-label="Slide navigation"><!-- Generated by JS --></nav>

    <!-- Slides — every slide MUST have a data-title for nav dot labels -->
    <section class="slide title-slide" data-title="Title">
        <h1 class="reveal">Presentation Title</h1>
        <p class="reveal">Subtitle or author</p>
    </section>

    <section class="slide" data-title="Section Name">
        <div class="slide-content">
            <h2 class="reveal">Slide Title</h2>
            <p class="reveal">Content...</p>
        </div>
    </section>

    <!-- More slides... -->

    <script>
        /* ===========================================
           SLIDE PRESENTATION CONTROLLER
           =========================================== */
        class SlidePresentation {
            constructor() {
                this.slides = document.querySelectorAll('.slide');
                this.currentSlide = 0;
                this.setupIntersectionObserver();
                this.setupKeyboardNav();
                this.setupTouchNav();
                this.setupProgressBar();
                this.setupNavDots();
            }

            setupIntersectionObserver() {
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('visible');
                            // Update current slide index
                            this.currentSlide = [...this.slides].indexOf(entry.target);
                            this.updateProgressBar();
                            this.updateNavDots();
                        }
                    });
                }, { threshold: 0.5 });

                this.slides.forEach(slide => observer.observe(slide));
            }

            setupKeyboardNav() {
                document.addEventListener('keydown', (e) => {
                    if (['ArrowDown', 'ArrowRight', 'Space', 'PageDown'].includes(e.key)) {
                        e.preventDefault();
                        this.goToSlide(this.currentSlide + 1);
                    } else if (['ArrowUp', 'ArrowLeft', 'PageUp'].includes(e.key)) {
                        e.preventDefault();
                        this.goToSlide(this.currentSlide - 1);
                    }
                });
            }

            setupTouchNav() {
                let startY = 0;
                document.addEventListener('touchstart', (e) => {
                    startY = e.touches[0].clientY;
                });
                document.addEventListener('touchend', (e) => {
                    const deltaY = startY - e.changedTouches[0].clientY;
                    if (Math.abs(deltaY) > 50) {
                        this.goToSlide(this.currentSlide + (deltaY > 0 ? 1 : -1));
                    }
                });
            }

            setupProgressBar() {
                this.progressBar = document.querySelector('.progress-bar');
                if (this.progressBar) this.updateProgressBar();
            }

            updateProgressBar() {
                if (!this.progressBar) return;
                const progress = ((this.currentSlide + 1) / this.slides.length) * 100;
                this.progressBar.style.width = `${progress}%`;
            }

            setupNavDots() {
                this.navDots = document.querySelector('.nav-dots');
                if (!this.navDots) return;
                // Each slide can have a data-title attribute for the label
                this.navDots.innerHTML = [...this.slides].map((slide, i) => {
                    const title = slide.dataset.title || '';
                    return `<div class="nav-dot-group">
                        <span class="nav-dot-label">${title}</span>
                        <button class="nav-dot${i === 0 ? ' active' : ''}" data-slide="${i}" aria-label="${title || 'Slide ' + (i+1)}"></button>
                    </div>`;
                }).join('');
                this.navDots.addEventListener('click', (e) => {
                    const dot = e.target.closest('.nav-dot');
                    if (dot) this.goToSlide(parseInt(dot.dataset.slide));
                });
            }

            updateNavDots() {
                if (!this.navDots) return;
                this.navDots.querySelectorAll('.nav-dot').forEach((dot, i) => {
                    dot.classList.toggle('active', i === this.currentSlide);
                });
                // Show label for active dot
                this.navDots.querySelectorAll('.nav-dot-group').forEach((group, i) => {
                    group.classList.toggle('active', i === this.currentSlide);
                });
            }

            goToSlide(index) {
                const target = Math.max(0, Math.min(this.slides.length - 1, index));
                this.slides[target].scrollIntoView({ behavior: 'smooth' });
            }
        }

        new SlidePresentation();
    </script>
</body>
</html>
```

## Required JavaScript Features

Every presentation must include:

1. **SlidePresentation Class** — Main controller with:
   - Keyboard navigation (arrows, space, page up/down)
   - Touch/swipe support
   - Progress bar updates
   - Navigation dots

2. **Intersection Observer** — For scroll-triggered animations:
   - Add `.visible` class when slides enter viewport
   - Trigger CSS transitions efficiently

3. **Optional Enhancements** (match to chosen style):
   - 3D tilt on hover (cards)
   - Particle system background (canvas) — Neon Cyber only
   - 3D scroll-linked rotation — product showcases
   - Glow pulse animations — FRXME style
   - Counter animations for stats

4. **Inline Editing** (only if user opted in during Phase 1):
   - Edit toggle button (hidden by default, revealed via hover hotzone or `E` key)
   - Auto-save to localStorage
   - Uses JS-based hover with 400ms delay timeout (NOT CSS sibling selectors)

## Inline Editing Implementation (Opt-In Only)

**If the user chose "No" for inline editing in Phase 1, do NOT generate any edit-related HTML, CSS, or JS.**

**Required approach: JS-based hover with 400ms delay timeout.**

HTML:
```html
<div class="edit-hotzone"></div>
<button class="edit-toggle" id="editToggle" title="Edit mode (E)">&#9998;</button>
```

CSS:
```css
.edit-hotzone {
    position: fixed; top: 0; left: 0;
    width: 80px; height: 80px;
    z-index: 10000;
}
.edit-toggle {
    position: fixed; top: 16px; left: 16px;
    opacity: 0; pointer-events: none;
    transition: opacity 0.3s ease;
    z-index: 10001;
    background: var(--bg-secondary, #222);
    color: var(--text-primary, #fff);
    border: 1px solid var(--border, #333);
    border-radius: 8px;
    padding: 8px 12px;
    cursor: pointer;
    font-size: 1rem;
}
.edit-toggle.show, .edit-toggle.active {
    opacity: 1; pointer-events: auto;
}
```

JS:
```javascript
const hotzone = document.querySelector('.edit-hotzone');
const editToggle = document.getElementById('editToggle');
let hideTimeout = null;
let isEditMode = false;

hotzone.addEventListener('mouseenter', () => {
    clearTimeout(hideTimeout);
    editToggle.classList.add('show');
});
hotzone.addEventListener('mouseleave', () => {
    hideTimeout = setTimeout(() => {
        if (!isEditMode) editToggle.classList.remove('show');
    }, 400);
});
editToggle.addEventListener('mouseenter', () => clearTimeout(hideTimeout));
editToggle.addEventListener('mouseleave', () => {
    hideTimeout = setTimeout(() => {
        if (!isEditMode) editToggle.classList.remove('show');
    }, 400);
});
editToggle.addEventListener('click', toggleEdit);
hotzone.addEventListener('click', toggleEdit);
document.addEventListener('keydown', (e) => {
    if ((e.key === 'e' || e.key === 'E') && !e.target.getAttribute('contenteditable')) {
        toggleEdit();
    }
});

function toggleEdit() {
    isEditMode = !isEditMode;
    editToggle.classList.toggle('active', isEditMode);
    document.querySelectorAll('h1, h2, h3, p, li, span').forEach(el => {
        el.contentEditable = isEditMode;
    });
}
```

## Image Pipeline (Skip If No Images)

**Dependency:** `pip install Pillow`

| Situation | Operation |
|-----------|-----------|
| Square logo on rounded aesthetic | Circular crop with Pillow |
| Image > 1MB | Resize to max 1200px dimension |
| Wrong aspect ratio | Manual crop |

Save processed images with `_processed` suffix. Never overwrite originals.

### Image Placement

Use direct file paths (not base64):

```html
<img src="assets/product.png" alt="Product" class="slide-image">
```

```css
.slide-image {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
    border-radius: 8px;
}
```

**Adapt border/shadow colors to match the chosen style's accent.** Never repeat the same image on multiple slides (except logos on title + closing).

## Code Quality

**Comments:** Every section needs clear comments explaining what it does.

**Accessibility:**
- Semantic HTML (`<section>`, `<nav>`, `<main>`)
- Keyboard navigation works fully
- ARIA labels where needed
- `prefers-reduced-motion` support (included in viewport-base.css)

## File Structure

Single presentations:
```
presentation.html    # Self-contained, all CSS/JS inline
assets/              # Images only, if any
```
