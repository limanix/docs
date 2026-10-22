import { defineConfig, globalIgnores } from 'eslint/config'
import pluginVue from 'eslint-plugin-vue'
import tseslint from 'typescript-eslint'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'

export default defineConfig(
  {
    name: 'app/files-to-lint',
    files: ['**/*.{ts,mts,tsx,vue}'],
  },

  globalIgnores(['**/dist/**', '**/dist-ssr/**', '**/coverage/**']),

  pluginVue.configs['flat/essential'],
  tseslint.configs.recommended,
  {
    name: 'app/vue-typescript',
    files: ['**/*.vue'],
    extends: [pluginVue.configs['flat/base']],
    languageOptions: {
      parserOptions: {
        parser: tseslint.parser,
        extraFileExtensions: ['.vue'],
      },
    },
    rules: {
      ...tseslint.configs.eslintRecommended.rules,
      'vue/block-lang': ['error', { script: { lang: 'ts' } }],
    },
  },
  skipFormatting,
)
