<script setup lang="ts">
withDefaults(defineProps<{ href: string; variant?: 'primary' | 'text'; size?: 'md' | 'lg' }>(), {
  variant: 'primary',
  size: 'md',
})
</script>

<template>
  <a
    class="c-action-link"
    :class="[`c-action-link--${variant}`, `c-action-link--${size}`]"
    :href="href"
  >
    <slot />
    <svg
      v-if="variant === 'text'"
      class="c-action-link__arrow"
      viewBox="0 0 20 20"
      fill="none"
      stroke="currentColor"
      stroke-width="1.6"
      stroke-linecap="round"
      stroke-linejoin="round"
      aria-hidden="true"
    >
      <path d="M4 10h11.5M11 5.5l4.5 4.5-4.5 4.5" />
    </svg>
  </a>
</template>
