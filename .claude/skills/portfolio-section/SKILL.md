---
name: portfolio-section
description: >-
  End-to-end recipe for adding, removing, or reordering a whole section on this
  Nuxt portfolio (a new content block on the single-page index.vue), or for
  surfacing a data field that isn't rendered yet. Use this when the user wants
  something structurally new — "add a Talks section", "add a Testimonials block",
  "show the project long description / GitHub stars", "add a blog", "make the
  writings link out", "remove the Awards section", "reorder the page so Projects
  comes before Experience". This is more than a content edit: it touches
  app/data, the template, and the navigation together. For pure text/data changes
  use portfolio-content; for styling tokens use portfolio-design.
---

# Adding / changing a section

The site is one long page: `app/pages/index.vue` imports every
`app/data/*.json` file and renders a sequence of `<section>` blocks inside
`<main>`. A "section" is a coordinated change across **three** places. Miss one
and the section is invisible, unstyled, or unreachable from the nav.

## The three touch points

1. **Data** — add `app/data/<name>.json` (array for repeated cards, object for a
   singular block). Follow the schema conventions in the `portfolio-content`
   skill.
2. **Template** — in `app/pages/index.vue`:
   - add the import near the other imports at the top of `<script setup>`:
     `import <name> from '../data/<name>.json'`
   - add a `<section>` inside `<main>`, positioned where it should appear on the
     page (order in the file = order on the page).
3. **Navigation** — if the section should be reachable from the menu, give the
   `<section>` an `id="..."` and add an entry to the `navItems` array in
   `index.vue`'s `<script setup>`. Both the desktop pill and the mobile overlay
   render from that one array, and the scrollspy observes it automatically.

## Step 1 — Data

Create the JSON. For a list section, mirror an existing array file (e.g.
`researchInterests.json`) including a unique `id` per item for `:key`. Keep it
valid JSON (no trailing commas/comments).

## Step 2 — Template section

Reuse the design system (see the `portfolio-design` skill) so it looks native.
Skeleton for a card-grid section on a paper band:

```html
<section id="talks" class="bg-paper py-32 px-6 lg:px-12">
  <div class="max-w-[1400px] mx-auto">
    <p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold-deep mb-6">§ 08 — Talks</p>
    <h2 v-reveal="60" class="font-display font-semibold text-5xl md:text-6xl lg:text-7xl leading-[0.95] tracking-tight mb-16">
      Talks &amp; <span class="italic font-normal">presentations</span>
    </h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <article v-for="(item, i) in talks" :key="item.id" v-reveal="i * 80"
               class="bg-paper border border-ink/10 p-8 flex flex-col gap-4">
        <p class="font-mono text-[10px] uppercase tracking-[0.2em] text-gold-deep">{{ item.event }} · {{ item.year }}</p>
        <h3 class="font-display text-2xl leading-tight">{{ item.title }}</h3>
        <p class="text-ink/65 leading-relaxed">{{ item.description }}</p>
      </article>
    </div>
  </div>
</section>
```

Bands alternate `bg-paper` / `bg-paper-2` / `bg-ink` — check the neighbours so
two same-coloured bands don't touch. For a dark band use
`relative bg-ink text-paper grain`, `text-gold` for the eyebrow and italic
word, and `text-paper/60`-style opacities for body text. Renumber the `§ NN`
eyebrows after inserting a section.

## Step 3 — Navigation

Add `{ id: 'talks', label: 'Talks' }` to `navItems` in index.vue. Keep the pill
short (it holds ~7 items at `lg`); not every section needs a nav entry.
Smooth scroll works automatically: a delegated click handler sends any
`<a href="#id">` through Lenis, so only the `id` must match.

## Surfacing an existing-but-unrendered field

Most fields are rendered now (projects show `longDescription` and `impact`;
publications render `doi`/`url` when non-empty; `project.featured` shows a
"Featured" tag). If you add a new optional field, render it inside that
section's `v-for` and guard it with `v-if`.

## Removing or reordering a section

- **Remove:** delete the `<section>` block, its `import`, and its `navItems`
  entry. You can leave the orphaned `app/data/*.json` file or delete it; if you
  delete it, make sure no remaining import references it.
- **Reorder on the page:** move the whole `<section>` block within `<main>`.
- **Reorder nav:** reorder `navItems` (keep it consistent with page order).

## Verify

Run `npm run dev`, then check: the section appears in the right place, the nav
links (desktop and mobile) scroll to it, and it's responsive at mobile width.
Also confirm the anchor still works after a hard reload.
