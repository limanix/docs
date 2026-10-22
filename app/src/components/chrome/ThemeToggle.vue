<script setup lang="ts">
import { ref, watch } from 'vue'
import { useReducedMotion } from '@/composables/useReducedMotion'
import { useTheme } from '@/composables/useTheme'
import { siteContent } from '@/contents'

const { key, light, dark } = siteContent.theme
const { theme, toggle } = useTheme()
const reduced = useReducedMotion()

const shown = ref<string>(theme.value)
const typing = ref(false)

watch(theme, (value) => {
  if (!typing.value) shown.value = value
})

const wait = (ms: number) => new Promise<void>((resolve) => window.setTimeout(resolve, ms))

async function switchTheme() {
  if (typing.value) return
  if (reduced.value) {
    toggle()
    return
  }
  typing.value = true
  while (shown.value) {
    shown.value = shown.value.slice(0, -1)
    await wait(45)
  }
  toggle()
  for (const character of theme.value) {
    shown.value += character
    await wait(65)
  }
  await wait(250)
  typing.value = false
}
</script>

<template>
  <button
    type="button"
    class="c-theme-toggle"
    :class="{ 'c-theme-toggle--typing': typing }"
    :aria-label="theme === 'light' ? dark : light"
    @click="switchTheme"
  >
    <span class="c-theme-toggle__key">{{ key }} = </span
    ><span class="c-theme-toggle__value">"{{ shown }}<span class="c-theme-toggle__cursor" />"</span>
  </button>
</template>
