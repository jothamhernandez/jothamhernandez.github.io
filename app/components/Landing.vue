<script setup lang="ts">
import { onMounted } from 'vue'
import Lenis from 'lenis'

onMounted(() => {
  const lenis = new Lenis()

  function raf(time: number) {
    lenis.raf(time)
    requestAnimationFrame(raf)
  }

  requestAnimationFrame(raf)

  // Handle anchor link clicks for smooth scrolling
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e: Event) => {
      e.preventDefault()
      const targetId = (anchor as HTMLAnchorElement).getAttribute('href')
      if (targetId && targetId !== '#') {
        lenis.scrollTo(targetId)
      }
    })
  })
})
</script>

<template>
  <div class="w-full bg-white font-['Inter']">
    <!-- Navigation -->
    <nav class="sticky top-0 z-50 w-full px-8 py-4 bg-white/80 backdrop-blur-md border-b border-gray-100 flex justify-between items-center">
      <div class="text-zinc-900 text-xl font-bold font-noto-serif">Jotham Hernandez</div>
      <div class="hidden md:flex gap-8 items-center font-noto-serif">
        <a href="#research" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Research</a>
        <a href="#expertise" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Expertise</a>
        <a href="#teaching" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Teaching</a>
        <a href="#projects" class="text-zinc-500 text-sm font-semibold hover:text-zinc-900 transition-colors">Projects</a>
      </div>
