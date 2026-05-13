<script setup lang="ts">

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
    <NuxtPage />
  </div>
</template>
