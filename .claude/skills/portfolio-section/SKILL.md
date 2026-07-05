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
   `<section>` an `id="..."` and add a matching `<a href="#id">` link in **both**
   nav lists.

## Step 1 — Data

Create the JSON. For a list section, mirror an existing array file (e.g.
`researchInterests.json`) including a unique `id` per item for `:key`. Keep it
valid JSON (no trailing commas/comments).

## Step 2 — Template section

Reuse the design system (see the `portfolio-design` skill) so it looks native.
Skeleton for a card-grid section on a light background:

```html
<section id="talks" class="py-32">
  <div class="mb-16">
    <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif mb-4">Talks & Presentations</h2>
    <div class="w-24 h-1 bg-yellow-800"></div>
  </div>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
    <div v-for="item in talks" :key="item.id"
         class="p-8 bg-white border border-zinc-100 shadow-sm rounded flex flex-col gap-4">
      <h3 class="text-zinc-900 text-lg font-bold font-noto-serif">{{ item.title }}</h3>
      <p class="text-zinc-600 text-sm leading-relaxed">{{ item.description }}</p>
    </div>
  </div>
</section>
```

To make the band full-bleed with its own background, add
`bg-zinc-100 -mx-6 lg:-mx-24 px-6 lg:px-24` to the `<section>`. The page
alternates white / `zinc-100` bands — check the neighbors and alternate so two
same-colored bands don't sit adjacent. There's one `bg-black text-white` band
(Expertise); copy its inverted treatment if you want another dark section.

## Step 3 — Navigation (do BOTH lists)

The nav exists twice in `index.vue`: a desktop list (`hidden md:flex …`) and a
mobile overlay list (`… md:hidden`). Add the anchor to **both** or the link is
missing on one form factor:

```html
<!-- desktop list -->
<a href="#talks" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Talks</a>
<!-- mobile overlay list -->
<a href="#talks" @click="closeMenu" class="text-zinc-900 text-2xl font-bold font-noto-serif">Talks</a>
```

Smooth-scroll to the anchor works automatically: Lenis intercepts `a[href^="#"]`
clicks on mount, so no JS wiring is needed — just ensure the `id` on the section
matches the `href`.

## Surfacing an existing-but-unrendered field

Some data still exists but isn't shown: `project.longDescription` and
`project.impact`. To display one, add markup inside that section's `v-for`
referencing the field (guard optional fields with `v-if`). Example — surface a
project's impact statement:

```html
<p v-if="project.impact" class="text-zinc-500 text-xs italic leading-relaxed mb-4">
  {{ project.impact }}
</p>
```

(Publications already render `doi`/`url` conditionally, and `project.featured`
renders a "Featured" ribbon — those are wired up; just populate the data.)

## Removing or reordering a section

- **Remove:** delete the `<section>` block, its `import`, and its nav links (both
  lists). You can leave the orphaned `app/data/*.json` file or delete it; if you
  delete it, make sure no remaining import references it.
- **Reorder on the page:** move the whole `<section>` block within `<main>`.
- **Reorder nav:** move the `<a>` in both lists (nav order is independent of
  section order, but keeping them consistent is less confusing).

## Verify

Run `npm run dev`, then check: the section appears in the right place, the nav
links (desktop and mobile) scroll to it, and it's responsive at mobile width.
Also confirm the anchor still works after a hard reload.
