# Jabella Painting and Carpentry website

A one-page static site for Jabella Painting and Carpentry (Boca Raton, Delray
Beach, Highland Beach), structured after the Evercoat Painting Co. demo page:
a scroll-scrubbed painting film hero, then services, a before/after slider,
inspiration, why-us, process, about, promise, FAQ and an estimate form.

All photography and footage were generated through Higgsfield (Seedream 5 Pro
stills, Seedance 2.0 clips) from one shared style preamble. See `BRIEF.md`.

## Files
- `index.html`, `site.css`, `site.js`: the page. No build step, no framework.
- `assets/hero.mp4` (desktop, 1080p) and `assets/hero-m.mp4` (phone, 720p): the
  15 s hero film, encoded with a dense keyframe interval so it scrubs cleanly.
  `hero-start.webp` is its first frame, `hero-end.webp` its last.
- `assets/*.webp`: section imagery. `logo.webp` / `logo-white.webp` are the
  supplied logo, upscaled 2.4x with Lanczos (the Higgsfield upscaler rejected
  the 304 px source).
- `out/`: raw generations and `jobs.json` (filename to Higgsfield job ID), so
  any still can be fed back into a later generation.
- `lab/`: verification scripts and screenshots (`walk.mjs`, `interact.mjs`).

## Preview
```
node /Users/macbookm5pro/.claude/skills/scroll-craft-higgsfield/scripts/serve.mjs --root . --port 4510
```
or any static server. The `.claude/launch.json` entry `jabella-live` attaches
the Claude browser pane to port 4510.

## Verify
```
node lab/walk.mjs --out lab/walk                       # desktop, 16 scroll positions
node lab/walk.mjs --out lab/mobile --width 390 --height 844
node lab/walk.mjs --out lab/reduced --reduced-motion   # static hero fallback
node lab/interact.mjs                                  # slider, FAQ, form, menu, tab order
```
`node_modules` is a symlink to the Harbor build's (playwright-core).

## Before launch, replace
- The team photo (`assets/team.webp` is a generated placeholder crew).
- Phone, email, address, license number, years in business, warranty terms.
- The form endpoint: `site.js` only shows a success state. Wire it to
  GoHighLevel, Formspree or similar.
- `og:image` and the canonical URL once the domain exists.
