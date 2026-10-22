<script setup lang="ts">
import ActionLink from '@/components/ui/ActionLink.vue'
import type { ClosingContent, LinksContent } from '@/contents'

defineProps<{ content: ClosingContent; links: LinksContent }>()
</script>

<template>
  <section class="closing" aria-labelledby="closing-title">
    <div class="closing__inner o-container">
      <h2 id="closing-title">{{ content.title }}</h2>
      <ActionLink :href="links.download" size="lg">{{ content.primary }}</ActionLink>
    </div>
  </section>
</template>
