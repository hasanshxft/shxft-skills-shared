# Proposal Generator

A Claude Code skill for creating animation-rich HTML slide presentations and client proposals. Built and refined by SHXFT Studio.

## What it does

Generates self-contained HTML decks with:
- Co-branded client proposals with 3D product viewers (Three.js)
- 8+ design presets (FRXME Dark, SHXFT Sketch, Bold Signal, Dark Botanical, Swiss Modern, Neon Cyber, SCXPE Architectural)
- Animation library with reveal effects, scroll-linked rotations, ambient particles
- Bilingual support (EN + any language toggle)
- Mobile-responsive with airtight portrait/landscape handling
- Reference video embeds with content protection
- WhatsApp CTA buttons, confetti celebrations, OG meta tags
- Full proposal narrative arc: Title → Your World → Challenge → Shift → Product → Concepts → Why Now → Next Steps

## Installation

Clone into your Claude Code skills folder:

```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/hasanshxft/proposal-generator.git deck
```

Restart Claude Code. Use with `/deck` to generate any presentation, or describe a client and Claude will trigger Proposal Mode automatically.

## Updating

```bash
cd ~/.claude/skills/deck
git pull
```

## Customisation

Before using, update the following to match your studio:
- `SKILL.md` — replace `hello@shxft.studio` with your contact email
- `SKILL.md` — replace SHXFT/FRXME parent brand references with your own brands
- `assets/shxft/` and `assets/frxme/` — replace with your brand logos
- `proposal-pricing.md` — update pricing tiers for your services
- `brief-templates.md` — adjust default brief structures

## Knowledge Base

The `knowledge/` folder tracks every proposal generated: client, brief, concepts, brand research, outcomes. This compounds over time and lets future proposals reference past wins. Add to it from your side as you generate decks.

## Contributing

Fork, improve, push back. Every refinement helps the next proposal land better. The skill evolves through real client work.

## Built by

[SHXFT Studio](https://shxft.studio) — Creative XR & Innovation Studio. Dubai.
