<script setup lang="ts">
import profile from '../data/profile.json'
import about from '../data/about.json'
import experience from '../data/experience.json'
import education from '../data/education.json'
import skills from '../data/skills.json'
import certifications from '../data/certifications.json'
import awards from '../data/awards.json'
import publications from '../data/publications.json'
import contact from '../data/contact.json'

useHead({
  title: `${profile.name} — Curriculum Vitae`,
  meta: [
    { name: 'description', content: `Curriculum Vitae of ${profile.name}.` },
    // A CV page shouldn't compete with the homepage in search results.
    { name: 'robots', content: 'noindex, follow' }
  ]
})

const print = () => {
  if (import.meta.client) window.print()
}
</script>

<template>
  <div class="min-h-screen bg-zinc-100 print:bg-white font-['Inter'] text-zinc-800">
    <!-- Action bar (hidden when printing) -->
    <div class="print:hidden sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-zinc-200">
      <div class="max-w-3xl mx-auto px-6 py-3 flex justify-between items-center">
        <NuxtLink to="/" class="text-zinc-500 text-[11px] font-bold tracking-widest uppercase font-['Manrope'] hover:text-yellow-800 transition-colors">← Back to site</NuxtLink>
        <button @click="print" class="px-5 py-2 bg-black text-white text-[11px] font-bold tracking-widest uppercase font-['Manrope'] hover:bg-zinc-800 transition-colors rounded-sm">Print / Save as PDF</button>
      </div>
    </div>

    <article class="max-w-3xl mx-auto bg-white print:max-w-none shadow-sm print:shadow-none my-8 print:my-0 p-10 sm:p-14 print:p-0">
      <!-- Header -->
      <header class="border-b-2 border-zinc-900 pb-6 mb-8">
        <h1 class="text-zinc-900 text-4xl font-bold font-noto-serif">{{ profile.name }}</h1>
        <p class="text-yellow-800 text-sm font-bold font-['Manrope'] mt-2">{{ profile.title }}</p>
        <div class="flex flex-wrap gap-x-5 gap-y-1 mt-4 text-[11px] text-zinc-500 font-['Manrope']">
          <a v-if="contact.email" :href="'mailto:' + contact.email" class="hover:text-yellow-800">{{ contact.email }}</a>
          <span v-if="profile.location">{{ profile.location }}</span>
          <a :href="profile.linkedin" target="_blank" rel="noopener" class="hover:text-yellow-800">LinkedIn</a>
          <a :href="profile.orcid" target="_blank" rel="noopener" class="hover:text-yellow-800">ORCID</a>
          <a :href="profile.googleScholar" target="_blank" rel="noopener" class="hover:text-yellow-800">Google Scholar</a>
        </div>
      </header>

      <!-- Profile summary -->
      <section class="mb-8 break-inside-avoid">
        <h2 class="text-zinc-900 text-xs font-bold tracking-[0.2em] uppercase font-['Manrope'] mb-3 border-b border-zinc-200 pb-1">Profile</h2>
        <p class="text-sm leading-relaxed text-zinc-600">{{ about.paragraphs[0] }}</p>
      </section>

      <!-- Experience -->
      <section class="mb-8">
        <h2 class="text-zinc-900 text-xs font-bold tracking-[0.2em] uppercase font-['Manrope'] mb-4 border-b border-zinc-200 pb-1">Professional Experience</h2>
        <div class="flex flex-col gap-5">
          <div v-for="(job, index) in experience" :key="index" class="break-inside-avoid">
            <div class="flex justify-between items-baseline gap-4">
              <h3 class="text-zinc-900 text-base font-bold font-noto-serif">{{ job.role }}</h3>
              <span class="text-zinc-400 text-[10px] font-bold uppercase tracking-widest whitespace-nowrap font-['Manrope']">{{ job.startDate }} — {{ job.endDate }}</span>
            </div>
            <p class="text-yellow-800 text-xs font-bold font-['Manrope']">{{ job.organization }} · {{ job.location }}</p>
            <ul class="list-disc list-outside ml-4 mt-2 flex flex-col gap-1">
              <li v-for="highlight in job.highlights" :key="highlight" class="text-xs leading-relaxed text-zinc-600">{{ highlight }}</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Education -->
      <section class="mb-8 break-inside-avoid">
        <h2 class="text-zinc-900 text-xs font-bold tracking-[0.2em] uppercase font-['Manrope'] mb-4 border-b border-zinc-200 pb-1">Education</h2>
        <div class="flex flex-col gap-4">
          <div v-for="(edu, index) in education" :key="index">
            <div class="flex justify-between items-baseline gap-4">
              <h3 class="text-zinc-900 text-base font-bold font-noto-serif">{{ edu.degree }} in {{ edu.field }}</h3>
              <span class="text-zinc-400 text-[10px] font-bold uppercase tracking-widest whitespace-nowrap font-['Manrope']">{{ edu.startDate }} — {{ edu.endDate }}</span>
            </div>
            <p class="text-yellow-800 text-xs font-bold font-['Manrope']">{{ edu.institution }} · {{ edu.location }}</p>
          </div>
        </div>
      </section>

      <!-- Publications -->
      <section class="mb-8 break-inside-avoid">
        <h2 class="text-zinc-900 text-xs font-bold tracking-[0.2em] uppercase font-['Manrope'] mb-4 border-b border-zinc-200 pb-1">Publications & Research Writing</h2>
        <ul class="flex flex-col gap-3">
          <li v-for="(pub, index) in publications" :key="index" class="text-xs leading-relaxed text-zinc-600">
            <span class="text-zinc-900 font-bold">{{ pub.authors }}</span> ({{ pub.year }}). <span class="italic">{{ pub.title }}.</span> {{ pub.venue }}. <span class="text-zinc-400 uppercase tracking-widest text-[9px] font-bold">{{ pub.status }}</span>
          </li>
        </ul>
      </section>

      <!-- Skills -->
      <section class="mb-8 break-inside-avoid">
        <h2 class="text-zinc-900 text-xs font-bold tracking-[0.2em] uppercase font-['Manrope'] mb-4 border-b border-zinc-200 pb-1">Technical Expertise</h2>
        <div class="flex flex-col gap-2">
          <div v-for="group in skills" :key="group.id" class="text-xs leading-relaxed">
            <span class="text-zinc-900 font-bold">{{ group.category }}:</span>
            <span class="text-zinc-600"> {{ group.skills.join(', ') }}</span>
          </div>
        </div>
      </section>

      <!-- Certifications & Awards -->
      <section class="break-inside-avoid">
        <h2 class="text-zinc-900 text-xs font-bold tracking-[0.2em] uppercase font-['Manrope'] mb-4 border-b border-zinc-200 pb-1">Certifications & Awards</h2>
        <ul class="flex flex-col gap-1.5">
          <li v-for="(cert, index) in certifications" :key="'c'+index" class="text-xs leading-relaxed text-zinc-600">
            <span class="text-zinc-900 font-bold">{{ cert.title }}</span> — {{ cert.issuer }} <template v-if="cert.category !== 'recognition'">({{ cert.issued.slice(0, 4) }})</template><a v-if="cert.credentialUrl" :href="cert.credentialUrl" class="text-yellow-800 print:text-zinc-500"> · verify</a>
          </li>
          <li v-for="(award, index) in awards" :key="'a'+index" class="text-xs leading-relaxed text-zinc-600">
            <span class="text-zinc-900 font-bold">{{ award.title }}</span> — {{ award.organization }} ({{ award.year }})
          </li>
        </ul>
      </section>
    </article>
  </div>
</template>

<style scoped>
@media print {
  @page {
    margin: 1.6cm;
  }
}
</style>
