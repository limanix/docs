<script setup lang="ts">
import { ref, useId } from 'vue'
import InlineText from '@/components/ui/InlineText.vue'
import PageSection from '@/components/ui/PageSection.vue'
import type { FaqContent } from '@/contents'

defineProps<{ content: FaqContent }>()

const id = useId()
const open = ref(-1)

const toggle = (index: number) => {
  open.value = open.value === index ? -1 : index
}
</script>

<template>
  <PageSection :id="content.id" :title="content.title" compact>
    <div class="faq__list">
      <div
        v-for="(item, index) in content.items"
        :key="item.question"
        class="faq__item"
        :class="{ 'faq__item--open': open === index }"
      >
        <h3 class="faq__question">
          <button
            :id="`${id}-q${index}`"
            type="button"
            class="faq__toggle"
            :aria-expanded="open === index"
            :aria-controls="`${id}-a${index}`"
            @click="toggle(index)"
          >
            <span>{{ item.question }}</span>
            <svg
              class="faq__chevron"
              viewBox="0 0 16 16"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
              aria-hidden="true"
            >
              <path d="m6 3.5 4.5 4.5L6 12.5" />
            </svg>
          </button>
        </h3>
        <div
          :id="`${id}-a${index}`"
          class="faq__answer"
          role="region"
          :aria-labelledby="`${id}-q${index}`"
          :inert="open !== index"
        >
          <div class="faq__answer-inner">
            <p class="faq__text"><InlineText :text="item.answer" /></p>
          </div>
        </div>
      </div>
    </div>
  </PageSection>
</template>
