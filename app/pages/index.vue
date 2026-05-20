<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
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
import writings from '../data/writings.json'
import contact from '../data/contact.json'
import seo from '../data/seo.json'

const isMenuOpen = ref(false)
const showScrollTop = ref(false)
const currentYear = computed(() => new Date().getFullYear())

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
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
      children: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Person",
        "name": profile.name,
        "jobTitle": profile.currentRole,
        "url": seo.canonicalUrl,
        "sameAs": [
          profile.linkedin,
          profile.orcid,
          profile.googleScholar
        ]
      })
    }
  ]
})

let lenis: Lenis | null = null

const scrollToTop = () => {
  if (lenis) {
    lenis.scrollTo(0)
  }
}

onMounted(() => {
  lenis = new Lenis()

  function raf(time: number) {
    lenis?.raf(time)
    requestAnimationFrame(raf)
  }

  requestAnimationFrame(raf)

  // Track scroll position for "Back to Top" button
  const handleScroll = () => {
    showScrollTop.value = window.scrollY > 500
  }

  window.addEventListener('scroll', handleScroll)
  
  lenis.on('scroll', (e: any) => {
    // Sync with Lenis scroll as well for consistency
    showScrollTop.value = e.scroll > 500
  })

  // Handle anchor link clicks for smooth scrolling
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e: Event) => {
      const targetId = (anchor as HTMLAnchorElement).getAttribute('href')
      if (targetId && targetId.startsWith('#') && targetId !== '#') {
        e.preventDefault()
        lenis?.scrollTo(targetId)
      }
    })
  })
})
</script>

