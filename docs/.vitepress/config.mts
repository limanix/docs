import { defineConfig, type HeadConfig } from 'vitepress'

const site = 'https://limanix.dev'
const docs = 'https://docs.limanix.dev'
const description =
  'Guides and reference for LimaNix: NixOS development machines on your Mac, declared in one TOML file.'
const keywords =
  'LimaNix, documentation, NixOS, Nix, Lima, macOS, Mac, virtual machine, Linux VM, development environment, limanix.toml, lmx'
const imageAlt = 'LimaNix Docs: guides and reference for NixOS dev machines on your Mac'

export default defineConfig({
  srcDir: 'pages',
  outDir: 'dist',
  lang: 'en-US',
  title: 'LimaNix Docs',
  titleTemplate: ':title | LimaNix Docs',
  description,
  cleanUrls: true,
  metaChunk: true,
  sitemap: { hostname: docs },

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico', sizes: '48x48' }],
    ['link', { rel: 'icon', href: '/favicon.png', type: 'image/png', sizes: '96x96' }],
    ['link', { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' }],
    ['meta', { name: 'theme-color', content: '#1a1d2e', media: '(prefers-color-scheme: dark)' }],
    ['meta', { name: 'theme-color', content: '#fdfaf0', media: '(prefers-color-scheme: light)' }],
    ['meta', { name: 'robots', content: 'index, follow' }],
    ['meta', { name: 'author', content: 'LimaNix contributors' }],
    ['meta', { name: 'keywords', content: keywords }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: 'LimaNix Docs' }],
    ['meta', { property: 'og:locale', content: 'en_US' }],
    ['meta', { property: 'og:image', content: `${docs}/og-image.jpg` }],
    ['meta', { property: 'og:image:width', content: '1200' }],
    ['meta', { property: 'og:image:height', content: '630' }],
    ['meta', { property: 'og:image:type', content: 'image/jpeg' }],
    ['meta', { property: 'og:image:alt', content: imageAlt }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:image', content: `${docs}/og-image.jpg` }],
    ['meta', { name: 'twitter:image:alt', content: imageAlt }],
  ],

  transformHead({ pageData }) {
    const path = pageData.relativePath.replace(/(^|\/)index\.md$/, '$1').replace(/\.md$/, '')
    const url = `${docs}/${path}`
    const title = pageData.title ? `${pageData.title} | LimaNix Docs` : 'LimaNix Docs'
    const summary = pageData.description || description
    const head: HeadConfig[] = [
      ['link', { rel: 'canonical', href: url }],
      ['meta', { property: 'og:url', content: url }],
      ['meta', { property: 'og:title', content: title }],
      ['meta', { property: 'og:description', content: summary }],
      ['meta', { name: 'twitter:title', content: title }],
      ['meta', { name: 'twitter:description', content: summary }],
    ]
    return head
  },

  transformHtml(html) {
    return html
      .replace(
        /<script id="check-dark-mode">[\s\S]*?<\/script>/,
        '<script src="/head.js"></script>',
      )
      .replace(/<script id="check-mac-os">[\s\S]*?<\/script>/, '')
  },

  markdown: {
    theme: { light: 'catppuccin-mocha', dark: 'catppuccin-mocha' },
    config(md) {
      const render = md.renderer.rules.code_inline!
      md.renderer.rules.code_inline = (tokens, index, options, env, self) => {
        const { content } = tokens[index]
        if (content.length <= 40 && !/\s/.test(content)) tokens[index].attrJoin('class', 'nowrap')
        return render(tokens, index, options, env, self)
      }
    },
  },

  themeConfig: {
    logo: { src: '/llama.webp', alt: 'LimaNix llama' },
    siteTitle: 'LimaNix Docs',

    nav: [
      { text: 'Overview', link: '/', activeMatch: '^/(quick-start|install|faq)?$' },
      { text: 'Virtual machines', link: '/vms/', activeMatch: '^/vms/' },
      { text: 'Configuration', link: '/config/', activeMatch: '^/config/' },
      { text: 'Modules', link: '/modules/', activeMatch: '^/modules/' },
      { text: 'Reference', link: '/reference/cli', activeMatch: '^/reference/' },
      { text: 'Download', link: `${site}/download` },
    ],

    sidebar: [
      {
        text: 'Get started',
        items: [
          { text: 'What is LimaNix?', link: '/' },
          { text: 'Quick start', link: '/quick-start' },
          { text: 'Install', link: '/install' },
          { text: 'Frequently asked questions', link: '/faq' },
        ],
      },
      {
        text: 'Virtual machines',
        items: [
          { text: 'Using virtual machines', link: '/vms/' },
          { text: 'Shell and sessions', link: '/vms/shell' },
          { text: 'Changing a VM', link: '/vms/update' },
          { text: 'Files and storage', link: '/vms/storage' },
          { text: 'Resources and architecture', link: '/vms/resources' },
          { text: 'Network', link: '/vms/network' },
        ],
      },
      {
        text: 'Configuration',
        items: [
          { text: 'The limanix.toml file', link: '/config/' },
          { text: 'Shell', link: '/config/shell' },
          { text: 'Toolchains', link: '/config/toolchains' },
          { text: 'Modules and packages', link: '/config/modules' },
          { text: 'Shared folders', link: '/config/mounts' },
          { text: 'Dotfiles', link: '/config/dotfiles' },
          { text: 'Environment and theme', link: '/config/environment' },
        ],
      },
      {
        text: 'Inside the VM',
        items: [
          { text: 'The terminal', link: '/inside/terminal' },
          { text: 'Languages', link: '/inside/languages' },
          { text: 'The lmx command', link: '/inside/lmx' },
          { text: 'Clipboard', link: '/inside/clipboard' },
          { text: 'Packages on the fly', link: '/inside/packages' },
        ],
      },
      {
        text: 'Modules',
        items: [
          { text: 'The catalog', link: '/modules/' },
          { text: 'Docker', link: '/modules/docker' },
          { text: 'PostgreSQL', link: '/modules/postgres' },
          { text: 'Google Cloud CLI', link: '/modules/gcloud' },
          { text: 'Claude Code', link: '/modules/claude-code' },
          { text: 'Posting', link: '/modules/posting' },
          { text: 'Harlequin', link: '/modules/harlequin' },
          { text: 'Your own modules', link: '/modules/custom' },
        ],
      },
      {
        text: 'Help',
        items: [
          { text: 'Troubleshooting', link: '/troubleshooting' },
          { text: 'How it works', link: '/architecture' },
        ],
      },
      {
        text: 'Reference',
        items: [
          { text: 'limanix command', link: '/reference/cli' },
          { text: 'limanix.toml', link: '/reference/config' },
          { text: 'lmx command', link: '/reference/lmx' },
        ],
      },
    ],

    search: { provider: 'local' },
    socialLinks: [{ icon: 'github', link: 'https://github.com/limanix' }],
    editLink: {
      pattern: 'https://github.com/limanix/docs/edit/main/docs/pages/:path',
      text: 'Edit this page on GitHub',
    },
    outline: { level: [2, 3], label: 'On this page' },
    notFound: {
      title: 'Page not found',
      quote: 'This page does not exist or has moved. Search the docs or start from the overview.',
      linkLabel: 'Go to the overview',
      linkText: 'Go to the overview',
    },
    footer: {
      message: 'Free and open source under the Apache License 2.0.',
      copyright: `© ${new Date().getFullYear()} LimaNix contributors`,
    },
  },
})
