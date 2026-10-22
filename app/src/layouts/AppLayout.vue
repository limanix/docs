<script setup lang="ts">
import SiteFooter from '@/components/chrome/SiteFooter.vue'
import SiteHeader from '@/components/chrome/SiteHeader.vue'
</script>

<template>
  <div class="o-app-layout">
    <SiteHeader />
    <main class="o-app-layout__main">
      <RouterView />
    </main>
    <SiteFooter />
  </div>
</template>
