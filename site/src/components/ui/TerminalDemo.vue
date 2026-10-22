<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import AppWindow from '@/components/ui/AppWindow.vue'
import CodeLine from '@/components/ui/CodeLine.vue'
import { useInView } from '@/composables/useInView'
import { useReducedMotion } from '@/composables/useReducedMotion'
import type { DemoContent } from '@/contents'
import { demoScript, finalLines, tomlLine, type Beat } from '@/utils/terminal'

const props = defineProps<{ content: DemoContent }>()

const TYPE = 46
const typeDelay = (count: number) => TYPE + ((count * 37) % 5) * 9

const config = computed(() => props.content.config.map(tomlLine))
const script = computed(() => demoScript(props.content))

const root = ref<HTMLElement | null>(null)
const inView = useInView(root)
const reduced = useReducedMotion()

const state = ref<'idle' | 'playing' | 'done'>('idle')
const played = ref(0)
const typed = ref(-1)

const screen = computed(() => {
  const beats: Beat[] = script.value.beats.slice(0, played.value)
  const current = script.value.beats[played.value]
  if (current?.kind === 'type' && typed.value >= 0) {
    beats.push({ ...current, command: current.command.slice(0, typed.value) })
  }
  return finalLines(beats).slice(-script.value.rows)
})

let run = 0
const wait = (ms: number) => new Promise<void>((resolve) => window.setTimeout(resolve, ms))

async function play() {
  const current = ++run
  const live = () => current === run
  state.value = 'playing'
  played.value = 0
  typed.value = -1
  for (const [index, beat] of script.value.beats.entries()) {
    if (beat.kind === 'type') {
      typed.value = 0
      await wait(beat.delay)
      for (let count = 1; count <= beat.command.length; count++) {
        if (!live()) return
        typed.value = count
        await wait(typeDelay(count))
      }
      if (!live()) return
      typed.value = -1
    }
    played.value = index + 1
    await wait(beat.pause)
    if (!live()) return
  }
  state.value = 'done'
}

function finish() {
  run++
  played.value = script.value.beats.length
  typed.value = -1
  state.value = 'done'
}

watch(
  [inView, reduced],
  ([seen, still]) => {
    if (still) finish()
    else if (seen && state.value === 'idle') play()
  },
  { immediate: true },
)

onBeforeUnmount(() => run++)
</script>

<template>
  <div ref="root" class="c-demo">
    <AppWindow :title="content.directory" role="img" :aria-label="content.label">
      <div class="c-demo__panes" :style="{ '--rows': script.rows }">
        <div class="c-demo__editor">
          <p class="c-demo__file">{{ content.file }}</p>
          <ol class="c-demo__code">
            <li v-for="(line, index) in config" :key="index"><CodeLine :line="line" /></li>
          </ol>
        </div>
        <div class="c-demo__shell">
          <div v-for="(line, index) in screen" :key="index" class="c-demo__line">
            <CodeLine :line="line" /><span
              v-if="index === screen.length - 1"
              class="c-demo__cursor"
              :class="{ 'c-demo__cursor--blink': state === 'done' && !reduced }"
            />
          </div>
        </div>
      </div>
    </AppWindow>
    <button v-if="state === 'done' && !reduced" type="button" class="c-demo__replay" @click="play">
      {{ content.replay }}
    </button>
  </div>
</template>