<!--      <button class="px-6 py-2 bg-black text-white text-xs font-bold tracking-widest uppercase rounded font-['Manrope']">CONTACT</button>-->
    </nav>

    <main class="max-w-7xl mx-auto px-6 lg:px-24">
      <!-- Hero Section -->
      <section class="relative min-h-[80vh] flex items-center py-24 overflow-hidden">
        <div class="w-full grid grid-cols-1 lg:grid-cols-2 items-center gap-12">
          <div class="flex flex-col gap-6 z-10">
            <span class="text-yellow-800 text-sm font-bold tracking-[0.3em] uppercase font-['Manrope']">PORTFOLIO & ACADEMIC RECORD</span>
            <h1 class="text-zinc-900 text-6xl lg:text-7xl font-bold font-noto-serif leading-[1.1]">
              Jotham Hernandez
            </h1>
            <p class="text-zinc-600 text-2xl lg:text-3xl font-normal font-noto-serif leading-relaxed max-w-2xl">
              Technology Professional, Lecturer, and Emerging Researcher in ICT Convergence.
            </p>
            <div class="flex gap-4 pt-4">
              <a href="#projects" class="px-8 py-4 bg-black text-white text-xs font-bold tracking-widest uppercase font-['Manrope'] inline-block">VIEW WORK</a>
              <a href="#research" class="px-8 py-4 border border-zinc-200 text-zinc-900 text-xs font-bold tracking-widest uppercase font-['Manrope'] hover:bg-zinc-50 transition-colors inline-block">RESEARCH PROFILE</a>
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
        <div class="lg:col-span-4 aspect-[4/5] bg-zinc-200 overflow-hidden rounded-sm grayscale">
          <img src="https://placehold.co/800x1000" alt="Profile" class="w-full h-full object-cover opacity-90" />
        </div>
        <div class="lg:col-span-8 flex flex-col gap-8">
          <h2 class="text-zinc-900 text-3xl lg:text-4xl font-bold font-noto-serif leading-tight">
            Synthesizing Practical Systems with Institutional Knowledge
          </h2>
          <div class="flex flex-col gap-6 text-zinc-600 text-lg leading-relaxed font-['Inter']">
            <p>
              As an IT professional and former lecturer, my career has been defined by the intersection of rigorous technical implementation and academic inquiry. I bridge the gap between building resilient digital infrastructures and the theoretical frameworks that govern them.
            </p>
            <p>
              With a foundation in diverse technologies and a passion for ICT convergence, I am transitioning toward a focused research trajectory. My goal is to advance how institutions leverage emerging technologies to create sustainable, human-centered ecosystems.
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
          <div class="p-10 bg-white border border-zinc-100 shadow-sm flex flex-col gap-6">
            <div class="w-10 h-10 flex items-center justify-center text-yellow-800">
              <span class="text-2xl">☀</span>
            </div>
            <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">ICT Convergence</h3>
            <p class="text-zinc-600 text-sm leading-relaxed">
              Exploring the integration of disparate information and communication technologies into cohesive, intelligent systems.
            </p>
          </div>
          <div class="p-10 bg-white border border-zinc-100 shadow-sm flex flex-col gap-6">
            <div class="w-10 h-10 flex items-center justify-center text-yellow-800">
              <span class="text-2xl">📍</span>
            </div>
            <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">Human-Centered AI & Web Systems</h3>
            <p class="text-zinc-600 text-sm leading-relaxed">
              Investigating how artificial intelligence can be ethically integrated into web architectures to enhance user agency and accessibility across institutional platforms.
            </p>
          </div>
          <div class="p-10 bg-white border border-zinc-100 shadow-sm flex flex-col gap-6">
            <div class="w-10 h-10 flex items-center justify-center text-yellow-800">
              <span class="text-2xl">☁</span>
            </div>
            <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">Cloud Infrastructure & EdTech</h3>
            <p class="text-zinc-600 text-sm leading-relaxed">
              Researching scalable cloud-native frameworks designed specifically for educational delivery and large-scale academic resource management.
            </p>
          </div>
          <div class="p-10 bg-white border border-zinc-100 shadow-sm flex flex-col gap-6">
            <div class="w-10 h-10 flex items-center justify-center text-yellow-800">
              <span class="text-2xl">🌴</span>
            </div>
            <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">Network Resilience</h3>
            <p class="text-zinc-600 text-sm leading-relaxed">
              Studies on autonomous network healing and adaptive infrastructure for mission-critical institutional operations.
            </p>
          </div>
        </div>
      </section>
    </main>

    <!-- Core Expertise -->
    <section id="expertise" class="bg-black py-32 text-white">
      <div class="max-w-7xl mx-auto px-6 lg:px-24">
        <div class="mb-20">
          <h2 class="text-4xl font-bold font-noto-serif mb-4">Core Expertise</h2>
          <span class="text-zinc-500 text-xs font-medium tracking-widest uppercase font-['Manrope']">TECHNICAL COMPETENCIES & PROFESSIONAL DOMAINS</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 lg:gap-x-16 lg:gap-y-20">
          <div class="pl-6 border-l-2 border-orange-200 flex flex-col gap-4">
            <h3 class="text-xl font-bold font-noto-serif">Web Development</h3>
            <p class="text-zinc-500 text-sm leading-relaxed font-['Inter']">
              Full-stack architecture with focus on Vue, PHP, Python, and secure API integration for enterprise-level applications.
            </p>
          </div>
          <div class="pl-6 border-l-2 border-orange-200 flex flex-col gap-4">
            <h3 class="text-xl font-bold font-noto-serif">Cloud & SysAdmin</h3>
            <p class="text-zinc-500 text-sm leading-relaxed font-['Inter']">
              Management of AWS/Azure environments, containerization (Docker/K8s), and automated CI/CD pipelines.
            </p>
          </div>
          <div class="pl-6 border-l-2 border-orange-200 flex flex-col gap-4">
            <h3 class="text-xl font-bold font-noto-serif">Network Infrastructure</h3>
            <p class="text-zinc-500 text-sm leading-relaxed font-['Inter']">
              Design and optimization of campus-wide LAN/WAN architectures and cybersecurity protocols.
            </p>
          </div>
          <div class="pl-6 border-l-2 border-orange-200 flex flex-col gap-4">
            <h3 class="text-xl font-bold font-noto-serif">API Architecture</h3>
            <p class="text-zinc-500 text-sm leading-relaxed font-['Inter']">
              Developing RESTful and GraphQL interfaces for high-concurrency data exchange between legacy and modern systems.
            </p>
          </div>
          <div class="pl-6 border-l-2 border-orange-200 flex flex-col gap-4">
            <h3 class="text-xl font-bold font-noto-serif">Tech Documentation</h3>
            <p class="text-zinc-500 text-sm leading-relaxed font-['Inter']">
              Crafting meticulous technical specifications, white papers, and instructional manuals for complex software ecosystems.
            </p>
          </div>
          <div class="pl-6 border-l-2 border-orange-200 flex flex-col gap-4">
            <h3 class="text-xl font-bold font-noto-serif">Academic Instruction</h3>
            <p class="text-zinc-500 text-sm leading-relaxed font-['Inter']">
              Curriculum development and classroom leadership in Computer Science fundamentals and advanced ICT topics.
            </p>
          </div>
        </div>
      </div>
    </section>

    <main class="max-w-7xl mx-auto px-6 lg:px-24">
      <!-- Teaching Experience -->
      <section id="teaching" class="py-32 bg-zinc-100 -mx-6 lg:-mx-24 px-6 lg:px-24">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-16">
          <div class="lg:col-span-4 flex flex-col gap-6">
            <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif leading-tight">Teaching Experience</h2>
            <p class="text-zinc-600 text-base leading-relaxed font-['Inter']">
              During my tenure as a lecturer, I focused on making complex computational concepts accessible through practical, project-based learning. My pedagogy emphasizes the "why" behind the code.
            </p>
          </div>
          <div class="lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-y-12 gap-x-16">
            <div class="flex flex-col gap-3">
              <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">Database Systems</h3>
              <span class="text-yellow-800 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">CORE INSTRUCTION</span>
              <p class="text-zinc-600 text-sm leading-relaxed font-['Inter']">Modeling, SQL optimization, and NoSQL architectures for enterprise scale.</p>
            </div>
            <div class="flex flex-col gap-3">
              <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">Programming Logic</h3>
              <span class="text-yellow-800 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">FOUNDATIONAL INSTRUCTION</span>
              <p class="text-zinc-600 text-sm leading-relaxed font-['Inter']">Algorithmic thinking and problem solving using C++, Java, and Python.</p>
            </div>
            <div class="flex flex-col gap-3">
              <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">Data Structures</h3>
              <span class="text-yellow-800 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">CORE INSTRUCTION</span>
              <p class="text-zinc-600 text-sm leading-relaxed font-['Inter']">Analysis of linear and non-linear structures for efficient computation.</p>
            </div>
            <div class="flex flex-col gap-3">
              <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">Operating Systems</h3>
              <span class="text-yellow-800 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">ADVANCED INSTRUCTION</span>
              <p class="text-zinc-600 text-sm leading-relaxed font-['Inter']">Process management, memory allocation, and kernel architectures.</p>
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
            A selection of institutional infrastructure projects and technical implementations developed for academic and corporate environments.
          </p>
        </div>

        <div class="flex flex-col gap-32">
          <!-- Project 1 -->
          <div class="relative group">
            <div class="w-full lg:w-3/4 aspect-video bg-zinc-100 overflow-hidden rounded-sm">
              <img src="https://placehold.co/1200x800" alt="ICT Infrastructure" class="w-full h-full object-cover opacity-80" />
            </div>
            <div class="lg:absolute right-0 top-1/2 lg:-translate-y-1/2 w-full lg:w-[500px] p-10 bg-white border border-zinc-100 shadow-xl lg:mt-0 mt-8">
              <span class="text-yellow-800 text-[10px] font-bold tracking-[0.2em] uppercase font-['Manrope']">INSTITUTIONAL SYSTEMS</span>
              <h3 class="text-zinc-900 text-2xl font-bold font-noto-serif mt-4 mb-4">Institutional ICT Infrastructure Migration</h3>
              <p class="text-zinc-600 text-sm leading-relaxed mb-8 font-['Inter']">
                Led the comprehensive overhaul and migration of campus-wide network services to a hybrid cloud architecture, improving uptime by 40% and enhancing security protocols for 5,000+ active users.
              </p>
              <div class="flex gap-2 font-['Manrope']">
                <span class="px-3 py-1 bg-orange-100 text-yellow-800 text-[10px] font-bold uppercase rounded-full">AWS</span>
                <span class="px-3 py-1 bg-orange-100 text-yellow-800 text-[10px] font-bold uppercase rounded-full">CISCO</span>
                <span class="px-3 py-1 bg-orange-100 text-yellow-800 text-[10px] font-bold uppercase rounded-full">DOCKER</span>
              </div>
            </div>
          </div>

          <!-- Project 2 -->
          <div class="relative group flex flex-col lg:items-end">
            <div class="w-full lg:w-3/4 aspect-video bg-zinc-100 overflow-hidden rounded-sm">
              <img src="https://placehold.co/1200x800" alt="Monitoring Platform" class="w-full h-full object-cover opacity-80" />
            </div>
            <div class="lg:absolute left-0 top-1/2 lg:-translate-y-1/2 w-full lg:w-[500px] p-10 bg-white border border-zinc-100 shadow-xl lg:mt-0 mt-8">
              <span class="text-yellow-800 text-[10px] font-bold tracking-[0.2em] uppercase font-['Manrope']">CLOUD OPTIMIZATION</span>
              <h3 class="text-zinc-900 text-2xl font-bold font-noto-serif mt-4 mb-4">Internal Service Monitoring Platform</h3>
              <p class="text-zinc-600 text-sm leading-relaxed mb-8 font-['Inter']">
                Developed a bespoke dashboard for real-time monitoring of institutional digital assets. Built with a focus on data visualization and proactive threat detection using machine learning heuristics.
              </p>
              <div class="flex gap-2 font-['Manrope']">
                <span class="px-3 py-1 bg-orange-100 text-yellow-800 text-[10px] font-bold uppercase rounded-full">REACT</span>
                <span class="px-3 py-1 bg-orange-100 text-yellow-800 text-[10px] font-bold uppercase rounded-full">PYTHON</span>
                <span class="px-3 py-1 bg-orange-100 text-yellow-800 text-[10px] font-bold uppercase rounded-full">GRAFANA</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Education -->
      <section class="py-32 text-center">
        <div class="flex flex-col items-center mb-20 gap-4">
          <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif">Education</h2>
          <div class="w-24 h-1 bg-yellow-800"></div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="p-12 bg-white border border-zinc-100 flex flex-col items-center gap-6 shadow-sm">
            <div class="w-12 h-10 flex items-center justify-center">
               <span class="text-3xl text-yellow-800">🎓</span>
            </div>
            <div class="flex flex-col gap-2">
              <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">Master of Science in ICT Convergence</h3>
              <span class="text-yellow-800 text-sm font-bold font-['Manrope']">Handong Global University</span>
            </div>
            <p class="text-zinc-600 text-sm leading-relaxed font-['Inter']">
              Advanced research focusing on the synthesis of information technology and industrial application.
            </p>
          </div>
          <div class="p-12 bg-white border border-zinc-100 flex flex-col items-center gap-6 shadow-sm">
            <div class="w-12 h-10 flex items-center justify-center">
              <span class="text-3xl text-yellow-800">🎖</span>
            </div>
            <div class="flex flex-col gap-2">
              <h3 class="text-zinc-900 text-xl font-bold font-noto-serif">Bachelor of Science in Information Technology</h3>
              <span class="text-yellow-800 text-sm font-bold font-['Manrope']">Informatics International College</span>
            </div>
            <p class="text-zinc-600 text-sm leading-relaxed font-['Inter']">
              Comprehensive study of computer systems, software engineering, and network management.
            </p>
          </div>
        </div>
      </section>

      <!-- Certifications -->
      <section class="py-32 bg-zinc-100 -mx-6 lg:-mx-24 px-6 lg:px-24">
        <div class="flex items-center gap-8 mb-16">
          <h2 class="text-zinc-900 text-3xl font-bold font-noto-serif whitespace-nowrap">Certifications & Awards</h2>
          <div class="w-full h-px bg-zinc-200"></div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 font-['Inter']">
          <div class="p-8 bg-white text-center border border-zinc-100 shadow-sm rounded flex flex-col gap-2">
            <span class="text-yellow-800 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">CERTIFICATION</span>
            <p class="text-zinc-900 text-sm font-bold">AWS Certified Solutions Architect</p>
          </div>
          <div class="p-8 bg-white text-center border border-zinc-100 shadow-sm rounded flex flex-col gap-2">
            <span class="text-yellow-800 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">AWARD</span>
            <p class="text-zinc-900 text-sm font-bold">Gold Medalist: National Web Design</p>
          </div>
          <div class="p-8 bg-white text-center border border-zinc-100 shadow-sm rounded flex flex-col gap-2">
            <span class="text-yellow-800 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">CERTIFICATION</span>
            <p class="text-zinc-900 text-sm font-bold">Python Data Science Specialization</p>
          </div>
          <div class="p-8 bg-white text-center border border-zinc-100 shadow-sm rounded flex flex-col gap-2">
            <span class="text-yellow-800 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">HACKATHON</span>
            <p class="text-zinc-900 text-sm font-bold">Top 10 Finalist: Unity Game Jam</p>
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
      <section class="py-32 bg-zinc-100 -mx-6 lg:-mx-24 px-6 lg:px-24">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-20">
          <div class="flex flex-col gap-10">
            <div class="flex flex-col gap-6">
              <h2 class="text-zinc-900 text-4xl font-bold font-noto-serif">Get in Touch</h2>
              <p class="text-zinc-600 text-lg leading-relaxed max-w-md font-['Inter']">
                Open to research collaborations, speaking engagements, and consulting on institutional ICT transformation.
              </p>
            </div>
            <div class="flex flex-col gap-6 font-['Inter']">
              <div class="flex items-center gap-4 text-zinc-900">
                <span class="text-xl text-yellow-800">✉</span>
                <span>jotham_hernandez@hotmail.com</span>
              </div>
              <div class="flex items-center gap-4 text-zinc-900">
                <span class="text-xl text-yellow-800">🔗</span>
                <span>linkedin.com/in/jothamhernandez</span>
              </div>
            </div>
          </div>
