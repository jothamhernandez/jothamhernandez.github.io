---
name: portfolio-design
description: >-
  The visual design system for this Nuxt + Tailwind CSS v4 portfolio: fonts,
  color palette, spacing rhythm, section patterns, and component styles. Use
  this whenever writing or changing any markup/styling in app/pages/index.vue,
  app/pages/privacy.vue, or app/app.vue — new sections, cards, buttons, headings,
  responsive tweaks, dark/black bands, hover states — so the result stays
  on-brand. Trigger on requests like "add a section that looks like the others",
  "restyle the projects cards", "make this match the site", "change the accent
  color", or any Tailwind class edit to the pages.
---

# Portfolio design system

This is an editorial, academic-portfolio aesthetic: serif display type, a
near-monochrome zinc palette, a single warm accent, generous vertical rhythm,
and full-bleed alternating section backgrounds. Match these tokens so new work
looks native. Tailwind is v4, configured via `@tailwindcss/vite` (no
`tailwind.config.js`); the only custom theme token lives in
`app/assets/css/main.css`.

## Typography

Three families, loaded from Google Fonts via `<link>` tags in `nuxt.config.ts`
`app.head` (with `preconnect` for performance — not a render-blocking CSS
`@import`). The `@theme` token block still lives in `app/assets/css/main.css`:

- **Inter** — default body/UI. The page root sets `font-['Inter']`. Use for
  paragraphs, descriptions, form fields.
- **Noto Serif** — display/headings. Apply with the `font-noto-serif` utility
  (defined as `--font-noto-serif` in the `@theme` block of `main.css`). Use for
  every `<h1>`/`<h2>`/`<h3>` and the brand wordmark.
- **Manrope** — small uppercase labels, eyebrows, buttons, tags, dates. Apply
  inline with `font-['Manrope']`, almost always paired with
  `uppercase tracking-widest` (or `tracking-[0.3em]`) and a tiny size
  (`text-[10px]`/`text-xs`).

Heading scale in use: hero `text-6xl lg:text-7xl`, section titles `text-4xl`,
card titles `text-xl`/`text-2xl` — all `font-bold font-noto-serif`.

## Color palette

- **Neutrals:** `zinc` scale. Text `text-zinc-900` (near-black headings),
  `text-zinc-600` (body), `text-zinc-500`/`text-zinc-400` (muted/labels).
  Surfaces `bg-white` and `bg-zinc-100`; borders `border-zinc-100`/`zinc-200`.
- **Accent:** `yellow-800` (a warm brown-gold) for links, eyebrows, dividers,
  active states, and icon glyphs — with `orange-50`/`orange-100`/`orange-200`
  as its soft tints (icon chips, tags on light). This is the site's one accent —
  don't introduce new hues; to rebrand, swap `yellow-800` + its orange tints.
- **Dark band:** the Technical Expertise section is `bg-black text-white` with
  `zinc-900` chips and `zinc-800` borders. Reuse this exact treatment for any
  inverted section.

## Spacing & layout rhythm

- Content is centered in `<main class="max-w-7xl mx-auto px-6 lg:px-24">`.
- Sections use vertical padding `py-32` (a few use `py-24`). Keep the cadence.
- **Full-bleed bands:** to make a section span edge-to-edge with its own
  background while content stays aligned, use the negative-margin trick:
  `-mx-6 lg:-mx-24 px-6 lg:px-24` plus a `bg-*`. Used by About, Experience,
  Expertise, Certifications, Contact — alternating white / `zinc-100` / black.
- Grids: two-column feature layouts use `lg:grid-cols-12` with `col-span-4` /
  `col-span-8`; card grids use `md:grid-cols-2` / `lg:grid-cols-3` with
  `gap-6`/`gap-8`.

## Recurring component patterns

**Section heading + accent underline** (left-aligned sections):

```html
<div class="mb-16">
  <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif mb-4">Section Title</h2>
  <div class="w-24 h-1 bg-yellow-800"></div>
</div>
```

**Eyebrow label** (above a heading or on a card):

```html
<span class="text-yellow-800 text-[10px] font-bold tracking-[0.2em] uppercase font-['Manrope']">LABEL</span>
```

**Light card:** `p-8 bg-white border border-zinc-100 shadow-sm rounded flex flex-col gap-4`.

**Tag chip (light):** `px-3 py-1 bg-orange-100 text-yellow-800 text-[9px] font-bold uppercase rounded-full`.
**Tag chip (dark band):** `px-2 py-1 bg-zinc-900 text-zinc-400 text-[10px] font-bold uppercase rounded border border-zinc-800`.

**Primary button:** `px-8 py-4 bg-black text-white text-xs font-bold tracking-widest uppercase font-['Manrope']`.
**Secondary button:** same box with `border border-zinc-200 text-zinc-900 hover:bg-zinc-50 transition-colors`.

**Text link (underline-on-accent):** `border-b-2 border-yellow-800 pb-1 hover:text-yellow-800 transition-colors` with `text-[10px] font-bold tracking-widest uppercase`.

## Interaction & motion

- Smooth scrolling is handled by **Lenis** (initialized in `index.vue`
  `onMounted`). Native `scroll-behavior` is disabled in CSS on purpose — don't
  re-enable it. In-page `#anchor` links are intercepted to scroll via Lenis, so
  new nav/anchor links work automatically as long as the target `id` exists.
- Standard hover transition is `transition-colors` (or `transition-transform`
  for the project image `group-hover:scale-105`). Keep durations subtle
  (`duration-300`–`duration-700`).
- **Accessibility:** interactive controls use `focus-visible:outline-2
  focus-visible:outline-yellow-800 focus-visible:outline-offset-2` (never bare
  `focus:outline-none` — that strips keyboard focus). Decorative glyphs/emoji and
  the geometric hero shape carry `aria-hidden="true"`; the menu toggle exposes
  `:aria-expanded`. Preserve these when editing.
- The mobile nav is an overlay toggled by `isMenuOpen`; the back-to-top button
  appears after 500px of scroll. If you add a top-level nav item, update **both**
  the desktop and mobile lists (see `portfolio-section`).

## Responsive

Mobile-first. Breakpoints in use are `md:` (~768px) and `lg:` (~1024px).
Desktop nav shows at `md:`; multi-column grids and the `lg:px-24` gutter kick in
at `lg:`. Always provide a single-column mobile fallback for new grids.
