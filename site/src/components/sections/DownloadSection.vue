<script setup lang="ts">
import ActionLink from '@/components/ui/ActionLink.vue'
import InlineText from '@/components/ui/InlineText.vue'
import type { DownloadContent, LinksContent } from '@/contents'

defineProps<{ content: DownloadContent; links: LinksContent }>()
</script>

<template>
  <section class="download o-container" aria-labelledby="download-title">
    <h1 id="download-title"><InlineText :text="content.title" /></h1>
    <p class="download__lead">{{ content.lead }}</p>
    <a class="download__notes" :href="links.latest">{{ content.notes }}</a>
    <div class="download__binaries">
      <ActionLink
        v-for="binary in content.binaries"
        :key="binary.asset"
        class="download__binary"
        :href="links.binaries + binary.asset"
        size="lg"
      >
        <span class="download__label">
          <span>{{ content.action }}</span>
          <span class="download__platform">{{ binary.label }}</span>
        </span>
      </ActionLink>
    </div>
    <ActionLink class="download__guide" :href="links.guide" variant="text" size="lg">{{
      content.guide
    }}</ActionLink>
  </section>
</template>
