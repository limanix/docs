import { readFile, rm, writeFile } from 'node:fs/promises'

const dist = new URL('../dist/', import.meta.url)
const server = new URL('../dist-ssr/', import.meta.url)
const { render } = await import(new URL('entry-server.js', server).href)

const pages = { '/': 'index.html', '/download': 'download.html' }
const mount = '<div id="app"></div>'

for (const [url, file] of Object.entries(pages)) {
  const path = new URL(file, dist)
  const html = await readFile(path, 'utf8')
  if (!html.includes(mount)) throw new Error(`${file} has no ${mount}`)
  await writeFile(path, html.replace(mount, `<div id="app">${await render(url)}</div>`))
  console.log(`prerendered ${url} into ${file}`)
}

await rm(server, { recursive: true })
