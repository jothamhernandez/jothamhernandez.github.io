<script setup lang="ts">
import Landing from './components/Landing.vue'

useHead({
  script: [
    {
      src: 'https://www.googletagmanager.com/gtag/js?id=G-LMPTJSNQ9T',
      async: true
    },
    {
      innerHTML: `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-LMPTJSNQ9T');
      `,
      type: 'text/javascript'
    }
  ]
})
</script>

<template>
  <div>
    <NuxtRouteAnnouncer />
    <Landing />
<!--    <NuxtWelcome />-->
  </div>
</template>
