---
name: portfolio-deploy
description: >-
  Build, preview, and deploy this Nuxt 4 portfolio, including the Docker
  workflow. Use when the user wants to run the site locally, produce a
  production build, preview it, containerize it, ship it, or debug a
  build/deploy failure. Trigger on "run the site", "build for production",
  "deploy my portfolio", "does it build?", "make the Docker image", "the build
  is failing", "preview the production version", or questions about hosting,
  the Dockerfile, SSR vs static, or the output directory.
---

# Build, preview & deploy

Nuxt 4 project. Package manager is **npm** (`package-lock.json` present). There
is no test suite and no linter configured — "does it work" means it builds and
renders.

## ⚠️ Node version — must be 20.12+ (not the default 20.11)

Nuxt's CLI (`nuxi`/`@clack/core`) imports `styleText` from `node:util`, which
only exists in **Node ≥ 20.12** (also fine on 22/24). This machine's default
`node` is `v20.11.1`, which crashes every `nuxt` command with
`does not provide an export named 'styleText'`. Before `npm run dev/build/generate`,
select a compatible version, e.g.:

```bash
nvm use 20.12.2   # or: nvm use 24
```

Installed nvm versions include `v20.12.2` and `v24.12.0`. The `.claude/launch.json`
dev config already points at the `v20.12.2` node binary so the preview tooling
works. Consider pinning this with an `.nvmrc` (`20.12.2`) and an `engines` field
in `package.json` so the requirement is explicit. The Dockerfile's `node:20-alpine`
resolves to a current 20.x that already includes `styleText`, so container builds
are unaffected.

## Local commands (from package.json)

| Task | Command | Notes |
|---|---|---|
| Install deps | `npm install` | runs `nuxt prepare` via postinstall |
| Dev server | `npm run dev` | http://localhost:3000, HMR, Nuxt devtools on |
| Production build (SSR) | `npm run build` | outputs `.output/` (server + public) |
| Preview prod build | `npm run preview` | serves the `.output/` build locally |
| Static build | `npm run generate` | prerenders to `.output/public/` for static hosts |

The repo's default deploy target is the **SSR Node server** (`npm run build` →
`node .output/server/index.mjs`), which the Dockerfile uses. Use
`npm run generate` instead only if deploying to a purely static host (Netlify/
GitHub Pages/S3), which serves `.output/public/`. The `dist` symlink →
`.output/public` exists for static-host convenience and is only populated after
`generate`.

## Verifying a change before shipping

1. `npm run build` — must complete with no errors.
2. `npm run preview` — open http://localhost:3000 and confirm the change renders,
   the page is responsive, nav anchors scroll, and no console errors appear.

Since there are no automated tests, this manual build+preview pass is the gate.
Report the actual build result — if it fails, surface the error, don't claim
success.

## Docker

The `Dockerfile` is a two-stage build (Node 20 Alpine): stage 1 installs deps
and runs `npm run build`; stage 2 copies `.output/` and runs the SSR server.

```bash
# Build the image
docker build -t portfolio .

# Run it (maps container 3000 → host 3000)
docker run --rm -p 3000:3000 portfolio
```

Runtime env is set in the image: `HOST=0.0.0.0`, `PORT=3000`,
`NODE_ENV=production`. `.dockerignore` keeps `node_modules`, `.output`, `.nuxt`,
and `.git` out of the build context so the build is reproducible from source.

## Config that affects deploys

- **Site URL / domain:** `nuxt.config.ts` `site.url` feeds the sitemap and must
  match the real deployed host. It is aligned on `https://www.jothamhernandez.com`
  with the canonical host in `app/data/seo.json` and `public/robots.txt` — keep
  all three in sync (see the `portfolio-seo` skill) and 301-redirect apex → www.
- **Routes:** `/` (homepage), `/privacy`, and `/cv` (print-optimized CV). New
  `app/pages/*.vue` files become routes and are picked up by the sitemap.
- **`compatibilityDate`** in `nuxt.config.ts` pins Nitro/Nuxt behavior; bump it
  deliberately, not incidentally.
- **Favicon/head links** are declared in `nuxt.config.ts` `app.head`.

## Common failure modes

- **Build fails after a dependency bump:** delete `node_modules` and
  `package-lock.json`, `npm install`, rebuild — or pin the offending package back.
- **Content change not showing in Docker:** the image builds from source at build
  time; rebuild the image (`docker build`) — it won't pick up host file edits at
  runtime.
- **Blank page / hydration error in preview:** check the browser console; usually
  a malformed `app/data/*.json` file (trailing comma, wrong shape). Validate the
  JSON you last edited.
