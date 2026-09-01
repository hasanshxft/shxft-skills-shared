<!-- linter:skip-file -->
# AI-tell hard bans — machine-enforced

Every item here is enforced by `scripts/lint-copy.py`. Any line containing any of these blocks the deck push. If a hard-banned word feels like the right one, the sentence is wrong. Rewrite the sentence.

The bans are precise. Each one has a documented failure case where it appeared in real copy and was caught (by a client, a colleague, or a linter downstream).

---

## Lexical hard bans

### Filler / puff words

Never use these in client-facing copy:

- **unlock** ("unlock the potential of...")
- **elevate** ("elevate your brand...")
- **leverage** ("leverage AR...")
- **seamless / seamlessly** (implies frictionless without evidence)
- **empower / empowerment** (management-speak)
- **harness** ("harness the power of...")
- **tapestry** ("rich tapestry of...")
- **landscape** ("digital landscape," "shifting landscape," "marketing landscape")
- **revolutionize / revolutionary**
- **supercharge / turbocharge**
- **curate / curated** (unless literally editorial curation)
- **foster** ("foster community," "foster engagement")
- **embark** ("embark on a journey")
- **delve / delve into**
- **navigate** ("navigate the complexities...")
- **robust** ("robust platform")
- **cutting-edge**
- **best-in-class**
- **holistic**
- **synergy / synergies**
- **transform / transformation** — permitted ONLY when the subject is literally XR/AR/VR (physical-to-digital) or a body-tracking effect. Never permitted for "digital transformation," "business transformation," "customer transformation."
- **journey** ("customer journey," "your journey," "our journey")
- **passionate** ("passionate about")
- **solutions** ("digital solutions," "our solutions," "creative solutions")
- **industry-leading**
- **cutting edge**
- **premium quality**
- **end-to-end** (describe the ends instead)
- **thought leadership**
- **best-in-class**
- **paradigm shift**
- **game-changer / game-changing**
- **disrupt / disruption / disruptive**
- **circle back**
- **at the end of the day**
- **that being said**
- **needless to say**
- **in short**
- **simply put**
- **ultimately** (as a sentence opener)
- **essentially** (as a hedge)
- **actually** (as a filler)
- **basically** (as a filler)
- **kind of / sort of / a bit** (hedging)

### Banned openers

Blocked at the start of any paragraph or slide:

- *"Introducing..."*
- *"Discover..."*
- *"Experience the..."*
- *"Welcome to a new era of..."*
- *"In today's [X] landscape..."*
- *"In a world where..."*
- *"Picture this:"*
- *"Imagine this:"*
- *"Ever notice how...?"*
- *"Sound familiar?"*
- *"Let's dive in / dive into..."*
- *"Now imagine..."*
- *"Simply put,"*
- *"That being said,"*
- *"Whether you're X or Y..."*
- *"When it comes to..."*

### Banned closers / rhetorical devices

- *"The result?"* — as a rhetorical question ending a paragraph
- *"The takeaway?"* — same pattern
- *"The bottom line?"* — same
- *"Sound familiar?"* — closer or opener, both banned
- *"Enter [product]."* — cliche introduction
- *"[Product] is here to change all that."*
- *"But here's the thing..."*
- *"That's where [product] comes in."*
- *"That's why we built [product]."* — softened version banned in headlines, permitted only in body copy with a specific reason attached

---

## Structural hard bans

### Em-dashes and en-dashes

**All em-dashes `—` and en-dashes `–` are banned in client-facing copy.** Use:
- Period + space + capital for a hard break: `"The lens works. It shipped in a week."`
- Colon for introduction: `"Three lenses land: Runner, Frame, Scan."`
- Comma for a soft join: `"Snap lens, always-on, one a month."`
- The SHXFT house-style middle-dot separator ` . ` (space + period + space) for label-list joining: `"Sep 23 . Our Story . National Day"` — used in labels, eyebrows, metadata, not sentences.

