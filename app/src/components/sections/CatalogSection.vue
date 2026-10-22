<script setup lang="ts">
import PageSection from '@/components/ui/PageSection.vue'
import type { CatalogContent } from '@/contents'

defineProps<{ content: CatalogContent }>()
</script>

<template>
  <PageSection :id="content.id" :title="content.title" :lead="content.lead">
    <ul class="catalog__items">
      <li v-for="item in content.items" :key="item" class="catalog__item">{{ item }}</li>
    </ul>
  </PageSection>
</template>