<template>
  <div class="w-full bg-white font-['Inter']">
    <!-- Navigation -->
    <nav class="sticky top-0 z-50 w-full px-8 py-4 bg-white/80 backdrop-blur-md border-b border-gray-100 flex justify-between items-center">
      <div class="text-zinc-900 text-xl font-bold font-noto-serif">{{ profile.name }}</div>
      
      <!-- Mobile Menu Toggle -->
      <button @click="toggleMenu" class="md:hidden flex flex-col justify-center items-center w-10 h-10 gap-1.5 z-[70] focus:outline-none" aria-label="Toggle Menu">
        <span :class="['w-6 h-0.5 bg-zinc-900 block transition-all duration-300', isMenuOpen ? 'rotate-45 translate-y-2' : '']"></span>
        <span :class="['w-6 h-0.5 bg-zinc-900 block transition-opacity duration-300', isMenuOpen ? 'opacity-0' : '']"></span>
        <span :class="['w-6 h-0.5 bg-zinc-900 block transition-all duration-300', isMenuOpen ? '-rotate-45 -translate-y-2' : '']"></span>
      </button>

      <!-- Desktop Navigation -->
      <div class="hidden md:flex gap-8 items-center font-noto-serif">
        <a href="#research" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Research</a>
        <a href="#experience" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Experience</a>
        <a href="#expertise" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Expertise</a>
        <a href="#projects" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Projects</a>
        <a href="#education" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Education</a>
        <a href="#writings" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Writings</a>
        <a href="#contact" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Contact</a>
      </div>

      <!-- Mobile Navigation Overlay -->
      <div :class="['fixed inset-0 bg-white z-[60] h-[100vh] flex flex-col items-center justify-start gap-8 transition-transform duration-500 md:hidden pt-24 pb-12', isMenuOpen ? 'translate-x-0' : 'translate-x-full']">
        <a href="#research" @click="closeMenu" class="text-zinc-900 text-2xl font-bold font-noto-serif">Research</a>
        <a href="#experience" @click="closeMenu" class="text-zinc-900 text-2xl font-bold font-noto-serif">Experience</a>
        <a href="#expertise" @click="closeMenu" class="text-zinc-900 text-2xl font-bold font-noto-serif">Expertise</a>
        <a href="#projects" @click="closeMenu" class="text-zinc-900 text-2xl font-bold font-noto-serif">Projects</a>
        <a href="#education" @click="closeMenu" class="text-zinc-900 text-2xl font-bold font-noto-serif">Education</a>
        <a href="#writings" @click="closeMenu" class="text-zinc-900 text-2xl font-bold font-noto-serif">Writings</a>
        <a href="#contact" @click="closeMenu" class="text-zinc-900 text-2xl font-bold font-noto-serif">Contact</a>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-6 lg:px-24">
      <!-- Hero Section -->
      <section class="relative min-h-[80vh] flex items-center py-24 overflow-hidden">
        <div class="w-full grid grid-cols-1 lg:grid-cols-2 items-center gap-12">
          <div class="flex flex-col gap-6 z-10">
            <span class="text-yellow-800 text-sm font-bold tracking-[0.3em] uppercase font-['Manrope']">PORTFOLIO & ACADEMIC RECORD</span>
            <h1 class="text-zinc-900 text-6xl lg:text-7xl font-bold font-noto-serif leading-[1.1]">
              {{ hero.headline }}
            </h1>
            <h2 class="text-zinc-600 text-2xl lg:text-3xl font-normal font-noto-serif leading-relaxed max-w-2xl">
              {{ hero.subtitle }}
            </h2>
            <p class="text-zinc-500 text-lg max-w-xl font-['Inter']">
              {{ hero.summary }}
            </p>
            <div class="flex gap-4 pt-4">
              <a :href="hero.primaryCta.url" class="px-8 py-4 bg-black text-white text-xs font-bold tracking-widest uppercase font-['Manrope'] inline-block">{{ hero.primaryCta.text }}</a>
              <a :href="hero.secondaryCta.url" class="px-8 py-4 border border-zinc-200 text-zinc-900 text-xs font-bold tracking-widest uppercase font-['Manrope'] hover:bg-zinc-50 transition-colors inline-block">{{ hero.secondaryCta.text }}</a>
            </div>
          </div>
          <div class="absolute right-[-10%] top-1/2 -translate-y-1/2 opacity-5 pointer-events-none">
            <div class="w-[600px] h-[600px] border border-zinc-900 flex items-center justify-center">
              <div class="w-[450px] h-[450px] border border-zinc-900 rotate-45"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- About Section -->
      <section class="py-24 grid grid-cols-1 lg:grid-cols-12 gap-16 items-start bg-zinc-100 -mx-6 lg:-mx-24 px-6 lg:px-24">
        <div class="lg:col-span-4 aspect-[4/5] bg-zinc-200 overflow-hidden rounded-sm" v-if="about.image">
          <img :src="about.image" alt="Profile" class="w-full h-full object-cover opacity-90" />
        </div>
        <div class="lg:col-span-8 flex flex-col gap-8">
          <h2 class="text-zinc-900 text-3xl lg:text-4xl font-bold font-noto-serif leading-tight">
            {{ about.title }}
          </h2>
          <div class="flex flex-col gap-6 text-zinc-600 text-lg leading-relaxed font-['Inter']">
            <p v-for="(para, index) in about.paragraphs" :key="index">
              {{ para }}
            </p>
          </div>
        </div>
      </section>

      <!-- Research Interests -->
      <section id="research" class="py-32">
        <div class="mb-16">
          <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif mb-4">Research Interests</h2>
          <div class="w-24 h-1 bg-yellow-800"></div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div v-for="interest in researchInterests" :key="interest.id" class="p-10 bg-white border border-zinc-100 shadow-sm flex flex-col gap-6">
            <div class="w-10 h-10 flex items-center justify-center text-yellow-800 bg-orange-50 rounded-full font-bold">
              {{ interest.icon }}
            </div>
            <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">{{ interest.title }}</h3>
            <p class="text-zinc-600 text-sm leading-relaxed">
              {{ interest.description }}
            </p>
            <div class="flex flex-wrap gap-2 mt-auto">
              <span v-for="tag in interest.tags" :key="tag" class="text-[10px] text-zinc-400 uppercase tracking-widest font-bold">#{{ tag }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Professional Experience -->
      <section id="experience" class="py-32 bg-zinc-100 -mx-6 lg:-mx-24 px-6 lg:px-24">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-16">
          <div class="lg:col-span-4 flex flex-col gap-6">
            <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif leading-tight">Professional Experience</h2>
            <p class="text-zinc-600 text-base leading-relaxed font-['Inter']">
              A track record of technical leadership and institutional contribution across the public sector, education, and software development.
            </p>
          </div>
          <div class="lg:col-span-8 flex flex-col gap-12">
            <div v-for="(job, index) in experience" :key="index" class="flex flex-col gap-4 pb-8 border-b border-zinc-200 last:border-0">
              <div class="flex flex-col md:flex-row md:justify-between md:items-start gap-2">
                <div>
                  <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">{{ job.role }}</h3>
                  <div class="flex items-center gap-2 text-yellow-800 text-sm font-bold font-['Manrope']">
                    <span>{{ job.organization }}</span>
                    <span class="text-zinc-300">•</span>
                    <span class="text-zinc-500 font-normal uppercase tracking-widest text-[10px]">{{ job.location }}</span>
                  </div>
                </div>
                <div class="text-zinc-500 text-xs font-bold tracking-widest uppercase font-['Manrope'] bg-white px-3 py-1 border border-zinc-200 rounded">
                  {{ job.startDate }} — {{ job.endDate }}
                </div>
              </div>
              <p class="text-zinc-600 text-sm leading-relaxed font-['Inter'] font-medium">
                {{ job.summary }}
              </p>
              <ul class="list-disc list-outside ml-4 flex flex-col gap-2">
                <li v-for="highlight in job.highlights" :key="highlight" class="text-zinc-500 text-sm leading-relaxed font-['Inter']">
                  {{ highlight }}
                </li>
              </ul>
              <div class="flex flex-wrap gap-2 mt-2">
                <span v-for="tech in job.technologies" :key="tech" class="px-2 py-1 bg-white text-zinc-400 text-[9px] font-bold uppercase rounded border border-zinc-200">
                  {{ tech }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Core Expertise -->
      <section id="expertise" class="bg-black py-32 text-white -mx-6 lg:-mx-24 px-6 lg:px-24 mb-32">
        <div class="max-w-7xl mx-auto">
          <div class="mb-20">
            <h2 class="text-4xl font-bold font-noto-serif mb-4">Technical Expertise</h2>
            <span class="text-zinc-500 text-xs font-medium tracking-widest uppercase font-['Manrope']">TECHNICAL COMPETENCIES & PROFESSIONAL DOMAINS</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 lg:gap-x-16 lg:gap-y-20">
            <div v-for="skillGroup in skills" :key="skillGroup.id" class="pl-6 border-l-2 border-orange-200 flex flex-col gap-4">
              <h3 class="text-xl font-bold font-noto-serif">{{ skillGroup.category }}</h3>
              <p class="text-zinc-500 text-sm leading-relaxed font-['Inter']">
                {{ skillGroup.description }}
              </p>
              <div class="flex flex-wrap gap-2 mt-2">
                <span v-for="skill in skillGroup.skills" :key="skill" class="px-2 py-1 bg-zinc-900 text-zinc-400 text-[10px] font-bold uppercase rounded border border-zinc-800">{{ skill }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Selected Projects -->
      <section id="projects" class="py-32">
        <div class="flex flex-col md:flex-row justify-between items-end mb-20 gap-8">
          <div class="flex flex-col gap-4">
            <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif">Selected Projects</h2>
            <div class="w-24 h-1 bg-yellow-800"></div>
          </div>
          <p class="text-zinc-600 text-sm leading-relaxed max-w-sm font-['Inter']">
            A selection of research projects, institutional implementations, and technical solutions.
          </p>
        </div>

        <div class="flex flex-col gap-32">
          <div v-for="(project, index) in projects" :key="project.id" :class="['relative group flex flex-col', index % 2 === 1 ? 'lg:items-end' : '']">
            <div class="w-full lg:w-3/4 aspect-video bg-zinc-100 overflow-hidden rounded-sm relative">
              <img :src="project.image || 'https://placehold.co/1200x800'" :alt="project.title" class="w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-700" />
              <div class="absolute top-4 left-4 flex gap-2">
                <span class="px-3 py-1 bg-black/50 backdrop-blur-md text-white text-[9px] font-bold uppercase rounded-full tracking-widest">{{ project.status }}</span>
                <span class="px-3 py-1 bg-yellow-800/80 backdrop-blur-md text-white text-[9px] font-bold uppercase rounded-full tracking-widest">{{ project.type }}</span>
              </div>
            </div>
            <div :class="['lg:absolute top-1/2 lg:-translate-y-1/2 w-full lg:w-[500px] p-10 bg-white border border-zinc-100 shadow-xl lg:mt-0 mt-8 z-10', index % 2 === 1 ? 'left-0' : 'right-0']">
              <span class="text-yellow-800 text-[10px] font-bold tracking-[0.2em] uppercase font-['Manrope']">{{ project.role }} • {{ project.year }}</span>
              <h3 class="text-zinc-900 text-2xl font-bold font-noto-serif mt-4 mb-4">{{ project.title }}</h3>
              <p class="text-zinc-600 text-sm leading-relaxed mb-6 font-['Inter']">
                {{ project.shortDescription }}
              </p>
              <div class="flex flex-wrap gap-2 mb-8 font-['Manrope']">
                <span v-for="tech in project.technologyStack" :key="tech" class="px-3 py-1 bg-orange-100 text-yellow-800 text-[9px] font-bold uppercase rounded-full">{{ tech }}</span>
              </div>
              <div class="flex gap-4">
                <a v-if="project.liveUrl" :href="project.liveUrl" target="_blank" class="text-zinc-900 text-[10px] font-bold tracking-widest uppercase border-b-2 border-yellow-800 pb-1 hover:text-yellow-800 transition-colors">Live Project</a>
                <a v-if="project.repositoryUrl" :href="project.repositoryUrl" target="_blank" class="text-zinc-900 text-[10px] font-bold tracking-widest uppercase border-b-2 border-yellow-800 pb-1 hover:text-yellow-800 transition-colors">Repository</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Education -->
      <section id="education" class="py-32 text-center">
        <div class="flex flex-col items-center mb-20 gap-4">
          <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif">Education</h2>
          <div class="w-24 h-1 bg-yellow-800"></div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div v-for="(edu, index) in education" :key="index" class="p-12 bg-white border border-zinc-100 flex flex-col items-center gap-6 shadow-sm">
            <div class="w-12 h-10 flex items-center justify-center">
               <span class="text-3xl text-yellow-800">🎓</span>
            </div>
            <div class="flex flex-col gap-2">
              <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">{{ edu.degree }} in {{ edu.field }}</h3>
              <span class="text-yellow-800 text-sm font-bold font-['Manrope']">{{ edu.institution }}</span>
              <span class="text-zinc-400 text-[10px] font-bold uppercase tracking-widest">{{ edu.startDate }} — {{ edu.endDate }} | {{ edu.location }}</span>
            </div>
            <p class="text-zinc-600 text-sm leading-relaxed font-['Inter']">
              {{ edu.description }}
            </p>
          </div>
        </div>
      </section>

      <!-- Certifications & Awards -->
      <section class="py-32 bg-zinc-100 -mx-6 lg:-mx-24 px-6 lg:px-24">
        <div class="flex items-center gap-8 mb-16">
          <h2 class="text-zinc-900 text-3xl font-bold font-noto-serif whitespace-nowrap">Certifications & Awards</h2>
          <div class="w-full h-px bg-zinc-200"></div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 font-['Inter']">
          <div v-for="(cert, index) in certifications" :key="'cert-'+index" class="p-8 bg-white border border-zinc-100 shadow-sm rounded flex flex-col gap-4">
            <div class="flex justify-between items-start">
              <span class="text-yellow-800 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">CERTIFICATION</span>
              <span class="text-zinc-400 text-[10px] font-bold uppercase">{{ cert.year }}</span>
            </div>
            <div>
              <p class="text-zinc-900 text-sm font-bold mb-1">{{ cert.title }}</p>
              <p class="text-zinc-500 text-[10px] uppercase tracking-wider font-bold">{{ cert.issuer }}</p>
            </div>
            <p class="text-zinc-600 text-xs leading-relaxed">{{ cert.description }}</p>
            <a v-if="cert.credentialUrl" :href="cert.credentialUrl" target="_blank" class="text-yellow-800 text-[10px] font-bold uppercase tracking-widest mt-auto">View Credential</a>
          </div>
          <div v-for="(award, index) in awards" :key="'award-'+index" class="p-8 bg-white border border-zinc-100 shadow-sm rounded flex flex-col gap-4 border-l-4 border-l-yellow-800">
            <div class="flex justify-between items-start">
              <span class="text-yellow-800 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">AWARD</span>
              <span class="text-zinc-400 text-[10px] font-bold uppercase">{{ award.year }}</span>
            </div>
            <div>
              <p class="text-zinc-900 text-sm font-bold mb-1">{{ award.title }}</p>
              <p class="text-zinc-500 text-[10px] uppercase tracking-wider font-bold">{{ award.organization }}</p>
            </div>
            <p class="text-zinc-600 text-xs leading-relaxed">{{ award.description }}</p>
          </div>
        </div>
      </section>

      <!-- Research & Writing -->
      <section id="writings" class="py-32">
        <div class="mb-16">
          <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif mb-4">Research & Writing</h2>
          <div class="w-24 h-1 bg-yellow-800"></div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="(writing, index) in writings" :key="index" class="group p-8 border border-zinc-100 hover:border-yellow-800 transition-colors flex flex-col gap-6">
            <div class="flex justify-between items-start">
              <span class="px-2 py-1 bg-zinc-100 text-zinc-500 text-[9px] font-bold uppercase rounded">{{ writing.type }}</span>
              <span class="text-zinc-400 text-[10px] font-bold uppercase">{{ writing.status }}</span>
            </div>
            <h3 class="text-zinc-900 text-lg font-bold font-noto-serif group-hover:text-yellow-800 transition-colors leading-tight">{{ writing.title }}</h3>
            <p class="text-zinc-600 text-sm leading-relaxed font-['Inter']">
              {{ writing.description }}
            </p>
            <div class="flex flex-wrap gap-2 mt-auto">
              <span v-for="tag in writing.tags" :key="tag" class="text-[9px] text-zinc-400 uppercase font-bold tracking-tighter">#{{ tag }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Vision -->
      <section class="py-32 text-center max-w-4xl mx-auto">
        <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif mb-12">Academic and Professional Vision</h2>
        <p class="text-zinc-600 text-2xl font-noto-serif leading-relaxed italic mb-8">
          "My mission is to facilitate the seamless convergence of emerging technologies within institutional frameworks, ensuring that technical innovation serves as a catalyst for educational excellence and social progress."
        </p>
        <div class="flex items-center justify-center gap-4">
          <div class="w-12 h-px bg-yellow-800"></div>
          <span class="text-zinc-900 text-xs font-bold tracking-widest uppercase font-['Manrope']">JOTHAM HERNANDEZ</span>
          <div class="w-12 h-px bg-yellow-800"></div>
        </div>
      </section>

      <!-- Contact -->
      <section id="contact" class="py-32 bg-zinc-100 -mx-6 lg:-mx-24 px-6 lg:px-24">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-20">
          <div class="flex flex-col gap-10">
            <div class="flex flex-col gap-6">
              <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif">Get in Touch</h2>
              <p class="text-zinc-600 text-lg leading-relaxed max-w-md font-['Inter']">
                {{ contact.cta }}
              </p>
            </div>
            <div class="flex flex-col gap-6 font-['Inter']">
              <div class="flex items-center gap-4 text-zinc-900" v-if="contact.email">
                <span class="text-xl text-yellow-800">✉</span>
                <a :href="'mailto:' + contact.email" class="hover:text-yellow-800 transition-colors">{{ contact.email }}</a>
              </div>
              <div class="flex items-center gap-4 text-zinc-900" v-if="contact.linkedin">
                <span class="text-xl text-yellow-800">🔗</span>
                <a :href="contact.linkedin" target="_blank" class="hover:text-yellow-800 transition-colors">LinkedIn Profile</a>
              </div>
              <div class="flex items-center gap-4 text-zinc-900" v-if="contact.location">
                <span class="text-xl text-yellow-800">📍</span>
                <span>{{ contact.location }}</span>
              </div>
            </div>
          </div>
          <div class="bg-white p-12 border border-zinc-100 shadow-sm font-['Inter']">
            <form class="flex flex-col gap-8" @submit.prevent>
              <div class="flex flex-col gap-2">
                <label class="text-zinc-500 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">NAME</label>
                <input type="text" required class="w-full bg-zinc-50 border-b border-zinc-200 py-3 focus:outline-none focus:border-black transition-colors" />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-zinc-500 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">EMAIL</label>
                <input type="email" required class="w-full bg-zinc-50 border-b border-zinc-200 py-3 focus:outline-none focus:border-black transition-colors" />
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-zinc-500 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">INQUIRY</label>
                <textarea rows="4" required class="w-full bg-zinc-50 border-b border-zinc-200 py-3 focus:outline-none focus:border-black transition-colors resize-none"></textarea>
              </div>
              <button type="submit" class="w-full py-4 bg-black text-white text-xs font-bold tracking-widest uppercase font-['Manrope'] hover:bg-zinc-800 transition-colors">SEND MESSAGE</button>
            </form>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="py-12 px-8 bg-zinc-100 border-t border-zinc-200">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="text-zinc-900 text-lg font-bold font-noto-serif">{{ profile.name }}</div>
        <div class="flex flex-wrap justify-center gap-8 text-zinc-400 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">
          <a :href="profile.linkedin" target="_blank" class="hover:text-zinc-900 transition-colors">LINKEDIN</a>
          <a :href="profile.orcid" target="_blank" class="hover:text-zinc-900 transition-colors">ORCID</a>
          <a :href="profile.googleScholar" target="_blank" class="hover:text-zinc-900 transition-colors">GOOGLE SCHOLAR</a>
          <NuxtLink to="/privacy" class="hover:text-zinc-900 transition-colors">PRIVACY POLICY</NuxtLink>
        </div>
        <div class="text-zinc-400 text-[10px] font-bold tracking-widest font-['Manrope'] uppercase">
          © {{ currentYear }} {{ profile.name }}. ALL INTELLECTUAL RIGHTS RESERVED.
        </div>
      </div>
    </footer>

    <!-- Back to Top Button -->
    <button 
      @click="scrollToTop" 
      :class="['fixed bottom-10 right-10 z-[100] w-14 h-14 bg-black text-white flex items-center justify-center shadow-2xl transition-all duration-500 hover:bg-zinc-800 focus:outline-none rounded-full', showScrollTop ? 'opacity-100 translate-y-0 pointer-events-auto' : 'opacity-0 translate-y-10 pointer-events-none']"
      aria-label="Back to Top"
    >
      <span class="text-2xl">↑</span>
    </button>
  </div>
</template>

<style scoped>
</style>
