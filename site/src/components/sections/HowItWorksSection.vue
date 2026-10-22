<script setup lang="ts">
import { computed, ref } from 'vue'
import InlineText from '@/components/ui/InlineText.vue'
import PageSection from '@/components/ui/PageSection.vue'
import type { HowItWorksContent } from '@/contents'

const props = defineProps<{ content: HowItWorksContent }>()

const chosen = ref(0)
const command = computed(() => props.content.commands[chosen.value])
const lit = (row: string) => !command.value || command.value.rows.includes(row)

const choose = (index: number) => {
  chosen.value = chosen.value === index ? -1 : index
}
</script>

<template>
  <PageSection :id="content.id" :title="content.title" :lead="content.lead">
    <div class="flow">
      <div class="flow__commands" role="group" :aria-label="content.commandsLabel">
        <button
          v-for="(item, index) in content.commands"
          :key="item.name"
          type="button"
          class="flow__command"
          :class="{ 'flow__command--active': chosen === index }"
          :aria-pressed="chosen === index"
          @click="choose(index)"
        >
          {{ item.name }}
        </button>
      </div>
      <p class="flow__caption" aria-live="polite">
        <InlineText :text="command ? command.text : content.hint" />
      </p>
      <div
        class="flow__diagram"
        :class="{ 'flow__diagram--focused': command }"
        :style="{ gridTemplateRows: `repeat(${content.rows.length + 1}, auto)` }"
      >
        <span class="flow__panel flow__panel--mac" aria-hidden="true" />
        <span class="flow__panel flow__panel--vm" aria-hidden="true" />
        <p class="flow__side flow__side--mac">{{ content.mac }}</p>
        <p class="flow__side flow__side--vm">{{ content.vm }}</p>
        <template v-for="(row, index) in content.rows" :key="row.id">
          <div
            class="flow__cell flow__cell--mac"
            :class="{ 'flow__cell--lit': lit(row.id) }"
            :style="{ gridRow: index + 2 }"
          >
            <span class="flow__where">{{ content.mac }}</span>
            <span class="flow__name"><InlineText :text="row.mac.name" /></span>
            <span class="flow__text"><InlineText :text="row.mac.text" /></span>
          </div>
          <div
            class="flow__link"
            :class="[`flow__link--${row.link.direction}`, { 'flow__link--lit': lit(row.id) }]"
            :style="{ gridRow: index + 2 }"
          >
            <span class="flow__label">{{ row.link.label }}</span>
            <span class="flow__line" aria-hidden="true" />
          </div>
          <div
            class="flow__cell flow__cell--vm"
            :class="{ 'flow__cell--lit': lit(row.id) }"
            :style="{ gridRow: index + 2 }"
          >
            <span class="flow__where">{{ content.vm }}</span>
            <span class="flow__name"><InlineText :text="row.vm.name" /></span>
            <span class="flow__text"><InlineText :text="row.vm.text" /></span>
          </div>
        </template>
      </div>
    </div>
  </PageSection>
</template>
