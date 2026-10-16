---
name: portfolio-content
description: >-
  Edit the content of this Nuxt portfolio site by changing the JSON files in
  app/data/ — not the Vue markup. Use this whenever the user wants to add,
  remove, reorder, or reword anything shown on the site: a new job or
  experience, a project, a skill/expertise group, a research interest, a
  certification, award, publication/writing, education entry, the hero text,
  about paragraphs, contact details, or profile links. Trigger even when the
  user just says "update my portfolio", "add this to my site", "fix the wording
  on my experience", or pastes a resume bullet — the content lives in data, so
  reach for this skill before touching index.vue.
---

# Editing portfolio content

All visible content on this site is data-driven. `app/pages/index.vue` is a
fixed template that renders whatever it finds in `app/data/*.json`. **To change
content, edit the JSON — never hardcode text into the template.** This keeps the
markup clean and lets content change without risking layout breakage.

## Workflow

1. Identify which data file owns the content (table below).
2. Edit the JSON, matching the existing shape of neighboring entries exactly.
3. Keep valid JSON: double-quoted keys/strings, no trailing commas, no comments.
4. Verify with `npx nuxt dev` (or `npm run dev`) and check the section renders.

Arrays render in file order — reorder entries to reorder cards on the page.

## Data file map

| File | Shape | Renders in section | Item fields |
|------|-------|--------------------|-------------|
| `profile.json` | object | Nav brand, footer, JSON-LD | `name`, `title`, `currentRole`, `email`, `location`, `linkedin`, `orcid`, `googleScholar`, `credly` |
| `hero.json` | object | Hero + institutions strip | `headline` (the name), `eyebrow`, `statement` (one-line positioning), `primaryCta`/`secondaryCta{text,url}`, `cvUrl`, `availability` (portrait status line), `locations`, `credentials[{org,title,href}]` (3-item rail under the CTAs), `institutions[]` (strip below the hero; only bodies he genuinely worked/studied with or holds credentials from); `subtitle`/`summary` are legacy, unused |
| `about.json` | object | About + Vision | `title`, `paragraphs[]`, `image` (`/portrait.jpg`, shown in the hero; strip EXIF/GPS before adding a new photo), `vision` (the word-by-word quote) |
| `researchInterests.json` | array | Research + hero graph | `id`, `title`, `graphLabel` (short label drawn in the hero graph & marquee), `description`, `icon`, `tags[]` (first 3 become graph nodes) |
| `experience.json` | array | Professional Experience | `role`, `organization`, `location`, `startDate`, `endDate`, `isCurrent`, `summary`, `highlights[]`, `technologies[]` |
| `skills.json` | array | Technical Expertise | `id`, `category`, `description`, `skills[]` |
| `projects.json` | array | Selected Projects | `id`, `title`, `type`, `status`, `year`, `role`, `shortDescription`, `longDescription`, `impact`, `technologyStack[]`, `image` (`/projects/<id>.webp`, 1600×900 navy/gold cover — regenerate or add one with `scripts/project-covers/gen.py`, see its docstring), `liveUrl`, `repositoryUrl`, `featured` (+ unused: `tags`) |
| `education.json` | array | Education | `institution`, `degree`, `field`, `startDate`, `endDate`, `location`, `description` |
| `certifications.json` | array | Certifications & Credentials (`#certifications`) | `id`, `title`, `issuer`, `category` (`certification` \| `recognition` \| `course` — picks the sub-group), `issued` (`YYYY-MM-DD` or `YYYY`), `expires`, `badgeImage`, `credentialUrl`, `description`, `featured`, `verifiedBy` (`"Credly"` counts toward the verified total). Credly data: `https://www.credly.com/users/jotham-hernandez/badges.json` |
| `awards.json` | array | Certifications & Awards | `title`, `organization`, `year`, `description` |
| `publications.json` | array | Publications & Research Writing | `title`, `authors`, `venue`, `type`, `status`, `year`, `doi`, `url`, `tags[]` |
| `contact.json` | object | Contact | `cta`, `email`, `linkedin`, `website`, `location` |
| `seo.json` | object | `<head>` meta (see portfolio-seo) | `title`, `description`, `canonicalUrl`, `ogImage`, `keywords[]`, `twitterHandle` |

## Field behavior that will surprise you

Read these before editing — several fields have conditional or no rendering:

- **Conditionally rendered links (empty string = hidden).** A project's `liveUrl`
  and `repositoryUrl`, a certification's `credentialUrl`, and a publication's
  `doi`/`url` render as links only when non-empty (`v-if`). Leave them `""` to
  hide the button rather than deleting the key.
- **`about.image` and `contact.email` toggle blocks.** If `about.image` is falsy
  the image column is hidden; if `contact.email` is falsy/`null` the email card in
  the contact section disappears. `contact.email` and `profile.email` are two
  separate fields — the contact section reads `contact.email`, the CV and JSON-LD
  read from both; keep them consistent.
- **`project.featured: true`** now renders a "Featured" ribbon on the project
  image — use it to spotlight your strongest work (e.g. Skills Bridge).
- **Fields present in data but NOT rendered today:** `project.longDescription`
  and `project.impact`. Adding a value there changes nothing on the page. To
  surface them, that needs a template change — see the `portfolio-section` skill.
- **Content also feeds the CV.** `app/pages/cv.vue` (the `/cv` page) renders from
  `profile`, `about`, `experience`, `education`, `publications`, `skills`,
  `certifications`, and `awards` — so a content edit updates both the homepage and
  the printable CV automatically.
- **`researchInterest.icon` is short text, not an image** (e.g. `"AI"`, `"Gov"`).
  It's shown inside a small circle. Keep it to ~1–4 characters.
- **`experience.isCurrent`** is metadata only; the visible date comes from
  `startDate`/`endDate` (use `"Present"` as `endDate` for ongoing roles).
- **`id` fields** are Vue `:key`s — keep them unique within their file.

## Adding an entry (example: a new job)

Append an object to `app/data/experience.json` matching the existing shape:

```json
{
  "role": "Senior Platform Engineer",
  "organization": "Acme Corp",
  "location": "Remote",
  "startDate": "2024",
  "endDate": "Present",
  "isCurrent": true,
  "summary": "One-line framing of the role.",
  "highlights": ["Bullet one.", "Bullet two."],
  "technologies": ["Kubernetes", "Go"]
}
```

Newest-first ordering is the site convention for experience, projects, and
publications — put recent items at the top of the array.

## Content voice

Match the site's existing register: formal, academic, results-oriented.
`highlights`/`summary` are terse sentences; `technologies`/`tags`/`skills` are
short proper-noun labels rendered uppercase by CSS (don't SHOUT in the JSON —
write `"Cloud Infrastructure"`, the template uppercases it).
