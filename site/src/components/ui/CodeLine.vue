<script setup lang="ts">
import type { Line } from '@/utils/terminal'

defineProps<{ line: Line }>()
</script>

<template>
  <span
    v-for="(segment, index) in line"
    :key="index"
    :class="segment.paint && `c-paint--${segment.paint}`"
    >{{ segment.text }}</span
  >
</template>
