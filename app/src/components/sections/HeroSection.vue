<script setup lang="ts">
import ActionLink from '@/components/ui/ActionLink.vue'
import InlineText from '@/components/ui/InlineText.vue'
import TerminalDemo from '@/components/ui/TerminalDemo.vue'
import type { DemoContent, HeroContent, LinksContent } from '@/contents'

defineProps<{ content: HeroContent; demo: DemoContent; links: LinksContent }>()
</script>

<template>
  <section class="hero" aria-labelledby="hero-title">
    <div class="o-container">
      <h1 id="hero-title">
        <template v-for="(line, index) in content.title" :key="index">
          <span class="hero__line"><InlineText :text="line" /></span>{{ ' ' }}
        </template>
      </h1>
      <p class="hero__lead"><InlineText :text="content.lead" /></p>
      <div class="hero__actions">
        <ActionLink :href="links.download" size="lg">{{ content.primary }}</ActionLink>
        <ActionLink :href="links.guide" variant="text" size="lg">{{
          content.secondary
        }}</ActionLink>
      </div>
      <div class="hero__stage">
        <TerminalDemo :content="demo" />
      </div>
    </div>
  </section>
</template>
