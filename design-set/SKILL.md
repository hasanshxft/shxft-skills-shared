---
name: design-set
description: One entry point for ALL aesthetic and design work. Call this whenever building, redesigning, polishing, animating, or auditing any UI, landing page, site, app screen, or brand look. It routes to the installed design set (frontend-design, taste-skill, design-motion-principles, impeccable, ui-ux-pro-max) in the right order so you never have to pick which one. Respects locked brand systems.
---

# /design-set — the design set orchestrator

You do not need to know which sub-skill to use. This routes for you. Call `/design-set` for any look-and-feel work; frame the task, then pull the right tools in order.

## STEP 1 — Frame the task (one line)

- **A. New build** — a page/site/screen from scratch or near-scratch.
- **B. Redesign / polish** — improve something that already exists.
- **C. Motion** — add or fix animation, transitions, micro-interactions.
- **D. Audit only** — "is this any good / does it have AI tells" with no rebuild.
- **E. Brand direction** — palette, fonts, style for a NEW brand with no identity yet.

## STEP 2 — Check for a locked brand (NON-NEGOTIABLE)

Before applying any skill, check `~/.claude/CLAUDE.md` for a locked design system on this brand (MNTOR = Manrope + Clean green/ink; SHXFT = Onest B&W; CNQR = Antonio/Space Grotesk; RIVLS = Space Grotesk/navy; Bites = Clash/Satoshi; FRXME = teal glass). **If one exists, it WINS.** The skills below elevate craft, spacing, hierarchy, and motion WITHIN that system. They never override committed fonts, palette, or the vibe-coded-tells bans in Hasan's memory.

## STEP 3 — Route (load only what the task needs)

| Task | Pipeline (in order) |
|---|---|
| **A. New build** | `frontend-design` (direction/thesis) → `taste-skill` flagship `skills/taste-skill/SKILL.md` (build) → `design-motion-principles` create mode → `impeccable` audit |
| **B. Redesign / polish** | `taste-skill` `skills/redesign-skill/SKILL.md` (audit-first upgrade) → `design-motion-principles` audit → apply → `impeccable` audit |
| **C. Motion** | `design-motion-principles` (create or audit — it self-detects) |
| **D. Audit only** | `impeccable` detectors + `taste-skill/skills/redesign-skill` diagnosis + `design-motion-principles` audit. Report findings, propose fixes, do NOT rewrite unasked. |
| **E. Brand direction (new brand)** | `ui-ux-pro-max` (2-3 palette + font-pairing options) → `frontend-design` (commit with a point of view) |

Special looks: minimalist → `taste-skill/skills/minimalist-skill`; brutalist → `.../brutalist-skill`; brand-kit imagery → `.../brandkit`; per-section design images → `.../imagegen-frontend-web`.

## STEP 4 — Always finish with the taste check

1. No AI tells (Inter/Lucide defaults, purple-on-black, cards-in-cards, emoji-as-icons, round-number fake stats, fake logo walls) — cross-check `feedback_vibe_coded_sites` memory.
2. Motion is opacity/transform/scale only, no colored glows (hard rule).
3. It still reads as the CLIENT's brand, not a template.

## Principle

Match complexity to the vision. Minimal needs precision in spacing/type/detail; maximal needs elaborate execution. Elegance is executing the chosen vision well, not adding more.
