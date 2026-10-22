<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ text: string }>()

interface Part {
  kind: 'text' | 'code' | 'accent' | 'link'
  text: string
  href?: string
}

const LINK = /^\[([^\]]+)\]\(([^)]+)\)$/

const parts = computed(() =>
  props.text
    .split(/(`[^`]+`|\*[^*]+\*|\[[^\]]+\]\([^)]+\))/)
    .filter(Boolean)
    .map((part): Part => {
      const marked = part.length > 2 ? part[0] : ''
      if (marked === '`' && part.endsWith('`')) return { kind: 'code', text: part.slice(1, -1) }
      if (marked === '*' && part.endsWith('*')) return { kind: 'accent', text: part.slice(1, -1) }
      const link = LINK.exec(part)
      if (link?.[1] && link[2]) return { kind: 'link', text: link[1], href: link[2] }
      return { kind: 'text', text: part }
    }),
)
</script>

<template>
  <template v-for="(part, index) in parts" :key="index">
    <code v-if="part.kind === 'code'" class="c-inline-code">{{ part.text }}</code>
    <span v-else-if="part.kind === 'accent'" class="u-gradient-text">{{ part.text }}</span>
    <a v-else-if="part.kind === 'link'" class="c-inline-link" :href="part.href">{{ part.text }}</a>
    <template v-else>{{ part.text }}</template>
  </template>
</template>
