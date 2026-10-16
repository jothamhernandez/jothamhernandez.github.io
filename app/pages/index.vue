<script setup lang="ts">
import { onMounted, onBeforeUnmount, computed, ref, watch } from 'vue'
import Lenis from 'lenis'

// Import data
import profile from '../data/profile.json'
import hero from '../data/hero.json'
import about from '../data/about.json'
import researchInterests from '../data/researchInterests.json'
import experience from '../data/experience.json'
import skills from '../data/skills.json'
import projects from '../data/projects.json'
import education from '../data/education.json'
import certifications from '../data/certifications.json'
import awards from '../data/awards.json'
import publications from '../data/publications.json'
import contact from '../data/contact.json'
import seo from '../data/seo.json'
import type { GraphNode, GraphLink } from '../components/HeroGraph.vue'

const isMenuOpen = ref(false)
const showScrollTop = ref(false)
const navSolid = ref(false)
const pageProgress = ref(0)
const activeSection = ref('')
const timelineProgress = ref(0)
const visionProgress = ref(0)
const graphBurst = ref(0)
const currentYear = computed(() => new Date().getFullYear())

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const navItems = [
  { id: 'about', label: 'About' },
  { id: 'research', label: 'Research' },
  { id: 'publications', label: 'Publications' },
  { id: 'projects', label: 'Projects' },
  { id: 'experience', label: 'Experience' },
  { id: 'expertise', label: 'Expertise' },
  { id: 'certifications', label: 'Credentials' }
]

// Certifications are grouped by `category`; most recent first within each group.
const byNewest = (a: { issued: string }, b: { issued: string }) => b.issued.localeCompare(a.issued)
const professionalCerts = certifications.filter((c) => c.category === 'certification').sort(byNewest)
const recognitionBadges = certifications.filter((c) => c.category === 'recognition').sort(byNewest)
const courseBadges = certifications.filter((c) => c.category === 'course').sort(byNewest)
const verifiedCount = certifications.filter((c) => c.verifiedBy === 'Credly').length

// "2024-01-26" -> "Jan 2024"; bare years pass through unchanged.
const formatMonthYear = (date: string) => {
  if (!/^\d{4}-\d{2}/.test(date)) return date
  const [y, m] = date.split('-').map(Number)
  return new Date(Date.UTC(y!, m! - 1, 1)).toLocaleDateString('en-US', { month: 'short', year: 'numeric', timeZone: 'UTC' })
}

const pad = (n: number) => String(n).padStart(2, '0')

// Headline numbers — all derived from the data files so they stay truthful.
const firstYear = Math.min(...experience.map((e) => Number(e.startDate)))
const stats = [
  { value: new Date().getFullYear() - firstYear, suffix: '+', label: 'Years building ICT systems' },
  { value: verifiedCount, suffix: '', label: 'Verified credentials' },
  { value: recognitionBadges.length, suffix: '', label: 'WorldSkills world competitions' },
  { value: researchInterests.length, suffix: '', label: 'Active research directions' }
]
const statDisplay = ref(stats.map((s) => s.value))
const statsEl = ref<HTMLElement | null>(null)

// Hero knowledge graph, assembled from the same data the page renders.
const topicForSkillGroup: Record<string, string> = {
  'cloud-infrastructure': 'cloud-public-sector',
  'web-api-development': 'digital-gov',
  'networking-security': 'cloud-public-sector',
  'database-systems': 'skills-intelligence',
  'ai-data-research': 'hybrid-rag',
  'teaching-training': 'hci-learning-analytics'
}
const graph = (() => {
  const nodes: GraphNode[] = [{ id: 'core', label: profile.name, kind: 'core' }]
  const links: GraphLink[] = []
  const seen = new Set<string>()
  const addSkill = (name: string, topic: string) => {
    const id = 'skill:' + name.toLowerCase()
    if (!seen.has(id)) {
      seen.add(id)
      nodes.push({ id, label: name, kind: 'skill' })
    }
    links.push({ source: topic, target: id })
  }
  for (const r of researchInterests) {
    nodes.push({ id: r.id, label: r.graphLabel, kind: 'topic' })
    links.push({ source: 'core', target: r.id })
    r.tags.slice(0, 3).forEach((t) => addSkill(t, r.id))
  }
  for (const g of skills) {
    const topic = topicForSkillGroup[g.id]
    if (topic) g.skills.slice(0, 3).forEach((s) => addSkill(s, topic))
  }
  const orgs: [string, string, string[]][] = [
    ['org:tesda', 'TESDA', ['digital-gov', 'skills-intelligence']],
    ['org:handong', 'Handong', ['digital-gov', 'hybrid-rag']],
    ['org:worldskills', 'WorldSkills', ['hci-learning-analytics']],
    ['org:aws', 'AWS', ['cloud-public-sector']]
  ]
  for (const [id, label, related] of orgs) {
    nodes.push({ id, label, kind: 'org' })
    links.push({ source: 'core', target: id })
    related.forEach((r) => links.push({ source: id, target: r }))
  }
  links.push({ source: 'hybrid-rag', target: 'skills-intelligence' })
  links.push({ source: 'digital-gov', target: 'cloud-public-sector' })
  return { nodes, links }
})()

// "Profile at a glance" panel in About — all derived from the data files.
const currentStudy = education[0]!
const worldskillsRole = experience.find((e) => e.role.includes('WorldSkills'))
const glance = [
  { label: 'Current role', value: profile.currentRole },
  { label: 'Graduate study', value: `${currentStudy.degree}, ${currentStudy.field} — ${currentStudy.institution}` },
  { label: 'Research focus', value: researchInterests.slice(0, 3).map((r) => r.graphLabel).join(' · ') },
  ...(worldskillsRole ? [{ label: 'WorldSkills', value: `${worldskillsRole.role}, ${worldskillsRole.startDate}–${worldskillsRole.endDate.toLowerCase()}` }] : []),
  { label: 'Certified', value: professionalCerts.slice(0, 2).map((c) => c.title).join(' · ') },
  { label: 'Based in', value: contact.location }
]

const visionWords = about.vision.split(' ')

// Structured data (schema.org Person) — built from the same JSON the page renders,
// so it stays in sync with the visible content and enriches search/AI results.
const structuredData = {
  '@context': 'https://schema.org',
  '@type': 'Person',
  name: profile.name,
  jobTitle: profile.currentRole,
  url: seo.canonicalUrl,
  image: seo.ogImage,
  email: contact.email ? 'mailto:' + contact.email : undefined,
  worksFor: {
    '@type': 'Organization',
    name: 'TESDA — Technical Education and Skills Development Authority'
  },
  alumniOf: education.map((e) => ({ '@type': 'CollegeOrUniversity', name: e.institution })),
  knowsAbout: researchInterests.map((r) => r.title),
  sameAs: [profile.linkedin, profile.orcid, profile.googleScholar, profile.credly],
  hasCredential: certifications
    .filter((c) => c.credentialUrl)
    .map((c) => ({
      '@type': 'EducationalOccupationalCredential',
      name: c.title,
      credentialCategory: c.category === 'certification' ? 'Professional Certification' : 'Badge',
      recognizedBy: { '@type': 'Organization', name: c.issuer },
      url: c.credentialUrl
    }))
}

