module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'plugin:prettier/recommended',
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: [
    'react',
    'react-hooks',
    '@typescript-eslint/eslint-plugin',
    'prettier',
    'react-refresh',
    'import'
  ],
  settings: {
    'import/resolver': {
        node: {
            extensions: ['.js', '.jsx', '.ts', '.tsx'],
        },
    },
  },
  rules: {
    '@typescript-eslint/no-explicit-any': 'off',
    "jsx-quotes": ["error", "prefer-single"],
    "react/jsx-wrap-multilines": ["error", {
      "declaration": "parens-new-line",
      "assignment": "parens-new-line",
      "return": "parens-new-line",
      "arrow": "parens-new-line",
      "condition": "parens-new-line",
      "logical": "parens-new-line",
      "prop": "parens-new-line"
    }],
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    "semi": ["error", "always"],
    'no-console': [
      'error',
      {
        allow: ['error', 'warn', 'info'],
      },
  ],
  'capitalized-comments': ['off'],
  'prettier/prettier': ['error'],
  'react-hooks/rules-of-hooks': 'error',
  'react-hooks/exhaustive-deps': 'warn',
  'react/no-array-index-key': 'warn',
  "no-nested-ternary": "error",
  'import/no-unresolved': [
    'error',
    {
      ignore: [
        '@/pages/',
        '@/components/',
        '@/libs/',
        '@/models/',
        '@/store',
        '@/persistedState/',
        '@/styles/',
        '@/assets/',
      ],
    },
  ],
  'import/order': [
    'error',
    {
      'newlines-between': 'always',
      groups: [
        'builtin',
        'external',
        'internal',
        'parent',
        'sibling',
        'index',
      ],
      pathGroupsExcludedImportTypes: ['builtin'],
    },
  ],
  'padding-line-between-statements': [
    'error',
    { blankLine: 'always', prev: 'if', next: '*' },
    { blankLine: 'always', prev: '*', next: 'if' },
    { blankLine: 'always', prev: '*', next: 'return' },
  ],
  'react/jsx-indent': ['error', 4, { indentLogicalExpressions: true }],
  'no-underscore-dangle': 0,
  'no-unexpected-multiline': 'error',
  '@typescript-eslint/no-use-before-define': ['warn'],
  // '@typescript-eslint/unbound-method': ['warn'],
  // '@typescript-eslint/prefer-regexp-exec': 'warn',
  // Prettier conflicts
  'import/newline-after-import': 0,
  'react/jsx-indent': 0,
  },
}
