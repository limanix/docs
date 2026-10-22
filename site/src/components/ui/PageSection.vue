<script setup lang="ts">
import { useId, type VNode } from 'vue'
import InlineText from '@/components/ui/InlineText.vue'

defineProps<{ id: string; title: string; lead?: string; compact?: boolean }>()
defineSlots<{ default(): VNode[] }>()

const titleId = `section-${useId()}`
</script>

<template>
  <section
    :id="id"
    class="c-page-section"
    :class="{ 'c-page-section--compact': compact }"
    :aria-labelledby="titleId"
  >
    <div class="o-container">
      <header class="c-page-section__head">
        <h2 :id="titleId" class="c-page-section__title"><InlineText :text="title" /></h2>
        <p v-if="lead" class="c-page-section__lead"><InlineText :text="lead" /></p>
      </header>
      <div class="c-page-section__body">
        <slot />
      </div>
    </div>
  </section>
</template>
