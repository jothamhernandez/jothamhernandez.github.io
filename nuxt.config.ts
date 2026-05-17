import tailwindcss from '@tailwindcss/vite'
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  site: {
    url: 'https://jothamhernandez.com', // Replace with your actual domain if different
    name: 'Jotham Hernandez Portfolio'
  },
  modules: ['@nuxtjs/sitemap'],
  app: {
    head: {
      link: [{ rel: 'icon', type: 'image/png', href: '/favicon.png' }]
    }
  },
  css: ['./app/assets/css/main.css'],
  vite: {
    plugins: [
      tailwindcss(),
    ]
  }
})