Hyphens `-` remain permitted for compound modifiers ("first-party," "on-floor") and only there. The `<title>` and `<og:title>` meta tags can use a hyphen as a brand separator (e.g., `"SHXFT Studio - SquatWolf Playbook"`).

### The "Not X, it's Y" construction

Banned when it appears more than once per deck. Signature AI-generated antithesis.

Examples that would block:
- *"It's not a mirror, it's a portal."*
- *"It's not a campaign, it's a movement."*
- *"It's not an ad, it's a conversation."*

Permitted once per deck if the construction is doing genuine strategic work (naming a real reframe). Twice or more = ban.

### Bold-header-colon inline lists

Banned pattern:
```
**Speed:** it ships faster. **Clarity:** users get it. **Trust:** they come back.
```

This is the #1 formatting fingerprint of LLM-generated body copy. If a list needs sub-labels, break it into an actual bulleted list or use ledes without bold-colon coupling.

### Adverbial-semicolon coupling

Banned pattern:
```
Weather is changing; however, agriculture adapts.
The lens works; moreover, it scales.
```

Semicolons themselves are fine when they join two closely related independent clauses without a conjunctive adverb (`however, moreover, therefore, furthermore, additionally`). The semicolon-plus-adverb tic is the AI structural fingerprint.

### Additionally / Moreover / Furthermore as sentence openers

Banned as sentence openers. Post-2023 LLM corpora over-produce these as connective tissue.

Replace with:
- Period + start a new sentence (most cases)
- A shorter conjunction: "Also," "And," "Plus," "Then"
- Or restructure so the connection is implicit

### Ascending tricolons

Three-item lists where each item is longer than the last:
```
Fast, reliable, and scalable across every touchpoint.
Sharp, deliberate, and calibrated for global scale.
Speed, precision, and long-term brand equity.
```

Banned when the pattern appears more than twice per deck. A single ascending tricolon is elegant. Three back-to-back is the signature AI move.

### Vague authority attribution

Banned phrases:
- *"Industry reports suggest..."*
- *"Experts argue..."*
- *"Studies show..."* (without named source)
- *"Recent data indicates..."* (without named source)
- *"Observers have noted..."*
- *"It has been said that..."*
- *"According to industry sources..."*

Cite the source or don't make the claim. This is `feedback_cite_stats_in_decks.md` restated.

### Present-participle closer tags

Banned when they appear at the end of sentences as pseudo-analysis:
- *"...highlighting the shift toward..."*
- *"...underscoring the trend in..."*
- *"...fostering community around..."*
- *"...positioning the brand as..."*
- *"...marking a departure from..."*

These are AI synthesis-without-attribution moves. If a sentence needs to state its own significance, the significance wasn't clear enough.

---

## Formatting hard bans

- **Decorative emoji** on stat tiles, KPI cards, section dividers, hero headlines. Custom monoline SVGs in brand accent color instead. Functional emoji on step-list bullets is context-dependent (see soft flags).
- **Lucide icons** on client-facing sites and decks. Use custom hand-drawn SVG in brand accent color instead. (Fine for internal CNQR OS.)
- **Any bulleted list where every bullet starts with a bold word followed by a colon** (unless it's actually a table row misformatted).

---

## Hard-ban exceptions (documented, narrow)

- **"Transform"** — permitted when the subject is literally physical-to-digital XR/AR/VR or body-tracking (e.g., "the lens transforms your face"). Banned everywhere else.
- **"Journey"** — permitted when literally a physical or narrative journey (a marathon, a trip, a customer's actual multi-step movement through a store). Banned for "customer journey," "brand journey," "our journey."
- **Em-dash in `<title>` / meta tags only** — the hyphen brand separator (e.g., `"SHXFT - Genie"`) uses a hyphen, not em-dash. But if a legitimate exception arises in metadata, en-dash is permitted with an inline linter override comment `<!-- linter:allow-dash -->`.

Every other listed word/phrase/structure is banned without exception. If you need to reach for one, rewrite the sentence.
