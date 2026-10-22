<script setup lang="ts">
import { useId } from 'vue'
import type { FeatureIcon, Tone } from '@/contents'

defineProps<{ icon: FeatureIcon; tone: Tone }>()

const id = useId()

const TILE =
  'M100 50L100 66.8L99.8 72.1L99.6 76L99.3 79.1L98.9 81.8L98.4 84L97.9 86.1L97.2 87.9L96.4 89.5L95.6 91L94.6 92.3L93.5 93.5L92.3 94.6L91 95.6L89.5 96.4L87.9 97.2L86.1 97.9L84 98.4L81.8 98.9L79.1 99.3L76 99.6L72.1 99.8L66.8 100L50 100L33.2 100L27.9 99.8L24 99.6L20.9 99.3L18.2 98.9L16 98.4L13.9 97.9L12.1 97.2L10.5 96.4L9 95.6L7.7 94.6L6.5 93.5L5.4 92.3L4.4 91L3.6 89.5L2.8 87.9L2.1 86.1L1.6 84L1.1 81.8L0.7 79.1L0.4 76L0.2 72.1L0 66.8L0 50L0 33.2L0.2 27.9L0.4 24L0.7 20.9L1.1 18.2L1.6 16L2.1 13.9L2.8 12.1L3.6 10.5L4.4 9L5.4 7.7L6.5 6.5L7.7 5.4L9 4.4L10.5 3.6L12.1 2.8L13.9 2.1L16 1.6L18.2 1.1L20.9 0.7L24 0.4L27.9 0.2L33.2 0L50 0L66.8 0L72.1 0.2L76 0.4L79.1 0.7L81.8 1.1L84 1.6L86.1 2.1L87.9 2.8L89.5 3.6L91 4.4L92.3 5.4L93.5 6.5L94.6 7.7L95.6 9L96.4 10.5L97.2 12.1L97.9 13.9L98.4 16L98.9 18.2L99.3 20.9L99.6 24L99.8 27.9L100 33.2Z'

const paths: Record<FeatureIcon, string[]> = {
  folder: [
    'M3.5 7.5a2 2 0 0 1 2-2h3.6l2 2.2h7.4a2 2 0 0 1 2 2v7.8a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z',
  ],
  sliders: [
    'M4 7h9M17 7h3M4 12h3M11 12h9M4 17h11M19 17h1',
    'M13 7a2 2 0 1 0 4 0 2 2 0 1 0-4 0M7 12a2 2 0 1 0 4 0 2 2 0 1 0-4 0M15 17a2 2 0 1 0 4 0 2 2 0 1 0-4 0',
  ],
  layers: ['m12 3 9 5-9 5-9-5z', 'm3 12 9 5 9-5', 'm3 16 9 5 9-5'],
  terminal: [
    'M5.5 4h13A2.5 2.5 0 0 1 21 6.5v11a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 17.5v-11A2.5 2.5 0 0 1 5.5 4z',
    'm7 9.5 3 2.5-3 2.5',
    'M12.5 15H17',
  ],
  braces: [
    'M9 4H8a2 2 0 0 0-2 2v4a2 2 0 0 1-2 2 2 2 0 0 1 2 2v4a2 2 0 0 0 2 2h1',
    'M15 4h1a2 2 0 0 1 2 2v4a2 2 0 0 0 2 2 2 2 0 0 0-2 2v4a2 2 0 0 1-2 2h-1',
  ],
  pulse: ['M3 12h4l2.5-6 5 12 2.5-6h4'],
}
</script>

<template>
  <span class="c-feature-icon" :class="`u-tone-${tone}`" aria-hidden="true">
    <svg class="c-feature-icon__tile" viewBox="0 0 100 100">
      <defs>
        <linearGradient :id="`${id}-fill`" x1="0" y1="0" x2="1" y2="1">
          <stop class="c-feature-icon__from" offset="0" />
          <stop class="c-feature-icon__to" offset="1" />
        </linearGradient>
        <clipPath :id="`${id}-clip`"><path :d="TILE" /></clipPath>
      </defs>
      <path :d="TILE" :fill="`url(#${id}-fill)`" />
      <path class="c-feature-icon__edge" :d="TILE" :clip-path="`url(#${id}-clip)`" />
    </svg>
    <svg
      class="c-feature-icon__glyph"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="1.6"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <path v-for="(d, index) in paths[icon]" :key="index" :d="d" />
    </svg>
  </span>
</template>
