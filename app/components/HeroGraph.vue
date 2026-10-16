<script setup lang="ts">
// The hero's signature piece: a live force-directed knowledge graph of Jotham's
// research areas, organizations, and skills (built from app/data in index.vue).
// Canvas-only, ~50 nodes, pauses offscreen, static under prefers-reduced-motion.
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'

export type GraphNode = { id: string; label: string; kind: 'core' | 'topic' | 'org' | 'skill' }
export type GraphLink = { source: string; target: string }

const props = defineProps<{
  nodes: GraphNode[]
  links: GraphLink[]
  /** Bump this number to fire a burst of retrieval pulses out of the core node. */
  burst?: number
  /** Draw node labels (desktop only). Off when the graph is purely ambient. */
  labels?: boolean
  /** Horizontal anchor of the graph on desktop, as a fraction of the width. */
  anchorX?: number
}>()

const canvas = ref<HTMLCanvasElement | null>(null)

type SimNode = GraphNode & { x: number; y: number; vx: number; vy: number; r: number; fixed: boolean; neighbors: Set<string>; phase: number }
type SimLink = { a: SimNode; b: SimNode; rest: number }
type Pulse = { link: SimLink; t: number; speed: number; forward: boolean; strong: boolean }

const STYLE = {
  core: { r: 11, fill: '#c9a96a' },
  topic: { r: 6.5, fill: '#c9a96a' },
  org: { r: 5, fill: '#f7f5f0' },
  skill: { r: 2.6, fill: '#5b6b82' }
} as const

let ctx: CanvasRenderingContext2D | null = null
let width = 0
let height = 0
let dpr = 1
let raf = 0
let running = false
let visible = true
let reduced = false
let nodes: SimNode[] = []
let links: SimLink[] = []
let pulses: Pulse[] = []
let byId = new Map<string, SimNode>()
let hovered: SimNode | null = null
let dragging: SimNode | null = null
let pointer = { x: -9999, y: -9999, active: false }
let lastPulse = 0
let io: IntersectionObserver | null = null
let ro: ResizeObserver | null = null

const center = () => {
  // Desktop: graph sits to the right of the headline. Mobile: centered behind it.
  const wide = width >= 1024
  return { x: wide ? width * (props.anchorX ?? 0.68) : width * 0.62, y: wide ? height * 0.5 : height * 0.3 }
}
const scale = () => Math.max(0.55, Math.min(1.25, Math.min(width, height) / 720))

function build() {
  const c = center()
  const s = scale()
  byId = new Map()
  nodes = props.nodes.map((n, i) => {
    const angle = (i / props.nodes.length) * Math.PI * 2
    const dist = n.kind === 'core' ? 0 : n.kind === 'topic' ? 160 * s : n.kind === 'org' ? 230 * s : 300 * s
    const node: SimNode = {
      ...n,
      x: c.x + Math.cos(angle) * dist + (Math.random() - 0.5) * 20,
      y: c.y + Math.sin(angle) * dist + (Math.random() - 0.5) * 20,
      vx: 0,
      vy: 0,
      r: STYLE[n.kind].r,
      fixed: false,
      neighbors: new Set(),
      phase: Math.random() * Math.PI * 2
    }
    byId.set(n.id, node)
    return node
  })
  links = []
  for (const l of props.links) {
    const a = byId.get(l.source)
    const b = byId.get(l.target)
    if (!a || !b) continue
    a.neighbors.add(b.id)
    b.neighbors.add(a.id)
    const rest = (a.kind === 'core' || b.kind === 'core' ? 150 : a.kind === 'skill' || b.kind === 'skill' ? 62 : 120) * s
    links.push({ a, b, rest })
  }
}

