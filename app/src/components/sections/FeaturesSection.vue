<script setup lang="ts">
import { computed, ref, useId } from 'vue'
import CodeBlock from '@/components/ui/CodeBlock.vue'
import FeatureIcon from '@/components/ui/FeatureIcon.vue'
import InlineText from '@/components/ui/InlineText.vue'
import PageSection from '@/components/ui/PageSection.vue'
import type { FeaturesContent } from '@/contents'

const props = defineProps<{ content: FeaturesContent }>()

const id = useId()
const active = ref(0)
const current = computed(() => props.content.items[active.value])
</script>

<template>
  <PageSection :id="content.id" :title="content.title" :lead="content.lead">
    <div class="features">
      <button
        v-for="(item, index) in content.items"
        :id="`${id}-item${index}`"
        :key="item.title"
        type="button"
        class="features__item"
        :class="{ 'features__item--active': active === index }"
        :style="{ order: index * 2, gridRow: index + 1 }"
        :aria-expanded="active === index"
        :aria-controls="`${id}-window`"
        @click="active = index"
      >
        <FeatureIcon class="features__icon" :icon="item.icon" :tone="item.tone" />
        <span class="features__copy">
          <span class="features__title">{{ item.title }}</span>
          <span class="features__text"><InlineText :text="item.text" /></span>
        </span>
      </button>
      <div
        v-if="current"
        :id="`${id}-window`"
        class="features__stage"
        role="region"
        :aria-labelledby="`${id}-item${active}`"
        :style="{ order: active * 2 + 1, gridRow: `1 / span ${content.items.length}` }"
      >
        <Transition name="features-swap" mode="out-in">
          <CodeBlock :key="active" :lines="current.code" :label="current.window" />
        </Transition>
      </div>
    </div>
  </PageSection>
</template>
