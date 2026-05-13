<script setup lang="ts">
import profile from '../data/profile.json'

const currentYear = new Date().getFullYear()

useHead({
  title: `Privacy Policy | ${profile.name}`,
  meta: [
    { name: 'description', content: `Privacy Policy for ${profile.name}'s portfolio website.` }
  ]
})
</script>

<template>
  <div class="w-full bg-white font-['Inter'] min-h-screen flex flex-col">
    <!-- Navigation -->
    <nav class="sticky top-0 z-50 w-full px-8 py-4 bg-white/80 backdrop-blur-md border-b border-gray-100 flex justify-between items-center">
      <NuxtLink to="/" class="text-zinc-900 text-xl font-bold font-noto-serif hover:text-yellow-800 transition-colors">{{ profile.name }}</NuxtLink>
      <NuxtLink to="/" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors font-noto-serif">Back to Home</NuxtLink>
    </nav>

    <main class="max-w-4xl mx-auto px-6 py-24 flex-grow">
      <h1 class="text-zinc-900 text-5xl font-bold font-noto-serif mb-12">Privacy Policy</h1>
      
      <div class="prose prose-zinc lg:prose-lg max-w-none text-zinc-600 leading-relaxed space-y-8 font-['Inter']">
        <section>
          <h2 class="text-zinc-900 text-2xl font-bold font-noto-serif mb-4">Introduction</h2>
          <p>
            Your privacy is important to me. This Privacy Policy explains how I collect, use, and protect any information you provide when using this website.
          </p>
        </section>

        <section>
          <h2 class="text-zinc-900 text-2xl font-bold font-noto-serif mb-4">Information Collection</h2>
          <p>
            I only collect information that you voluntarily provide through the contact form, such as your name, email address, and the content of your inquiry. This website also uses Google Analytics to collect anonymous traffic data to help me understand how visitors use the site.
          </p>
        </section>

        <section>
          <h2 class="text-zinc-900 text-2xl font-bold font-noto-serif mb-4">Use of Information</h2>
          <p>
            Any personal information you provide is used solely to respond to your inquiries or to provide the services you requested. I do not sell, rent, or lease my contact lists to third parties.
          </p>
        </section>

        <section>
          <h2 class="text-zinc-900 text-2xl font-bold font-noto-serif mb-4">Cookies</h2>
          <p>
            This website uses cookies (small text files placed on your device) to help provide a better user experience. You can choose to disable cookies in your browser settings, although this may affect how you interact with this and other websites.
          </p>
        </section>

        <section>
          <h2 class="text-zinc-900 text-2xl font-bold font-noto-serif mb-4">Security</h2>
          <p>
            I am committed to ensuring that your information is secure. In order to prevent unauthorized access or disclosure, I have put in place suitable physical, electronic, and managerial procedures to safeguard and secure the information collected online.
          </p>
        </section>

        <section>
          <h2 class="text-zinc-900 text-2xl font-bold font-noto-serif mb-4">Contact Me</h2>
          <p>
            If you have any questions about this Privacy Policy, please contact me through the form on the main page.
          </p>
        </section>
      </div>
    </main>

    <!-- Footer -->
    <footer class="py-12 px-8 bg-zinc-100 border-t border-zinc-200">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="text-zinc-900 text-lg font-bold font-noto-serif">{{ profile.name }}</div>
        <div class="flex flex-wrap justify-center gap-8 text-zinc-400 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">
          <a :href="profile.linkedin" target="_blank" class="hover:text-zinc-900 transition-colors">LINKEDIN</a>
          <a :href="profile.orcid" target="_blank" class="hover:text-zinc-900 transition-colors">ORCID</a>
          <a :href="profile.googleScholar" target="_blank" class="hover:text-zinc-900 transition-colors">GOOGLE SCHOLAR</a>
          <NuxtLink to="/" class="hover:text-zinc-900 transition-colors">HOME</NuxtLink>
        </div>
        <div class="text-zinc-400 text-[10px] font-bold tracking-widest font-['Manrope'] uppercase">
          © {{ currentYear }} {{ profile.name }}. ALL INTELLECTUAL RIGHTS RESERVED.
        </div>
      </div>
    </footer>
  </div>
</template>
