// Applies the theme the visitor chose before the page paints; without a choice the CSS follows
// the system. useTheme writes the same key.
try {
  const theme = localStorage.getItem('theme')
  if (theme === 'light' || theme === 'dark') {
    document.documentElement.dataset.theme = theme
    const page = theme === 'light' ? '#fdfaf0' : '#000000'
    for (const meta of document.querySelectorAll('meta[name="theme-color"]')) meta.content = page
  }
} catch {
  // Storage is unavailable: the system theme applies.
}