// SEO Meta
useHead({
  title: seo.title,
  meta: [
    { name: 'description', content: seo.description },
    { name: 'keywords', content: seo.keywords.join(', ') },
    // Open Graph
    { property: 'og:title', content: seo.title },
    { property: 'og:description', content: seo.description },
    { property: 'og:url', content: seo.canonicalUrl },
    { property: 'og:image', content: seo.ogImage },
    { property: 'og:type', content: 'website' },
    // Twitter
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: seo.title },
    { name: 'twitter:description', content: seo.description },
    { name: 'twitter:image', content: seo.ogImage },
    { name: 'twitter:site', content: seo.twitterHandle }
  ],
  link: [
    { rel: 'canonical', href: seo.canonicalUrl }
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify(structuredData)
    }
  ]
})

// Cursor spotlight for the expertise cards
const onSpotlight = (e: PointerEvent) => {
  const el = e.currentTarget as HTMLElement
  const rect = el.getBoundingClientRect()
  el.style.setProperty('--mx', `${e.clientX - rect.left}px`)
  el.style.setProperty('--my', `${e.clientY - rect.top}px`)
}

let lenis: Lenis | null = null
let rafId = 0
let scrollTicking = false
let sectionObserver: IntersectionObserver | null = null
let statsObserver: IntersectionObserver | null = null
const timelineEl = ref<HTMLElement | null>(null)
const visionEl = ref<HTMLElement | null>(null)
let reducedMotion = false
const burstTimers: ReturnType<typeof setTimeout>[] = []
let burstInterval: ReturnType<typeof setInterval> | undefined

const scrollToTop = () => {
  if (lenis) lenis.scrollTo(0)
  else window.scrollTo({ top: 0 })
}

const clamp01 = (n: number) => Math.min(1, Math.max(0, n))

function updateScrollState() {
  scrollTicking = false
  const y = window.scrollY
  const vh = window.innerHeight
  const max = document.documentElement.scrollHeight - vh
  pageProgress.value = max > 0 ? y / max : 0
  navSolid.value = y > 40
  showScrollTop.value = y > 500
  if (timelineEl.value) {
    const r = timelineEl.value.getBoundingClientRect()
    timelineProgress.value = clamp01((vh * 0.6 - r.top) / r.height)
  }
  if (visionEl.value) {
    const r = visionEl.value.getBoundingClientRect()
    visionProgress.value = reducedMotion ? 1 : clamp01((vh * 0.85 - r.top) / (r.height + vh * 0.25))
  }
}
const onScroll = () => {
  if (!scrollTicking) {
    scrollTicking = true
    requestAnimationFrame(updateScrollState)
  }
}

// In-page anchors scroll through Lenis (delegated, so it covers every #link on the page)
const onAnchorClick = (e: MouseEvent) => {
  const anchor = (e.target as HTMLElement).closest('a[href^="#"]') as HTMLAnchorElement | null
  if (!anchor) return
  const targetId = anchor.getAttribute('href')
  if (targetId && targetId !== '#' && document.querySelector(targetId)) {
    e.preventDefault()
    lenis?.scrollTo(targetId, { offset: -16 })
    history.replaceState(null, '', targetId)
  }
}

// Freeze the page behind the mobile menu; Escape closes it.
watch(isMenuOpen, (open) => { if (open) lenis?.stop(); else lenis?.start() })
const onKeydown = (e: KeyboardEvent) => { if (e.key === 'Escape') closeMenu() }

function countUp() {
  const start = performance.now()
  const duration = 1400
  const step = (now: number) => {
    const t = clamp01((now - start) / duration)
    const eased = 1 - Math.pow(1 - t, 3)
    statDisplay.value = stats.map((s) => Math.round(s.value * eased))
    if (t < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}

onMounted(() => {
  reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  lenis = new Lenis()

  function raf(time: number) {
    lenis?.raf(time)
    rafId = requestAnimationFrame(raf)
  }
  rafId = requestAnimationFrame(raf)

  window.addEventListener('scroll', onScroll, { passive: true })
  document.addEventListener('click', onAnchorClick)
  window.addEventListener('keydown', onKeydown)
  updateScrollState()

  // Scrollspy for the nav
  sectionObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) activeSection.value = entry.target.id
      }
    },
    { rootMargin: '-45% 0px -50% 0px' }
  )
  navItems.forEach((item) => {
    const el = document.getElementById(item.id)
    if (el) sectionObserver!.observe(el)
  })

  // A calm "retrieval" pulse through the hero graph: once on load, then every 12s
  burstTimers.push(setTimeout(() => graphBurst.value++, 1200))
  burstInterval = setInterval(() => graphBurst.value++, 12000)

  // Count-up for the stats strip (SSR renders the final numbers)
  if (!reducedMotion && statsEl.value) {
    statDisplay.value = stats.map(() => 0)
    statsObserver = new IntersectionObserver(([entry]) => {
      if (entry?.isIntersecting) {
        countUp()
        statsObserver?.disconnect()
      }
    }, { threshold: 0.4 })
    statsObserver.observe(statsEl.value)
  }
})

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId)
  burstTimers.forEach(clearTimeout)
  clearInterval(burstInterval)
  lenis?.destroy()
  window.removeEventListener('scroll', onScroll)
  document.removeEventListener('click', onAnchorClick)
  window.removeEventListener('keydown', onKeydown)
  sectionObserver?.disconnect()
  statsObserver?.disconnect()
})
</script>

