<script setup lang="ts">
import { computed } from 'vue'
import AppWindow from '@/components/ui/AppWindow.vue'
import CodeLine from '@/components/ui/CodeLine.vue'
import { codeLine } from '@/utils/terminal'

const props = defineProps<{ lines: string[]; label: string }>()

const painted = computed(() => props.lines.map(codeLine))
</script>

<template>
  <AppWindow :title="label">
    <code class="c-code__body">
      <span v-for="(line, index) in painted" :key="index" class="c-code__line"
        ><CodeLine :line="line"
      /></span>
    </code>
  </AppWindow>
</template>
