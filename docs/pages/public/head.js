// What VitePress would run inline before the page paints, moved to a file for the CSP: the color
// theme, and the class that shows ⌘ instead of Ctrl in the search hint on a Mac.
;(() => {
  let preference = 'auto'
  try {
    preference = localStorage.getItem('vitepress-theme-appearance') || 'auto'
  } catch {
    // Storage is unavailable: the system theme applies.
  }
  const dark = window.matchMedia('(prefers-color-scheme: dark)').matches
  if (preference === 'auto' ? dark : preference === 'dark') {
    document.documentElement.classList.add('dark')
  }
  document.documentElement.classList.toggle('mac', /Mac|iPhone|iPod|iPad/i.test(navigator.platform))
})()
