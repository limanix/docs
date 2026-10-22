<script setup lang="ts">
import DownloadSection from '@/components/sections/DownloadSection.vue'
import { siteContent } from '@/contents'

const { downloadPage, links } = siteContent
</script>

<template>
  <DownloadSection :content="downloadPage" :links="links" />
</template>