<!--          <div class="bg-white p-12 border border-zinc-100 shadow-sm font-['Inter']">-->
<!--            <form class="flex flex-col gap-8">-->
<!--              <div class="flex flex-col gap-2">-->
<!--                <label class="text-zinc-500 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">NAME</label>-->
<!--                <input type="text" class="w-full bg-zinc-50 border-b border-zinc-200 py-3 focus:outline-none focus:border-black transition-colors" />-->
<!--              </div>-->
<!--              <div class="flex flex-col gap-2">-->
<!--                <label class="text-zinc-500 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">EMAIL</label>-->
<!--                <input type="email" class="w-full bg-zinc-50 border-b border-zinc-200 py-3 focus:outline-none focus:border-black transition-colors" />-->
<!--              </div>-->
<!--              <div class="flex flex-col gap-2">-->
<!--                <label class="text-zinc-500 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">INQUIRY</label>-->
<!--                <textarea rows="4" class="w-full bg-zinc-50 border-b border-zinc-200 py-3 focus:outline-none focus:border-black transition-colors resize-none"></textarea>-->
<!--              </div>-->
<!--              <button class="w-full py-4 bg-black text-white text-xs font-bold tracking-widest uppercase font-['Manrope']">SEND MESSAGE</button>-->
<!--            </form>-->
<!--          </div>-->
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="py-12 px-8 bg-zinc-100 border-t border-zinc-200">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="text-zinc-900 text-lg font-bold font-noto-serif">Jotham Hernandez</div>
        <div class="flex flex-wrap justify-center gap-8 text-zinc-400 text-[10px] font-bold tracking-widest uppercase font-['Manrope']">
<!--          <a href="#" class="hover:text-zinc-900 transition-colors">CURRICULUM VITAE</a>-->
          <a href="https://www.linkedin.com/in/jothamhernandez" class="hover:text-zinc-900 transition-colors">LINKEDIN</a>
          <a href="https://orcid.org/0009-0007-4090-6332" target="_blank" class="hover:text-zinc-900 transition-colors">ORCID</a>
          <a href="https://scholar.google.com/citations?hl=en&user=lfh7S-UAAAAJ" class="hover:text-zinc-900 transition-colors">GOOGLE SCHOLAR</a>
        </div>
        <div class="text-zinc-400 text-[10px] font-bold tracking-widest font-['Manrope']">
          © 2024 JOTHAM HERNANDEZ. ALL INTELLECTUAL RIGHTS RESERVED.
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>

</style>