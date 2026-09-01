# SHXFT shared skills

Claude Code skills for building SHXFT decks and writing in the house voice.

| Skill | What it does |
|---|---|
| `deck/` | Builds animation-rich single-file HTML proposal decks. Includes the house style presets, animation patterns and the hard-won mobile/3D fixes. |
| `copy/` | House voice plus the AI-tell linter. Catches the banned words and vibe-coded phrasing. |
| `deck-to-pdf/` | Turns a finished HTML deck into a shareable PDF. |
| `design-set/` | Router that picks the right design skill for a given task. |

## Install

Clone, then symlink into your Claude skills directory:

```bash
git clone https://github.com/hasanshxft/shxft-skills-shared.git
cd shxft-skills-shared
mkdir -p ~/.claude/skills
for s in deck copy deck-to-pdf design-set; do
  ln -sfn "$PWD/$s" ~/.claude/skills/$s
done
```

Then run `/deck` or `/copy` in Claude Code.

`git pull` to take updates.

## Note

This is the craft layer only. Client commercial files (pricing, deal terms,
negotiation positions) are deliberately not in this repo.
