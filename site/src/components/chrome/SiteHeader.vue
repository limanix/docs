<script setup lang="ts">
import llama from '@/assets/llama.webp'
import ThemeToggle from '@/components/chrome/ThemeToggle.vue'
import ActionLink from '@/components/ui/ActionLink.vue'
import { useScrolled } from '@/composables/useScrolled'
import { siteContent } from '@/contents'

const scrolled = useScrolled(32)
</script>

<template>
  <header class="site-header" :class="{ 'site-header--scrolled': scrolled }">
    <div class="site-header__bar o-bar">
      <a class="site-header__brand" :href="siteContent.links.home">
        <img
          class="site-header__logo"
          :src="llama"
          :alt="siteContent.brand.logoAlt"
          width="24"
          height="24"
        />
        <span>{{ siteContent.brand.name }}</span>
      </a>
      <nav class="site-header__nav" aria-label="Main">
        <a
          v-for="item in siteContent.navigation"
          :key="item.href"
          class="site-header__link"
          :href="item.href"
          >{{ item.label }}</a
        >
      </nav>
      <div class="site-header__actions">
        <ThemeToggle />
        <ActionLink :href="siteContent.links.download">{{ siteContent.download.label }}</ActionLink>
      </div>
    </div>
  </header>
</template>
