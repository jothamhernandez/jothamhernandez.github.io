---
name: portfolio-design
description: >-
  The visual design system for this Nuxt + Tailwind CSS v4 portfolio: fonts,
  color palette, spacing rhythm, section patterns, and component styles. Use
  this whenever writing or changing any markup/styling in app/pages/index.vue,
  app/pages/privacy.vue, app/pages/cv.vue, app/components/*, or app/app.vue —
  new sections, cards, buttons, headings, responsive tweaks, dark/ink bands,
  hover states — so the result stays on-brand. Trigger on requests like "add a
  section that looks like the others", "restyle the projects cards", "make this
  match the site", "change the accent color", or any Tailwind class edit.
---

# Portfolio design system — "institutional navy, ivory, one brass-gold accent"

Positioning: a **public-sector technologist and policy researcher** (ICT Officer
at TESDA, graduate researcher in ICT Convergence at Handong, WorldSkills Expert,
AWS-certified). The site must read as *professional and credible first*,
impressive second. The owner explicitly asked for "really professional": no
playful gimmicks (tilted ribbons, typing consoles, quirky italics, joke
captions). Impressiveness comes from restraint, typography, real credentials,
and one signature element: an ambient knowledge-graph canvas (`HeroGraph.vue`,
labels off) behind the hero portrait — a nod to his HybridRAG research.

Tailwind is v4 via `@tailwindcss/vite` (no `tailwind.config.js`). All tokens
live in the `@theme` block of `app/assets/css/main.css`.

## Typography

Loaded from Google Fonts in `nuxt.config.ts` (`app.head.link`, with preconnect).

- **Source Serif 4** — display serif. Utility `font-display` (aliased as
  `font-noto-serif` for cv/privacy). Headings are `font-semibold`; one word in
  a section title may be `italic font-normal` (gold on navy) for an editorial,
  academic feel. Use italics sparingly.
- **Inter** — body/UI (`font-sans`, the page default).
- **IBM Plex Mono** — labels, eyebrows, dates, tags, data. Almost always
  `font-mono text-[10px]/[11px] uppercase tracking-[0.18em–0.25em]`.

Scale: hero name `text-[clamp(3.25rem,7.5vw,7rem)] font-semibold`, section
titles `text-5xl md:text-6xl lg:text-7xl font-semibold leading-[0.95]`.

## Color tokens

| Token | Use |
|---|---|
| `ink` #0b1a2e / `ink-2` / `ink-3` | deep navy bands, text on ivory |
| `paper` #f7f5f0 / `paper-2` #edeae2 | ivory bands (alternate them) |
| `gold` #c9a96a | accent **on navy** and primary buttons |
| `gold-deep` #7d5f26 | accent **on ivory** (AA contrast) — never `gold` text on ivory |
| `muted` | low-emphasis labels on navy |

Opacity steps carry hierarchy (`text-paper/85`, `/70`, `/45`; `text-ink/75`,
`/60`, `/45`). Borders `border-white/10–15` on navy, `border-ink/10–15` on
ivory. No other hues. Buttons are `rounded-sm` (only the floating nav is a pill).

## Section rhythm

Sections are full-bleed and alternate ink / paper / paper-2. Order: Hero (ink:
name, statement, CTAs, credential rail + framed portrait) → Institutions strip
(paper) → About+stats+"Profile at a glance" panel (paper) → Research
(ink) → Publications (paper-2) → Work (paper) → Experience (paper-2) →
Expertise (ink) → Credentials (paper) → Education (paper-2) → Vision (ink) →
Contact (ink) → footer (ink-2, three-column: identity / sections / documents).

Every section: `py-32 px-6 lg:px-12`, inner `max-w-[1400px] mx-auto`. Dark
bands add `relative grain` (film-grain overlay from main.css).

Section header pattern:

```html
<p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold-deep mb-6">§ 04 — Projects</p>
<h2 v-reveal="60" class="font-display text-5xl md:text-6xl lg:text-7xl leading-[0.95] tracking-tight">
  Selected <span class="italic font-normal">projects</span>
</h2>
```

(On ink: eyebrow `text-gold`, italic word `text-gold`.) Keep the `§ NN`
numbering sequential when adding/reordering sections.

## Components

- **Primary button:** `h-11/h-12 px-6/7 rounded-sm bg-gold text-ink text-sm font-semibold hover:bg-paper`.
- **Secondary:** `rounded-sm border border-ink/20 hover:bg-ink hover:text-paper` (on ink: `border-white/20 hover:bg-white/10`).
- **Chip/tag:** `font-mono text-[10px] uppercase tracking-wider px-2 py-1 border rounded-sm` (`border-white/10 text-paper/50` on ink, `border-ink/15 text-ink/55` or `bg-paper-2` on paper).
- **Card on paper:** `bg-paper border border-ink/10 p-8 lg:p-10` with `hover:-translate-y-1` + soft shadow.
- **Expertise spotlight card:** class `spotlight` + `@pointermove="onSpotlight"` (sets `--mx/--my`).
- **Nav:** fixed floating pill (`bg-ink/85 backdrop-blur`) with scrollspy — active item `bg-gold text-ink`. Items come from `navItems` in index.vue. The mobile menu overlay lives **outside** `<nav>` (backdrop-blur would trap a fixed child).

## Motion

- `v-reveal` (plugin `app/plugins/reveal.ts`) fades/slides an element in once;
  value = delay ms (`v-reveal="120"`). Stagger lists with `i * 60–90`.
- The hero graph fires a calm pulse burst on load and every 12s (`graphBurst`).
- Scroll-linked: reading-progress bar, experience timeline spine fill, Vision
  quote word-by-word reveal, stats count-up. All computed in one rAF-throttled
  scroll handler in index.vue.
- Smooth scroll is **Lenis**; anchors are handled by a delegated click handler,
  so any `<a href="#id">` works. Don't re-enable CSS `scroll-behavior`.
- Everything respects `prefers-reduced-motion` (CSS + JS checks). Keep it that way.
- The root wrapper has `overflow-x-clip` (not `hidden`) so the sticky/fixed UI
  keeps working while the rotated ribbon can't cause sideways scroll.

## Accessibility

Global gold `:focus-visible` ring is in main.css — don't strip outlines.
Decorative glyphs get `aria-hidden="true"`. The graph canvas has `role="img"`
and an aria-label; the console has an `sr-only` static version.

## Responsive

Mobile-first; `lg:` (1024px) is the main switch (desktop nav, side-by-side hero,
graph labels). Below `lg` the graph sits behind the text with a stronger veil
and no canvas labels. Always give new grids a single-column fallback and verify
at 375px with no horizontal overflow.
