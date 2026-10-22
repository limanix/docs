<script setup lang="ts">
defineProps<{ title: string }>()
</script>

<template>
  <div class="c-window">
    <div class="c-window__bar">
      <span class="c-window__lights" aria-hidden="true"><span /><span /><span /></span>
      <span class="c-window__title">{{ title }}</span>
    </div>
    <slot />
  </div>
</template>
