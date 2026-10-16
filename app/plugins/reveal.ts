// v-reveal: fades/slides an element in the first time it enters the viewport.
// Optional value = delay in ms, e.g. v-reveal="120". Styles live in main.css ([data-reveal]).
// SSR renders data-reveal so there's no flash; reduced-motion users see content immediately (CSS).
import type { Directive } from 'vue'

export default defineNuxtPlugin((nuxtApp) => {
  let observer: IntersectionObserver | null = null

  const getObserver = () => {
    if (!observer) {
      observer = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-revealed')
              observer?.unobserve(entry.target)
            }
          }
        },
        { rootMargin: '0px 0px -10% 0px', threshold: 0.08 }
      )
    }
    return observer
  }

  const reveal: Directive<HTMLElement, number | undefined> = {
    getSSRProps(binding) {
      return {
        'data-reveal': '',
        style: binding.value ? `--reveal-delay:${binding.value}ms` : undefined
      }
    },
    mounted(el, binding) {
      el.setAttribute('data-reveal', '')
      if (binding.value) el.style.setProperty('--reveal-delay', `${binding.value}ms`)
      getObserver().observe(el)
    },
    unmounted(el) {
      observer?.unobserve(el)
    }
  }

  nuxtApp.vueApp.directive('reveal', reveal)
})
