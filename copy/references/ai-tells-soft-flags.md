<!-- linter:skip-file -->
# AI-tell soft flags — surface but don't block

The hard bans in `ai-tells-hard-bans.md` are non-negotiable. These soft flags are patterns that read AI *in aggregate* — one instance is usually fine, multiple in the same section is a fingerprint. The linter surfaces them for review, doesn't reflexively block.

Judgement: does this instance do work, or is it default LLM output?

---

## Rhythm and shape

### Uniform sentence length (low burstiness)

The single most reliable AI signal at scale. Real writers vary sentence length dramatically. LLMs default to ~27-word sentences with narrow variance.

**Detection:** paragraph-level. Flag when the standard deviation of sentence lengths in a paragraph is below 40% of the mean. Two 25-word sentences followed by two 27-word sentences is a fingerprint. Two 25-word sentences followed by a five-word sentence and a fifteen-word sentence is a real writer.

**Fix:** cut a sentence in half. Combine two into one longer thought. Alternate. Break the pattern deliberately.

### Ascending tricolon overuse

One ascending tricolon per section: elegant. Two or more back-to-back: fingerprint.

**Detection:** flag paragraphs with more than one instance of a three-item list where item 3 is longer than item 2 which is longer than item 1.

Example fingerprint:
> Fast, reliable, and scalable to every touchpoint. Sharp, deliberate, and calibrated for the modern buyer. Smart, adaptive, and always evolving with your needs.

**Fix:** vary the shape. Two-item, four-item, or single-word list.

### Colon-then-list rhythm

Pattern: `[claim]: [item], [item], [item].`

Example: *"Here's what changed: speed, clarity, trust."*

One is fine. Three in a page is a tell.

**Fix:** replace with sentence structure. *"Speed changed. Clarity changed. Trust changed. All three, at the same time."*

### Symmetric echo close

Final line of a paragraph or section restates the opener with a small variation. Reads polished but artificial.

Example fingerprint:
> Opener: *"Snap is where they are themselves."*
> Closer: *"Because on Snap, they get to be themselves."*

**Fix:** the closer should DO something the opener didn't. Advance the argument. Land the punchline. Don't echo.

### Present-participle closer tags

Sentences ending in `-ing` phrases that add pseudo-significance:
- *"...highlighting the shift..."*
- *"...underscoring the trend..."*
- *"...marking a new era..."*
- *"...positioning them as leaders..."*

Blocked as hard ban in `ai-tells-hard-bans.md`. Soft version here: `-ing` closers doing legitimate work (describing an actual action being taken) are permitted.

**Detection:** flag any sentence ending in an `-ing` phrase that starts with `highlighting, underscoring, marking, positioning, fostering, driving, enabling, showcasing, illustrating, demonstrating`.

**Fix:** end on a noun or a period.

---

## Openers and transitions

### Scene-setter openers

Any opener that establishes atmosphere before saying anything:
- *"Picture this:"* — banned as hard
- *"Imagine a world where..."* — banned as hard
- *"In today's landscape..."* — banned as hard
- *"It's Monday morning and..."* — soft flag
- *"You're a marketing director..."* — soft flag
- *"Every day, thousands of..."* — soft flag

Soft flagged versions might work in narrative case studies. Never in first-paragraph opener of a deck slide.

**Fix:** start with the noun. Start with the verb. Start with the specific.

### "Furthermore / Moreover / Additionally" as connectives

Hard-banned as sentence openers (see `ai-tells-hard-bans.md`).

Soft flagged when they appear mid-paragraph as pseudo-transitions:
> "The lens works. Furthermore, it ships in a week."

**Fix:** period + start a new sentence. Or a shorter connective ("Also," "Plus," "And").

### Rhetorical questions that aren't rhetorical

Fake-Socratic openers:
- *"Have you ever wondered why...?"*
- *"What if I told you...?"*
- *"Ever notice how...?"* — banned as hard
- *"Isn't it time we...?"*

Real rhetorical questions doing work are permitted rarely. Fake ones (LLM-generated attempts at engagement) are the tell.

**Fix:** state the observation directly.

---

## Content patterns

### Hedge stacks

Three or more hedges within a section reads as commitment avoidance:
- *typically*
- *generally*
- *may*
- *some argue*
- *often considered*
- *is thought to be*
- *tends to*
- *in most cases*

**Detection:** flag sections with 3+ hedges per 100 words.

**Fix:** delete every hedge and see if the claim survives. If it does, ship without hedges. If it doesn't, the claim needed evidence, not softening.

### The "challenges and future" close

LLMs default to closing arguments with acknowledgment of challenges + speculation about future solutions:
> "Despite these advances, the industry faces significant challenges. As technology evolves, we can expect further innovation."

Universally hollow. If a real challenge exists, name it and address it. If not, don't manufacture one.

**Fix:** end on the last real thing you said. No wrap-up. No forward-looking speculation.

### Vague-authority attribution

Hard-banned in `ai-tells-hard-bans.md`. Soft-flagged variants:
- *"Marketing professionals report..."*
- *"Modern brands are increasingly..."*
- *"Today's consumers..."*

Not blocked but flagged. If you're going to make a claim about a group, cite one specific example instead. *"Nike, Adidas and Gymshark all run monthly Snap media buys. None of them ship monthly Lenses."* > *"Modern brands are missing the Lens opportunity."*

### Over-explanation of causation

LLM tell: explicit "because" clauses that state what the reader would infer:
- *"Because it's fun, people record themselves and post..."* — the "because it's fun" is unnecessary.
- *"Because the reach compounds, brands own their audience..."* — the "because" is doing the reader's job.

**Fix:** delete the "because" clause. Trust the reader.

---

## Formatting tells

### Bold-header-colon inline lists

Hard-banned in body text. Soft-flagged when appearing in lede paragraphs or callouts:
> *Speed. Clarity. Trust.*

The pure noun-list without bold-header is fine. The moment it becomes `**Speed:** [description]. **Clarity:** [description].` inline, it's the LLM formatting fingerprint.

### Excessive parenthetical asides

Pattern: parenthetical inserts appearing more than 3 times per page. LLM default for hedging claims mid-sentence.

Example fingerprint:
> "The lens (which we built in a week) hit 31M plays (mostly organic, some paid) across MENA (primarily KSA and UAE)."

**Fix:** rewrite as sentences. *"The lens hit 31M plays organically. We built it in a week. Most traction came from KSA and UAE."*

### Overuse of dashes as parentheticals

Real writers use em-dashes for parenthetical asides — like this — occasionally. LLMs use them 3-5x per paragraph.

Em-dashes are hard-banned anyway. But hyphens and en-dashes used in the same parenthetical role trigger this soft flag.

**Fix:** replace with commas or periods. The reader doesn't notice missing dashes. They notice too-many.

---

## The judgement question

For every soft flag the linter surfaces, ask:

> *Is this instance doing genuine strategic work — carrying a specific meaning the plain version can't — or is this default LLM output the writer left in place?*

If it's doing work: keep. Note why.
If it's default output: rewrite.

The soft flag file exists because the same pattern that reads as AI in one paragraph can be a deliberate rhetorical move in another. Judgement is required. But default is: rewrite.