<template>
  <div class="w-full bg-paper text-ink font-sans overflow-x-clip">
    <!-- Reading progress -->
    <div class="fixed top-0 left-0 right-0 h-[2px] z-[80] pointer-events-none" aria-hidden="true">
      <div class="h-full bg-gold origin-left" :style="{ transform: `scaleX(${pageProgress})` }"></div>
    </div>

    <!-- Navigation -->
    <nav class="fixed top-4 inset-x-4 lg:inset-x-8 z-[70] flex justify-between items-center pointer-events-none" aria-label="Primary">
      <a href="#top" class="pointer-events-auto group flex items-center gap-3" aria-label="Back to top — Jotham Hernandez">
        <span :class="['w-11 h-11 rounded-full flex items-center justify-center font-display font-semibold text-base tracking-tight transition-colors duration-500 border', navSolid ? 'bg-ink text-gold border-white/10' : 'bg-transparent text-paper border-white/20']">JH</span>
      </a>

      <div :class="['hidden lg:flex pointer-events-auto items-center gap-1 rounded-full px-2 py-1.5 border transition-colors duration-500', navSolid ? 'bg-ink/85 backdrop-blur-md border-white/10' : 'bg-white/5 backdrop-blur-sm border-white/10']">
        <a
          v-for="item in navItems"
          :key="item.id"
          :href="'#' + item.id"
          :class="['relative px-3.5 py-1.5 rounded-full text-[13px] font-medium transition-colors', activeSection === item.id ? 'text-ink bg-gold' : 'text-paper/70 hover:text-paper']"
          :aria-current="activeSection === item.id ? 'true' : undefined"
        >{{ item.label }}</a>
      </div>

      <div class="flex items-center gap-2 pointer-events-auto">
        <a href="#contact" class="hidden sm:inline-flex items-center gap-2 px-5 h-11 rounded-full bg-gold text-ink text-[13px] font-semibold hover:bg-paper transition-colors">
          Get in touch <span aria-hidden="true">→</span>
        </a>
        <button
          @click="toggleMenu"
          :aria-expanded="isMenuOpen"
          aria-controls="mobile-menu"
          class="lg:hidden w-11 h-11 rounded-full bg-ink/85 backdrop-blur-md border border-white/10 flex flex-col justify-center items-center gap-1.5"
          aria-label="Toggle menu"
        >
          <span :class="['w-5 h-px bg-paper block transition-all duration-300', isMenuOpen ? 'rotate-45 translate-y-[3.5px]' : '']"></span>
          <span :class="['w-5 h-px bg-paper block transition-all duration-300', isMenuOpen ? '-rotate-45 -translate-y-[3.5px]' : '']"></span>
        </button>
      </div>
    </nav>

    <!-- Mobile menu (kept outside <nav> so backdrop-blur doesn't trap the fixed overlay) -->
    <div
      id="mobile-menu"
      :class="['fixed inset-0 z-[60] bg-ink text-paper lg:hidden flex flex-col justify-between px-6 pt-28 pb-10 transition-[opacity,visibility] duration-500', isMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible']"
      :inert="!isMenuOpen || undefined"
    >
      <div class="flex flex-col gap-3">
        <a
          v-for="(item, i) in [...navItems, { id: 'contact', label: 'Contact' }]"
          :key="item.id"
          :href="'#' + item.id"
          @click="closeMenu"
          class="group flex items-baseline gap-4 font-display text-4xl sm:text-5xl"
        >
          <span class="font-mono text-xs text-gold">{{ pad(i + 1) }}</span>
          <span class="group-hover:text-gold transition-colors">{{ item.label }}</span>
        </a>
      </div>
      <div class="flex flex-wrap gap-x-6 gap-y-2 font-mono text-[11px] uppercase tracking-widest text-paper/50">
        <a :href="profile.googleScholar" target="_blank" rel="noopener" class="hover:text-gold">Scholar</a>
        <a :href="profile.orcid" target="_blank" rel="noopener" class="hover:text-gold">ORCID</a>
        <a :href="profile.linkedin" target="_blank" rel="noopener" class="hover:text-gold">LinkedIn</a>
        <a :href="profile.credly" target="_blank" rel="noopener" class="hover:text-gold">Credly</a>
      </div>
    </div>

    <main id="top">
      <!-- ============ HERO ============ -->
      <section class="relative min-h-[100svh] bg-ink text-paper grain overflow-hidden flex flex-col">
        <ClientOnly>
          <HeroGraph :nodes="graph.nodes" :links="graph.links" :burst="graphBurst" :labels="false" :anchor-x="0.75" />
        </ClientOnly>
        <!-- legibility veil -->
        <div class="absolute inset-0 pointer-events-none bg-gradient-to-t from-ink via-ink/85 to-ink/55 lg:bg-gradient-to-r lg:from-ink lg:via-ink/80 lg:to-ink/20" aria-hidden="true"></div>

        <div class="relative z-10 flex-1 w-full max-w-[1400px] mx-auto px-6 lg:px-12 pt-32 lg:pt-36 pb-16 grid grid-cols-1 lg:grid-cols-12 gap-14 lg:gap-16 items-center pointer-events-none">
          <div class="lg:col-span-7 flex flex-col gap-8 pointer-events-auto">
            <p v-reveal class="flex items-center gap-3 font-mono text-[11px] uppercase tracking-[0.22em] text-gold">
              <span class="w-8 h-px bg-gold shrink-0" aria-hidden="true"></span>{{ hero.eyebrow }}
            </p>
            <h1 v-reveal="80" class="font-display font-semibold leading-[0.95] tracking-[-0.025em] text-[clamp(3.25rem,7.5vw,7rem)]">
              {{ hero.headline }}
            </h1>
            <p v-reveal="160" class="font-display italic display-soft text-2xl lg:text-[2rem] leading-snug text-paper/85 max-w-2xl">
              {{ hero.statement }}
            </p>
            <div v-reveal="220" class="flex flex-wrap items-center gap-3">
              <a :href="hero.primaryCta.url" class="group inline-flex items-center gap-3 h-12 px-7 rounded-sm bg-gold text-ink text-sm font-semibold hover:bg-paper transition-colors">
                {{ hero.primaryCta.text }} <span class="transition-transform group-hover:translate-x-1" aria-hidden="true">→</span>
              </a>
              <a :href="hero.secondaryCta.url" class="inline-flex items-center h-12 px-7 rounded-sm border border-white/25 text-paper text-sm font-semibold hover:bg-white/10 transition-colors">{{ hero.secondaryCta.text }}</a>
              <NuxtLink v-if="hero.cvUrl" :to="hero.cvUrl" class="inline-flex items-center gap-2 h-12 px-4 text-paper/70 text-sm font-semibold hover:text-paper transition-colors">
                Curriculum vitae <span aria-hidden="true">↗</span>
              </NuxtLink>
            </div>
            <dl v-reveal="280" class="grid grid-cols-1 sm:grid-cols-3 border-t border-white/15 mt-2">
              <div v-for="(cred, i) in hero.credentials" :key="cred.org" :class="['py-5 sm:pr-5 flex flex-col gap-1.5', i > 0 ? 'border-t sm:border-t-0 sm:border-l border-white/15 sm:pl-5' : '']">
                <dt class="font-mono text-[10px] uppercase tracking-[0.2em] text-gold">{{ cred.org }}</dt>
                <dd><a :href="cred.href" class="text-paper/85 text-sm leading-snug hover:text-paper transition-colors">{{ cred.title }}</a></dd>
              </div>
            </dl>
          </div>

          <div v-reveal="120" class="lg:col-span-5 pointer-events-auto">
            <figure class="relative w-full max-w-[400px] mx-auto lg:ml-auto lg:mr-0">
              <div class="absolute inset-0 translate-x-4 translate-y-4 border border-gold/40" aria-hidden="true"></div>
              <div class="relative overflow-hidden bg-ink-2 shadow-[0_40px_80px_-30px_rgba(0,0,0,0.7)]">
                <img :src="about.image" alt="Portrait of Jotham Hernandez" width="1000" height="1250" fetchpriority="high" class="w-full aspect-[4/5] object-cover object-[50%_20%]" />
                <figcaption class="absolute inset-x-0 bottom-0 p-5 pt-16 bg-gradient-to-t from-ink via-ink/80 to-transparent flex flex-col gap-1.5">
                  <span class="flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.2em] text-gold">
                    <span class="relative flex w-2 h-2" aria-hidden="true">
                      <span class="absolute inline-flex h-full w-full rounded-full bg-gold opacity-60 motion-safe:animate-ping"></span>
                      <span class="relative inline-flex w-2 h-2 rounded-full bg-gold"></span>
                    </span>
                    {{ hero.availability }}
                  </span>
                  <span class="text-paper text-sm">{{ profile.currentRole }}</span>
                </figcaption>
              </div>
            </figure>
          </div>
        </div>

        <div class="relative z-10 w-full max-w-[1400px] mx-auto px-6 lg:px-12 pb-8 hidden lg:flex items-center gap-6 font-mono text-[10px] uppercase tracking-[0.2em] text-paper/40 pointer-events-none">
          <span class="flex items-center gap-2"><span class="inline-block w-px h-6 bg-paper/30" aria-hidden="true"></span>Scroll to explore</span>
          <span class="ml-auto">{{ hero.locations }}</span>
        </div>
      </section>

      <!-- ============ INSTITUTIONS ============ -->
      <section aria-labelledby="institutions-label" class="bg-paper border-b border-ink/10 px-6 lg:px-12">
        <div class="max-w-[1400px] mx-auto py-10 flex flex-col lg:flex-row lg:items-center gap-6 lg:gap-12">
          <p id="institutions-label" class="font-mono text-[10px] uppercase tracking-[0.22em] text-ink/50 lg:w-44 shrink-0 leading-relaxed">Institutions &amp; credentialing bodies</p>
          <ul class="flex-1 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-px bg-ink/10 border border-ink/10">
            <li v-for="name in hero.institutions" :key="name" class="bg-paper px-3 py-5 flex items-center justify-center text-center font-display text-base lg:text-lg leading-tight text-ink/65 hover:text-ink transition-colors">{{ name }}</li>
          </ul>
        </div>
      </section>

      <!-- ============ ABOUT + STATS ============ -->
      <section id="about" class="relative bg-paper pt-28 pb-28 px-6 lg:px-12">
        <div class="max-w-[1400px] mx-auto">
          <div ref="statsEl" class="grid grid-cols-2 lg:grid-cols-4 border-t border-ink/15 mb-28">
            <div v-for="(stat, i) in stats" :key="stat.label" v-reveal="i * 90" :class="['pt-6 pb-2 pr-4', i % 2 === 1 ? 'pl-4 lg:pl-6 border-l border-ink/15' : i > 0 ? 'lg:pl-6 lg:border-l lg:border-ink/15' : '']">
              <p class="font-display font-semibold text-6xl lg:text-7xl leading-none tracking-tight tabular-nums">{{ statDisplay[i] }}<span class="text-gold-deep">{{ stat.suffix }}</span></p>
              <p class="mt-3 font-mono text-[10px] uppercase tracking-[0.18em] text-ink/60 max-w-[14rem]">{{ stat.label }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-14 lg:gap-20 items-start">
            <div class="lg:col-span-7 flex flex-col gap-10">
              <p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold-deep">§ 01 — About</p>
              <h2 v-reveal="60" class="font-display font-semibold text-4xl md:text-5xl lg:text-6xl leading-[1.05] tracking-tight">
                {{ about.title }}
              </h2>
              <div class="flex flex-col gap-6 text-ink/75 text-lg leading-relaxed max-w-2xl">
                <p v-for="(para, index) in about.paragraphs" :key="index" v-reveal="index * 80">{{ para }}</p>
              </div>
            </div>
            <aside v-reveal="120" class="lg:col-span-5 lg:sticky lg:top-28 bg-white border border-ink/10 shadow-[0_30px_60px_-40px_rgba(11,26,46,0.45)]" aria-labelledby="glance-title">
              <div class="px-7 py-5 border-b border-ink/10 flex items-center justify-between">
                <h3 id="glance-title" class="font-mono text-[11px] uppercase tracking-[0.22em] text-ink">Profile at a glance</h3>
                <span class="w-2 h-2 bg-gold-deep" aria-hidden="true"></span>
              </div>
              <dl class="divide-y divide-ink/10">
                <div v-for="row in glance" :key="row.label" class="px-7 py-4 grid grid-cols-3 gap-4">
                  <dt class="font-mono text-[10px] uppercase tracking-[0.18em] text-ink/50 pt-0.5">{{ row.label }}</dt>
                  <dd class="col-span-2 text-ink/85 text-[15px] leading-snug">{{ row.value }}</dd>
                </div>
              </dl>
              <div class="px-7 py-5 border-t border-ink/10 flex flex-wrap gap-x-6 gap-y-2">
                <a :href="profile.orcid" target="_blank" rel="noopener" class="text-sm font-semibold border-b border-gold-deep hover:text-gold-deep transition-colors">ORCID ↗</a>
                <a :href="profile.googleScholar" target="_blank" rel="noopener" class="text-sm font-semibold border-b border-gold-deep hover:text-gold-deep transition-colors">Google Scholar ↗</a>
                <a :href="profile.linkedin" target="_blank" rel="noopener" class="text-sm font-semibold border-b border-gold-deep hover:text-gold-deep transition-colors">LinkedIn ↗</a>
              </div>
            </aside>
          </div>
        </div>
      </section>

      <!-- ============ RESEARCH ============ -->
      <section id="research" class="relative bg-ink text-paper grain py-32 px-6 lg:px-12">
        <div class="relative max-w-[1400px] mx-auto">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-20 items-end">
            <div class="lg:col-span-7">
              <p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold mb-6">§ 02 — Research</p>
              <h2 v-reveal="60" class="font-display font-semibold text-5xl md:text-6xl lg:text-7xl leading-[0.95] tracking-tight">Research <span class="italic font-normal text-gold">directions</span></h2>
            </div>
            <p v-reveal="120" class="lg:col-span-5 text-paper/60 text-lg leading-relaxed">
              Five threads, one question: how can institutions adopt AI and digital infrastructure in ways people can understand and trust?
            </p>
          </div>

          <ol class="border-t border-white/10">
            <li v-for="(interest, i) in researchInterests" :key="interest.id" v-reveal="i * 60" class="group border-b border-white/10">
              <div class="grid grid-cols-12 gap-4 lg:gap-8 py-8 lg:py-10 items-baseline transition-colors duration-500 group-hover:bg-white/[0.02]">
                <span class="col-span-2 lg:col-span-1 font-mono text-sm text-gold">{{ pad(i + 1) }}</span>
                <h3 class="col-span-10 lg:col-span-5 font-display text-2xl md:text-3xl lg:text-4xl leading-tight tracking-tight transition-all duration-500 group-hover:text-gold">{{ interest.title }}</h3>
                <div class="col-span-12 lg:col-span-6 col-start-3 lg:col-start-auto flex flex-col gap-4">
                  <p class="text-paper/60 leading-relaxed">{{ interest.description }}</p>
                  <div class="flex flex-wrap gap-2">
                    <span v-for="tag in interest.tags" :key="tag" class="font-mono text-[10px] uppercase tracking-wider px-2 py-1 rounded border border-white/10 text-paper/50">{{ tag }}</span>
                  </div>
                </div>
              </div>
            </li>
          </ol>
        </div>
      </section>

      <!-- ============ PUBLICATIONS ============ -->
      <section id="publications" class="bg-paper-2 py-32 px-6 lg:px-12">
        <div class="max-w-[1400px] mx-auto">
          <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-8 mb-16">
            <div>
              <p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold-deep mb-6">§ 03 — Publications</p>
              <h2 v-reveal="60" class="font-display font-semibold text-5xl md:text-6xl lg:text-7xl leading-[0.95] tracking-tight">Research <span class="italic font-normal">writing</span></h2>
            </div>
            <div v-reveal="120" class="flex flex-wrap gap-3">
              <a :href="profile.googleScholar" target="_blank" rel="noopener" class="inline-flex items-center gap-2 h-11 px-5 rounded-sm border border-ink/20 text-sm font-semibold hover:bg-ink hover:text-paper transition-colors">Google Scholar <span aria-hidden="true">↗</span></a>
              <a :href="profile.orcid" target="_blank" rel="noopener" class="inline-flex items-center gap-2 h-11 px-5 rounded-sm border border-ink/20 text-sm font-semibold hover:bg-ink hover:text-paper transition-colors">ORCID <span aria-hidden="true">↗</span></a>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <article
              v-for="(pub, index) in publications"
              :key="pub.title"
              v-reveal="index * 90"
              :class="['relative bg-paper border border-ink/10 p-8 lg:p-10 flex flex-col gap-5 hover:-translate-y-1 hover:shadow-[0_24px_50px_-28px_rgba(11,26,46,0.5)] transition-all duration-500', index === 0 ? 'lg:col-span-12 lg:grid lg:grid-cols-12 lg:gap-10' : 'lg:col-span-6']"
            >
              <div :class="index === 0 ? 'lg:col-span-4 flex flex-col gap-4' : 'flex items-center justify-between gap-4'">
                <span class="font-mono text-[10px] uppercase tracking-[0.2em] text-gold-deep">{{ pub.type }} · {{ pub.year }}</span>
                <span :class="['self-start font-mono text-[10px] uppercase tracking-[0.2em] px-2.5 py-1 border rounded-sm', pub.status === 'In Progress' ? 'border-gold-deep text-gold-deep' : 'border-ink/30 text-ink/50']">{{ pub.status }}</span>
              </div>
              <div :class="index === 0 ? 'lg:col-span-8 flex flex-col gap-5' : 'flex flex-col gap-5 flex-1'">
                <h3 :class="['font-display leading-[1.1] tracking-tight', index === 0 ? 'text-3xl md:text-4xl lg:text-5xl' : 'text-2xl md:text-3xl']">{{ pub.title }}</h3>
                <p v-if="pub.authors || pub.venue" class="font-mono text-xs text-ink/55">
                  <span v-if="pub.authors">{{ pub.authors }}</span><span v-if="pub.authors && pub.venue"> — </span><span v-if="pub.venue" class="italic">{{ pub.venue }}</span>
                </p>
                <p class="text-ink/70 leading-relaxed">
                  <span v-if="index === 0" class="font-mono text-[10px] uppercase tracking-[0.2em] text-ink/40 mr-2">Abstract</span>{{ pub.description }}
                </p>
                <div class="flex flex-wrap items-center gap-3 mt-auto pt-2">
                  <a v-if="pub.doi" :href="pub.doi" target="_blank" rel="noopener" class="font-mono text-[11px] uppercase tracking-widest border-b border-gold-deep text-ink hover:text-gold-deep">DOI ↗</a>
                  <a v-if="pub.url" :href="pub.url" target="_blank" rel="noopener" class="font-mono text-[11px] uppercase tracking-widest border-b border-gold-deep text-ink hover:text-gold-deep">Read ↗</a>
                  <span v-for="tag in pub.tags" :key="tag" class="font-mono text-[10px] text-ink/45">#{{ tag.replace(/\s+/g, '') }}</span>
                </div>
              </div>
            </article>
          </div>
        </div>
      </section>

      <!-- ============ PROJECTS ============ -->
      <section id="projects" class="bg-paper py-32 px-6 lg:px-12">
        <div class="max-w-[1400px] mx-auto">
          <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-8 mb-20">
            <div>
              <p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold-deep mb-6">§ 04 — Projects</p>
              <h2 v-reveal="60" class="font-display font-semibold text-5xl md:text-6xl lg:text-7xl leading-[0.95] tracking-tight">Selected <span class="italic font-normal">projects</span></h2>
            </div>
            <p v-reveal="120" class="text-ink/60 text-lg leading-relaxed max-w-md">Research prototypes, institutional frameworks, and production systems delivered for real-world use.</p>
          </div>

          <div class="flex flex-col gap-32 lg:gap-44 pt-10 lg:pt-16">
            <article v-for="(project, index) in projects" :key="project.id" class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-center group">
              <div v-reveal :class="['lg:col-span-7 relative', index % 2 === 1 ? 'lg:order-2' : '']">
                <span class="absolute -top-[4.5rem] lg:-top-[7.5rem] font-display font-semibold text-[7rem] lg:text-[11rem] leading-none text-transparent [-webkit-text-stroke:1px_rgba(11,26,46,0.22)] select-none z-0" :class="index % 2 === 1 ? 'right-2' : 'left-2'" aria-hidden="true">{{ pad(index + 1) }}</span>
                <div class="relative z-10 overflow-hidden bg-ink aspect-video shadow-[0_40px_80px_-40px_rgba(11,26,46,0.6)]">
                  <img :src="project.image" :alt="project.title + ' — project visual'" width="1600" height="900" loading="lazy" class="w-full h-full object-cover transition-transform duration-[1.2s] ease-out group-hover:scale-[1.04]" />
                </div>
              </div>
              <div v-reveal="120" :class="['lg:col-span-5 flex flex-col gap-5', index % 2 === 1 ? 'lg:order-1' : '']">
                <div class="flex flex-wrap items-center gap-3 font-mono text-[10px] uppercase tracking-[0.18em]">
                  <span class="text-[11px] tracking-[0.2em] text-gold-deep">{{ project.type }} · {{ project.year }}</span>
                  <span class="px-2 py-0.5 border border-ink/20 text-ink/60 rounded-sm">{{ project.status }}</span>
                  <span v-if="project.featured" class="px-2 py-0.5 bg-ink text-gold rounded-sm">Featured</span>
                </div>
                <h3 class="font-display text-4xl lg:text-5xl leading-[1.02] tracking-tight">{{ project.title }}</h3>
                <p class="text-ink/50 font-mono text-xs uppercase tracking-wider">Role — {{ project.role }}</p>
                <p class="text-ink/75 text-lg leading-relaxed">{{ project.shortDescription }}</p>
                <p v-if="project.longDescription" class="text-ink/60 leading-relaxed">{{ project.longDescription }}</p>
                <p v-if="project.impact" class="border-l-2 border-gold-deep pl-4 text-ink/80 italic font-display text-lg leading-snug">{{ project.impact }}</p>
                <div class="flex flex-wrap gap-2 pt-1">
                  <span v-for="tech in project.technologyStack" :key="tech" class="font-mono text-[10px] uppercase tracking-wider px-2.5 py-1 bg-paper-2 text-ink/70 rounded-sm">{{ tech }}</span>
                </div>
                <div v-if="project.liveUrl || project.repositoryUrl" class="flex gap-3 pt-3">
                  <a v-if="project.liveUrl" :href="project.liveUrl" target="_blank" rel="noopener" class="group/link inline-flex items-center gap-2 h-11 px-6 rounded-sm bg-ink text-paper text-sm font-semibold hover:bg-gold hover:text-ink transition-colors">Visit live <span class="transition-transform group-hover/link:translate-x-0.5 group-hover/link:-translate-y-0.5" aria-hidden="true">↗</span></a>
                  <a v-if="project.repositoryUrl" :href="project.repositoryUrl" target="_blank" rel="noopener" class="inline-flex items-center gap-2 h-11 px-6 rounded-sm border border-ink/20 text-sm font-semibold hover:bg-ink hover:text-paper transition-colors">Repository ↗</a>
                </div>
              </div>
            </article>
          </div>
        </div>
      </section>

      <!-- ============ EXPERIENCE ============ -->
      <section id="experience" class="bg-paper-2 py-32 px-6 lg:px-12">
        <div class="max-w-[1400px] mx-auto grid grid-cols-1 lg:grid-cols-12 gap-16">
          <div class="lg:col-span-4">
            <div class="lg:sticky lg:top-32 flex flex-col gap-6">
              <p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold-deep">§ 05 — Experience</p>
              <h2 v-reveal="60" class="font-display font-semibold text-5xl md:text-6xl leading-[0.95] tracking-tight">Career <span class="italic font-normal">trajectory</span></h2>
              <p v-reveal="120" class="text-ink/60 text-lg leading-relaxed">From software development and IT education to leading ICT at a national government authority, alongside a sustained role in WorldSkills.</p>
              <p class="font-display font-semibold text-7xl text-gold-deep tabular-nums" aria-hidden="true">{{ firstYear }}<span class="text-ink/30 not-italic">→</span></p>
            </div>
          </div>
          <div ref="timelineEl" class="lg:col-span-8 relative pl-10">
            <!-- spine fills as you scroll -->
            <div class="absolute left-[7px] top-2 bottom-2 w-px bg-ink/15" aria-hidden="true">
              <div class="absolute inset-0 bg-gold-deep origin-top" :style="{ transform: `scaleY(${timelineProgress})` }"></div>
            </div>
            <div class="flex flex-col gap-16">
              <article v-for="(job, index) in experience" :key="job.role + job.startDate" v-reveal class="relative flex flex-col gap-4">
                <span :class="['absolute -left-10 top-1.5 w-[15px] h-[15px] rounded-full border-2', job.isCurrent ? 'bg-gold border-gold-deep shadow-[0_0_0_6px_rgba(201,169,106,0.25)]' : 'bg-paper-2 border-ink/30']" aria-hidden="true"></span>
                <div class="flex flex-wrap items-center gap-3 font-mono text-[11px] uppercase tracking-[0.18em]">
                  <span class="text-ink">{{ job.startDate }} — {{ job.endDate }}</span>
                  <span v-if="job.isCurrent" class="px-2 py-0.5 bg-ink text-gold rounded-full text-[9px]">Current</span>
                </div>
                <h3 class="font-display text-3xl lg:text-4xl leading-tight tracking-tight">{{ job.role }}</h3>
                <p class="text-gold-deep font-semibold">{{ job.organization }} <span class="text-ink/40 font-normal">· {{ job.location }}</span></p>
                <p class="text-ink/75 text-lg leading-relaxed">{{ job.summary }}</p>
                <ul class="flex flex-col gap-2">
                  <li v-for="highlight in job.highlights" :key="highlight" class="flex gap-3 text-ink/65 leading-relaxed">
                    <span class="text-gold-deep mt-0.5" aria-hidden="true">↳</span>{{ highlight }}
                  </li>
                </ul>
                <div class="flex flex-wrap gap-2">
                  <span v-for="tech in job.technologies" :key="tech" class="font-mono text-[10px] uppercase tracking-wider px-2 py-1 border border-ink/15 text-ink/55 rounded-sm">{{ tech }}</span>
                </div>
              </article>
            </div>
          </div>
        </div>
      </section>

      <!-- ============ EXPERTISE ============ -->
      <section id="expertise" class="relative bg-ink text-paper grain py-32 px-6 lg:px-12">
        <div class="relative max-w-[1400px] mx-auto">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-20 items-end">
            <div class="lg:col-span-7">
              <p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold mb-6">§ 06 — Expertise</p>
              <h2 v-reveal="60" class="font-display font-semibold text-5xl md:text-6xl lg:text-7xl leading-[0.95] tracking-tight">Technical <span class="italic font-normal text-gold">expertise</span></h2>
            </div>
            <p v-reveal="120" class="lg:col-span-5 text-paper/60 text-lg leading-relaxed">Breadth across infrastructure, software, data, and capacity building: the full stack of public-sector digital transformation.</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-white/10 border border-white/10">
            <div
              v-for="(group, i) in skills"
              :key="group.id"
              v-reveal="(i % 3) * 80"
              class="spotlight p-8 lg:p-10 flex flex-col gap-5 min-h-[300px]"
              @pointermove="onSpotlight"
            >
              <div class="flex justify-between items-start">
                <span class="font-mono text-xs text-gold">{{ pad(i + 1) }}</span>
                <span class="font-mono text-[10px] text-paper/30">{{ group.skills.length }} tools</span>
              </div>
              <h3 class="font-display text-2xl lg:text-3xl leading-tight">{{ group.category }}</h3>
              <p class="text-paper/55 leading-relaxed">{{ group.description }}</p>
              <div class="flex flex-wrap gap-1.5 mt-auto">
                <span v-for="skill in group.skills" :key="skill" class="font-mono text-[10px] uppercase tracking-wide px-2 py-1 bg-white/5 border border-white/10 text-paper/70 rounded-sm">{{ skill }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============ CREDENTIALS ============ -->
      <section id="certifications" class="bg-paper py-32 px-6 lg:px-12">
        <div class="max-w-[1400px] mx-auto">
          <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-8 mb-16">
            <div>
              <p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold-deep mb-6">§ 07 — Credentials</p>
              <h2 v-reveal="60" class="font-display font-semibold text-5xl md:text-6xl lg:text-7xl leading-[0.95] tracking-tight">Verified <span class="italic font-normal">credentials</span></h2>
            </div>
            <a v-reveal="120" :href="profile.credly" target="_blank" rel="noopener" class="group flex items-center gap-5 self-start lg:self-auto">
              <span class="font-display text-6xl leading-none tabular-nums">{{ verifiedCount }}</span>
              <span class="flex flex-col gap-1">
                <span class="font-mono text-[10px] uppercase tracking-[0.2em] text-ink/55">Badges verified on Credly</span>
                <span class="text-sm font-semibold border-b border-gold-deep self-start group-hover:text-gold-deep transition-colors">View profile ↗</span>
              </span>
            </a>
          </div>

          <h3 class="font-mono text-[11px] uppercase tracking-[0.2em] text-ink/50 mb-6">Professional certifications</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-20">
            <div v-for="(cert, i) in professionalCerts" :key="cert.id" v-reveal="(i % 2) * 80" class="group bg-white/60 border border-ink/10 p-6 flex gap-5 items-start hover:border-ink/30 hover:bg-white transition-colors">
              <img v-if="cert.badgeImage" :src="cert.badgeImage" :alt="cert.title + ' badge'" width="88" height="88" loading="lazy" class="w-16 h-16 md:w-20 md:h-20 object-contain shrink-0 transition-transform duration-500 group-hover:-rotate-6 group-hover:scale-105" />
              <div class="flex flex-col gap-2 min-w-0 flex-1">
                <p class="font-mono text-[10px] uppercase tracking-[0.18em] text-gold-deep">{{ cert.issuer }}</p>
                <h4 class="font-display text-xl lg:text-2xl leading-snug">{{ cert.title }}</h4>
                <p class="text-ink/60 text-sm leading-relaxed">{{ cert.description }}</p>
                <div class="flex flex-wrap items-center justify-between gap-3 pt-2 mt-auto">
                  <span class="font-mono text-[10px] uppercase tracking-wider text-ink/45">
                    Issued {{ formatMonthYear(cert.issued) }}<template v-if="cert.expires"> · Valid through {{ formatMonthYear(cert.expires) }}</template>
                  </span>
                  <a v-if="cert.credentialUrl" :href="cert.credentialUrl" target="_blank" rel="noopener" class="font-mono text-[10px] uppercase tracking-widest text-ink border-b border-gold-deep hover:text-gold-deep transition-colors">Verify ↗</a>
                </div>
              </div>
            </div>
          </div>

          <h3 class="font-mono text-[11px] uppercase tracking-[0.2em] text-ink/50 mb-6">International recognition &amp; awards</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-20">
            <div v-for="(badge, i) in recognitionBadges" :key="badge.id" v-reveal="(i % 2) * 80" class="group bg-ink text-paper p-6 flex gap-5 items-start">
              <img v-if="badge.badgeImage" :src="badge.badgeImage" :alt="badge.title + ' badge'" width="88" height="88" loading="lazy" class="w-16 h-16 md:w-20 md:h-20 object-contain shrink-0 transition-transform duration-500 group-hover:-rotate-6 group-hover:scale-105" />
              <div class="flex flex-col gap-2 min-w-0 flex-1">
                <p class="font-mono text-[10px] uppercase tracking-[0.18em] text-gold">{{ badge.issuer }}</p>
                <h4 class="font-display text-xl lg:text-2xl leading-snug">{{ badge.title }}</h4>
                <p class="text-paper/60 text-sm leading-relaxed">{{ badge.description }}</p>
                <a v-if="badge.credentialUrl" :href="badge.credentialUrl" target="_blank" rel="noopener" class="font-mono text-[10px] uppercase tracking-widest text-paper border-b border-gold hover:text-gold transition-colors pt-2 self-start">Verify ↗</a>
              </div>
            </div>
            <div v-for="(award, i) in awards" :key="award.title" v-reveal="(i % 2) * 80" class="bg-white/60 border border-ink/10 border-l-4 border-l-gold-deep p-6 flex flex-col gap-2">
              <p class="font-mono text-[10px] uppercase tracking-[0.18em] text-gold-deep">{{ award.organization }} · {{ award.year }}</p>
              <h4 class="font-display text-xl lg:text-2xl leading-snug">{{ award.title }}</h4>
              <p class="text-ink/60 text-sm leading-relaxed">{{ award.description }}</p>
            </div>
          </div>

          <h3 class="font-mono text-[11px] uppercase tracking-[0.2em] text-ink/50 mb-6">Continuing education</h3>
          <ul class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <li v-for="course in courseBadges" :key="course.id" class="border border-ink/10 bg-white/40 p-4 flex items-center gap-4 hover:bg-white transition-colors">
              <img v-if="course.badgeImage" :src="course.badgeImage" :alt="course.title + ' badge'" width="48" height="48" loading="lazy" class="w-11 h-11 object-contain shrink-0" />
              <span v-else class="w-11 h-11 shrink-0 rounded-full bg-paper-2 text-gold-deep flex items-center justify-center font-mono text-[10px]" aria-hidden="true">{{ course.issued.slice(0, 4) }}</span>
              <div class="flex flex-col min-w-0">
                <component :is="course.credentialUrl ? 'a' : 'span'" :href="course.credentialUrl || undefined" :target="course.credentialUrl ? '_blank' : undefined" :rel="course.credentialUrl ? 'noopener' : undefined" class="text-sm font-semibold leading-snug" :class="course.credentialUrl ? 'hover:text-gold-deep transition-colors' : ''">{{ course.title }}</component>
                <span class="font-mono text-[10px] uppercase tracking-wider text-ink/45">{{ course.issuer }} · {{ formatMonthYear(course.issued) }}</span>
              </div>
            </li>
          </ul>
        </div>
      </section>

      <!-- ============ EDUCATION ============ -->
      <section id="education" class="bg-paper-2 py-28 px-6 lg:px-12">
        <div class="max-w-[1400px] mx-auto">
          <p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold-deep mb-6">§ 08 — Education</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-px bg-ink/15 border-y border-ink/15">
            <div v-for="(edu, i) in education" :key="edu.institution" v-reveal="i * 90" class="bg-paper-2 py-10 md:px-10 first:md:pl-0 flex flex-col gap-4">
              <p class="font-display font-semibold text-5xl lg:text-6xl text-gold-deep tabular-nums leading-none">{{ edu.endDate }}</p>
              <h3 class="font-display text-2xl lg:text-3xl leading-tight">{{ edu.degree }} in {{ edu.field }}</h3>
              <p class="font-semibold">{{ edu.institution }} <span class="text-ink/45 font-normal">· {{ edu.location }}</span></p>
              <p class="text-ink/60 leading-relaxed">{{ edu.description }}</p>
              <p class="font-mono text-[10px] uppercase tracking-[0.2em] text-ink/45">{{ edu.startDate }} — {{ edu.endDate }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ============ VISION (word-by-word reveal on scroll) ============ -->
      <section ref="visionEl" class="relative bg-ink text-paper grain py-40 lg:py-56 px-6 lg:px-12">
        <div class="relative max-w-5xl mx-auto">
          <p class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold mb-10">§ 09 — Vision</p>
          <blockquote class="font-display italic text-3xl md:text-5xl lg:text-6xl leading-[1.15] tracking-tight">
            <span class="text-gold">“</span><span
              v-for="(word, i) in visionWords"
              :key="i"
              class="transition-opacity duration-300"
              :style="{ opacity: visionProgress * visionWords.length > i ? 1 : 0.15 }"
            >{{ i < visionWords.length - 1 ? word + ' ' : word }}</span><span class="text-gold">”</span>
          </blockquote>
          <p class="mt-12 flex items-center gap-4 font-mono text-[11px] uppercase tracking-[0.25em] text-paper/50">
            <span class="w-12 h-px bg-gold" aria-hidden="true"></span>{{ profile.name }}
          </p>
        </div>
      </section>

      <!-- ============ CONTACT ============ -->
      <section id="contact" class="relative bg-ink text-paper px-6 lg:px-12 pt-24 pb-24 border-t border-white/10">
        <div class="max-w-[1400px] mx-auto grid grid-cols-1 lg:grid-cols-12 gap-14">
          <div class="lg:col-span-7 flex flex-col gap-8">
            <p v-reveal class="font-mono text-[11px] uppercase tracking-[0.25em] text-gold">§ 10 — Contact</p>
            <h2 v-reveal="60" class="font-display font-semibold text-4xl md:text-5xl lg:text-6xl leading-[1.05] tracking-tight">
              Open to research collaboration and <span class="italic font-normal text-gold">public-sector partnerships.</span>
            </h2>
            <p v-reveal="100" class="text-paper/70 text-lg leading-relaxed max-w-xl">{{ contact.cta }}</p>
            <a v-if="contact.email" v-reveal="160" :href="'mailto:' + contact.email" class="group inline-flex items-center gap-4 self-start font-display text-2xl md:text-3xl break-all border-b border-white/25 pb-2 hover:border-gold hover:text-gold transition-colors">
              {{ contact.email }} <span class="transition-transform group-hover:translate-x-2 shrink-0" aria-hidden="true">→</span>
            </a>
          </div>
          <div class="lg:col-span-5 lg:pt-14">
            <ul class="border-t border-white/10">
              <li v-for="link in [
                  { href: profile.linkedin, label: 'LinkedIn', sub: 'Professional network' },
                  { href: profile.googleScholar, label: 'Google Scholar', sub: 'Publications & citations' },
                  { href: profile.orcid, label: 'ORCID', sub: 'Persistent research identifier' },
                  { href: profile.credly, label: 'Credly', sub: 'Verified certifications' }
                ]" :key="link.label" class="border-b border-white/10">
                <a :href="link.href" target="_blank" rel="noopener" class="group flex items-center justify-between gap-6 py-5">
                  <span class="flex flex-col gap-1">
                    <span class="font-display text-xl group-hover:text-gold transition-colors">{{ link.label }}</span>
                    <span class="font-mono text-[10px] uppercase tracking-[0.2em] text-paper/45">{{ link.sub }}</span>
                  </span>
                  <span class="text-paper/50 group-hover:text-gold group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all" aria-hidden="true">↗</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="bg-ink-2 text-paper px-6 lg:px-12 pt-16 pb-8">
      <div class="max-w-[1400px] mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-12 gap-10 pb-12 border-b border-white/10">
          <div class="md:col-span-6 flex flex-col gap-3">
            <p class="font-display font-semibold text-2xl">{{ profile.name }}</p>
            <p class="text-paper/55 text-sm leading-relaxed max-w-md">{{ profile.title }}</p>
          </div>
          <nav class="md:col-span-3 flex flex-col gap-2 text-sm" aria-label="Footer">
            <p class="font-mono text-[10px] uppercase tracking-[0.2em] text-gold mb-2">Sections</p>
            <a v-for="item in navItems" :key="item.id" :href="'#' + item.id" class="text-paper/65 hover:text-paper transition-colors self-start">{{ item.label }}</a>
          </nav>
          <div class="md:col-span-3 flex flex-col gap-2 text-sm">
            <p class="font-mono text-[10px] uppercase tracking-[0.2em] text-gold mb-2">Documents</p>
            <NuxtLink v-if="hero.cvUrl" :to="hero.cvUrl" class="text-paper/65 hover:text-paper transition-colors self-start">Curriculum vitae</NuxtLink>
            <NuxtLink to="/privacy" class="text-paper/65 hover:text-paper transition-colors self-start">Privacy policy</NuxtLink>
            <a :href="profile.credly" target="_blank" rel="noopener" class="text-paper/65 hover:text-paper transition-colors self-start">Credential verification</a>
          </div>
        </div>
        <div class="pt-6 flex flex-col sm:flex-row justify-between gap-4 font-mono text-[10px] uppercase tracking-[0.2em] text-paper/40">
          <span>© {{ currentYear }} {{ profile.name }} · {{ contact.location }}</span>
          <button type="button" @click="scrollToTop" class="self-start uppercase tracking-[0.2em] hover:text-paper transition-colors">Back to top ↑</button>
        </div>
      </div>
    </footer>

    <!-- Back to Top Button -->
    <button
      @click="scrollToTop"
      :class="['fixed bottom-6 right-6 z-[50] w-12 h-12 bg-gold text-ink flex items-center justify-center shadow-2xl transition-all duration-500 hover:bg-paper rounded-full', showScrollTop ? 'opacity-100 translate-y-0 pointer-events-auto' : 'opacity-0 translate-y-10 pointer-events-none']"
      aria-label="Back to top"
      :tabindex="showScrollTop ? 0 : -1"
    >
      <span class="text-xl" aria-hidden="true">↑</span>
    </button>
  </div>
</template>
