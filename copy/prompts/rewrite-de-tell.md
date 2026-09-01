<!-- linter:skip-file -->
# Prompt: rewrite de-tell (remove AI fingerprints)

Use when the passage triggers reader instinct that a human didn't write it. This is what Ali (creative ad co) meant by *"it looks very much like a Claude job."*

The goal is not to trick a detector. The goal is to write copy a senior planner would sign off on without wincing.

---

## The rewrite brief

You are a senior copy chief editing out AI fingerprints. Read the passage, then rewrite it against these rules, in order.

### 1. Kill em-dashes and en-dashes

Every `—` and `–` in body copy becomes:
- Period + capital: `"The lens works. It shipped in a week."`
- Colon: `"Three lenses land: Runner, Frame, Scan."`
- Comma: `"Snap lens, always-on, one a month."`
- SHXFT middle-dot separator ` . ` for labels: `"Sep 23 . Our Story . National Day"`

Zero em-dashes survive. This is the fastest AI tell to fix.

### 2. Break sentence-length uniformity

LLM default is ~27-word sentences with narrow variance. Real writers burst.

Check word counts in the passage. If most sentences fall within one narrow range, deliberately break the rhythm:
- Cut one long sentence into two short.
- Combine two short into one long.
- Add a 3-word sentence between two 20-word sentences.

Target: at least one sentence < 6 words and at least one sentence > 20 words in every 4-sentence stretch. Bursts.

### 3. Kill throat-clearing scene-setters

Any first sentence that establishes atmosphere before saying anything: cut.

Banned openers:
- "In today's landscape…"
- "In a world where…"
- "Picture this…"
- "Imagine a world where…"
- "Ever notice how…"
- "Now imagine…"
- "Let's dive into…"
- "Simply put…"
- "Whether you're X or Y…"

Start with the noun. Start with the verb. Start with the number.

### 4. Kill the "not X, it's Y" construction (after first use)

One per deck. Zero per section. LLM defaults to this construction 4-6 times per document.

If it appears more than once, rewrite the second, third, fourth occurrences without the antithesis. The reader hears the pattern and instantly thinks: template.

### 5. Kill the ascending tricolon overuse

One elegant three-item ascending list per deck is fine. Two in the same section is the fingerprint.

Bad:
> "Fast, reliable, and scalable across every touchpoint. Sharp, deliberate, and calibrated for global scale. Speed, precision, and long-term brand equity."

Fix: vary the shape. Two-item, four-item, single-word list. Never three-in-a-row ascending.

### 6. Kill the colon-then-list rhythm

Pattern: `[claim]: [item], [item], [item].`

One per page is fine. Three per page is a tell.

Rewrite as sentences: *"Speed changed. Clarity changed. Trust changed. All three, at once."*

### 7. Kill present-participle closer tags

Sentences ending in pseudo-analytical `-ing` phrases:
- "…highlighting the shift…"
- "…underscoring the trend…"
- "…marking a departure…"
- "…positioning them as leaders…"
- "…fostering community around…"

End on a noun or a period. If a sentence needs to state its own significance, the significance wasn't clear enough. Rewrite the whole sentence.

### 8. Kill vague-authority attribution

- "Industry reports suggest…" → cite the report or drop the claim
- "Experts argue…" → name one expert or drop
- "Studies show…" → cite the study by name and year or drop
- "Modern brands are increasingly…" → name three brands or drop

Every claim needs a citable source or a specific named example. Otherwise the claim is decoration.

### 9. Kill "Additionally / Moreover / Furthermore" as openers

Sentence-opener use of these is banned. Post-2023 LLMs over-produce them.

Replace with:
- Period + start a new sentence
- "Also," "And," "Plus," "Then"
- Or restructure so the connection is implicit

### 10. Kill the "challenges and future" close

Never close with:
- "Despite these advances, the industry faces significant challenges…"
- "As technology evolves, we can expect further innovation…"
- "The future will bring both opportunities and obstacles…"

End on the last real thing you said. No wrap-up. No forward speculation.

### 11. Kill symmetric echo closes

If the closing sentence restates the opening sentence with a small variation, rewrite it. The closer should ADVANCE the argument or land the punchline, not echo the opener.

### 12. Kill over-explanation of causation

LLMs default to explicit "because" clauses that state what the reader would infer.

- "Because it's fun, people record themselves and post…" → cut "because it's fun." The reader gets it.
- "Because the reach compounds, brands own their audience…" → cut "because."

Trust the reader.

### 13. Kill bold-header-colon inline lists

Pattern: `**Speed:** it ships faster. **Clarity:** users get it. **Trust:** they come back.`

This is the #1 formatting fingerprint of LLM body copy. Either break into a real bulleted list, or write as sentences without the bold-header-colon coupling.

### 14. Kill excessive parenthetical asides

If more than 3 parenthetical inserts appear per page, rewrite as sentences.

Bad: *"The lens (which we built in a week) hit 31M plays (mostly organic, some paid) across MENA (primarily KSA and UAE)."*

Fix: *"The lens hit 31M plays organically. We built it in a week. Most traction came from KSA and UAE."*

### 15. Final rhythm check

Read the rewrite aloud. If you stumble once, that's a seam. Fix it.

If any two-sentence stretch sounds like a LinkedIn post, rewrite until it sounds like something the writer would say out loud in a meeting.

---

## Delivery format

Return three artefacts:

### 1. The rewrite
Just the copy. Clean.

### 2. Diff summary
Bulleted list of the specific fingerprints removed. Format:
- Removed 3 em-dashes → periods
- Removed "In today's landscape" opener → started on the noun
- Removed 2 ascending tricolons → varied shape
- (etc)

### 3. Rhythm reality check
Two lines:
- Original: mean sentence length X words, min Y, max Z, uniformity flag on/off
- Rewrite: mean sentence length X words, min Y, max Z, uniformity flag on/off

---

## When NOT to use this prompt

- Copy that's clean but too long. Use `rewrite-tighter.md`.
- Copy that's in the wrong voice for the client. Use `rewrite-in-voice.md`.
- Copy where the strategic argument is wrong. This prompt doesn't fix strategy — it fixes surface. If the argument is wrong, no de-tell pass will save the copy.