function tick(time: number) {
  const c = center()
  const s = scale()
  // repulsion
  for (let i = 0; i < nodes.length; i++) {
    const a = nodes[i]!
    for (let j = i + 1; j < nodes.length; j++) {
      const b = nodes[j]!
      let dx = b.x - a.x
      let dy = b.y - a.y
      let d2 = dx * dx + dy * dy
      if (d2 < 0.01) { dx = Math.random(); dy = Math.random(); d2 = 1 }
      if (d2 > 90000 * s * s) continue
      const f = (1400 * s) / d2
      const d = Math.sqrt(d2)
      const fx = (dx / d) * f
      const fy = (dy / d) * f
      a.vx -= fx; a.vy -= fy
      b.vx += fx; b.vy += fy
    }
  }
  // springs
  for (const l of links) {
    const dx = l.b.x - l.a.x
    const dy = l.b.y - l.a.y
    const d = Math.sqrt(dx * dx + dy * dy) || 1
    const f = (d - l.rest) * 0.012
    const fx = (dx / d) * f
    const fy = (dy / d) * f
    l.a.vx += fx; l.a.vy += fy
    l.b.vx -= fx; l.b.vy -= fy
  }
  const t = time / 1000
  for (const n of nodes) {
    // gravity toward the anchor (stronger for the core so the graph stays put)
    const g = n.kind === 'core' ? 0.02 : 0.0025
    n.vx += (c.x - n.x) * g
    n.vy += (c.y - n.y) * g
    // gentle breathing drift
    if (!reduced) {
      n.vx += Math.cos(t * 0.6 + n.phase) * 0.03
      n.vy += Math.sin(t * 0.5 + n.phase) * 0.03
    }
    // cursor: nodes lean away from the pointer, like reading a page
    if (pointer.active && n !== dragging) {
      const dx = n.x - pointer.x
      const dy = n.y - pointer.y
      const d2 = dx * dx + dy * dy
      if (d2 < 140 * 140 && d2 > 1) {
        const d = Math.sqrt(d2)
        const f = (1 - d / 140) * 0.9
        n.vx += (dx / d) * f
        n.vy += (dy / d) * f
      }
    }
    if (n === dragging) {
      n.x = pointer.x
      n.y = pointer.y
      n.vx = 0
      n.vy = 0
      continue
    }
    n.vx *= 0.86
    n.vy *= 0.86
    n.x += n.vx
    n.y += n.vy
  }
}

function spawnPulse(link: SimLink, strong = false, forward = Math.random() > 0.5) {
  pulses.push({ link, t: 0, speed: strong ? 0.018 : 0.006 + Math.random() * 0.006, forward, strong })
}

function fireBurst() {
  const core = nodes.find((n) => n.kind === 'core')
  if (!core) return
  for (const l of links) {
    if (l.a === core) spawnPulse(l, true, true)
    else if (l.b === core) spawnPulse(l, true, false)
  }
  // second hop, slightly later
  setTimeout(() => {
    for (const l of links) {
      if (l.a.kind === 'topic' || l.b.kind === 'topic') spawnPulse(l, true, l.a.kind === 'topic')
    }
  }, 550)
}

function draw() {
  if (!ctx) return
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, width, height)

  const focus = dragging || hovered
  const lit = (n: SimNode) => !focus || n === focus || focus.neighbors.has(n.id)

  // edges
  for (const l of links) {
    const on = focus && (l.a === focus || l.b === focus)
    ctx.strokeStyle = on ? 'rgba(201,169,106,0.65)' : focus ? 'rgba(247,245,240,0.04)' : 'rgba(247,245,240,0.09)'
    ctx.lineWidth = on ? 1.2 : 1
    ctx.beginPath()
    ctx.moveTo(l.a.x, l.a.y)
    ctx.lineTo(l.b.x, l.b.y)
    ctx.stroke()
  }

  // pulses
  for (const p of pulses) {
    const { a, b } = p.link
    const k = p.forward ? p.t : 1 - p.t
    const x = a.x + (b.x - a.x) * k
    const y = a.y + (b.y - a.y) * k
    const alpha = Math.sin(p.t * Math.PI)
    const glow = ctx.createRadialGradient(x, y, 0, x, y, p.strong ? 14 : 9)
    glow.addColorStop(0, `rgba(201,169,106,${0.9 * alpha})`)
    glow.addColorStop(1, 'rgba(201,169,106,0)')
    ctx.fillStyle = glow
    ctx.beginPath()
    ctx.arc(x, y, p.strong ? 14 : 9, 0, Math.PI * 2)
    ctx.fill()
  }

  // nodes
  for (const n of nodes) {
    const on = lit(n)
    ctx.globalAlpha = on ? 1 : 0.25
    if (n.kind === 'core') {
      ctx.strokeStyle = 'rgba(201,169,106,0.35)'
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.arc(n.x, n.y, n.r + 9 + Math.sin(performance.now() / 700) * (reduced ? 0 : 2), 0, Math.PI * 2)
      ctx.stroke()
    }
    if (n.kind === 'org') {
      ctx.strokeStyle = STYLE.org.fill
      ctx.lineWidth = 1.4
      ctx.fillStyle = '#0b1a2e'
      ctx.beginPath()
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2)
      ctx.fill()
      ctx.stroke()
    } else {
      ctx.fillStyle = n === focus ? '#f7f5f0' : STYLE[n.kind].fill
      ctx.beginPath()
      ctx.arc(n.x, n.y, n.r + (n === focus ? 2 : 0), 0, Math.PI * 2)
      ctx.fill()
    }

    // labels: topics & orgs always; skills only when in focus
    const showLabel = n.kind !== 'core' && (n.kind !== 'skill' || (focus && on))
    if (showLabel && props.labels !== false && width >= 1024) {
      ctx.textBaseline = 'middle'
      if (n.kind === 'topic') {
        ctx.font = 'italic 400 15px "Source Serif 4", Georgia, serif'
        ctx.fillStyle = on ? '#f7f5f0' : 'rgba(247,245,240,0.5)'
      } else {
        ctx.font = '500 10px "IBM Plex Mono", monospace'
        ctx.fillStyle = n.kind === 'org' ? 'rgba(247,245,240,0.75)' : 'rgba(201,169,106,0.9)'
      }
      const label = n.kind === 'org' ? n.label.toUpperCase() : n.label
      ctx.fillText(label, n.x + n.r + 8, n.y)
    }
    ctx.globalAlpha = 1
  }
}

