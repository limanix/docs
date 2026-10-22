import type { DemoContent, WelcomeContent } from '@/contents'

/** Colors of the terminal theme, named as lmx and Pure name them. */
export type Paint = 'blue' | 'green' | 'peach' | 'yellow' | 'magenta' | 'muted' | 'subtext' | 'bold'

export interface Segment {
  text: string
  paint?: Paint
}

export type Line = Segment[]

export type Beat =
  | { kind: 'print'; line: Line; pause: number }
  | { kind: 'type'; prompt: Line; command: string; delay: number; pause: number }
  | { kind: 'enter'; pause: number }

const plain = (text: string): Segment => ({ text })
const paint = (color: Paint, text: string): Segment => ({ text, paint: color })

export function tomlLine(source: string): Line {
  if (source.startsWith('[')) return [paint('yellow', source)]
  const equals = source.indexOf(' = ')
  if (equals < 0) return source ? [plain(source)] : []

  const line: Line = [paint('blue', source.slice(0, equals)), paint('subtext', ' = ')]
  let comment = false
  for (const part of source.slice(equals + 3).split(/("[^"]*")/)) {
    if (!part) continue
    const hash = comment || part.startsWith('"') ? -1 : part.indexOf('#')
    if (hash >= 0) {
      if (hash > 0) line.push(paint('subtext', part.slice(0, hash)))
      line.push(paint('muted', part.slice(hash)))
      comment = true
    } else {
      line.push(paint(comment ? 'muted' : part.startsWith('"') ? 'green' : 'subtext', part))
    }
  }
  return line
}

export function codeLine(source: string): Line {
  if (source.startsWith('#')) return [paint('muted', source)]
  if (!source.startsWith('$ ')) return tomlLine(source)
  const comment = source.indexOf('  #')
  if (comment < 0) return [paint('muted', '$ '), plain(source.slice(2))]
  return [
    paint('muted', '$ '),
    plain(source.slice(2, comment)),
    paint('muted', source.slice(comment)),
  ]
}

const INDENT = '  '
const GUEST = 42
const GAP = 4
const WIDTH = 78
const DETAIL = 8
const COMMAND = 35

const width = (line: Line) => line.reduce((total, segment) => total + [...segment.text].length, 0)

export function welcomeLines(welcome: WelcomeContent): Line[] {
  const captions: Line[] = [
    [paint('blue', welcome.title)],
    ...welcome.links.map((link) => [paint('subtext', link)]),
  ]
  const target = Math.min(Math.max(...welcome.shared.map((share) => share.path.length)), GUEST - 4)
  const guest: Line[] = [
    ...welcome.mark.map((mark, index) => {
      const caption = captions[index]
      return caption
        ? [paint('blue', mark.padEnd(8)), plain('  '), ...caption]
        : [paint('blue', mark)]
    }),
    [],
    [paint('bold', welcome.vm), plain('  '), paint('green', `● ${welcome.state}`)],
    [paint('subtext', welcome.system)],
    [paint('muted', welcome.generation)],
    [],
    [paint('blue', 'SYSTEM')],
    ...welcome.facts.map((fact) => [paint('muted', fact.term.padEnd(DETAIL)), plain(fact.value)]),
    [],
    [paint('blue', 'NETWORK')],
    ...welcome.network.map((entry) => [paint('subtext', entry)]),
    [],
    [paint('blue', 'SHARED')],
    ...welcome.shared.map((share) => [
      plain(`${share.path.padEnd(target)}  `),
      paint(share.mode === 'ro' ? 'peach' : 'green', share.mode),
    ]),
  ]
  const modules: Line[] = [
    [paint('blue', 'MODULES'), paint('muted', ` ${welcome.modules.length}`)],
    [],
    ...welcome.modules.map((module) => [plain(module)]),
  ]

  const lines: Line[] = [[]]
  for (let index = 0; index < Math.max(guest.length, modules.length); index++) {
    const left = guest[index] ?? []
    const right = modules[index] ?? []
    if (right.length) {
      lines.push([plain(INDENT), ...left, plain(' '.repeat(GUEST + GAP - width(left))), ...right])
    } else {
      lines.push(left.length ? [plain(INDENT), ...left] : [])
    }
  }
  return [
    ...lines,
    [],
    [plain(INDENT), paint('muted', '─'.repeat(WIDTH))],
    [],
    ...welcome.hints.map((hint) => [
      plain(INDENT),
      paint('blue', hint.command.padEnd(COMMAND)),
      plain('  '),
      paint('subtext', hint.action),
    ]),
    [],
  ]
}

const sign: Line = [paint('magenta', '❯'), plain(' ')]

export function demoScript(demo: DemoContent): { beats: Beat[]; rows: number } {
  const mac: Line = [paint('blue', demo.directory)]
  const vm: Line = [
    paint('muted', `${demo.user}@${demo.welcome.vm}`),
    plain(' '),
    paint('blue', '~'),
  ]
  const welcome = welcomeLines(demo.welcome)

  const beats: Beat[] = []
  demo.commands.forEach((command, index) => {
    if (index > 0) beats.push({ kind: 'print', line: [], pause: 0 })
    beats.push(
      { kind: 'print', line: mac, pause: 0 },
      { kind: 'type', prompt: sign, command: command.input, delay: index ? 500 : 900, pause: 350 },
      { kind: 'enter', pause: command.output.length ? 1200 : 700 },
      ...command.output.map((output) => ({
        kind: 'print' as const,
        line: [plain(output)],
        pause: 250,
      })),
    )
  })
  beats.push(
    ...welcome.map((line) => ({ kind: 'print' as const, line, pause: 22 })),
    { kind: 'print', line: vm, pause: 0 },
    { kind: 'type', prompt: sign, command: '', delay: 0, pause: 0 },
  )
  return { beats, rows: welcome.length - 1 + 2 }
}

export function finalLines(beats: Beat[]): Line[] {
  const lines: Line[] = []
  let pending = false
  for (const beat of beats) {
    if (beat.kind === 'enter') {
      lines.push([])
      pending = true
      continue
    }
    const line = beat.kind === 'print' ? beat.line : [...beat.prompt, plain(beat.command)]
    if (pending) lines[lines.length - 1] = line
    else lines.push(line)
    pending = false
  }
  return lines
}
