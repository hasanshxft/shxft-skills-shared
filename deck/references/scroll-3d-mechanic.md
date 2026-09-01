# Canonical scroll + 3D mechanic (COPY VERBATIM — do not re-derive)

**Reference deck: SquatWolf KSA (`PROPOSALS/SHXFT/squatwolf-ksa-launch/index.html`).**
It scrolls perfectly on every device and its 3D FRXME drags on mobile. Every deck
that scrolls slide-to-slide or embeds a 3D viewer MUST use this exact mechanic.
Do NOT invent a variant. The Dr Joy deck (2026-07-19) burned hours because it
diverged on the small details below; each divergence is called out so it never
recurs.

---

## 1. Scroll CSS — paste as-is

```css
/* html: ONLY these three properties. No overflow-y. No -webkit-overflow-scrolling. */
html { scroll-snap-type: y mandatory; scroll-behavior: smooth; overflow-x: hidden; }
body { overflow-x: hidden; /* + your bg/color/font */ }

.slide {
    width: 100%;              /* NOT 100vw — 100vw includes scrollbar width and causes h-overflow */
    min-height: 100vh;        /* min-height, NOT height */
    overflow: hidden;
    scroll-snap-align: start;
    position: relative;
    /* + your display/padding */
}

/* Mobile: breakpoint 820px, NOT 768. iPads/large phones are 810-834px and fall
   through a 768 gap, keeping snap mandatory -> first swipe "snaps back". */
@media (max-width: 820px) {
    html { scroll-snap-type: none; }
    .slide { min-height: auto; scroll-snap-align: none; padding: /* your mobile padding */; }
    .slide-cover { min-height: 100dvh; }   /* the TITLE/cover slide stays full-screen, then you scroll */
    /* collapse every multi-column grid to 1fr here */
}
```

**The title slide gets `class="slide slide-cover ..."`** so it fills the screen on
mobile while content slides flow to their content height.

### DO NOT (these each broke the Dr Joy deck)
- ❌ `-webkit-overflow-scrolling: touch` on html — iOS scroll-sticking culprit.
- ❌ `overflow-y: scroll` (or `auto`) on html — creates a nested scroll context that sticks on iOS. Leave overflow-y unset.
- ❌ breakpoint at 768px — use 820px everywhere (layout + snap).
- ❌ `width: 100vw` on slides — use `width: 100%`.
- ❌ inline `style="grid-template-columns: ..."` on a grid that must collapse on mobile — inline styles beat the media query, so the slide never stacks. Put column counts in CSS classes only.
- ❌ JS "capability detection" (`hover: none` / `pointer: coarse`) to disable snap — an iPad with a trackpad defeats it. The 820px CSS breakpoint is enough.

---

## 1b. Keyboard navigation — MANDATORY on every deck

Decks get presented. Presenters drive with arrow keys. A deck that ignores
them feels broken in front of a client, and this has been raised repeatedly.
Ship this in every deck, no exceptions.

```js
const slides=[...document.querySelectorAll('.slide')];
// Derive the current slide from viewport position, never from a counter, so it
// stays correct after any manual scroll, nav-dot click or hash jump.
function currentIndex(){
  let best=0,bestD=Infinity;
  slides.forEach((s,i)=>{const d=Math.abs(s.getBoundingClientRect().top);if(d<bestD){bestD=d;best=i;}});
  return best;
}
function go(dir){
  const i=currentIndex(), n=Math.min(slides.length-1,Math.max(0,i+dir));
  if(n!==i) slides[n].scrollIntoView({behavior:'smooth',block:'start'});
}
addEventListener('keydown',(e)=>{
  const t=e.target;
  if(t&&(t.tagName==='INPUT'||t.tagName==='TEXTAREA'||t.isContentEditable)) return;
  switch(e.key){
    case 'ArrowRight': case 'ArrowDown': case 'PageDown': case ' ': case 'Spacebar':
      e.preventDefault(); go(1); break;
    case 'ArrowLeft': case 'ArrowUp': case 'PageUp':
      e.preventDefault(); go(-1); break;
    case 'Home': e.preventDefault(); slides[0].scrollIntoView({behavior:'smooth'}); break;
    case 'End': e.preventDefault(); slides[slides.length-1].scrollIntoView({behavior:'smooth'}); break;
  }
});
```

Bind **all** of: left/right, up/down, PageUp/PageDown, space, Home, End.
Space is what most people press. `e.preventDefault()` matters, otherwise space
double-scrolls. Show a small `← →` hint for a few seconds on pointer devices,
then fade it.

### DO NOT
- ❌ ship a deck with no key handling. This is the single most common complaint.
- ❌ track position with an incrementing counter. It desyncs the moment the user scrolls.
- ❌ swallow keys while an input or textarea has focus.

---

## 2. 3D viewer — paste as-is

```css
/* Constrained panel, NOT full-screen. Text sits around it so the page scrolls. */
.frxme-3d-wrap { position: relative; aspect-ratio: 4/5; overflow: hidden; /* + border/bg */ }
.frxme-3d-wrap canvas { width: 100% !important; height: 100% !important; display: block; cursor: grab; }
/* NO touch-action declaration on the canvas — let OrbitControls manage it. */
@media (max-width: 820px) { .frxme-3d-wrap { aspect-ratio: 1/1; max-height: 50vh; } }
```

```js
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true; controls.enableZoom = false; controls.enablePan = false;
// ... polar limits, target ...
// OrbitControls stays ENABLED on all devices. The 3D is a small ~50vh panel with
// text above/below, so on mobile you drag the model and scroll on the text.
```

### DO NOT
- ❌ `controls.enabled = false` on touch — that freezes the model (Dr Joy "3D won't move").
- ❌ `canvas.style.touchAction = 'pan-y'` / `touch-action: none` overrides — leave it to OrbitControls.
- ❌ a full-screen / 60vh+ 3D that fills the mobile slide — with no text to grab, the canvas traps the swipe and the page feels frozen. Keep it ~50vh with content around it.

---

## The rule
When a deck needs slide scroll or a 3D viewer, open the SquatWolf deck, copy this
mechanic verbatim, then build the deck's content on top. Never tune scroll/3D from
scratch. If SquatWolf does it one way and you're tempted to do it another, don't.