function frame(time: number) {
  if (!running) return
  tick(time)
  if (!reduced) {
    if (time - lastPulse > 520) {
      lastPulse = time
      const l = links[Math.floor(Math.random() * links.length)]
      if (l) spawnPulse(l)
    }
    for (const p of pulses) p.t += p.speed
    pulses = pulses.filter((p) => p.t < 1)
  }
  draw()
  raf = requestAnimationFrame(frame)
}

function start() {
  if (running || reduced || !visible) return
  running = true
  raf = requestAnimationFrame(frame)
}
function stop() {
  running = false
  cancelAnimationFrame(raf)
}

function resize() {
  const el = canvas.value
  if (!el || !ctx) return
  const rect = el.getBoundingClientRect()
  const prevC = width ? center() : null
  width = rect.width
  height = rect.height
  dpr = Math.min(window.devicePixelRatio || 1, 2)
  el.width = Math.round(width * dpr)
  el.height = Math.round(height * dpr)
  if (!nodes.length) build()
  else if (prevC) {
    const c = center()
    for (const n of nodes) { n.x += c.x - prevC.x; n.y += c.y - prevC.y }
  }
  if (reduced) settleAndDraw()
}

function settleAndDraw() {
  for (let i = 0; i < 400; i++) tick(i * 16)
  draw()
}

function nodeAt(x: number, y: number) {
  let best: SimNode | null = null
  let bestD = 22 * 22
  for (const n of nodes) {
    const d = (n.x - x) ** 2 + (n.y - y) ** 2
    if (d < bestD) { bestD = d; best = n }
  }
  return best
}

function onPointerMove(e: PointerEvent) {
  const rect = canvas.value!.getBoundingClientRect()
  pointer = { x: e.clientX - rect.left, y: e.clientY - rect.top, active: true }
  if (!dragging) hovered = nodeAt(pointer.x, pointer.y)
  canvas.value!.style.cursor = dragging ? 'grabbing' : hovered ? 'grab' : 'default'
  if (reduced) draw()
}
function onPointerLeave() {
  pointer.active = false
  hovered = null
  if (reduced) draw()
}
function onPointerDown(e: PointerEvent) {
  const rect = canvas.value!.getBoundingClientRect()
  const n = nodeAt(e.clientX - rect.left, e.clientY - rect.top)
  if (n) {
    dragging = n
    canvas.value!.setPointerCapture(e.pointerId)
  }
}
function onPointerUp(e: PointerEvent) {
  if (dragging) {
    dragging = null
    canvas.value!.releasePointerCapture(e.pointerId)
  }
}

watch(() => props.burst, () => { if (!reduced) fireBurst() })

const onVisibility = () => { if (document.hidden) stop(); else start() }

onMounted(() => {
  const el = canvas.value!
  ctx = el.getContext('2d')
  reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  resize()
  ro = new ResizeObserver(resize)
  ro.observe(el)
  io = new IntersectionObserver(([entry]) => {
    visible = !!entry?.isIntersecting
    if (visible) start(); else stop()
  })
  io.observe(el)
  document.addEventListener('visibilitychange', onVisibility)
  // redraw once webfonts land so canvas labels use Source Serif 4 / IBM Plex Mono
  document.fonts?.ready.then(() => draw())
  start()
})

onBeforeUnmount(() => {
  stop()
  ro?.disconnect()
  io?.disconnect()
  document.removeEventListener('visibilitychange', onVisibility)
})
</script>

<template>
  <canvas
    ref="canvas"
    class="absolute inset-0 w-full h-full touch-pan-y"
    role="img"
    aria-label="Knowledge graph connecting Jotham Hernandez to his research areas, institutions, and skills."
    @pointermove="onPointerMove"
    @pointerleave="onPointerLeave"
    @pointerdown="onPointerDown"
    @pointerup="onPointerUp"
    @pointercancel="onPointerUp"
  />
</template>
