import { onBeforeUnmount, onMounted, ref, type Ref } from 'vue'

export function useInView(target: Ref<Element | null>) {
  const inView = ref(false)
  let observer: IntersectionObserver | undefined

  onMounted(() => {
    if (typeof IntersectionObserver === 'undefined' || !target.value) {
      inView.value = true
      return
    }
    observer = new IntersectionObserver((entries) => {
      inView.value = entries[entries.length - 1]?.isIntersecting ?? false
    })
    observer.observe(target.value)
  })

  onBeforeUnmount(() => observer?.disconnect())

  return inView
}
